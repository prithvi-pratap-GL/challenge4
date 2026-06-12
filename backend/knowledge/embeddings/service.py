"""Text embedding service supporting multiple providers."""

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def get_embedding_provider() -> str:
    """Get embedding provider from environment.

    Returns:
        Provider name: 'local' or 'openai_compatible'

    Raises:
        ValueError: If EMBEDDING_PROVIDER not set or invalid.
    """
    provider = os.getenv("EMBEDDING_PROVIDER")
    if not provider:
        raise ValueError("EMBEDDING_PROVIDER environment variable not set")

    if provider not in ("local", "openai_compatible"):
        raise ValueError(
            f"Invalid EMBEDDING_PROVIDER: {provider}. "
            "Must be 'local' or 'openai_compatible'"
        )

    return provider


def embed_text_local(text: str, model: Optional[str] = None) -> list[float]:
    """Embed text using local sentence-transformers model.

    Args:
        text: Text to embed.
        model: Model name from HuggingFace. Defaults to EMBEDDING_MODEL env var.

    Returns:
        Embedding vector.

    Raises:
        ImportError: If sentence-transformers not installed.
        ValueError: If configuration missing.
    """
    if not model:
        model = os.getenv("EMBEDDING_MODEL")
        if not model:
            raise ValueError("EMBEDDING_MODEL environment variable not set")

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ImportError(
            "sentence-transformers is required for local embeddings. "
            "Install with: pip install sentence-transformers"
        )

    logger.debug(f"Loading local embedding model: {model}")

    try:
        model_obj = SentenceTransformer(model)
        embedding = model_obj.encode(text, convert_to_tensor=False).tolist()
        logger.debug(f"Generated embedding of dimension {len(embedding)}")
        return embedding

    except Exception as e:
        logger.error(f"Failed to embed text with local model: {e}")
        raise


def embed_text_openai_compatible(
    text: str,
    model: Optional[str] = None,
) -> list[float]:
    """Embed text using OpenAI-compatible API.

    Args:
        text: Text to embed.
        model: Model name. Defaults to EMBEDDING_MODEL env var.

    Returns:
        Embedding vector.

    Raises:
        ValueError: If configuration missing.
    """
    if not model:
        model = os.getenv("EMBEDDING_MODEL")
        if not model:
            raise ValueError("EMBEDDING_MODEL environment variable not set")

    api_key = os.getenv("EMBEDDING_API_KEY")
    if not api_key:
        raise ValueError("EMBEDDING_API_KEY environment variable not set")

    base_url = os.getenv("EMBEDDING_BASE_URL")
    if not base_url:
        raise ValueError("EMBEDDING_BASE_URL environment variable not set")

    logger.debug(f"Embedding text with {model} at {base_url}")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.embeddings.create(input=text, model=model)
        embedding = response.data[0].embedding

        logger.debug(f"Generated embedding of dimension {len(embedding)}")
        return embedding

    except Exception as e:
        logger.error(f"Failed to embed text: {e}")
        raise


def embed_text(text: str, model: Optional[str] = None) -> list[float]:
    """Convert text to embedding vector.

    Supports multiple embedding providers via environment configuration:
    - local: Uses sentence-transformers for local embedding models
    - openai_compatible: Uses OpenAI SDK with any compatible API

    Args:
        text: Text to embed.
        model: Embedding model to use. Defaults to EMBEDDING_MODEL env var.

    Returns:
        List of floats representing the embedding vector.

    Raises:
        ValueError: If text is empty or configuration missing.
    """
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    provider = get_embedding_provider()

    if provider == "local":
        return embed_text_local(text, model)
    elif provider == "openai_compatible":
        return embed_text_openai_compatible(text, model)
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
