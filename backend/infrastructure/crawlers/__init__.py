"""
VentureMind AI — Web Crawler Infrastructure
Concrete implementations of domain crawler interfaces.
"""

from backend.infrastructure.crawlers.bs4_crawler import BeautifulSoupWebCrawler
from backend.infrastructure.crawlers.firecrawl_crawler import FirecrawlWebCrawler

__all__ = ["BeautifulSoupWebCrawler", "FirecrawlWebCrawler"]
