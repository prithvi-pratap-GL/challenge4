"""Knowledge module for storage and retrieval.

Handles embeddings, vector storage, and semantic retrieval.
"""

from .embeddings.service import embed_text
from .retrieval.service import retrieve_context
from .qdrant.service import store_knowledge
from .memory.service import save_startup_memory, get_startup_memory

__all__ = [
    "embed_text",
    "retrieve_context",
    "store_knowledge",
    "save_startup_memory",
    "get_startup_memory",
]
