"""Qdrant vector storage service."""

import hashlib
import json
import logging
import os
from typing import Optional

from qdrant_client.http import models

from backend.contracts import KnowledgeOutput, RetrievalOutput
from backend.knowledge.embeddings.service import embed_text
from .client import create_qdrant_client, ensure_collection_exists

logger = logging.getLogger(__name__)

_client = None


def get_qdrant_client():
    """Get or create Qdrant client (lazy singleton)."""
    global _client
    if _client is None:
        _client = create_qdrant_client()
    return _client


def get_collection_name() -> str:
    """Get collection name from environment.

    Returns:
        Collection name to use in Qdrant.

    Raises:
        ValueError: If QDRANT_COLLECTION not set.
    """
    collection = os.getenv("QDRANT_COLLECTION")
    if not collection:
        raise ValueError("QDRANT_COLLECTION environment variable not set")
    return collection


def generate_point_id(startup_id: str, field: str) -> int:
    """Generate deterministic point ID for a startup field.

    Args:
        startup_id: Unique startup identifier.
        field: Field name within startup knowledge.

    Returns:
        Integer hash for point ID.
    """
    combined = f"{startup_id}:{field}"
    hash_obj = hashlib.md5(combined.encode())
    # Convert first 8 bytes of hash to integer
    return int(hash_obj.hexdigest()[:16], 16) % (2**31)


async def store_knowledge(
    startup_id: str,
    knowledge: KnowledgeOutput,
) -> None:
    """Store startup knowledge in Qdrant.

    Generates embeddings for each field and stores as separate points
    for fine-grained retrieval.

    Args:
        startup_id: Unique startup identifier.
        knowledge: KnowledgeOutput with startup information.

    Raises:
        ValueError: If Qdrant configuration missing.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()

    # Ensure collection exists
    ensure_collection_exists(client, collection_name)

    logger.info(f"Storing knowledge for startup {startup_id}")

    points_to_insert = []

    # Store summary
    if knowledge.startup_summary:
        summary_embedding = embed_text(knowledge.startup_summary)
        point_id = generate_point_id(startup_id, "summary")

        points_to_insert.append(
            models.PointStruct(
                id=point_id,
                vector=summary_embedding,
                payload={
                    "startup_id": startup_id,
                    "field": "summary",
                    "content": knowledge.startup_summary,
                    "type": "startup_summary",
                },
            )
        )

    # Store business model
    if knowledge.business_model:
        business_embedding = embed_text(knowledge.business_model)
        point_id = generate_point_id(startup_id, "business_model")

        points_to_insert.append(
            models.PointStruct(
                id=point_id,
                vector=business_embedding,
                payload={
                    "startup_id": startup_id,
                    "field": "business_model",
                    "content": knowledge.business_model,
                    "type": "business_model",
                },
            )
        )

    # Store financials
    for i, financial in enumerate(knowledge.financials):
        if financial:
            financial_embedding = embed_text(financial)
            point_id = generate_point_id(startup_id, f"financial_{i}")

            points_to_insert.append(
                models.PointStruct(
                    id=point_id,
                    vector=financial_embedding,
                    payload={
                        "startup_id": startup_id,
                        "field": f"financial_{i}",
                        "content": financial,
                        "type": "financial",
                    },
                )
            )

    # Store market claims
    for i, claim in enumerate(knowledge.market_claims):
        if claim:
            claim_embedding = embed_text(claim)
            point_id = generate_point_id(startup_id, f"market_claim_{i}")

            points_to_insert.append(
                models.PointStruct(
                    id=point_id,
                    vector=claim_embedding,
                    payload={
                        "startup_id": startup_id,
                        "field": f"market_claim_{i}",
                        "content": claim,
                        "type": "market_claim",
                    },
                )
            )

    # Store risks
    for i, risk in enumerate(knowledge.risks):
        if risk:
            risk_embedding = embed_text(risk)
            point_id = generate_point_id(startup_id, f"risk_{i}")

            points_to_insert.append(
                models.PointStruct(
                    id=point_id,
                    vector=risk_embedding,
                    payload={
                        "startup_id": startup_id,
                        "field": f"risk_{i}",
                        "content": risk,
                        "type": "risk",
                    },
                )
            )

    # Store full context
    if knowledge.retrieved_context:
        context_embedding = embed_text(knowledge.retrieved_context)
        point_id = generate_point_id(startup_id, "context")

        points_to_insert.append(
            models.PointStruct(
                id=point_id,
                vector=context_embedding,
                payload={
                    "startup_id": startup_id,
                    "field": "context",
                    "content": knowledge.retrieved_context,
                    "type": "context",
                },
            )
        )

    if points_to_insert:
        try:
            client.upsert(
                collection_name=collection_name,
                points=points_to_insert,
            )
            logger.info(f"Stored {len(points_to_insert)} points for {startup_id}")

        except Exception as e:
            logger.error(f"Failed to store knowledge in Qdrant: {e}")
            raise
    else:
        logger.warning(f"No knowledge points to store for {startup_id}")


def search_knowledge(
    query: str,
    startup_id: Optional[str] = None,
    top_k: int = 5,
) -> list[dict]:
    """Search stored knowledge.

    Args:
        query: Search query string.
        startup_id: Optional filter to specific startup.
        top_k: Number of top results to return.

    Returns:
        List of search results with content and scores.
    """
    client = get_qdrant_client()
    collection_name = get_collection_name()

    logger.debug(f"Searching knowledge for query: {query}")

    try:
        # Generate embedding for query
        query_embedding = embed_text(query)

        # Build filter if startup_id specified
        query_filter = None
        if startup_id:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="startup_id",
                        match=models.MatchValue(value=startup_id),
                    )
                ]
            )

        # Search
        results = client.search(
            collection_name=collection_name,
            query_vector=query_embedding,
            query_filter=query_filter,
            limit=top_k,
        )

        # Extract results
        search_results = []
        for scored_point in results:
            search_results.append(
                {
                    "startup_id": scored_point.payload.get("startup_id"),
                    "field": scored_point.payload.get("field"),
                    "content": scored_point.payload.get("content"),
                    "type": scored_point.payload.get("type"),
                    "score": scored_point.score,
                }
            )

        logger.debug(f"Found {len(search_results)} results")
        return search_results

    except Exception as e:
        logger.error(f"Failed to search knowledge: {e}")
        return []
