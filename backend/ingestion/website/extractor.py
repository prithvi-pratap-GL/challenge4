"""Website content extraction."""

import json
import logging
import os
from typing import Any, Optional

import httpx
from openai import AsyncOpenAI

from backend.ingestion.vision.prompts import WEBSITE_ANALYSIS_PROMPT

logger = logging.getLogger(__name__)


async def fetch_website_content(url: str, timeout: int = 30) -> str:
    """Fetch website content.

    Args:
        url: Website URL.
        timeout: Request timeout in seconds.

    Returns:
        Plain text content from website.

    Raises:
        httpx.RequestError: If request fails.
    """
    if not url.startswith("http"):
        url = f"https://{url}"

    logger.debug(f"Fetching website: {url}")

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise


def extract_text_from_html(html: str) -> str:
    """Extract plain text from HTML.

    Removes script tags, style tags, and HTML markup.

    Args:
        html: Raw HTML content.

    Returns:
        Plain text extracted from HTML.
    """
    import re

    # Remove script and style elements
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html)

    # Decode HTML entities
    import html as html_module

    text = html_module.unescape(text)

    # Clean up whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


async def analyze_website_with_vision(
    content: str,
    url: str,
    model: Optional[str] = None,
) -> dict[str, Any]:
    """Analyze website content with LLM.

    Extracts structured information about the startup from website content.

    Args:
        content: Plain text content from website.
        url: Website URL (for context).
        model: Model to use. Defaults to env MODEL_NAME.

    Returns:
        Dictionary with extracted knowledge fields.

    Raises:
        ValueError: If required environment variables not set.
    """
    if not model:
        model = os.getenv("MODEL_NAME")
        if not model:
            raise ValueError("MODEL_NAME environment variable not set")

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable not set")

    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError("BASE_URL environment variable not set")

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    logger.debug(f"Analyzing website content from {url}")

    # Truncate content if too long (LLM context limits)
    max_chars = 8000
    if len(content) > max_chars:
        content = content[:max_chars] + "... [content truncated]"

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"{WEBSITE_ANALYSIS_PROMPT}\n\nWebsite: {url}\n\nContent:\n{content}",
                }
            ],
            max_tokens=1500,
        )

        response_text = response.choices[0].message.content
        analysis = json.loads(response_text)

        logger.debug(f"Website analysis complete for {url}")
        return analysis

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from website analysis: {e}")
        return {
            "startup_summary": "",
            "business_model": "",
            "risks": [],
            "financials": [],
            "market_claims": [],
            "evidence": [],
        }
    except Exception as e:
        logger.error(f"Failed to analyze website: {e}")
        raise


async def extract_website_knowledge(
    url: str,
    startup_name: str = "Unknown",
) -> dict[str, Any]:
    """Extract knowledge from a website.

    Orchestrates:
    1. Fetch website content
    2. Extract plain text
    3. Analyze with LLM
    4. Generate context

    Args:
        url: Website URL.
        startup_name: Name of the startup.

    Returns:
        Dictionary with extracted knowledge fields.
    """
    logger.info(f"Extracting knowledge from website: {url}")

    try:
        # Step 1: Fetch content
        html = await fetch_website_content(url)
        logger.debug(f"Fetched {len(html)} characters from {url}")

        # Step 2: Extract text
        text = extract_text_from_html(html)
        logger.debug(f"Extracted {len(text)} characters of text")

        # Step 3: Analyze with LLM
        analysis = await analyze_website_with_vision(
            content=text,
            url=url,
        )

        # Step 4: Assemble context
        context = assemble_website_context(analysis, startup_name, url)
        analysis["retrieved_context"] = context

        logger.info(f"Extracted knowledge from {url}")
        return analysis

    except Exception as e:
        logger.error(f"Failed to extract website knowledge: {e}")
        raise


def assemble_website_context(
    analysis: dict[str, Any],
    startup_name: str,
    url: str,
) -> str:
    """Assemble searchable context from website analysis.

    Args:
        analysis: Analysis results from LLM.
        startup_name: Name of startup.
        url: Website URL.

    Returns:
        Context string suitable for embedding and retrieval.
    """
    context_parts = [f"Website: {url}", f"Startup: {startup_name}"]

    if analysis.get("startup_summary"):
        context_parts.append(f"About: {analysis['startup_summary']}")

    if analysis.get("business_model"):
        context_parts.append(f"Business Model: {analysis['business_model']}")

    if analysis.get("market_claims"):
        context_parts.append(
            f"Market: {', '.join(analysis['market_claims'][:5])}"
        )

    if analysis.get("financials"):
        context_parts.append(
            f"Financials: {', '.join(analysis['financials'][:3])}"
        )

    return "\n".join(context_parts) or "No context available"
