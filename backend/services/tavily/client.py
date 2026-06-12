"""
Tavily Search API wrapper
Person 2 owns this - no other team accesses Tavily directly
"""

import os
from typing import List, Dict, Any


class TavilySearchService:
    """Wrapper around Tavily API for web search"""

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")
        # Import here to avoid dependency issues if tavily not installed
        from tavily import TavilyClient
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the web using Tavily
        Returns structured results with title, url, content
        """
        try:
            response = self.client.search(query, max_results=max_results)
            results = []

            for result in response.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0)
                })

            return results
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []

    def search_news(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for news/recent articles using Tavily"""
        try:
            response = self.client.search(
                query,
                max_results=max_results,
                include_answer=True
            )
            return response.get("results", [])
        except Exception as e:
            print(f"Tavily news search error: {e}")
            return []
