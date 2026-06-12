"""PDF extraction orchestration."""

import logging
from typing import Optional

from backend.contracts import KnowledgeOutput
from backend.ingestion.vision.analyzer import analyze_pitch_deck_images
from .renderer import render_pdf_pages

logger = logging.getLogger(__name__)


async def extract_pdf_knowledge(
    pdf_path: str,
    startup_name: str,
    render_dir: Optional[str] = None,
) -> KnowledgeOutput:
    """Extract knowledge from a PDF pitch deck.

    Orchestrates:
    1. Render PDF pages to images
    2. Analyze images with vision model
    3. Generate structured knowledge output

    Args:
        pdf_path: Path to PDF file.
        startup_name: Name of the startup.
        render_dir: Optional directory for rendered images.

    Returns:
        KnowledgeOutput with extracted information.
    """
    logger.info(f"Extracting knowledge from {pdf_path} for {startup_name}")

    # Step 1: Render pages
    image_paths = render_pdf_pages(pdf_path, output_dir=render_dir)
    logger.debug(f"Rendered {len(image_paths)} pages")

    # Step 2: Analyze images
    vision_output = await analyze_pitch_deck_images(
        image_paths=image_paths,
        startup_name=startup_name,
    )
    logger.debug("Vision analysis complete")

    # Step 3: Build knowledge output (from vision analysis)
    knowledge = KnowledgeOutput(
        startup_summary=vision_output.get("startup_summary", ""),
        business_model=vision_output.get("business_model", ""),
        risks=vision_output.get("risks", []),
        financials=vision_output.get("financials", []),
        market_claims=vision_output.get("market_claims", []),
        evidence=vision_output.get("evidence", []),
        retrieved_context=vision_output.get("retrieved_context", ""),
    )

    logger.info(f"Extracted knowledge for {startup_name}")
    return knowledge
