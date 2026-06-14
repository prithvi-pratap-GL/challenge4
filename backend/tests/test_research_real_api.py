"""
Test suite for Research Intelligence Module with REAL APIs
Phase 2: Integration Testing with Tavily API
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.contracts.startup import StartupInput
from backend.contracts.research import ResearchOutput, Founder, Competitor
from backend.agents.research.agent import run_research


def test_research_with_real_api():
    """Test research with real Tavily API"""
    print("\n" + "=" * 70)
    print("TEST 1: Research with Real Tavily API")
    print("=" * 70)

    startup_input = StartupInput(
        startup_name="OpenAI",
        website_url="https://openai.com",
        pitch_deck_path=None
    )

    print(f"\nResearching startup: {startup_input.startup_name}")
    print(f"Website: {startup_input.website_url}\n")

    try:
        research = run_research(startup_input)

        # Verify output structure
        assert isinstance(research, ResearchOutput), "Should return ResearchOutput"
        assert isinstance(research.founders, list), "founders should be list"
        assert isinstance(research.competitors, list), "competitors should be list"
        assert isinstance(research.market_summary, str), "market_summary should be string"
        assert isinstance(research.funding_summary, str), "funding_summary should be string"
        assert isinstance(research.industry_summary, str), "industry_summary should be string"
        assert isinstance(research.sources, list), "sources should be list"

        print("[OK] ResearchOutput structure is valid\n")

        # Display results
        print("RESULTS:")
        print("-" * 70)

        print(f"\nFounders ({len(research.founders)}):")
        for founder in research.founders:
            print(f"  • {founder.name}")
            print(f"    - Background: {founder.background[:60]}...")
            print(f"    - Credibility: {founder.credibility_score}/100")
            print(f"    - Sources: {len(founder.sources)}")

        print(f"\nCompetitors ({len(research.competitors)}):")
        for competitor in research.competitors:
            print(f"  • {competitor.name}")
            print(f"    - Position: {competitor.market_position[:60]}...")
            print(f"    - Funding: {competitor.funding[:40]}...")
            print(f"    - Differentiators: {competitor.key_differentiators[:50]}...")

        print(f"\nMarket Summary:")
        print(f"{research.market_summary[:300]}...\n")

        print(f"Funding Summary:")
        print(f"{research.funding_summary[:300]}...\n")

        print(f"Industry Summary:")
        print(f"{research.industry_summary[:300]}...\n")

        print(f"Total Sources Used: {len(research.sources)}")
        print("Sample sources:")
        for source in research.sources[:5]:
            print(f"  • {source}")

        print("\n" + "=" * 70)
        print("[PASS] Real API integration test successful!")
        print("=" * 70)
        return True

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_startups_real_api():
    """Test research on multiple startups"""
    print("\n" + "=" * 70)
    print("TEST 2: Research Multiple Startups with Real API")
    print("=" * 70)

    startups = [
        StartupInput("Stripe", "https://stripe.com"),
        StartupInput("Airbnb", "https://airbnb.com"),
        StartupInput("Notion", "https://notion.so"),
    ]

    results = {}

    for startup in startups:
        print(f"\n[{startup.startup_name}] Starting research...")
        try:
            research = run_research(startup)
            results[startup.startup_name] = {
                "status": "success",
                "founders": len(research.founders),
                "competitors": len(research.competitors),
                "sources": len(research.sources)
            }
            print(f"[{startup.startup_name}] SUCCESS: {len(research.founders)} founders, {len(research.competitors)} competitors, {len(research.sources)} sources")

        except Exception as e:
            results[startup.startup_name] = {
                "status": "failed",
                "error": str(e)
            }
            print(f"[{startup.startup_name}] FAILED: {e}")

    # Print summary
    print("\n" + "-" * 70)
    print("SUMMARY:")
    print("-" * 70)

    for startup_name, result in results.items():
        status = result["status"]
        if status == "success":
            print(f"✓ {startup_name}: {result['founders']} founders, {result['competitors']} competitors, {result['sources']} sources")
        else:
            print(f"✗ {startup_name}: {result['error']}")

    success_count = sum(1 for r in results.values() if r["status"] == "success")
    print(f"\nSuccess: {success_count}/{len(startups)}")

    print("=" * 70)
    return success_count > 0


def test_error_handling():
    """Test error handling with invalid startup"""
    print("\n" + "=" * 70)
    print("TEST 3: Error Handling")
    print("=" * 70)

    # Test with invalid/non-existent startup
    startup = StartupInput("XyzNonExistentCompany123", "https://nonexistent.test")

    print(f"\nTesting error handling with non-existent startup: {startup.startup_name}")

    try:
        research = run_research(startup)

        # Should still return a valid ResearchOutput
        assert isinstance(research, ResearchOutput), "Should return ResearchOutput even if no data found"

        print(f"[OK] Graceful degradation: {len(research.founders)} founders, {len(research.competitors)} competitors")
        print(f"[OK] Sources: {len(research.sources)}")

        print("\n[PASS] Error handling test passed")
        return True

    except Exception as e:
        print(f"[ERROR] Unexpected exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_performance():
    """Test API performance"""
    print("\n" + "=" * 70)
    print("TEST 4: API Performance")
    print("=" * 70)

    import time

    startup = StartupInput("Tesla", "https://tesla.com")

    print(f"\nMeasuring research time for {startup.startup_name}...")
    print("(This includes 5 agents making API calls)")

    start_time = time.time()

    try:
        research = run_research(startup)
        elapsed_time = time.time() - start_time

        print(f"\n[RESULT] Research completed in {elapsed_time:.2f} seconds")
        print(f"Data collected: {len(research.sources)} sources, {len(research.founders)} founders, {len(research.competitors)} competitors")

        if elapsed_time < 30:
            print(f"[PASS] Performance acceptable (< 30 seconds)")
            return True
        elif elapsed_time < 60:
            print(f"[WARN] Performance acceptable but could be optimized")
            return True
        else:
            print(f"[WARN] Performance slow, consider optimization")
            return True

    except Exception as e:
        print(f"[ERROR] Performance test failed: {e}")
        return False


def run_all_real_api_tests():
    """Run all real API tests"""
    print("\n" + "=" * 70)
    print("RESEARCH MODULE - REAL API INTEGRATION TESTS")
    print("Phase 2: Integration with Tavily API")
    print("=" * 70)

    results = {
        "Real API Integration": test_research_with_real_api(),
        "Multiple Startups": test_multiple_startups_real_api(),
        "Error Handling": test_error_handling(),
        "Performance": test_api_performance(),
    }

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 70)

    return passed == total


if __name__ == "__main__":
    print("\n[INFO] Starting Real API Integration Tests")
    print("[INFO] Make sure TAVILY_API_KEY is set in .env")
    print("[INFO] This will make real API calls to Tavily\n")

    success = run_all_real_api_tests()
    sys.exit(0 if success else 1)
