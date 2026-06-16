"""
VentureMind AI — Qdrant-based Retrieval Service Infrastructure
Hybrid semantic search with strict multi-tenant deal isolation.

Implements IRetrievalService using Qdrant vector search with deterministic
filtering to prevent cross-startup data leakage.
"""

import logging
import time
from typing import List, Optional

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models as qdrant_models

from backend.domain.interfaces import IRetrievalService
from backend.domain.schemas import PageCategory, RetrievedChunk, RetrievalResponse
from backend.infrastructure.embeddings.provider import EmbeddingProvider

logger = logging.getLogger(__name__)


class QdrantRetrievalService(IRetrievalService):
    """
    Production-ready retrieval service for hybrid semantic search.

    Features:
    - Strict deal/startup isolation via payload filtering
    - Category-based filtering (optional)
    - Performance tracking with execution time metrics
    - Graceful error handling with clear logging
    - Async-first design for high throughput

    Enforces isolation at the Qdrant filter level, preventing accidental
    cross-startup data leakage or hallucinations.
    """

    def __init__(
        self,
        qdrant_client: AsyncQdrantClient,
        embedding_provider: EmbeddingProvider,
        collection_name: str = "startup_website_chunks",
    ):
        """
        Initialize the Qdrant retrieval service.

        Args:
            qdrant_client: Async Qdrant client for vector search.
            embedding_provider: Provider for converting queries to vectors.
            collection_name: Qdrant collection to search (default: startup_website_chunks).
        """
        self.qdrant_client = qdrant_client
        self.embedding_provider = embedding_provider
        self.collection_name = collection_name
        logger.info(
            f"✓ Qdrant retrieval service initialized (collection: {collection_name})"
        )

    async def search(
        self,
        query: str,
        deal_id: str,
        top_k: int = 5,
        categories: Optional[List[PageCategory]] = None,
    ) -> RetrievalResponse:
        """
        Search across ingested documents with strict deal isolation.

        Enforces strict data isolation by filtering on deal_id, preventing
        cross-startup hallucinations or data leakage.

        Flow:
        1. Start timer for execution metrics
        2. Vectorize query using embedding provider
        3. Build Qdrant filter with deal_id isolation + optional category filter
        4. Execute vector search against Qdrant
        5. Map ScoredPoint results to RetrievedChunk Pydantic models
        6. Return complete RetrievalResponse with execution time

        Args:
            query: The search query string.
            deal_id: The deal/startup ID (REQUIRED for strict isolation).
            top_k: Maximum number of results to return (default: 5).
            categories: Optional filter by page categories.

        Returns:
            RetrievalResponse: Search results with metadata and execution time.

        Raises:
            RuntimeError: If Qdrant search fails.
        """
        start_time = time.time()
        logger.info(
            f"Starting search: query='{query}' deal_id={deal_id} top_k={top_k} "
            f"categories={[c.value for c in categories] if categories else 'None'}"
        )

        try:
            # ================================================================
            # Step 1: Timing (already started above)
            # ================================================================

            # ================================================================
            # Step 2: Vectorization
            # ================================================================
            logger.debug(f"Vectorizing query: '{query}'")
            query_vector = self.embedding_provider.embed(query)
            logger.debug(f"  ✓ Query vector dimension: {len(query_vector)}")

            # ================================================================
            # Step 3: Qdrant Filtering (Strict Isolation)
            # ================================================================
            logger.debug("Building Qdrant filter with deal_id isolation...")

            # CRUCIAL: Filter for exact deal_id match (strict isolation)
            deal_filter = qdrant_models.FieldCondition(
                key="deal_id",
                match=qdrant_models.MatchValue(value=deal_id),
            )

            # Optional: Filter by categories if provided
            filters = deal_filter

            if categories:
                category_values = [cat.value for cat in categories]
                logger.debug(f"  Adding category filter: {category_values}")

                category_filter = qdrant_models.FieldCondition(
                    key="payload.category",
                    match=qdrant_models.MatchAny(any=category_values),
                )

                # Combine filters: deal_id AND (categories)
                filters = qdrant_models.Filter(
                    must=[deal_filter, category_filter]
                )
            else:
                # Only deal_id filter
                filters = qdrant_models.Filter(must=[deal_filter])

            logger.debug("  ✓ Filter built with deal_id isolation")

            # ================================================================
            # Step 4: Vector Search
            # ================================================================
            logger.debug(
                f"Searching Qdrant collection '{self.collection_name}' "
                f"with top_k={top_k}"
            )

            search_results = await self.qdrant_client.query_points(
                collection_name=self.collection_name,
                query=query_vector, # query_points uses 'query' instead of 'query_vector'
                query_filter=filters,
                limit=top_k,
                with_payload=True,
            )

            points_list = search_results.points

            logger.info(f"  ✓ Qdrant returned {len(search_results.points)} results")

            # ================================================================
            # Step 5: Mapping to RetrievedChunk
            # ================================================================
            retrieved_chunks: List[RetrievedChunk] = []

            for scored_point in points_list:
                try:
                    # Extract fields from Qdrant ScoredPoint
                    chunk_id = scored_point.id
                    score = scored_point.score
                    payload = scored_point.payload or {}

                    # Extract source_id from payload (required for traceability)
                    source_id = payload.get("source_id", "unknown")

                    # Extract chunk text
                    text = payload.get("text", "")

                    # Build metadata dict from remaining payload
                    metadata = {
                        k: v
                        for k, v in payload.items()
                        if k not in ["text", "source_id"]
                    }

                    # Create RetrievedChunk
                    chunk = RetrievedChunk(
                        chunk_id=str(chunk_id),
                        text=text,
                        score=score,
                        source_id=source_id,
                        metadata=metadata,
                    )
                    retrieved_chunks.append(chunk)
                    logger.debug(
                        f"  Mapped chunk {chunk_id}: score={score:.4f} source={source_id}"
                    )

                except Exception as e:
                    logger.warning(
                        f"Failed to map Qdrant result {scored_point.id}: {e}"
                    )
                    continue

            logger.debug(f"Mapped {len(retrieved_chunks)} chunks to RetrievedChunk")

            # ================================================================
            # Step 6: Calculate Execution Time & Return
            # ================================================================
            execution_time_ms = (time.time() - start_time) * 1000

            response = RetrievalResponse(
                query=query,
                deal_id=deal_id,
                results=retrieved_chunks,
                execution_time_ms=execution_time_ms,
            )

            logger.info(
                f"✓ Search completed: {len(retrieved_chunks)} results in "
                f"{execution_time_ms:.2f}ms"
            )

            return response

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            error_msg = f"Qdrant search failed ({type(e).__name__}): {e}"
            logger.error(f"✗ {error_msg} (execution time: {execution_time_ms:.2f}ms)")
            raise RuntimeError(error_msg) from e
