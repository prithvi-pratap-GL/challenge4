"""PDF ingestion pipeline - public entrypoint."""

import asyncio
import logging

from backend.contracts import KnowledgeOutput
from .extractor import extract_pdf_knowledge

logger = logging.getLogger(__name__)


def ingest_pitch_deck(pdf_path: str, startup_name: str = "Unknown") -> KnowledgeOutput:
    """Public entrypoint: Ingest pitch deck PDF.

    This is the function P5 will call to process pitch decks.

    Args:
        pdf_path: Path to pitch deck PDF.
        startup_name: Name of the startup (used in analysis).

    Returns:
        KnowledgeOutput with extracted information.

    Raises:
        FileNotFoundError: If PDF doesn't exist.
        ValueError: If PDF is invalid.
    """
    logger.info(f"Ingesting pitch deck: {pdf_path}")

    # Run async function in event loop
    knowledge = asyncio.run(
        extract_pdf_knowledge(
            pdf_path=pdf_path,
            startup_name=startup_name,
        )
    )

    return knowledge
