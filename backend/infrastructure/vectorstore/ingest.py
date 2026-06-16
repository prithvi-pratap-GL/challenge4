import logging
from typing import List, Type

from pydantic import BaseModel
from qdrant_client.http import models as qdrant_models

from backend.embeddings.factory import get_embedding_provider
from backend.vectorstore.client import get_qdrant_client, retry_qdrant
from backend.vectorstore.schema import BaseVectorPayload

logger = logging.getLogger(__name__)


@retry_qdrant()
def upsert(
    collection_name: str,
    document_id: str,
    text: str,
    payload_model: Type[BaseVectorPayload],
    **payload_kwargs,
) -> None:
    """
    Upsert a single document into the specified collection using a typed payload model.
    """
    provider = get_embedding_provider()
    vector = provider.embed(text)

    # Construct the typed payload
    payload_data = {"text": text, **payload_kwargs}
    try:
        payload = payload_model(**payload_data)
    except Exception as e:
        logger.error("Failed to validate payload for document %s: %s", document_id, str(e))
        raise ValueError(f"Invalid payload for document {document_id}: {e}")

    client = get_qdrant_client()
    client.upsert(
        collection_name=collection_name,
        points=[
            qdrant_models.PointStruct(
                id=document_id,
                vector=vector,
                payload=payload.model_dump(),
            )
        ],
    )
    logger.debug("Upserted document %s to collection %s", document_id, collection_name)


@retry_qdrant()
def batch_upsert(
    collection_name: str,
    document_ids: List[str],
    texts: List[str],
    payload_model: Type[BaseVectorPayload],
    payload_kwargs_list: List[dict],
) -> None:
    """
    Upsert a batch of documents into the specified collection using typed payload models.
    """
    if len(document_ids) != len(texts) or len(document_ids) != len(payload_kwargs_list):
        raise ValueError("document_ids, texts, and payload_kwargs_list must have the same length")

    provider = get_embedding_provider()
    vectors = provider.embed_batch(texts)

    points = []
    for i, doc_id in enumerate(document_ids):
        payload_data = {"text": texts[i], **payload_kwargs_list[i]}
        try:
            payload = payload_model(**payload_data)
        except Exception as e:
            logger.error("Failed to validate payload for document %s: %s", doc_id, str(e))
            raise ValueError(f"Invalid payload for document {doc_id}: {e}")

        points.append(
            qdrant_models.PointStruct(
                id=doc_id,
                vector=vectors[i],
                payload=payload.model_dump(),
            )
        )

    client = get_qdrant_client()
    client.upsert(
        collection_name=collection_name,
        points=points,
    )
    logger.debug("Batch upserted %d documents to collection %s", len(document_ids), collection_name)


@retry_qdrant()
def delete_by_id(collection_name: str, document_id: str) -> None:
    """
    Delete a document from the specified collection by its ID.
    """
    client = get_qdrant_client()
    client.delete(
        collection_name=collection_name,
        points_selector=qdrant_models.PointIdsList(
            points=[document_id],
        ),
    )
    logger.debug("Deleted document %s from collection %s", document_id, collection_name)