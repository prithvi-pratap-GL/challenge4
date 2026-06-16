import logging
from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel
from qdrant_client.http import models as qdrant_models

from backend.embeddings.factory import get_embedding_provider
from backend.vectorstore.client import get_qdrant_client, retry_qdrant
from backend.vectorstore.schema import BaseVectorPayload

logger = logging.getLogger(__name__)


@retry_qdrant()
def semantic_search(
    collection_name: str,
    query: str,
    payload_model: Type[BaseVectorPayload],
    limit: int = 5,
    score_threshold: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Perform a semantic search on the specified collection.
    Returns a list of dictionaries containing 'id', 'score', and 'payload' (as typed model).
    """
    provider = get_embedding_provider()
    query_vector = provider.embed(query)

    client = get_qdrant_client()
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        score_threshold=score_threshold,
    )

    parsed_results = []
    for result in results:
        try:
            payload = payload_model.model_validate(result.payload or {})
            parsed_results.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": payload,
                }
            )
        except Exception as e:
            logger.warning("Failed to parse payload for result %s: %s", result.id, str(e))
            # Fallback to raw dict if validation fails
            parsed_results.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload or {},
                }
            )

    return parsed_results


@retry_qdrant()
def filtered_search(
    collection_name: str,
    query: str,
    payload_model: Type[BaseVectorPayload],
    filter_conditions: Dict[str, Any],
    limit: int = 5,
    score_threshold: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """
    Perform a filtered semantic search on the specified collection.
    filter_conditions is a dictionary where keys are payload field names
    and values are the expected values (or lists of values for MatchAny).
    """
    provider = get_embedding_provider()
    query_vector = provider.embed(query)

    must_conditions = []
    for key, value in filter_conditions.items():
        if isinstance(value, list):
            must_conditions.append(
                qdrant_models.FieldCondition(
                    key=key,
                    match=qdrant_models.MatchAny(any=value),
                )
            )
        else:
            must_conditions.append(
                qdrant_models.FieldCondition(
                    key=key,
                    match=qdrant_models.MatchValue(value=value),
                )
            )

    search_filter = qdrant_models.Filter(must=must_conditions)

    client = get_qdrant_client()
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        query_filter=search_filter,
        limit=limit,
        score_threshold=score_threshold,
    )

    parsed_results = []
    for result in results:
        try:
            payload = payload_model.model_validate(result.payload or {})
            parsed_results.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": payload,
                }
            )
        except Exception as e:
            logger.warning("Failed to parse payload for result %s: %s", result.id, str(e))
            parsed_results.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload or {},
                }
            )

    return parsed_results