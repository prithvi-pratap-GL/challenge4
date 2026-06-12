"""In-memory and persistent storage of analyzed startups.

Supports comparing startups and learning from prior analyses.
"""

import json
import logging
from pathlib import Path
from typing import Optional

from backend.contracts import KnowledgeOutput

logger = logging.getLogger(__name__)

# In-memory store
_startup_memory = {}


def get_memory_dir() -> Path:
    """Get directory for memory files.

    Creates directory if it doesn't exist.

    Returns:
        Path to memory directory.
    """
    memory_dir = Path("./data/startup_memory")
    memory_dir.mkdir(parents=True, exist_ok=True)
    return memory_dir


def save_startup_memory(
    startup_id: str,
    knowledge: KnowledgeOutput,
) -> None:
    """Save analyzed startup knowledge to memory.

    Stores both in-memory and persistently to disk for future reference.

    Args:
        startup_id: Unique startup identifier.
        knowledge: KnowledgeOutput from analysis.
    """
    logger.info(f"Saving memory for startup {startup_id}")

    # Save to in-memory store
    _startup_memory[startup_id] = knowledge.model_dump()

    # Save to disk
    try:
        memory_dir = get_memory_dir()
        memory_file = memory_dir / f"{startup_id}.json"

        # Convert to JSON-serializable format
        knowledge_dict = knowledge.model_dump()

        with open(memory_file, "w") as f:
            json.dump(knowledge_dict, f, indent=2)

        logger.debug(f"Saved startup memory to {memory_file}")

    except Exception as e:
        logger.error(f"Failed to save startup memory to disk: {e}")


def get_startup_memory(
    startup_id: str,
) -> Optional[KnowledgeOutput]:
    """Retrieve previously analyzed startup knowledge.

    Attempts to load from in-memory store first, then from disk.

    Args:
        startup_id: Unique startup identifier.

    Returns:
        KnowledgeOutput if found, None otherwise.
    """
    logger.info(f"Retrieving memory for startup {startup_id}")

    # Try in-memory store first
    if startup_id in _startup_memory:
        logger.debug(f"Found {startup_id} in memory")
        knowledge_dict = _startup_memory[startup_id]
        return KnowledgeOutput(**knowledge_dict)

    # Try disk storage
    try:
        memory_dir = get_memory_dir()
        memory_file = memory_dir / f"{startup_id}.json"

        if memory_file.exists():
            with open(memory_file, "r") as f:
                knowledge_dict = json.load(f)

            # Cache in memory
            _startup_memory[startup_id] = knowledge_dict

            logger.debug(f"Loaded {startup_id} from disk")
            return KnowledgeOutput(**knowledge_dict)

    except Exception as e:
        logger.error(f"Failed to load startup memory from disk: {e}")

    logger.debug(f"No memory found for {startup_id}")
    return None


def compare_startups(
    startup_id_1: str,
    startup_id_2: str,
) -> Optional[dict]:
    """Compare two previously analyzed startups.

    Useful for competitive analysis and pattern finding.

    Args:
        startup_id_1: First startup identifier.
        startup_id_2: Second startup identifier.

    Returns:
        Dictionary with comparison results, or None if either startup not found.
    """
    logger.info(f"Comparing startups {startup_id_1} and {startup_id_2}")

    knowledge_1 = get_startup_memory(startup_id_1)
    knowledge_2 = get_startup_memory(startup_id_2)

    if not knowledge_1 or not knowledge_2:
        logger.warning(
            f"Cannot compare: one or both startups not in memory"
        )
        return None

    # Build comparison
    comparison = {
        "startup_1": {
            "id": startup_id_1,
            "summary": knowledge_1.startup_summary,
            "business_model": knowledge_1.business_model,
            "risks": knowledge_1.risks,
            "financials": knowledge_1.financials,
        },
        "startup_2": {
            "id": startup_id_2,
            "summary": knowledge_2.startup_summary,
            "business_model": knowledge_2.business_model,
            "risks": knowledge_2.risks,
            "financials": knowledge_2.financials,
        },
        "common_risks": list(
            set(knowledge_1.risks) & set(knowledge_2.risks)
        ),
        "common_market_claims": list(
            set(knowledge_1.market_claims) & set(knowledge_2.market_claims)
        ),
    }

    logger.debug(f"Comparison complete")
    return comparison


def list_all_startups() -> list[str]:
    """List all startups in memory.

    Returns:
        List of startup IDs.
    """
    try:
        memory_dir = get_memory_dir()

        startup_ids = []

        # Load from disk
        for memory_file in memory_dir.glob("*.json"):
            startup_id = memory_file.stem
            startup_ids.append(startup_id)

        logger.debug(f"Found {len(startup_ids)} startups in memory")
        return startup_ids

    except Exception as e:
        logger.error(f"Failed to list startups: {e}")
        return []
