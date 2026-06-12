"""
Demo: Using Research Module with Real Tavily API
Person 2 - Research Intelligence Owner

This demonstrates how to use the research module with real APIs.
"""

import sys
import os
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.contracts.startup import StartupInput
from backend.agents.research.agent import run_research


def demo_single_startup():
    """Demo: Research a single startup with real API"""
    print("\n" + "=" * 80)
    print("DEMO 1: Single Startup Research with Real Tavily API")
    print("=" * 80)

    startup = StartupInput(
        startup_name="Stripe",
        website_url="https://stripe.com"
    )

    print(f"\nResearching: {startup.startup_name}")
    print(f"Website: {startup.website_url}")
    print("\nThis will make real Tavily API calls...")
    print("Processing: Founder → Competitors → Market → Funding → Industry")

    start_time = time.time()

    try:
        research = run_research(startup)
        elapsed = time.time() - start_time

        print(f"\nCompleted in {elapsed:.2f} seconds\n")

        # Display results
        print("RESULTS:")
        print("-" * 80)

        print(f"\nFOUNDERS ({len(research.founders)}):")
        for i, founder in enumerate(research.founders, 1):
            print(f"\n{i}. {founder.name}")
            print(f"   Background: {founder.background}")
            print(f"   Experience: {founder.experience}")
            print(f"   Credibility: {founder.credibility_score}/100")
            if founder.sources:
                print(f"   Source: {founder.sources[0]}")

        print(f"\n\nCOMPETITORS ({len(research.competitors)}):")
        for i, comp in enumerate(research.competitors, 1):
            print(f"\n{i}. {comp.name}")
            print(f"   Position: {comp.market_position}")
            print(f"   Funding: {comp.funding}")
            print(f"   Differentiators: {comp.key_differentiators}")
            if comp.sources:
                print(f"   Source: {comp.sources[0]}")

        print(f"\n\nMARKET ANALYSIS:")
        print(research.market_summary[:400] + "...\n")

        print(f"FUNDING HISTORY:")
        print(research.funding_summary[:400] + "...\n")

        print(f"INDUSTRY CONTEXT:")
        print(research.industry_summary[:400] + "...\n")

        print(f"SOURCES USED ({len(research.sources)}):")
        for url in research.sources[:10]:
            print(f"  • {url}")
        if len(research.sources) > 10:
            print(f"  ... and {len(research.sources) - 10} more")

        print("\n" + "=" * 80)
        return True

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False


def demo_multiple_startups():
    """Demo: Research multiple startups"""
    print("\n" + "=" * 80)
    print("DEMO 2: Research Multiple Startups")
    print("=" * 80)

    startups = [
        StartupInput("Notion", "https://notion.so"),
        StartupInput("Slack", "https://slack.com"),
        StartupInput("Figma", "https://figma.com"),
    ]

    print(f"\nResearching {len(startups)} startups:")
    for startup in startups:
        print(f"  • {startup.startup_name}")

    results = {}

    for i, startup in enumerate(startups, 1):
        print(f"\n[{i}/{len(startups)}] Researching {startup.startup_name}...")

        start_time = time.time()

        try:
            research = run_research(startup)
            elapsed = time.time() - start_time

            results[startup.startup_name] = {
                "success": True,
                "founders": len(research.founders),
                "competitors": len(research.competitors),
                "sources": len(research.sources),
                "time": elapsed
            }

            print(f"  ✓ Complete in {elapsed:.1f}s: {len(research.founders)} founders, {len(research.competitors)} competitors, {len(research.sources)} sources")

        except Exception as e:
            results[startup.startup_name] = {
                "success": False,
                "error": str(e)
            }
            print(f"  ✗ Failed: {e}")

    # Summary
    print("\n" + "-" * 80)
    print("SUMMARY:")
    print("-" * 80)

    successful = sum(1 for r in results.values() if r["success"])
    total_time = sum(r.get("time", 0) for r in results.values() if r["success"])

    for startup_name, result in results.items():
        if result["success"]:
            print(f"\n{startup_name}:")
            print(f"  Founders: {result['founders']}")
            print(f"  Competitors: {result['competitors']}")
            print(f"  Sources: {result['sources']}")
            print(f"  Time: {result['time']:.1f}s")
        else:
            print(f"\n{startup_name}: FAILED - {result['error']}")

    print(f"\n\nSuccess Rate: {successful}/{len(startups)}")
    print(f"Total Time: {total_time:.1f}s")
    if successful > 0:
        print(f"Average Time: {total_time / successful:.1f}s per startup")

    print("=" * 80)
    return successful > 0


def demo_json_export():
    """Demo: Export research to JSON"""
    print("\n" + "=" * 80)
    print("DEMO 3: Export Research to JSON")
    print("=" * 80)

    startup = StartupInput("Tesla", "https://tesla.com")

    print(f"\nResearching {startup.startup_name}...")

    try:
        research = run_research(startup)

        # Convert to dict
        research_dict = research.to_dict()

        # Pretty print
        json_str = json.dumps(research_dict, indent=2)

        print("\nJSON Output (first 600 chars):")
        print("-" * 80)
        print(json_str[:600] + "...")

        # Show structure
        print("\n\nJSON Structure:")
        print("-" * 80)
        print(f"Keys: {list(research_dict.keys())}")
        print(f"Founders: {len(research_dict['founders'])} items")
        print(f"Competitors: {len(research_dict['competitors'])} items")
        print(f"Sources: {len(research_dict['sources'])} items")

        # Save to file
        output_file = "research_output.json"
        with open(output_file, "w") as f:
            json.dump(research_dict, f, indent=2)

        print(f"\nSaved to: {output_file}")

        print("=" * 80)
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def demo_compare_startups():
    """Demo: Compare research from multiple startups"""
    print("\n" + "=" * 80)
    print("DEMO 4: Compare Startups (Side-by-Side)")
    print("=" * 80)

    startups = [
        StartupInput("OpenAI", "https://openai.com"),
        StartupInput("Anthropic", "https://anthropic.com"),
    ]

    print(f"\nComparing: {startups[0].startup_name} vs {startups[1].startup_name}")
    print("(This will show how research modules compare startups)\n")

    researches = {}

    for startup in startups:
        print(f"Researching {startup.startup_name}...")

        try:
            research = run_research(startup)
            researches[startup.startup_name] = research
            print(f"  ✓ Done\n")

        except Exception as e:
            print(f"  ✗ Failed: {e}\n")

    if len(researches) < 2:
        print("Could not complete comparison (not enough successful researches)")
        return False

    # Comparison table
    print("\n" + "-" * 80)
    print("COMPARISON:")
    print("-" * 80)

    print(f"{'Metric':<25} {startups[0].startup_name:<30} {startups[1].startup_name:<30}")
    print("-" * 80)

    max_founders = max(len(researches[s].founders) for s in researches)
    max_competitors = max(len(researches[s].competitors) for s in researches)
    max_sources = max(len(researches[s].sources) for s in researches)

    print(f"{'Founders Found':<25} {len(researches[startups[0].startup_name].founders):<30} {len(researches[startups[1].startup_name].founders):<30}")
    print(f"{'Competitors Found':<25} {len(researches[startups[0].startup_name].competitors):<30} {len(researches[startups[1].startup_name].competitors):<30}")
    print(f"{'Sources Used':<25} {len(researches[startups[0].startup_name].sources):<30} {len(researches[startups[1].startup_name].sources):<30}")

    # Founder comparison
    print("\n\nFOUNDER CREDIBILITY COMPARISON:")
    print("-" * 80)

    for startup_name, research in researches.items():
        print(f"\n{startup_name}:")
        for founder in research.founders[:3]:
            print(f"  • {founder.name}: {founder.credibility_score}/100")

    print("\n" + "=" * 80)
    return True


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  PERSON 2: RESEARCH INTELLIGENCE MODULE - REAL API DEMO".center(78) + "║")
    print("║" + "  Phase 2: Tavily API Integration".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    print("\nSelect a demo:")
    print("1. Single Startup Research")
    print("2. Multiple Startups Research")
    print("3. Export to JSON")
    print("4. Compare Startups")
    print("5. Run All Demos")

    # Auto-run demo 1 if no input (for automated testing)
    print("\nRunning Demo 1 (Single Startup)...\n")

    success = True
    success = demo_single_startup() and success

    # Optionally run more demos
    print("\n\nDone!")
    print("=" * 80)

    return success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(1)
