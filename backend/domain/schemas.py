from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PageCategory(str, Enum):
    """Enumeration of discovered page categories."""

    UNKNOWN = "unknown"
    ABOUT = "about"
    PRODUCT = "product"
    PRICING = "pricing"
    BLOG = "blog"
    CONTACT = "contact"
    TEAM = "team"
    CAREERS = "careers"
    PRESS = "press"


class CrawledPage(BaseModel):
    """Domain entity representing a crawled web page."""

    url: str = Field(..., description="The URL of the crawled page")
    title: Optional[str] = Field(None, description="The page title extracted from <title> tag")
    text: str = Field(..., description="Visible text content of the page")
    category: PageCategory = Field(
        default=PageCategory.UNKNOWN, description="The inferred category of the page"
    )


class PageAnalysis(BaseModel):
    """Structured output expected from the Vision model for a single PDF page."""

    page_number: int = Field(..., description="The page number of the analyzed document")
    page_type: str = Field(
        ..., description="Type of page (e.g., 'financial_table', 'chart', 'text', 'cover')"
    )
    visual_summary: str = Field(
        ..., description="Summary of visual elements like charts, graphs, or tables"
    )
    claims: List[str] = Field(default_factory=list, description="Key claims made on this page")
    metrics: List[str] = Field(
        default_factory=list, description="Financial or operational metrics extracted"
    )
    entities: List[str] = Field(
        default_factory=list, description="Named entities mentioned (companies, people, products)"
    )


class Source(BaseModel):
    """Domain entity representing the origin of ingested data."""

    id: str = Field(..., description="Unique identifier for the source")
    document_type: str = Field(..., description="Type of document (e.g., 'pdf', 'website')")
    file_path: Optional[str] = Field(None, description="Local file path or URL")
    startup_id: str = Field(..., description="Associated startup ID")


class Evidence(BaseModel):
    """Domain entity representing a traceable piece of extracted information."""

    id: str = Field(..., description="Unique identifier for the evidence")
    source_id: str = Field(..., description="Reference to the Source ID")
    content: str = Field(..., description="The actual evidence content or chunk text")
    page_number: Optional[int] = Field(None, description="Page number if applicable")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RetrievedChunk(BaseModel):
    """Domain entity representing a single semantic search result."""

    chunk_id: str = Field(..., description="Unique identifier of the chunk")
    text: str = Field(..., description="The actual chunk text content")
    score: float = Field(..., description="Semantic similarity score (0.0 to 1.0)")
    source_id: str = Field(..., description="Reference to the Source ID")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Rich metadata including url, title, category, context, etc.",
    )


class RetrievalResponse(BaseModel):
    """Final output payload for hybrid semantic retrieval."""

    query: str = Field(..., description="The original search query")
    deal_id: str = Field(..., description="The deal/startup ID for isolation")
    results: List[RetrievedChunk] = Field(
        ..., description="List of retrieved chunks ranked by relevance"
    )
    execution_time_ms: float = Field(
        ..., description="Total execution time in milliseconds"
    )


class ScoreCategory(str, Enum):
    """Enumeration of evaluation categories for investment scoring."""

    TEAM = "team"
    MARKET = "market"
    PRODUCT = "product"
    FINANCIAL = "financial"
    RISK = "risk"


class RecommendationStatus(str, Enum):
    """Enumeration of final investment recommendation statuses."""

    INVEST = "invest"
    WATCHLIST = "watchlist"
    PASS = "pass"


class Finding(BaseModel):
    """Domain entity representing an LLM-extracted fact about a startup."""

    finding_text: str = Field(
        ..., description="The extracted finding or fact about the startup"
    )
    supporting_chunk_ids: List[str] = Field(
        ..., description="List of chunk IDs from which this finding was extracted"
    )


class FactorScore(BaseModel):
    """Domain entity representing a deterministic score for a specific evaluation factor."""

    factor_name: str = Field(
        ..., description="The name of the evaluation factor (e.g., 'Domain Expertise')"
    )
    score: int = Field(
        ..., ge=0, le=100, description="Deterministic score (0-100)"
    )
    findings: List[Finding] = Field(
        ..., description="List of findings that contribute to this factor score"
    )


class CategoryScore(BaseModel):
    """Domain entity representing the aggregated score for a scoring category."""

    category: ScoreCategory = Field(
        ..., description="The scoring category (TEAM, MARKET, PRODUCT, FINANCIAL, RISK)"
    )
    factors: List[FactorScore] = Field(
        ..., description="List of factor scores that roll up to this category"
    )
    aggregate_score: int = Field(
        ..., ge=0, le=100, description="Aggregate score for the category (0-100)"
    )


class InvestmentRecommendation(BaseModel):
    """Final output payload for investment scoring and recommendation."""

    deal_id: str = Field(..., description="The deal/startup ID being evaluated")
    status: RecommendationStatus = Field(
        ..., description="Final recommendation status (INVEST, WATCHLIST, PASS)"
    )
    reasoning: str = Field(
        ..., description="Executive summary explaining the recommendation"
    )
    category_scores: List[CategoryScore] = Field(
        ..., description="Detailed scores broken down by evaluation category"
    )
    pdf_url: Optional[str] = Field(
        None, description="URL to the uploaded pitch deck PDF (if available)"
    )