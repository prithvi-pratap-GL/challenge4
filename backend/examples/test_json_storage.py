"""
Test script for JSON Storage functionality
Tests saving and loading research data to/from JSON files
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.contracts.research import ResearchOutput, Founder, Competitor
from backend.services.storage.json_storage import JSONStorageService


def test_json_storage():
    """Test JSON storage functionality"""
    print("\n[TEST] JSON Storage Test")
    print("=" * 60)

    # Initialize storage
    storage = JSONStorageService()

    # Create sample research data
    print("\n[STEP 1] Creating sample research data...")
    founders = [
        Founder(
            name="Patrick Collison",
            background="Ivy League / Top University graduate",
            experience="Founder and startup experience",
            credibility_score=85,
            sources=["https://crunchbase.com/person/patrick-collison"]
        ),
        Founder(
            name="John Collison",
            background="Technical background in software/engineering",
            experience="Senior executive experience in technology companies",
            credibility_score=80,
            sources=["https://linkedin.com/in/johncollison"]
        )
    ]

    competitors = [
        Competitor(
            name="Square",
            market_position="Market leader with significant share",
            funding="Public company",
            key_differentiators="Mobile-first or platform-based approach",
            sources=["https://square.com/about"]
        ),
        Competitor(
            name="PayPal",
            market_position="Established player with strong market presence",
            funding="Public company",
            key_differentiators="Unique value proposition and market approach",
            sources=["https://paypal.com/about"]
        )
    ]

    research_output = ResearchOutput(
        founders=founders,
        competitors=competitors,
        market_summary="Stripe operates in the payment processing market with strong growth",
        funding_summary="Series A-E funding rounds with institutional investors",
        industry_summary="FinTech industry experiencing rapid digital transformation",
        sources=[
            "https://stripe.com",
            "https://crunchbase.com/organization/stripe",
            "https://techcrunch.com/stripe"
        ]
    )

    print("[OK] Sample data created")
    print(f"  - {len(founders)} founders")
    print(f"  - {len(competitors)} competitors")
    print(f"  - {len(research_output.sources)} sources")

    # Test save
    print("\n[STEP 2] Saving research to JSON...")
    try:
        filepath = storage.save_research("Stripe", research_output)
        print(f"[OK] Saved to: {filepath}")
    except Exception as e:
        print(f"[FAIL] Failed to save: {e}")
        return False

    # Test load
    print("\n[STEP 3] Loading research from JSON...")
    try:
        loaded_data = storage.load_research(filepath)
        print(f"[OK] Loaded successfully")
        print(f"  - Startup: {loaded_data['startup_name']}")
        print(f"  - Timestamp: {loaded_data['timestamp']}")
        print(f"  - Founders: {len(loaded_data['research_data']['founders'])}")
        print(f"  - Competitors: {len(loaded_data['research_data']['competitors'])}")
    except Exception as e:
        print(f"[FAIL] Failed to load: {e}")
        return False

    # Test get latest
    print("\n[STEP 4] Getting latest research...")
    try:
        latest = storage.get_latest_research("Stripe")
        if latest:
            print(f"[OK] Got latest research")
            print(f"  - Timestamp: {latest['timestamp']}")
        else:
            print("[FAIL] No research found")
            return False
    except Exception as e:
        print(f"[FAIL] Failed to get latest: {e}")
        return False

    # Test list all
    print("\n[STEP 5] Listing all research files...")
    try:
        all_files = storage.list_all_research()
        print(f"[OK] Found {len(all_files)} research files")
        for file in all_files[:3]:
            print(f"  - {file.name}")
        if len(all_files) > 3:
            print(f"  ... and {len(all_files) - 3} more")
    except Exception as e:
        print(f"[FAIL] Failed to list: {e}")
        return False

    # Verify JSON structure
    print("\n[STEP 6] Verifying JSON structure...")
    try:
        import json
        with open(filepath, 'r') as f:
            json_data = json.load(f)

        assert "startup_name" in json_data
        assert "timestamp" in json_data
        assert "research_data" in json_data

        research_data = json_data["research_data"]
        assert "founders" in research_data
        assert "competitors" in research_data
        assert "market_summary" in research_data
        assert "funding_summary" in research_data
        assert "industry_summary" in research_data
        assert "sources" in research_data

        print("[OK] JSON structure is valid")
        print(f"  - Keys: {list(json_data.keys())}")
    except Exception as e:
        print(f"[FAIL] JSON structure invalid: {e}")
        return False

    # Test data integrity
    print("\n[STEP 7] Verifying data integrity...")
    try:
        assert loaded_data["startup_name"] == "Stripe"
        assert len(loaded_data["research_data"]["founders"]) == 2
        assert len(loaded_data["research_data"]["competitors"]) == 2
        assert loaded_data["research_data"]["founders"][0]["name"] == "Patrick Collison"
        assert loaded_data["research_data"]["competitors"][0]["name"] == "Square"

        print("[OK] All data integrity checks passed")
    except AssertionError as e:
        print(f"[FAIL] Data integrity check failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("[SUCCESS] ALL TESTS PASSED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_json_storage()
    sys.exit(0 if success else 1)
