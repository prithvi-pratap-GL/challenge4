"""Website ingestion pipeline - public entrypoint."""

import asyncio
import logging

from backend.contracts import KnowledgeOutput
from .extractor import extract_website_knowledge

logger = logging.getLogger(__name__)


def ingest_website(url: str, startup_name: str = "Unknown") -> KnowledgeOutput:
    """Public entrypoint: Ingest startup website.

    This is the function P5 will call to process websites.

    Args:
        url: Website URL to analyze.
        startup_name: Name of the startup (used in analysis).

    Returns:
        KnowledgeOutput with extracted information.

    Raises:
        httpx.RequestError: If website fetch fails.
        ValueError: If API key missing or other errors.
    """
    logger.info(f"Ingesting website: {url}")

    # Run async function in event loop
    knowledge_dict = asyncio.run(
        extract_website_knowledge(
            url=url,
            startup_name=startup_name,
        )
    )

    # Convert to KnowledgeOutput
    knowledge = KnowledgeOutput(
        startup_summary=knowledge_dict.get("startup_summary", ""),
        business_model=knowledge_dict.get("business_model", ""),
        risks=knowledge_dict.get("risks", []),
        financials=knowledge_dict.get("financials", []),
        market_claims=knowledge_dict.get("market_claims", []),
        evidence=knowledge_dict.get("evidence", []),
        retrieved_context=knowledge_dict.get("retrieved_context", ""),
    )

    return knowledge
