import logging
import threading
from typing import List, Optional

from sentence_transformers import SentenceTransformer

from backend.core.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingProvider:
    """Thread-safe, lazy-loading singleton embedding provider using sentence-transformers."""

    _instance: Optional["EmbeddingProvider"] = None
    _lock = threading.Lock()
    _model: Optional[SentenceTransformer] = None
    _model_name: str
    _device: str
    _dimension: int = 384

    def __new__(cls) -> "EmbeddingProvider":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EmbeddingProvider, cls).__new__(cls)
                    cls._instance._model_name = settings.embedding_model
                    cls._instance._device = settings.embedding_device
        return cls._instance

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    logger.info("Loading embedding model: %s on device: %s", self._model_name, self._device)
                    self._model = SentenceTransformer(self._model_name, device=self._device)
        return self._model

    def embed(self, text: str) -> List[float]:
        """Generate a single embedding for the given text."""
        model = self._get_model()
        embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        model = self._get_model()
        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, batch_size=32)
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        """Return the dimension of the embedding vectors."""
        return self._dimension


def get_embedding_provider() -> EmbeddingProvider:
    """Factory function to get the configured embedding provider."""
    return EmbeddingProvider()