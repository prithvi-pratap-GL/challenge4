"""Frozen contract models for VentureMind AI."""

from pydantic import BaseModel, Field
from typing import Optional


class StartupInput(BaseModel):
    """Input for startup analysis.

    Attributes:
        startup_name: Name of the startup.
        website_url: Optional URL of startup website.
        pitch_deck_path: Optional path to pitch deck PDF.
    """

    startup_name: str = Field(..., description="Name of the startup")
    website_url: Optional[str] = Field(None, description="URL of startup website")
    pitch_deck_path: Optional[str] = Field(None, description="Path to pitch deck PDF")


class KnowledgeOutput(BaseModel):
    """Structured knowledge about a startup.

    This is the primary output of the P3 Knowledge Intelligence module.
    Consumed by Bull, Bear, Reviewer, Red Team, and Committee agents.

    Attributes:
        startup_summary: Short overview of the startup.
        business_model: Explanation of how the company makes money.
        risks: List of identified risks.
        financials: Revenue, growth, and financial projections.
        market_claims: Market size, customer, growth, and competitive claims.
        evidence: Sources supporting the claims.
        retrieved_context: Combined searchable context for retrieval.
    """

    startup_summary: str = Field(
        ..., description="Short startup overview"
    )
    business_model: str = Field(
        ..., description="Explanation of how company makes money"
    )
    risks: list[str] = Field(
        default_factory=list, description="List of identified risks"
    )
    financials: list[str] = Field(
        default_factory=list, description="Revenue, growth, and financial information"
    )
    market_claims: list[str] = Field(
        default_factory=list, description="Market size and competitive advantage claims"
    )
    evidence: list[str] = Field(
        default_factory=list, description="Sources supporting claims"
    )
    retrieved_context: str = Field(
        ..., description="Combined searchable context for retrieval"
    )


class RetrievalOutput(BaseModel):
    """Retrieval results for startup context.

    Attributes:
        context: Retrieved context string.
        sources: List of source references.
    """

    context: str = Field(..., description="Retrieved context")
    sources: list[str] = Field(
        default_factory=list, description="Source references"
    )
