"""Semantic retrieval service for agents.

This is the ONLY retrieval function that agents should use.
Bull, Bear, Reviewer, Red Team, and Committee agents use this.
"""

import logging
from typing import Optional

from backend.contracts import RetrievalOutput
from backend.knowledge.qdrant.service import search_knowledge

logger = logging.getLogger(__name__)


def retrieve_context(
    query: str,
    startup_id: Optional[str] = None,
    top_k: int = 5,
) -> RetrievalOutput:
    """Retrieve relevant startup context for agent analysis.

    This is the primary interface for agents to query stored startup knowledge.

    Args:
        query: Natural language query about startup.
        startup_id: Optional filter to specific startup. If None, searches all.
        top_k: Number of top results to return.

    Returns:
        RetrievalOutput with context and sources.

    Example:
        >>> result = retrieve_context("What is the business model?", startup_id="acme-123")
        >>> print(result.context)
        >>> print(result.sources)
    """
    logger.info(f"Retrieving context for query: {query}")

    if not query or not query.strip():
        logger.warning("Empty query provided to retrieve_context")
        return RetrievalOutput(context="", sources=[])

    try:
        # Search knowledge base
        search_results = search_knowledge(
            query=query,
            startup_id=startup_id,
            top_k=top_k,
        )

        if not search_results:
            logger.debug(f"No results found for query: {query}")
            return RetrievalOutput(context="", sources=[])

        # Aggregate context from top results
        context_parts = []
        sources = []

        for result in search_results:
            if result.get("content"):
                context_parts.append(result["content"])

            # Build source reference
            source_ref = f"{result.get('field', 'unknown')} (score: {result.get('score', 0):.2f})"
            sources.append(source_ref)

        context = "\n\n".join(context_parts)

        logger.debug(f"Retrieved {len(context_parts)} context pieces")

        return RetrievalOutput(
            context=context,
            sources=sources,
        )

    except Exception as e:
        logger.error(f"Failed to retrieve context: {e}")
        return RetrievalOutput(context="", sources=[])
