"""Vision analyzer for pitch deck images."""

import asyncio
import base64
import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

import httpx
from openai import AsyncOpenAI

from .prompts import PITCH_DECK_ANALYSIS_PROMPT, DECK_CONTEXT_ASSEMBLY_PROMPT

logger = logging.getLogger(__name__)


def get_vision_client() -> AsyncOpenAI:
    """Create OpenAI-compatible client for vision analysis.

    Reads from environment:
    - API_KEY: API key for the LLM provider
    - BASE_URL: API endpoint URL

    Returns:
        Configured AsyncOpenAI client.

    Raises:
        ValueError: If required environment variables not set.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL environment variable not set")

    return AsyncOpenAI(api_key=api_key, base_url=base_url)


async def encode_image_to_base64(image_path: str) -> str:
    """Encode image file to base64.

    Args:
        image_path: Path to image file.

    Returns:
        Base64 encoded image data.

    Raises:
        FileNotFoundError: If image doesn't exist.
    """
    image_file = Path(image_path)
    if not image_file.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


async def analyze_pitch_deck_images(
    image_paths: list[str],
    startup_name: str,
    model: Optional[str] = None,
) -> dict[str, Any]:
    """Analyze pitch deck images and extract structured information.

    Processes all deck slides and extracts:
    - Startup summary
    - Business model
    - Financial information
    - Market claims
    - Risks
    - Evidence

    Args:
        image_paths: List of paths to rendered deck slides.
        startup_name: Name of the startup.
        model: Vision model to use. Defaults to env MODEL_NAME.

    Returns:
        Dictionary with extracted knowledge fields.
    """
    if not model:
        model = os.getenv("VISION_MODEL")
        if not model:
            raise ValueError("VISION_MODEL environment variable not set")

    client = get_vision_client()
    analyses = []

    logger.info(f"Analyzing {len(image_paths)} slides for {startup_name}")

    # Analyze each slide
    for i, image_path in enumerate(image_paths):
        try:
            logger.debug(f"Analyzing slide {i + 1}")

            image_data = await encode_image_to_base64(image_path)

            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}",
                                    "detail": "high",
                                },
                            },
                            {
                                "type": "text",
                                "text": f"{PITCH_DECK_ANALYSIS_PROMPT}\n\nSlide {i + 1} of {len(image_paths)}.",
                            },
                        ],
                    }
                ],
                max_tokens=1500,
            )

            # Parse response
            response_text = response.choices[0].message.content
            slide_analysis = json.loads(response_text)
            analyses.append(slide_analysis)

            logger.debug(f"Slide {i + 1} analyzed successfully")

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from slide {i + 1}: {e}")
            continue
        except Exception as e:
            logger.error(f"Failed to analyze slide {i + 1}: {e}")
            continue

    if not analyses:
        logger.warning(f"No slides successfully analyzed for {startup_name}")
        return {
            "startup_summary": "",
            "business_model": "",
            "risks": [],
            "financials": [],
            "market_claims": [],
            "evidence": [],
            "retrieved_context": "",
        }

    # Aggregate results
    aggregated = aggregate_slide_analyses(analyses)

    # Assemble context
    aggregated["retrieved_context"] = assemble_context(aggregated)

    logger.info(f"Vision analysis complete for {startup_name}")
    return aggregated


def aggregate_slide_analyses(analyses: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate analyses from multiple slides.

    Combines information from all slides into cohesive output.

    Args:
        analyses: List of per-slide analysis results.

    Returns:
        Aggregated knowledge dictionary.
    """
    summary_parts = []
    business_model_parts = []
    all_risks = []
    all_financials = []
    all_market_claims = []
    all_evidence = []

    for analysis in analyses:
        if "startup_summary" in analysis and analysis["startup_summary"]:
            summary_parts.append(analysis["startup_summary"])

        if "business_model" in analysis and analysis["business_model"]:
            business_model_parts.append(analysis["business_model"])

        if "risks" in analysis and isinstance(analysis["risks"], list):
            all_risks.extend(analysis["risks"])

        if "financials" in analysis and isinstance(analysis["financials"], list):
            all_financials.extend(analysis["financials"])

        if "market_claims" in analysis and isinstance(analysis["market_claims"], list):
            all_market_claims.extend(analysis["market_claims"])

        if "evidence" in analysis and isinstance(analysis["evidence"], list):
            all_evidence.extend(analysis["evidence"])

    return {
        "startup_summary": " ".join(summary_parts) or "Startup under analysis",
        "business_model": " ".join(business_model_parts) or "Business model details not clearly stated",
        "risks": list(dict.fromkeys(all_risks)),  # Remove duplicates
        "financials": list(dict.fromkeys(all_financials)),
        "market_claims": list(dict.fromkeys(all_market_claims)),
        "evidence": list(dict.fromkeys(all_evidence)),
    }


def assemble_context(aggregated: dict[str, Any]) -> str:
    """Assemble comprehensive searchable context.

    Combines all extracted information into a single searchable string.

    Args:
        aggregated: Aggregated knowledge dictionary.

    Returns:
        Context string suitable for embedding and retrieval.
    """
    context_parts = []

    if aggregated.get("startup_summary"):
        context_parts.append(f"Startup: {aggregated['startup_summary']}")

    if aggregated.get("business_model"):
        context_parts.append(f"Business Model: {aggregated['business_model']}")

    if aggregated.get("market_claims"):
        context_parts.append(
            f"Market Claims: {', '.join(aggregated['market_claims'][:5])}"
        )

    if aggregated.get("financials"):
        context_parts.append(
            f"Financials: {', '.join(aggregated['financials'][:5])}"
        )

    if aggregated.get("risks"):
        context_parts.append(f"Risks: {', '.join(aggregated['risks'][:5])}")

    if aggregated.get("evidence"):
        context_parts.append(
            f"Evidence: {', '.join(aggregated['evidence'][:5])}"
        )

    return "\n".join(context_parts) or "No context available"
