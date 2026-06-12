"""Test module to verify P3 implementation without external dependencies.

This test validates:
1. All modules can be imported correctly
2. All contracts are properly defined
3. All public APIs exist and have correct signatures
4. No circular imports or missing dependencies
"""

import sys
import logging
from typing import get_type_hints

# Add repo root to path for imports
sys.path.insert(0, '.')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all modules can be imported."""
    logger.info("Testing imports...")

    try:
        from backend.contracts import StartupInput, KnowledgeOutput, RetrievalOutput
        logger.info("✓ Contracts imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import contracts: {e}")
        return False

    try:
        from backend.ingestion.pdf.renderer import render_pdf_pages
        logger.info("✓ PDF renderer imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import PDF renderer: {e}")
        return False

    try:
        from backend.ingestion.pdf.pipeline import ingest_pitch_deck
        logger.info("✓ PDF pipeline imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import PDF pipeline: {e}")
        return False

    try:
        from backend.ingestion.website.pipeline import ingest_website
        logger.info("✓ Website pipeline imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import website pipeline: {e}")
        return False

    try:
        from backend.ingestion.vision.analyzer import analyze_pitch_deck_images
        logger.info("✓ Vision analyzer imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import vision analyzer: {e}")
        return False

    try:
        from backend.knowledge.embeddings.service import embed_text
        logger.info("✓ Embeddings service imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import embeddings service: {e}")
        return False

    try:
        from backend.knowledge.qdrant.service import store_knowledge, search_knowledge
        logger.info("✓ Qdrant service imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import Qdrant service: {e}")
        return False

    try:
        from backend.knowledge.retrieval.service import retrieve_context
        logger.info("✓ Retrieval service imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import retrieval service: {e}")
        return False

    try:
        from backend.knowledge.memory.service import (
            save_startup_memory,
            get_startup_memory,
        )
        logger.info("✓ Memory service imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import memory service: {e}")
        return False

    return True


def test_contracts():
    """Test that contracts are properly defined."""
    logger.info("\nTesting contracts...")

    from backend.contracts import StartupInput, KnowledgeOutput, RetrievalOutput

    # Test StartupInput
    try:
        startup = StartupInput(
            startup_name="Test Startup",
            website_url="https://test.com",
            pitch_deck_path="/path/to/deck.pdf",
        )
        assert startup.startup_name == "Test Startup"
        assert startup.website_url == "https://test.com"
        logger.info("✓ StartupInput contract valid")
    except Exception as e:
        logger.error(f"✗ StartupInput contract failed: {e}")
        return False

    # Test KnowledgeOutput
    try:
        knowledge = KnowledgeOutput(
            startup_summary="A test startup",
            business_model="B2B SaaS",
            risks=["Market risk"],
            financials=["$1M ARR"],
            market_claims=["$10B TAM"],
            evidence=["Slide 5"],
            retrieved_context="Test context",
        )
        assert knowledge.startup_summary == "A test startup"
        assert len(knowledge.risks) == 1
        logger.info("✓ KnowledgeOutput contract valid")
    except Exception as e:
        logger.error(f"✗ KnowledgeOutput contract failed: {e}")
        return False

    # Test RetrievalOutput
    try:
        retrieval = RetrievalOutput(
            context="Retrieved context",
            sources=["source1", "source2"],
        )
        assert retrieval.context == "Retrieved context"
        assert len(retrieval.sources) == 2
        logger.info("✓ RetrievalOutput contract valid")
    except Exception as e:
        logger.error(f"✗ RetrievalOutput contract failed: {e}")
        return False

    return True


def test_public_apis():
    """Test that public APIs have correct signatures."""
    logger.info("\nTesting public APIs...")

    from backend.ingestion.pdf.pipeline import ingest_pitch_deck
    from backend.ingestion.website.pipeline import ingest_website
    from backend.knowledge.retrieval.service import retrieve_context
    from backend.knowledge.embeddings.service import embed_text
    from backend.contracts import KnowledgeOutput, RetrievalOutput

    # Check signatures
    import inspect

    # ingest_pitch_deck
    sig = inspect.signature(ingest_pitch_deck)
    params = list(sig.parameters.keys())
    assert "pdf_path" in params, "ingest_pitch_deck missing pdf_path parameter"
    logger.info("✓ ingest_pitch_deck signature valid")

    # ingest_website
    sig = inspect.signature(ingest_website)
    params = list(sig.parameters.keys())
    assert "url" in params, "ingest_website missing url parameter"
    logger.info("✓ ingest_website signature valid")

    # retrieve_context
    sig = inspect.signature(retrieve_context)
    params = list(sig.parameters.keys())
    assert "query" in params, "retrieve_context missing query parameter"
    logger.info("✓ retrieve_context signature valid")

    # embed_text
    sig = inspect.signature(embed_text)
    params = list(sig.parameters.keys())
    assert "text" in params, "embed_text missing text parameter"
    logger.info("✓ embed_text signature valid")

    return True


def test_folder_structure():
    """Test that folder structure is correct."""
    logger.info("\nTesting folder structure...")

    from pathlib import Path

    required_folders = [
        "backend/ingestion",
        "backend/ingestion/pdf",
        "backend/ingestion/website",
        "backend/ingestion/vision",
        "backend/knowledge",
        "backend/knowledge/embeddings",
        "backend/knowledge/qdrant",
        "backend/knowledge/retrieval",
        "backend/knowledge/memory",
        "backend/contracts",
    ]

    for folder in required_folders:
        folder_path = Path(folder)
        if folder_path.exists():
            logger.info(f"✓ {folder} exists")
        else:
            logger.error(f"✗ {folder} missing")
            return False

    required_files = [
        "backend/contracts/models.py",
        "backend/ingestion/pdf/renderer.py",
        "backend/ingestion/pdf/extractor.py",
        "backend/ingestion/pdf/pipeline.py",
        "backend/ingestion/website/extractor.py",
        "backend/ingestion/website/pipeline.py",
        "backend/ingestion/vision/analyzer.py",
        "backend/ingestion/vision/prompts.py",
        "backend/knowledge/embeddings/service.py",
        "backend/knowledge/qdrant/client.py",
        "backend/knowledge/qdrant/service.py",
        "backend/knowledge/retrieval/service.py",
        "backend/knowledge/memory/service.py",
    ]

    for file in required_files:
        file_path = Path(file)
        if file_path.exists():
            logger.info(f"✓ {file} exists")
        else:
            logger.error(f"✗ {file} missing")
            return False

    return True


def main():
    """Run all tests."""
    logger.info("""
╔════════════════════════════════════════════════════════════════════════════╗
║              P3 Knowledge Intelligence Module - Structure Test              ║
║                                                                             ║
║  This test validates module structure without requiring external APIs.      ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)

    results = {
        "Folder Structure": test_folder_structure(),
        "Imports": test_imports(),
        "Contracts": test_contracts(),
        "Public APIs": test_public_apis(),
    }

    logger.info("\n" + "=" * 80)
    logger.info("TEST RESULTS")
    logger.info("=" * 80)

    all_passed = True
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        logger.info(f"{symbol} {test_name}: {status}")
        if not result:
            all_passed = False

    logger.info("=" * 80)

    if all_passed:
        logger.info("\n✓ All tests passed!")
        logger.info("\nModule is ready for use. Next steps:")
        logger.info("1. Set up environment variables (.env)")
        logger.info("2. Configure OpenAI API key")
        logger.info("3. Set up Qdrant vector database")
        logger.info("4. Run examples: python backend/examples.py")
        return 0
    else:
        logger.error("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
