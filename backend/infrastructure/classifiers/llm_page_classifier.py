"""
VentureMind AI — LLM-based Page Classifier Infrastructure
Semantic page categorization using Hugging Face Router with JSON-mode LLM inference.

Implements IPageClassifier using AsyncOpenAI pointing to the Hugging Face Router.
Optimized for token efficiency and deterministic JSON output.
"""

import json
import logging
from typing import Optional

from openai import AsyncOpenAI

from backend.core.settings import settings
from backend.domain.interfaces import IPageClassifier
from backend.domain.schemas import PageCategory

logger = logging.getLogger(__name__)


class LlmPageClassifier(IPageClassifier):
    """
    Production-ready page classifier using LLM via Hugging Face Router.

    Features:
    - Token-efficient classification (1000-char text truncation)
    - JSON-mode LLM inference for deterministic output
    - Graceful fallback to UNKNOWN on any failure
    - Comprehensive error handling and logging
    - Async-first design for high throughput
    """

    def __init__(self):
        """
        Initialize the LLM page classifier.

        Instantiates AsyncOpenAI client pointing to the Hugging Face Router
        using API key and base URL from Pydantic settings.
        """
        self.api_key = settings.hf_router_api_key
        self.base_url = settings.hf_router_base_url
        self.model = settings.llm_model_name
        self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        logger.info(f"✓ LLM page classifier initialized (model: {self.model})")

    async def classify_page(self, text: str) -> PageCategory:
        """
        Classify a page based on its Markdown text content.

        Uses LLM with JSON-mode to extract a deterministic category.
        Handles errors gracefully by returning UNKNOWN.

        Args:
            text: The Markdown text content of the page (will be truncated to 1000 chars).

        Returns:
            PageCategory: The inferred category, or UNKNOWN if classification fails.
        """
        # Token efficiency: truncate to first 1000 characters
        truncated_text = text[:1000] if text else ""

        if not truncated_text:
            logger.warning("Empty text provided for classification, returning UNKNOWN")
            return PageCategory.UNKNOWN

        # Build the system prompt with all enum values
        category_values = ", ".join([f'"{cat.value}"' for cat in PageCategory])
        system_prompt = (
            f"You are a page classification router. Analyze the provided page content and classify it "
            f"into one of these exact categories: {category_values}.\n\n"
            f"Return a JSON object with a single key 'category' containing one of the category values above.\n"
            f"Be precise and deterministic. If unsure, use 'unknown'."
        )

        user_prompt = f"Classify this page content:\n\n{truncated_text}"

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,  # Deterministic output
                max_tokens=100,  # Classification only needs a few tokens
            )

            # Extract and parse the JSON response
            response_text = response.choices[0].message.content
            if not response_text:
                logger.warning("Empty response from LLM, returning UNKNOWN")
                return PageCategory.UNKNOWN

            response_json = json.loads(response_text)
            category_str = response_json.get("category", "unknown").lower()

            # Validate against PageCategory enum
            for category in PageCategory:
                if category.value == category_str:
                    logger.debug(f"✓ Classified page as: {category.value}")
                    return category

            # If no match found, log and return UNKNOWN
            logger.warning(f"LLM returned unknown category '{category_str}', returning UNKNOWN")
            return PageCategory.UNKNOWN

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse LLM JSON response: {e}")
            return PageCategory.UNKNOWN
        except ValueError as e:
            logger.warning(f"Invalid response format from LLM: {e}")
            return PageCategory.UNKNOWN
        except Exception as e:
            logger.error(
                f"LLM classification failed ({type(e).__name__}): {e}. "
                f"Returning UNKNOWN."
            )
            return PageCategory.UNKNOWN
