"""VentureMind AI Backend - P3 Knowledge Intelligence Module."""

from backend.contracts import StartupInput, KnowledgeOutput, RetrievalOutput
from backend.ingestion.pdf.pipeline import ingest_pitch_deck
from backend.ingestion.website.pipeline import ingest_website
from backend.knowledge.retrieval.service import retrieve_context
from backend.knowledge.embeddings.service import embed_text

__all__ = [
    "StartupInput",
    "KnowledgeOutput",
    "RetrievalOutput",
    "ingest_pitch_deck",
    "ingest_website",
    "retrieve_context",
    "embed_text",
]
