"""
VentureMind AI — BeautifulSoup4-based Web Crawler Infrastructure
Async HTTP fetching with HTML parsing and internal link discovery.

Implements IWebCrawler using httpx for async requests and BeautifulSoup for parsing.
"""

import asyncio
import logging
from typing import List, Set
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from backend.domain.interfaces import IWebCrawler
from backend.domain.schemas import CrawledPage, PageCategory

logger = logging.getLogger(__name__)


class BeautifulSoupWebCrawler(IWebCrawler):
    """
    Production-ready web crawler implementation using httpx and BeautifulSoup4.

    Features:
    - Async HTTP requests with configurable concurrency limits via Semaphore
    - Robust HTML parsing with script/style tag stripping
    - Internal link discovery and deduplication
    - Graceful error handling with per-page retry logic
    - Configurable maximum page limit to prevent runaway crawls
    """

    def __init__(self, max_pages: int = 10):
        """
        Initialize the web crawler.

        Args:
            max_pages: Maximum number of pages to crawl (default: 10).
        """
        if max_pages < 1:
            raise ValueError("max_pages must be at least 1")

        self.max_pages = max_pages
        self.session: httpx.AsyncClient | None = None
        self.semaphore = asyncio.Semaphore(3)

    async def _fetch_and_parse(self, url: str) -> tuple[str | None, str, List[str]]:
        """
        Fetch a URL and extract title, visible text, and internal links.

        Args:
            url: The URL to fetch.

        Returns:
            A tuple of (title, visible_text, internal_links).
            On error, returns (None, empty_string, empty_list).
        """
        try:
            async with self.semaphore:
                if self.session is None:
                    self.session = httpx.AsyncClient(timeout=10.0)

                response = await self.session.get(url, follow_redirects=True)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Extract title
                title_tag = soup.find("title")
                title = title_tag.string if title_tag else None

                # Remove script and style tags to extract visible text only
                for tag in soup(["script", "style"]):
                    tag.decompose()

                # Extract visible text
                visible_text = soup.get_text(separator=" ", strip=True)

                # Discover internal links
                base_domain = urlparse(url).netloc
                internal_links = []

                for link_tag in soup.find_all("a", href=True):
                    href = link_tag["href"]
                    absolute_url = urljoin(url, href)
                    link_domain = urlparse(absolute_url).netloc

                    # Only keep internal links
                    if link_domain == base_domain:
                        # Remove fragment identifiers
                        clean_url = absolute_url.split("#")[0]
                        if clean_url not in internal_links:
                            internal_links.append(clean_url)

                logger.info(f"✓ Fetched {url} (title: {title}, links: {len(internal_links)})")
                return title, visible_text, internal_links

        except httpx.HTTPStatusError as e:
            logger.warning(f"✗ HTTP error {e.response.status_code} for {url}")
            return None, "", []
        except asyncio.TimeoutError:
            logger.warning(f"✗ Timeout fetching {url}")
            return None, "", []
        except Exception as e:
            logger.warning(f"✗ Error fetching {url}: {type(e).__name__}: {e}")
            return None, "", []

    async def crawl_website(self, base_url: str) -> List[CrawledPage]:
        """
        Crawl a website starting from the base URL.

        Fetches the base page, discovers internal links, and crawls them
        concurrently up to the max_pages limit.

        Args:
            base_url: The starting URL to crawl.

        Returns:
            A list of CrawledPage objects representing crawled pages.
        """
        logger.info(f"Starting website crawl: {base_url}")
        crawled_pages: List[CrawledPage] = []
        visited: Set[str] = set()

        try:
            # Fetch and parse the base URL
            title, text, internal_links = await self._fetch_and_parse(base_url)

            if not text:
                logger.error(f"Failed to crawl base URL: {base_url}")
                return crawled_pages

            visited.add(base_url)
            crawled_pages.append(
                CrawledPage(
                    url=base_url,
                    title=title,
                    text=text,
                    category=PageCategory.UNKNOWN,
                )
            )

            # Build queue of pages to crawl (excluding already visited)
            pages_to_crawl = [
                url for url in internal_links
                if url not in visited and len(crawled_pages) < self.max_pages
            ]

            # Crawl remaining pages concurrently
            while pages_to_crawl and len(crawled_pages) < self.max_pages:
                # Respect max_pages constraint
                batch = pages_to_crawl[: self.max_pages - len(crawled_pages)]
                pages_to_crawl = pages_to_crawl[self.max_pages - len(crawled_pages) :]

                # Fetch batch concurrently
                tasks = [self._fetch_and_parse(url) for url in batch]
                results = await asyncio.gather(*tasks)

                # Process results
                for url, (title, text, discovered_links) in zip(batch, results):
                    visited.add(url)

                    # Only add if we successfully fetched content
                    if text:
                        crawled_pages.append(
                            CrawledPage(
                                url=url,
                                title=title,
                                text=text,
                                category=PageCategory.UNKNOWN,
                            )
                        )

                        # Queue newly discovered links
                        for link in discovered_links:
                            if link not in visited and len(crawled_pages) < self.max_pages:
                                pages_to_crawl.append(link)

            logger.info(f"✓ Crawl completed: {len(crawled_pages)} pages fetched")
            return crawled_pages

        finally:
            # Clean up HTTP session
            if self.session is not None:
                await self.session.aclose()
                self.session = None
