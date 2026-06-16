import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from qdrant_client import AsyncQdrantClient, QdrantClient
from qdrant_client.http import models as qdrant_models

from backend.core.settings import settings
from backend.infrastructure.embeddings.provider import get_embedding_provider

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_qdrant(max_retries: int = 3, delay: float = 1.0):
    """Decorator to add retry logic with exponential backoff to Qdrant operations."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(
                        "Qdrant operation '%s' failed (attempt %d/%d): %s",
                        func.__name__,
                        attempt + 1,
                        max_retries,
                        str(e),
                    )
                    if attempt == max_retries - 1:
                        logger.error(
                            "Qdrant operation '%s' failed after %d retries",
                            func.__name__,
                            max_retries,
                        )
                        raise
                    await asyncio.sleep(delay * (2**attempt))
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator


def get_qdrant_client() -> QdrantClient:
    """Initialize and return a synchronous Qdrant client."""
    if not settings.qdrant_url:
        logger.error("QDRANT_URL environment variable is not set")
        raise ValueError("QDRANT_URL environment variable is not set")

    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False,
    )


def get_async_qdrant_client() -> AsyncQdrantClient:
    """Initialize and return an asynchronous Qdrant client."""
    if not settings.qdrant_url:
        logger.error("QDRANT_URL environment variable is not set")
        raise ValueError("QDRANT_URL environment variable is not set")

    return AsyncQdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False,
    )


@retry_qdrant()
async def ensure_collections_exist() -> None:
    """
    Ensure that the required ingestion collections exist in Qdrant.
    Creates them with the configured embedding dimension and cosine distance if they do not exist.
    """
    client = get_async_qdrant_client()
    provider = get_embedding_provider()

    collections = await client.get_collections()
    collection_names = [c.name for c in collections.collections]

    required_collections = ["pitch_deck_chunks", "startup_website_chunks"]

    for collection_name in required_collections:
        if collection_name not in collection_names:
            logger.info("Creating collection: %s", collection_name)
            await client.create_collection(
                collection_name=collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=provider.dimension,
                    distance=qdrant_models.Distance.COSINE,
                ),
            )
        else:
            logger.debug("Collection %s already exists", collection_name)