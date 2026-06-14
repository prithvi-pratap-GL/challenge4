"""
Research Enrichment Service - Firecrawl Integration
Person 2 owns this - enriches Tavily search results with full page content
"""

import hashlib
from typing import Dict, List, Any, Optional
from backend.services.firecrawl.client import FirecrawlService


class ResearchEnricher:
    """
    Enriches research with full-page content from key sources
    Uses Firecrawl to extract detailed information from URLs
    Gracefully handles failures without blocking research
    """

    def __init__(self):
        try:
            self.firecrawl = FirecrawlService()
            self.enabled = True
        except Exception as e:
            print(f"[WARN] Firecrawl initialization failed: {e}. Research will continue without enrichment.")
            self.firecrawl = None
            self.enabled = False

        self.cache = {}  # In-memory cache: url_hash -> enrichment result

    def enrich_sources(self, urls: List[str], max_urls: int = 3) -> Dict[str, Dict]:
        """
        Enrich top URLs with full page content from Firecrawl

        Args:
            urls: List of URLs to enrich (from Tavily search results)
            max_urls: Max number of URLs to scrape (default 3 to control costs)

        Returns:
            Dict mapping URL -> {markdown, status, title, description, etc}
        """
        if not self.enabled or not self.firecrawl:
            return {}

        enriched = {}
        urls_to_scrape = urls[:max_urls] if urls else []

        for url in urls_to_scrape:
            try:
                url_hash = self._hash_url(url)

                # Check cache first
                if url_hash in self.cache:
                    enriched[url] = self.cache[url_hash]
                    print(f"[CACHE] Enrichment hit for {url[:50]}...")
                    continue

                # Scrape with Firecrawl
                print(f"[ENRICHING] Scraping {url[:50]}...")
                result = self.firecrawl.scrape_url(url)

                # Store in cache
                self.cache[url_hash] = result
                enriched[url] = result

            except Exception as e:
                print(f"[WARN] Enrichment failed for {url}: {e}")
                enriched[url] = {
                    "url": url,
                    "status": "failed",
                    "error": str(e)
                }

        return enriched

    def merge_content(self, tavily_content: str, enriched_data: Dict[str, Any]) -> str:
        """
        Merge Tavily snippet with Firecrawl full content

        Args:
            tavily_content: Original snippet from Tavily
            enriched_data: Full content dict from Firecrawl

        Returns:
            Merged content string (prefers Firecrawl markdown if available)
        """
        if enriched_data.get("status") == "success" and enriched_data.get("markdown"):
            markdown = enriched_data.get("markdown", "")
            # Return first 1000 chars of markdown to avoid token explosion
            return markdown[:1000] if len(markdown) > 1000 else markdown

        # Fallback to Tavily content if enrichment unavailable
        return tavily_content

    def _hash_url(self, url: str) -> str:
        """Hash URL for cache key"""
        return hashlib.md5(url.encode()).hexdigest()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get enrichment cache statistics"""
        return {
            "cache_size": len(self.cache),
            "enabled": self.enabled,
            "cached_urls": list(self.cache.keys())[:5]  # Show first 5
        }
