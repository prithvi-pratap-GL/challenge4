"""
VentureMind AI — Firecrawl-based Web Crawler Infrastructure
Handles JavaScript-heavy Single Page Applications using the Firecrawl SDK.

Implements IWebCrawler using Firecrawl for rendering and Markdown extraction.
Optimized for modern web applications (React, Webflow, Vue.js, etc.).
"""

import logging
from typing import List

from firecrawl import FirecrawlApp

from backend.core.settings import settings
from backend.domain.interfaces import IWebCrawler
from backend.domain.schemas import CrawledPage, PageCategory

logger = logging.getLogger(__name__)


class FirecrawlWebCrawler(IWebCrawler):
    """
    Production-ready web crawler for JavaScript-heavy websites using Firecrawl.

    Features:
    - Full JavaScript rendering via Firecrawl's cloud infrastructure
    - Automatic Markdown extraction for cleaner content
    - Configurable crawl depth and page limits
    - Robust error handling with graceful degradation
    - Automatic link discovery and internal-only filtering
    """

    def __init__(self):
        """
        Initialize the Firecrawl web crawler.

        Loads the Firecrawl API key from Pydantic settings.

        Raises:
            ValueError: If FIRECRAWL_API_KEY is not set in environment.
        """
        if not settings.firecrawl_api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is not set")

        self.client = FirecrawlApp(api_key=settings.firecrawl_api_key)
        logger.info("✓ Firecrawl client initialized")

    async def crawl_website(self, base_url: str) -> List[CrawledPage]:
        """
        Crawl a JavaScript-heavy website using Firecrawl.

        Firecrawl handles:
        - Full page rendering (JavaScript execution)
        - Markdown extraction
        - Automatic internal link discovery
        - Metadata extraction

        Args:
            base_url: The starting URL to crawl.

        Returns:
            A list of CrawledPage objects representing crawled pages.

        Raises:
            RuntimeError: If the Firecrawl API call fails.
        """
        logger.info(f"Starting Firecrawl crawl: {base_url}")

        try:
            # Call Firecrawl's crawl_url method with Markdown output
            crawl_response = self.client.crawl_url(
                url=base_url,
                params={
                    "limit": 10,  # Max pages to crawl
                    "scrapeOptions": {
                        "formats": ["markdown"],  # Request Markdown format for clean extraction
                    },
                },
            )

            if not crawl_response or "data" not in crawl_response:
                logger.error(f"Firecrawl returned unexpected response: {crawl_response}")
                raise RuntimeError("Firecrawl API returned invalid response structure")

            crawled_pages: List[CrawledPage] = []
            pages_data = crawl_response.get("data", [])

            logger.info(f"Firecrawl discovered {len(pages_data)} pages")

            # Map Firecrawl response to CrawledPage objects
            for page_data in pages_data:
                try:
                    url = page_data.get("url")
                    if not url:
                        logger.warning("Skipping page without URL")
                        continue

                    # Extract title from metadata or use None
                    metadata = page_data.get("metadata", {})
                    title = metadata.get("title") or metadata.get("ogTitle")

                    # Extract content (Markdown format)
                    content = page_data.get("markdown") or page_data.get("content", "")

                    if not content:
                        logger.warning(f"Skipping {url}: no content extracted")
                        continue

                    # Create CrawledPage with extracted data
                    crawled_page = CrawledPage(
                        url=url,
                        title=title,
                        text=content,
                        category=PageCategory.UNKNOWN,
                    )
                    crawled_pages.append(crawled_page)
                    logger.debug(f"✓ Added page: {url} (title: {title})")

                except Exception as e:
                    logger.warning(f"Error processing page data: {e}")
                    continue

            logger.info(f"✓ Crawl completed: {len(crawled_pages)} pages processed")
            return crawled_pages

        except RuntimeError as e:
            # Re-raise RuntimeError as-is
            logger.error(f"Firecrawl API error: {e}")
            raise
        except Exception as e:
            # Wrap other exceptions in RuntimeError
            error_msg = f"Firecrawl crawl failed: {type(e).__name__}: {e}"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
