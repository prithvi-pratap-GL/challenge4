"""
VentureMind AI — FastAPI Dependency Injection
Configures and wires together all service dependencies for the API layer.

Follows DDD principles: API layer only handles HTTP, delegates to services.
All business logic remains in the Service and Infrastructure layers.
"""

import logging
from typing import AsyncGenerator

from backend.core.settings import settings
from backend.infrastructure.extractors import LlmFindingExtractor
from backend.infrastructure.retrieval import QdrantRetrievalService
from backend.infrastructure.embeddings.provider import get_embedding_provider
from backend.infrastructure.vectorstore.qdrant_client import get_async_qdrant_client
from backend.services.scoring import DeterministicScoringService

logger = logging.getLogger(__name__)


async def get_scoring_service() -> AsyncGenerator[DeterministicScoringService, None]:
    """
    FastAPI dependency injection for DeterministicScoringService.

    Wires together the complete service chain:
    1. Qdrant client + Embedding provider → QdrantRetrievalService
    2. Retrieval service → LlmFindingExtractor
    3. Finding extractor → DeterministicScoringService

    Yields configured service instance for request handling.

    Returns:
        AsyncGenerator yielding DeterministicScoringService instance.

    Raises:
        RuntimeError: If configuration or initialization fails.
    """
    try:
        logger.info("Initializing scoring service dependencies...")

        # ================================================================
        # Initialize Infrastructure Layer
        # ================================================================
        logger.debug("  Loading Qdrant client...")
        qdrant_client = get_async_qdrant_client()

        logger.debug("  Loading embedding provider...")
        embedding_provider = get_embedding_provider()

        # ================================================================
        # Initialize Retrieval Service (Infrastructure)
        # ================================================================
        logger.debug("  Initializing retrieval service...")
        retrieval_service = QdrantRetrievalService(
            qdrant_client=qdrant_client,
            embedding_provider=embedding_provider,
            collection_name="startup_website_chunks",
        )

        # ================================================================
        # Initialize Finding Extractor (Infrastructure)
        # ================================================================
        logger.debug("  Initializing finding extractor...")
        finding_extractor = LlmFindingExtractor(
            retrieval_service=retrieval_service,
        )

        # ================================================================
        # Initialize Scoring Service (Service Layer)
        # ================================================================
        logger.debug("  Initializing scoring service...")
        scoring_service = DeterministicScoringService(
            finding_extractor=finding_extractor,
        )

        logger.info("✓ All service dependencies initialized successfully")

        yield scoring_service

    except Exception as e:
        logger.error(f"✗ Failed to initialize service dependencies: {e}", exc_info=True)
        raise RuntimeError(f"Service initialization failed: {e}") from e
