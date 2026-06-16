"""
Ingestion service module.
Provides pipelines for extracting, chunking, and vectorizing data from various sources.
"""

from backend.services.ingestion.pdf.pipeline import PdfIngestionService

__all__ = [
    "PdfIngestionService",
]