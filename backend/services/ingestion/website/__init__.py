"""
VentureMind AI — Website Ingestion Service
Orchestration layer for crawling, classifying, chunking, and embedding startup websites.
"""

from backend.services.ingestion.website.pipeline import (
    EvidenceRepository,
    SourceRepository,
    WebsiteIngestionResult,
    WebsiteIngestionService,
)

__all__ = [
    "WebsiteIngestionService",
    "WebsiteIngestionResult",
    "SourceRepository",
    "EvidenceRepository",
]
