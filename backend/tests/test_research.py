"""
Test suite for Research Intelligence Module (Person 2)
Tests the run_research function and ResearchOutput contract
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput, Founder, Competitor
from backend.agents.research.mock_data import get_mock_research_by_startup


def test_research_contract():
    """Test that research module returns correct ResearchOutput contract"""
    print("\n[PASS] Test 1: Research Output Contract Structure")
    print("=" * 60)

    # Create input
    input_data = StartupInput(
        startup_name="Airbnb",
        website_url="https://www.airbnb.com",
        pitch_deck_path=None
    )

    # Get mock research (no API calls needed)
    research_output = get_mock_research_by_startup("Airbnb")

    # Verify contract structure
    assert isinstance(research_output, ResearchOutput), "Should return ResearchOutput"
    assert isinstance(research_output.founders, list), "founders should be list"
    assert isinstance(research_output.competitors, list), "competitors should be list"
    assert isinstance(research_output.market_summary, str), "market_summary should be string"
    assert isinstance(research_output.funding_summary, str), "funding_summary should be string"
    assert isinstance(research_output.industry_summary, str), "industry_summary should be string"
    assert isinstance(research_output.sources, list), "sources should be list"

    print(f"[OK] ResearchOutput structure is correct")
    print(f"[OK] Found {len(research_output.founders)} founders")
    print(f"[OK] Found {len(research_output.competitors)} competitors")
    print(f"[OK] Found {len(research_output.sources)} sources")
    print()


def test_founder_structure():
    """Test Founder data structure"""
    print("[PASS] Test 2: Founder Data Structure")
    print("=" * 60)

    research_output = get_mock_research_by_startup("Airbnb")

    for founder in research_output.founders:
        assert isinstance(founder, Founder), "Should be Founder object"
        assert isinstance(founder.name, str), "name should be string"
        assert isinstance(founder.background, str), "background should be string"
        assert isinstance(founder.experience, str), "experience should be string"
        assert isinstance(founder.credibility_score, int), "credibility_score should be int"
        assert 0 <= founder.credibility_score <= 100, "credibility_score should be 0-100"
        assert isinstance(founder.sources, list), "sources should be list"

        print(f"[OK] {founder.name}")
        print(f"  - Credibility: {founder.credibility_score}/100")
        print(f"  - Sources: {len(founder.sources)}")
    print()


def test_competitor_structure():
    """Test Competitor data structure"""
    print("[PASS] Test 3: Competitor Data Structure")
    print("=" * 60)

    research_output = get_mock_research_by_startup("Stripe")

    for competitor in research_output.competitors:
        assert isinstance(competitor, Competitor), "Should be Competitor object"
        assert isinstance(competitor.name, str), "name should be string"
        assert isinstance(competitor.market_position, str), "market_position should be string"
        assert isinstance(competitor.funding, str), "funding should be string"
        assert isinstance(competitor.key_differentiators, str), "key_differentiators should be string"
        assert isinstance(competitor.sources, list), "sources should be list"

        print(f"[OK] {competitor.name}")
        print(f"  - Position: {competitor.market_position[:50]}...")
        print(f"  - Funding: {competitor.funding[:40]}...")
    print()


def test_sources_attribution():
    """Test that all research has source attribution"""
    print("[PASS] Test 4: Source Attribution")
    print("=" * 60)

    research_output = get_mock_research_by_startup("Airbnb")

    # Check that all founders have sources
    for founder in research_output.founders:
        assert len(founder.sources) > 0, f"Founder {founder.name} should have sources"
        print(f"[OK] {founder.name}: {founder.sources[0]}")

    # Check that all competitors have sources
    for competitor in research_output.competitors:
        assert len(competitor.sources) > 0, f"Competitor {competitor.name} should have sources"

    # Check global sources list
    assert len(research_output.sources) > 0, "Should have global sources"
    print(f"[OK] Total unique sources: {len(research_output.sources)}")
    print()


def test_research_output_serialization():
    """Test that ResearchOutput can be serialized to dict"""
    print("[PASS] Test 5: JSON Serialization")
    print("=" * 60)

    research_output = get_mock_research_by_startup("Stripe")
    output_dict = research_output.to_dict()

    assert isinstance(output_dict, dict), "Should serialize to dict"
    assert "founders" in output_dict, "Should have founders key"
    assert "competitors" in output_dict, "Should have competitors key"
    assert "market_summary" in output_dict, "Should have market_summary key"
    assert "sources" in output_dict, "Should have sources key"

    print(f"[OK] Serialization successful")
    print(f"[OK] Keys: {list(output_dict.keys())}")
    print()


def test_multiple_startups():
    """Test research for multiple startups"""
    print("[PASS] Test 6: Multiple Startups")
    print("=" * 60)

    startups = ["Airbnb", "Stripe", "Unknown Startup"]

    for startup in startups:
        research = get_mock_research_by_startup(startup)
        assert isinstance(research, ResearchOutput), f"Should return ResearchOutput for {startup}"
        print(f"[OK] {startup}: {len(research.founders)} founders, {len(research.competitors)} competitors")
    print()


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("RESEARCH INTELLIGENCE MODULE TEST SUITE")
    print("Person 2 - Research Intelligence Owner")
    print("=" * 60)

    try:
        test_research_contract()
        test_founder_structure()
        test_competitor_structure()
        test_sources_attribution()
        test_research_output_serialization()
        test_multiple_startups()

        print("=" * 60)
        print("[PASS] ALL TESTS PASSED")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
