"""
Firecrawl API wrapper for website extraction
Person 2 owns this - extracts structured data from URLs
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class FirecrawlService:
    """Wrapper around Firecrawl API for website data extraction"""

    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable not set")
        # Import here to avoid dependency issues if firecrawl not installed
        from firecrawl import FirecrawlApp
        self.app = FirecrawlApp(api_key=api_key)

    def scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Scrape a single URL and return structured data
        Returns markdown content, metadata, links
        """
        try:
            response = self.app.scrape_url(url)

            # Response is a Document object, not dict
            return {
                "url": url,
                "markdown": getattr(response, "markdown", ""),
                "html": getattr(response, "html", ""),
                "metadata": {
                    "title": getattr(response, "title", ""),
                    "description": getattr(response.metadata, "description", ""),
                    "url": getattr(response.metadata, "url", ""),
                } if hasattr(response, "metadata") else {},
                "links": getattr(response, "links", []),
                "status_code": getattr(response.metadata, "status_code", 200) if hasattr(response, "metadata") else 200,
                "status": "success"
            }
        except Exception as e:
            print(f"Firecrawl scrape error for {url}: {e}")
            return {
                "url": url,
                "status": "failed",
                "error": str(e)
            }

    def scrape_company_website(self, url: str) -> Dict[str, Any]:
        """
        Scrape company website for key information
        Returns team, about, products, pricing info
        """
        result = self.scrape_url(url)
        if result.get("status") == "failed":
            return result

        markdown = result.get("markdown", "")

        # Extract key sections (basic heuristic)
        return {
            "url": url,
            "status": "success",
            "content": markdown,
            "has_team_page": "team" in markdown.lower(),
            "has_pricing": "pricing" in markdown.lower(),
            "has_about": "about" in markdown.lower(),
            "content_length": len(markdown),
        }
