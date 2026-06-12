"""Complete ingestion pipeline - wires all components together."""

import asyncio
import logging
from typing import Optional

from backend.contracts import StartupInput, KnowledgeOutput
from backend.ingestion.pdf.pipeline import ingest_pitch_deck
from backend.ingestion.website.pipeline import ingest_website
from backend.knowledge.qdrant.service import store_knowledge
from backend.knowledge.memory.service import save_startup_memory

logger = logging.getLogger(__name__)


async def ingest_startup(
    startup_input: StartupInput,
    startup_id: str,
) -> KnowledgeOutput:
    """Complete startup ingestion pipeline.

    Ingests startup data from all available sources and produces unified KnowledgeOutput.

    Orchestrates:
    1. Ingest pitch deck (if available)
    2. Ingest website (if available)
    3. Merge results
    4. Store in Qdrant
    5. Save to memory

    Args:
        startup_input: StartupInput with URLs/paths to analyze.
        startup_id: Unique identifier for the startup.

    Returns:
        Unified KnowledgeOutput from all sources.

    Raises:
        ValueError: If neither pitch deck nor website provided.
    """
    logger.info(f"Starting ingestion pipeline for {startup_input.startup_name}")

    if not startup_input.pitch_deck_path and not startup_input.website_url:
        raise ValueError(
            "Must provide either pitch_deck_path or website_url"
        )

    knowledge_outputs = []

    # Ingest pitch deck
    if startup_input.pitch_deck_path:
        try:
            logger.info(f"Ingesting pitch deck: {startup_input.pitch_deck_path}")
            deck_knowledge = ingest_pitch_deck(
                pdf_path=startup_input.pitch_deck_path,
                startup_name=startup_input.startup_name,
            )
            knowledge_outputs.append(deck_knowledge)
            logger.debug("Pitch deck ingestion complete")

        except Exception as e:
            logger.error(f"Failed to ingest pitch deck: {e}")
            # Continue with website if deck fails

    # Ingest website
    if startup_input.website_url:
        try:
            logger.info(f"Ingesting website: {startup_input.website_url}")
            website_knowledge = ingest_website(
                url=startup_input.website_url,
                startup_name=startup_input.startup_name,
            )
            knowledge_outputs.append(website_knowledge)
            logger.debug("Website ingestion complete")

        except Exception as e:
            logger.error(f"Failed to ingest website: {e}")
            # Continue even if website fails

    if not knowledge_outputs:
        raise ValueError(
            "Failed to ingest from all sources"
        )

    # Merge results
    merged_knowledge = merge_knowledge_outputs(knowledge_outputs)

    # Store in vector database
    try:
        await store_knowledge(
            startup_id=startup_id,
            knowledge=merged_knowledge,
        )
        logger.debug("Stored knowledge in Qdrant")

    except Exception as e:
        logger.warning(f"Failed to store in Qdrant: {e}")
        # Continue even if storage fails

    # Save to memory
    try:
        save_startup_memory(
            startup_id=startup_id,
            knowledge=merged_knowledge,
        )
        logger.debug("Saved startup memory")

    except Exception as e:
        logger.warning(f"Failed to save startup memory: {e}")
        # Continue even if save fails

    logger.info(f"Ingestion pipeline complete for {startup_input.startup_name}")
    return merged_knowledge


def merge_knowledge_outputs(
    outputs: list[KnowledgeOutput],
) -> KnowledgeOutput:
    """Merge multiple KnowledgeOutput sources into unified output.

    Combines:
    - Summaries from all sources
    - Business models from all sources
    - Deduplicates risks, claims, financials, evidence

    Args:
        outputs: List of KnowledgeOutput from different sources.

    Returns:
        Merged KnowledgeOutput.
    """
    if not outputs:
        raise ValueError("No outputs to merge")

    if len(outputs) == 1:
        return outputs[0]

    logger.debug(f"Merging {len(outputs)} knowledge outputs")

    # Combine summaries
    summaries = [o.startup_summary for o in outputs if o.startup_summary]
    merged_summary = " ".join(summaries) or "Startup under analysis"

    # Combine business models
    business_models = [o.business_model for o in outputs if o.business_model]
    merged_business_model = " ".join(business_models) or "Business model details not clearly stated"

    # Combine and deduplicate other lists
    all_risks = []
    all_financials = []
    all_market_claims = []
    all_evidence = []

    for output in outputs:
        all_risks.extend(output.risks)
        all_financials.extend(output.financials)
        all_market_claims.extend(output.market_claims)
        all_evidence.extend(output.evidence)

    # Remove duplicates while preserving order
    merged_risks = list(dict.fromkeys(all_risks))
    merged_financials = list(dict.fromkeys(all_financials))
    merged_market_claims = list(dict.fromkeys(all_market_claims))
    merged_evidence = list(dict.fromkeys(all_evidence))

    # Combine context
    contexts = [o.retrieved_context for o in outputs if o.retrieved_context]
    merged_context = "\n\n".join(contexts) or "No context available"

    merged = KnowledgeOutput(
        startup_summary=merged_summary,
        business_model=merged_business_model,
        risks=merged_risks,
        financials=merged_financials,
        market_claims=merged_market_claims,
        evidence=merged_evidence,
        retrieved_context=merged_context,
    )

    logger.debug("Knowledge outputs merged")
    return merged


def ingest_startup_sync(
    startup_input: StartupInput,
    startup_id: str,
) -> KnowledgeOutput:
    """Synchronous wrapper for async ingestion pipeline.

    Args:
        startup_input: StartupInput with URLs/paths.
        startup_id: Unique startup identifier.

    Returns:
        KnowledgeOutput from ingestion.
    """
    return asyncio.run(ingest_startup(startup_input, startup_id))
