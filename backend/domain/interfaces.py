from abc import ABC, abstractmethod
from typing import List, Optional

from backend.domain.schemas import (
    CrawledPage,
    Finding,
    InvestmentRecommendation,
    PageAnalysis,
    PageCategory,
    RetrievalResponse,
    ScoreCategory,
)


class IWebCrawler(ABC):
    """Abstract base class defining the contract for web crawler implementations."""

    @abstractmethod
    async def crawl_website(self, base_url: str) -> List[CrawledPage]:
        """
        Crawl a website starting from the base URL.

        Args:
            base_url: The starting URL to crawl.

        Returns:
            List[CrawledPage]: A list of crawled pages with extracted content.
        """
        pass


class IPageClassifier(ABC):
    """Abstract base class defining the contract for page classification implementations."""

    @abstractmethod
    async def classify_page(self, text: str) -> PageCategory:
        """
        Classify a page based on its text content.

        Args:
            text: The Markdown text content of the page.

        Returns:
            PageCategory: The inferred category of the page.
        """
        pass


class IRetrievalService(ABC):
    """Abstract base class defining the contract for hybrid semantic retrieval."""

    @abstractmethod
    async def search(
        self,
        query: str,
        deal_id: str,
        top_k: int = 5,
        categories: Optional[List[PageCategory]] = None,
    ) -> RetrievalResponse:
        """
        Search across ingested documents with strict deal isolation.

        Enforces strict data isolation by requiring deal_id to prevent
        cross-startup hallucinations or data leakage.

        Args:
            query: The search query string.
            deal_id: The deal/startup ID (REQUIRED for strict isolation).
            top_k: Maximum number of results to return (default: 5).
            categories: Optional filter by page categories.

        Returns:
            RetrievalResponse: Search results with metadata and execution time.
        """
        pass


class IFindingExtractor(ABC):
    """Abstract base class defining the contract for LLM-based finding extraction."""

    @abstractmethod
    async def extract_findings(
        self, deal_id: str, category: ScoreCategory
    ) -> List[Finding]:
        """
        Extract findings from ingested data for a specific evaluation category.

        Uses retrieval and LLM to surface facts relevant to the given category
        (e.g., TEAM, MARKET, PRODUCT, FINANCIAL, RISK).

        Args:
            deal_id: The deal/startup ID for strict isolation.
            category: The scoring category to extract findings for.

        Returns:
            List[Finding]: Extracted findings with supporting evidence traces.
        """
        pass


class IScoringEngine(ABC):
    """Abstract base class defining the contract for the deterministic scoring engine."""

    @abstractmethod
    async def evaluate_startup(self, deal_id: str) -> InvestmentRecommendation:
        """
        Evaluate a startup and produce an investment recommendation.

        Orchestrates the complete scoring workflow:
        1. Extract findings across all categories
        2. Apply deterministic scoring logic to each factor
        3. Aggregate to category scores
        4. Synthesize final recommendation

        Args:
            deal_id: The deal/startup ID to evaluate.

        Returns:
            InvestmentRecommendation: Complete scoring and recommendation.
        """
        pass


class IPdfParser(ABC):
    """Abstract base class defining the contract for PDF parsing implementations."""

    @abstractmethod
    async def parse_page(self, image_path: str, raw_text: str) -> PageAnalysis:
        """
        Parse a single page given its image path and raw text.
        
        Args:
            image_path: Path to the rendered PNG image of the page.
            raw_text: Raw text extracted from the same page.
            
        Returns:
            PageAnalysis: Structured analysis of the page content.
        """
        pass

    @abstractmethod
    async def parse(self, file_path: str) -> List[PageAnalysis]:
        """
        Parse an entire PDF file and return a list of PageAnalysis objects.
        (Optional wrapper, concurrent page-level parsing is preferred).
        """
        pass