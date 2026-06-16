import logging

from qdrant_client.http import models as qdrant_models

from backend.embeddings.factory import get_embedding_provider
from backend.vectorstore.client import get_qdrant_client, retry_qdrant
from backend.vectorstore.schema import COLLECTION_REGISTRY

logger = logging.getLogger(__name__)


@retry_qdrant()
def ensure_collection_exists(collection_name: str) -> None:
    """
    Ensure that a collection exists in Qdrant.
    If it does not exist, it will be created with the configured embedding dimension
    and cosine distance metric.
    """
    client = get_qdrant_client()
    provider = get_embedding_provider()

    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]

    if collection_name not in collection_names:
        logger.info("Creating collection: %s", collection_name)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=qdrant_models.VectorParams(
                size=provider.dimension,
                distance=qdrant_models.Distance.COSINE,
            ),
        )
    else:
        logger.debug("Collection %s already exists", collection_name)


@retry_qdrant()
def validate_collection(collection_name: str) -> bool:
    """
    Validate that an existing collection has the correct dimension and distance metric.
    """
    client = get_qdrant_client()
    provider = get_embedding_provider()

    try:
        collection_info = client.get_collection(collection_name=collection_name)
        vector_config = collection_info.config.params.vectors

        # Handle both single vector config and named vector config
        if isinstance(vector_config, qdrant_models.VectorParams):
            actual_dim = vector_config.size
            actual_dist = vector_config.distance
        else:
            # Named vectors (take the first one)
            first_vector_name = list(vector_config.keys())[0]
            actual_dim = vector_config[first_vector_name].size
            actual_dist = vector_config[first_vector_name].distance

        if actual_dim != provider.dimension:
            logger.error(
                "Collection %s has invalid dimension: expected %d, got %d",
                collection_name,
                provider.dimension,
                actual_dim,
            )
            return False

        if actual_dist != qdrant_models.Distance.COSINE:
            logger.error(
                "Collection %s has invalid distance metric: expected COSINE, got %s",
                collection_name,
                actual_dist,
            )
            return False

        logger.debug("Collection %s validation passed", collection_name)
        return True

    except Exception as e:
        logger.error("Failed to validate collection %s: %s", collection_name, str(e))
        return False


@retry_qdrant()
def initialize_all_collections() -> None:
    """Initialize and validate all collections defined in the schema registry."""
    logger.info("Initializing all vector store collections")
    for collection_name in COLLECTION_REGISTRY.keys():
        ensure_collection_exists(collection_name)
        if not validate_collection(collection_name):
            logger.warning(
                "Collection %s failed validation. It may need to be recreated.",
                collection_name,
            )
    logger.info("Vector store collections initialization complete")