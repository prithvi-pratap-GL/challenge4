import logging
import os
import time
from functools import wraps
from typing import Any, Callable, TypeVar

from qdrant_client import QdrantClient

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_qdrant(max_retries: int = 3, delay: float = 1.0):
    """Decorator to add retry logic to Qdrant operations."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
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
                    time.sleep(delay * (2**attempt))  # Exponential backoff
            raise RuntimeError("Unreachable")

        return wrapper

    return decorator


def get_qdrant_client() -> QdrantClient:
    """
    Initialize and return a Qdrant client using environment variables.

    Environment variables:
        QDRANT_URL: The URL of the Qdrant server.
        QDRANT_API_KEY: The API key for authentication (optional).
    """
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url:
        logger.error("QDRANT_URL environment variable is not set")
        raise ValueError("QDRANT_URL environment variable is not set")

    logger.info("Initializing Qdrant client with URL: %s", url)
    return QdrantClient(
        url=url,
        api_key=api_key,
        prefer_grpc=False,
    )