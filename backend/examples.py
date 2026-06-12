"""Example usage of the Knowledge Intelligence module.

Shows how P5 orchestrator and agents use the module.
"""

import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from backend.contracts import StartupInput
from backend.ingestion.pipeline import ingest_startup_sync
from backend.knowledge.retrieval.service import retrieve_context
from backend.knowledge.memory.service import get_startup_memory, list_all_startups

# ==============================================================================
# EXAMPLE 1: P5 Orchestrator - Complete Ingestion Pipeline
# ==============================================================================


def example_orchestrator_pitch_deck():
    """P5 calls ingest_pitch_deck to process a startup pitch deck."""
    logger.info("\n=== Example 1: Orchestrator Processing Pitch Deck ===\n")

    # Create input
    startup_input = StartupInput(
        startup_name="TechStartup Inc",
        website_url=None,
        pitch_deck_path="path/to/pitch_deck.pdf",
    )

    try:
        # P5 orchestrator calls the ingestion pipeline
        knowledge = ingest_startup_sync(
            startup_input=startup_input,
            startup_id="techstartup-inc-001",
        )

        # Print results
        print("=== Knowledge Output ===")
        print(f"Summary: {knowledge.startup_summary}")
        print(f"Business Model: {knowledge.business_model}")
        print(f"Risks: {knowledge.risks}")
        print(f"Market Claims: {knowledge.market_claims}")
        print(f"Financials: {knowledge.financials}")
        print(f"Evidence: {knowledge.evidence}")
        print(f"Context ({len(knowledge.retrieved_context)} chars): {knowledge.retrieved_context[:200]}...")

    except FileNotFoundError:
        print("Note: Example requires actual PDF file. This is for demonstration.")


def example_orchestrator_website():
    """P5 calls ingest_website to process a startup website."""
    logger.info("\n=== Example 2: Orchestrator Processing Website ===\n")

    startup_input = StartupInput(
        startup_name="WebStartup Inc",
        website_url="https://webstartup.example.com",
        pitch_deck_path=None,
    )

    try:
        knowledge = ingest_startup_sync(
            startup_input=startup_input,
            startup_id="webstartup-inc-001",
        )

        print("=== Knowledge Output ===")
        print(f"Summary: {knowledge.startup_summary}")
        print(f"Business Model: {knowledge.business_model}")
        print(f"Risks: {knowledge.risks}")
        print(f"Market Claims: {knowledge.market_claims}")

    except Exception as e:
        print(f"Note: Example requires live website and API key. Error: {e}")


def example_orchestrator_both():
    """P5 orchestrator processes both pitch deck and website."""
    logger.info("\n=== Example 3: Orchestrator Processing Both Sources ===\n")

    startup_input = StartupInput(
        startup_name="FullStack Startup",
        website_url="https://fullstack.example.com",
        pitch_deck_path="path/to/deck.pdf",
    )

    try:
        # Ingest both sources - they'll be merged
        knowledge = ingest_startup_sync(
            startup_input=startup_input,
            startup_id="fullstack-001",
        )

        print("=== Merged Knowledge ===")
        print(f"Summary: {knowledge.startup_summary}")
        print(f"Business Model: {knowledge.business_model}")
        print(f"Risks: {knowledge.risks}")

    except Exception as e:
        print(f"Note: Example requires both sources. Error: {e}")


# ==============================================================================
# EXAMPLE 4: Bull Agent - Query Knowledge Base
# ==============================================================================


def example_bull_agent_analysis():
    """Bull agent retrieves context to make bullish analysis."""
    logger.info("\n=== Example 4: Bull Agent Analysis ===\n")

    # Assume startup was previously ingested
    startup_id = "acme-corp-001"

    # Query 1: Business model opportunity
    print("Bull Agent Query 1: What is the business model?")
    result = retrieve_context(
        query="What is the business model and how does the company make money?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")
    print(f"Sources: {result.sources}\n")

    # Query 2: Market opportunity
    print("Bull Agent Query 2: What is the market opportunity?")
    result = retrieve_context(
        query="What is the total addressable market and growth potential?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")
    print(f"Sources: {result.sources}\n")

    # Query 3: Team/Founder strength
    print("Bull Agent Query 3: What about the founding team?")
    result = retrieve_context(
        query="Who are the founders and what is their background and experience?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")


# ==============================================================================
# EXAMPLE 5: Bear Agent - Risk Analysis
# ==============================================================================


def example_bear_agent_analysis():
    """Bear agent retrieves context to make bearish analysis."""
    logger.info("\n=== Example 5: Bear Agent Risk Analysis ===\n")

    startup_id = "acme-corp-001"

    # Query 1: Risks
    print("Bear Agent Query 1: What are the main risks?")
    result = retrieve_context(
        query="What are the key risks and challenges facing the company?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")
    print(f"Sources: {result.sources}\n")

    # Query 2: Competitive landscape
    print("Bear Agent Query 2: What about competitors?")
    result = retrieve_context(
        query="Who are the competitors and what is the competitive landscape?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")
    print(f"Sources: {result.sources}\n")

    # Query 3: Unit economics
    print("Bear Agent Query 3: What are the unit economics?")
    result = retrieve_context(
        query="What are the unit economics, CAC, LTV, and payback period?",
        startup_id=startup_id,
    )
    print(f"Retrieved: {result.context[:300]}...")


# ==============================================================================
# EXAMPLE 6: Retrieval Without Startup Filter
# ==============================================================================


def example_cross_startup_search():
    """Search across all startups in the knowledge base."""
    logger.info("\n=== Example 6: Cross-Startup Pattern Search ===\n")

    # Committee agent searches across all analyzed startups
    print("Committee Agent Query: Which startups mention AI/ML in their business model?")
    result = retrieve_context(
        query="AI machine learning artificial intelligence business model",
        startup_id=None,  # Search all startups
        top_k=10,
    )
    print(f"Retrieved context:\n{result.context}\n")
    print(f"Sources: {result.sources}")


# ==============================================================================
# EXAMPLE 7: Memory Operations
# ==============================================================================


def example_memory_operations():
    """Work with startup memory for comparison and pattern finding."""
    logger.info("\n=== Example 7: Memory Operations ===\n")

    startup_id_1 = "acme-corp-001"
    startup_id_2 = "competitor-startup-001"

    # Retrieve saved memory
    print(f"Retrieving memory for {startup_id_1}...")
    knowledge_1 = get_startup_memory(startup_id_1)
    if knowledge_1:
        print(f"Summary: {knowledge_1.startup_summary}")
    else:
        print(f"No memory found for {startup_id_1}")

    # List all analyzed startups
    print("\nAll analyzed startups in memory:")
    startups = list_all_startups()
    for startup_id in startups:
        print(f"  - {startup_id}")


# ==============================================================================
# EXAMPLE 8: Direct Module Usage (Lower Level)
# ==============================================================================


def example_direct_module_usage():
    """Direct usage of P3 module components (not typical P5 orchestration)."""
    logger.info("\n=== Example 8: Direct Module Usage ===\n")

    from backend.ingestion.pdf.pipeline import ingest_pitch_deck
    from backend.ingestion.website.pipeline import ingest_website
    from backend.knowledge.embeddings.service import embed_text
    from backend.knowledge.memory.service import save_startup_memory

    # Direct pitch deck ingestion
    print("Direct pitch deck ingestion:")
    try:
        knowledge = ingest_pitch_deck("path/to/deck.pdf", "MyStartup")
        print(f"Success: {knowledge.startup_summary[:100]}")
    except FileNotFoundError:
        print("Note: Requires actual PDF file")

    # Direct website ingestion
    print("\nDirect website ingestion:")
    try:
        knowledge = ingest_website("https://example.com", "MyStartup")
        print(f"Success: {knowledge.startup_summary[:100]}")
    except Exception as e:
        print(f"Note: Requires live website and API key. Error: {e}")

    # Direct embedding
    print("\nDirect embedding:")
    try:
        embedding = embed_text("This is a test text to embed")
        print(f"Generated embedding of size {len(embedding)}")
    except Exception as e:
        print(f"Note: Requires OpenAI API key. Error: {e}")


# ==============================================================================
# MAIN
# ==============================================================================


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                  VentureMind Knowledge Intelligence Examples                ║
║                                                                             ║
║  This demonstrates how the P3 Knowledge Intelligence module is used by:     ║
║  - P5 Orchestrator (ingestion)                                             ║
║  - Bull Agent (bullish analysis)                                           ║
║  - Bear Agent (bearish analysis)                                           ║
║  - Reviewer Agent                                                          ║
║  - Red Team Agent                                                          ║
║  - Committee Agent                                                         ║
║                                                                             ║
║  Requirements for full examples:                                           ║
║  - OPENAI_API_KEY environment variable set                                 ║
║  - QDRANT_URL and QDRANT_COLLECTION environment variables set             ║
║  - Access to example PDF files or live websites                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)

    print("\nNote: These examples are demonstrations. Full execution requires:")
    print("  1. Environment variables configured")
    print("  2. API keys set (OpenAI, Qdrant)")
    print("  3. Actual startup data (PDFs, websites)")
    print("  4. Qdrant vector database running")
    print("\nYou can adapt these examples for your use case.\n")

    # Uncomment examples to run (with proper setup):
    # example_orchestrator_pitch_deck()
    # example_orchestrator_website()
    # example_orchestrator_both()
    # example_bull_agent_analysis()
    # example_bear_agent_analysis()
    # example_cross_startup_search()
    # example_memory_operations()
    # example_direct_module_usage()

    print("Examples are ready to use. See source code for implementation details.")
