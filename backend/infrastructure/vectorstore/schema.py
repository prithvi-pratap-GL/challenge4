from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class BaseVectorPayload(BaseModel):
    """Base class for all vector store payloads."""

    text: str = Field(..., description="The original text content")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class PitchDeckChunkPayload(BaseVectorPayload):
    startup_id: str
    document_id: str
    page_number: Optional[int] = None


class StartupWebsiteChunkPayload(BaseVectorPayload):
    startup_id: str
    url: str
    section: Optional[str] = None


class CompetitorIntelligencePayload(BaseVectorPayload):
    startup_id: str
    competitor_name: str
    source_url: Optional[str] = None


class BenchmarkNarrativePayload(BaseVectorPayload):
    benchmark_id: str
    category: str


class DealMemoryPayload(BaseVectorPayload):
    deal_id: str
    startup_id: str
    notes: Optional[str] = None


# Registry of all collections and their payload types
COLLECTION_REGISTRY: Dict[str, type[BaseVectorPayload]] = {
    "pitch_deck_chunks": PitchDeckChunkPayload,
    "startup_website_chunks": StartupWebsiteChunkPayload,
    "competitor_intelligence": CompetitorIntelligencePayload,
    "benchmark_narratives": BenchmarkNarrativePayload,
    "deal_memory": DealMemoryPayload,
}