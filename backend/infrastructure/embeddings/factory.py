import logging

from backend.embeddings.provider import EmbeddingProvider
from backend.embeddings.local import LocalEmbeddingProvider

logger = logging.getLogger(__name__)


def get_embedding_provider() -> EmbeddingProvider:
    """Factory function to get the configured embedding provider."""
    logger.debug("Retrieving embedding provider instance")
    return LocalEmbeddingProvider()