"""Qdrant client initialization."""

import logging
import os
from typing import Optional

from qdrant_client import QdrantClient
from qdrant_client.http import models

logger = logging.getLogger(__name__)


def create_qdrant_client() -> QdrantClient:
    """Create Qdrant client from environment configuration.

    Reads from environment:
    - QDRANT_URL: Qdrant server URL
    - QDRANT_API_KEY: Optional API key for authentication
    - QDRANT_TIMEOUT: Optional timeout in seconds

    Returns:
        Configured QdrantClient instance.

    Raises:
        ValueError: If required environment variables not set.
    """
    url = os.getenv("QDRANT_URL")
    if not url:
        raise ValueError("QDRANT_URL environment variable not set")

    api_key = os.getenv("QDRANT_API_KEY")
    timeout = os.getenv("QDRANT_TIMEOUT", "30")

    try:
        timeout_sec = int(timeout)
    except ValueError:
        logger.warning(f"Invalid timeout value: {timeout}, using default 30")
        timeout_sec = 30

    logger.debug(f"Creating Qdrant client for {url}")

    try:
        client = QdrantClient(
            url=url,
            api_key=api_key if api_key else None,
            timeout=timeout_sec,
        )

        # Test connection
        client.get_collections()
        logger.info(f"Successfully connected to Qdrant at {url}")

        return client

    except Exception as e:
        logger.error(f"Failed to create Qdrant client: {e}")
        raise


def ensure_collection_exists(
    client: QdrantClient,
    collection_name: str,
    vector_size: int = 1536,
) -> None:
    """Ensure collection exists in Qdrant, create if needed.

    Args:
        client: Qdrant client.
        collection_name: Name of collection.
        vector_size: Size of embedding vectors.
    """
    try:
        client.get_collection(collection_name)
        logger.debug(f"Collection {collection_name} exists")

    except Exception:
        logger.info(f"Creating collection {collection_name}")

        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

        logger.info(f"Created collection {collection_name}")
