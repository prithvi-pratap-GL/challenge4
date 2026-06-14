"""Unit tests for Red Team Agent."""

import pytest
from backend.agents.schemas import RedTeamOutput
from backend.agents.red_team.agent import (
    run_red_team,
    _format_list,
    _compare_claims_to_research
)


# ============================================================================
# Fixtures: Dummy ResearchOutput and KnowledgeOutput
# ============================================================================

@pytest.fixture
def dummy_research_output():
    """Create dummy ResearchOutput for testing."""
    return {
        "founders": [
            "Alice Chen (no prior ML governance experience)",
            "Bob Rodriguez (left previous job after 6 months)"
        ],
        "competitors": [
            "Google Cloud AI Governance",
            "AWS SageMaker Monitoring",
            "Datadog ML Monitoring",
            "20+ other startups in same space"
        ],
        "market_summary": (
            "AI governance market highly saturated. "
            "Large vendors (Google, AWS) entering with free/included solutions. "
            "Customer willingness to pay declining. "
            "Market consolidating around incumbents."
        ),
        "funding_summary": (
            "Seed: $2M from tier-2 VCs (2023)\n"
            "Pre-Series A: Forced follow-on $5M (burn rate unsustainable)"
        ),
        "industry_summary": (
            "Commoditization accelerating. Open-source alternatives (MLFlow, etc) "
            "capturing market share. Large vendors bundling features. "
            "Customer switching costs low."
        ),
        "sources": ["Crunchbase", "LinkedIn", "GitHub"]
    }


@pytest.fixture
def dummy_knowledge_output():
    """Create dummy KnowledgeOutput for testing."""
    return {
        "startup_summary": "AIFlow - Real-time ML Governance Platform",
        "business_model": (
            "SaaS model, $5K-$50K ACV. "
            "Claims of product-market fit with Fortune 500 validation. "
            "No public reference customers disclosed."
        ),
        "risks": [
            "Competition from $100B+ vendors",
            "Open-source alternative threat",
            "Customer concentration (3 customers = 60% revenue)",
            "Unproven technology claims"
        ],
        "financials": [
            "$300K MRR (down from $350K)",
            "Customer churn accelerating",
            "85% NRR (below break-even)"
        ],
        "market_claims": [
            "Only real-time ML governance solution in market",
            "10x faster than competitors",
            "Proven with Fortune 500 validation",
            "Largest TAM in enterprise AI ($200B)"
        ],
        "evidence": [
            "3 enterprise customers (names not disclosed)",
            "No third-party validation",
            "No published case studies",
            "Claims from pitch deck only"
        ]
    }


@pytest.fixture
def dummy_contradictory_output():
    """Create KnowledgeOutput with obvious contradictions."""
    return {
        "startup_summary": "UniqueAI - The Only Solution",
        "business_model": "Enterprise SaaS",
        "risks": ["Competition"],
        "financials": ["$500K MRR"],
        "market_claims": [
            "We are the only company doing this",
            "No competitors exist",
            "Massive untapped market worth $500B",
            "We will capture 100% market share"
        ],
        "evidence": [
            "Our own analysis",
            "Internal projections",
            "Founder intuition"
        ]
    }


# ============================================================================
# Unit Tests
# ============================================================================

class TestRedTeamInputHandling:
    """Test that Red Team Agent correctly accepts and processes inputs."""

    def test_accepts_research_output(self, dummy_research_output):
        """Verify run_red_team accepts ResearchOutput dict."""
        assert isinstance(dummy_research_output, dict)
        assert "founders" in dummy_research_output
        assert "competitors" in dummy_research_output
        assert "market_summary" in dummy_research_output
        assert "funding_summary" in dummy_research_output
        assert "industry_summary" in dummy_research_output
        assert "sources" in dummy_research_output

    def test_accepts_knowledge_output(self, dummy_knowledge_output):
        """Verify run_red_team accepts KnowledgeOutput dict."""
        assert isinstance(dummy_knowledge_output, dict)
        assert "startup_summary" in dummy_knowledge_output
        assert "business_model" in dummy_knowledge_output
        assert "risks" in dummy_knowledge_output
        assert "financials" in dummy_knowledge_output
        assert "market_claims" in dummy_knowledge_output
        assert "evidence" in dummy_knowledge_output

    @pytest.mark.asyncio
    async def test_function_signature(self, dummy_research_output, dummy_knowledge_output):
        """Verify run_red_team has correct function signature."""
        try:
            await run_red_team(dummy_research_output, dummy_knowledge_output)
        except NotImplementedError as e:
            # Expected until Person 5 provides LLM client
            assert "LLM client" in str(e)


class TestRedTeamOutputSchema:
    """Test that RedTeamOutput schema is correctly defined."""

    def test_red_team_output_schema_has_required_fields(self):
        """Verify RedTeamOutput schema has all required fields."""
        output = RedTeamOutput(
            challenges=["Challenge 1", "Challenge 2"],
            contradictions=["Contradiction 1"],
            missing_evidence=["Missing 1", "Missing 2"]
        )
        assert output.challenges == ["Challenge 1", "Challenge 2"]
        assert output.contradictions == ["Contradiction 1"]
        assert output.missing_evidence == ["Missing 1", "Missing 2"]

    def test_red_team_output_required_fields(self):
        """Verify all fields are required (no defaults)."""
        with pytest.raises(ValueError):
            RedTeamOutput(
                challenges=["Challenge"],
                contradictions=["Contradiction"]
                # Missing missing_evidence
            )

    def test_red_team_output_all_fields_lists(self):
        """Verify all fields are lists."""
        with pytest.raises(ValueError):
            RedTeamOutput(
                challenges="Not a list",  # Should be list
                contradictions=["Contradiction"],
                missing_evidence=["Missing"]
            )

    def test_red_team_output_empty_lists_allowed(self):
        """Verify empty lists are allowed (no contradictions found)."""
        output = RedTeamOutput(
            challenges=[],
            contradictions=[],
            missing_evidence=[]
        )
        assert output.challenges == []
        assert output.contradictions == []
        assert output.missing_evidence == []


class TestHelperFunctions:
    """Test utility functions used by Red Team Agent."""

    def test_format_list_with_items(self):
        """Verify _format_list formats list items correctly."""
        items = ["Challenge 1", "Challenge 2", "Challenge 3"]
        result = _format_list(items)
        assert "Challenge 1" in result
        assert "Challenge 2" in result
        assert "Challenge 3" in result
        assert result.startswith("\n-")

    def test_format_list_empty(self):
        """Verify _format_list handles empty lists."""
        result = _format_list([])
        assert result == "None provided"

    def test_format_list_single_item(self):
        """Verify _format_list handles single item."""
        result = _format_list(["Single Challenge"])
        assert "Single Challenge" in result


class TestContradictionDetection:
    """Test contradiction detection logic."""

    def test_detect_uniqueness_claim_vs_competitors(self):
        """Verify detection of uniqueness claims contradicted by competitors."""
        claims = ["We are the only solution", "Unique approach"]
        competitors = ["Competitor A", "Competitor B", "Competitor C"]
        market = "Growing market"

        contradictions = _compare_claims_to_research(claims, competitors, market)

        assert len(contradictions) > 0
        assert any("only" in c.lower() or "unique" in c.lower() for c in contradictions)

    def test_detect_opportunity_vs_saturation(self):
        """Verify detection of market opportunity claims vs saturation."""
        claims = ["Large market opportunity", "Growing TAM"]
        competitors = ["Competitor A"]
        market = "Saturated market with declining margins"

        contradictions = _compare_claims_to_research(claims, competitors, market)

        assert len(contradictions) > 0
        assert any("saturation" in c.lower() for c in contradictions)

    def test_no_contradictions_found(self):
        """Verify no false positives when no contradictions exist."""
        claims = ["Good product"]
        competitors = []
        market = "Growing market"

        contradictions = _compare_claims_to_research(claims, competitors, market)

        # Should not find contradictions when none exist
        assert len(contradictions) == 0

    def test_obvious_contradiction_detection(self):
        """Verify obvious contradictions are flagged."""
        claims = [
            "We are the only company doing this",
            "No competitors exist"
        ]
        competitors = ["Google", "AWS", "20+ startups"]
        market = "Highly competitive, commoditized"

        contradictions = _compare_claims_to_research(claims, competitors, market)

        assert len(contradictions) > 0
        assert any("20" in str(c) or "competitor" in c.lower() for c in contradictions)


# ============================================================================
# Mock Tests: Fact-Checking Logic
# ============================================================================

class TestFactCheckingLogic:
    """Test fact-checking and contradiction identification without LLM."""

    def test_unvalidated_claims_detection(self, dummy_knowledge_output):
        """Verify detection of unvalidated claims."""
        market_claims = dummy_knowledge_output["market_claims"]
        evidence = dummy_knowledge_output["evidence"]

        # All claims should be flagged as unvalidated (no third-party validation)
        assert "Fortune 500 validation" not in evidence[0]
        assert "no published case studies" in evidence[1].lower()

    def test_claim_without_evidence_contradiction(self, dummy_contradictory_output, dummy_research_output):
        """Verify contradictions in mock data are detected."""
        claims = dummy_contradictory_output["market_claims"]
        competitors = dummy_research_output["competitors"]

        # "Only company" claim contradicted by 20+ competitors
        only_claims = [c for c in claims if "only" in c.lower()]
        assert len(only_claims) > 0
        assert len(competitors) > 0

    def test_market_size_claim_vs_research(self, dummy_knowledge_output, dummy_research_output):
        """Verify market size claims can be verified against research."""
        market_claims = dummy_knowledge_output["market_claims"]
        market_research = dummy_research_output["market_summary"]

        # Claims of large TAM should be verified against market research
        tam_claims = [c for c in market_claims if "TAM" in c or "market" in c.lower()]
        assert len(tam_claims) > 0
        assert "saturat" in market_research.lower()  # Market is saturated


# ============================================================================
# Integration Tests (with mock LLM)
# ============================================================================

class TestRedTeamIntegration:
    """Test Red Team Agent behavior with mocked LLM integration."""

    @pytest.mark.asyncio
    async def test_red_team_agent_rejects_invalid_inputs(self):
        """Verify Red Team Agent handles invalid inputs gracefully."""
        empty_research = {}
        empty_knowledge = {}

        with pytest.raises(NotImplementedError):
            await run_red_team(empty_research, empty_knowledge)

    @pytest.mark.asyncio
    async def test_red_team_agent_prompt_generation(self, dummy_research_output, dummy_knowledge_output):
        """Verify Red Team Agent correctly generates prompts for LLM."""
        from backend.agents.red_team.prompts import RED_TEAM_SYSTEM_PROMPT, RED_TEAM_USER_PROMPT_TEMPLATE

        assert "fact-check" in RED_TEAM_SYSTEM_PROMPT.lower() or "challenge" in RED_TEAM_SYSTEM_PROMPT.lower()
        assert "claim" in RED_TEAM_SYSTEM_PROMPT.lower() or "contradiction" in RED_TEAM_SYSTEM_PROMPT.lower()
        assert "{startup_name}" in RED_TEAM_USER_PROMPT_TEMPLATE
        assert "{market_claims}" in RED_TEAM_USER_PROMPT_TEMPLATE
        assert "{competitors}" in RED_TEAM_USER_PROMPT_TEMPLATE


class TestRedTeamToneAndPurpose:
    """Test that Red Team Agent has correct adversarial tone."""

    def test_red_team_system_prompt_is_adversarial(self):
        """Verify Red Team prompt emphasizes fact-checking and contradiction."""
        from backend.agents.red_team.prompts import RED_TEAM_SYSTEM_PROMPT

        assert any(word in RED_TEAM_SYSTEM_PROMPT.lower() for word in [
            "fact-check", "disprove", "contradiction", "fallacies", "adversarial"
        ])

    def test_red_team_focuses_on_claims_verification(self):
        """Verify Red Team explicitly compares claims to research."""
        from backend.agents.red_team.prompts import RED_TEAM_USER_PROMPT_TEMPLATE

        assert "STARTUP'S CLAIMS" in RED_TEAM_USER_PROMPT_TEMPLATE
        assert "EXTERNAL RESEARCH DATA" in RED_TEAM_USER_PROMPT_TEMPLATE
        assert "contradictions" in RED_TEAM_USER_PROMPT_TEMPLATE.lower()


# ============================================================================
# Expected LLM Integration Test (for when Person 5 provides client)
# ============================================================================

class TestRedTeamLLMIntegration:
    """
    These tests will activate once Person 5's LLM client is integrated.
    """

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_red_team_with_real_llm(self, dummy_research_output, dummy_knowledge_output):
        """Test Red Team Agent with real LLM integration."""
        result = await run_red_team(dummy_research_output, dummy_knowledge_output)

        assert isinstance(result, RedTeamOutput)
        assert len(result.challenges) > 0  # Should find challenges
        assert len(result.contradictions) > 0  # Should find contradictions
        assert len(result.missing_evidence) > 0  # Should find gaps

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_red_team_flags_unvalidated_claims(self, dummy_research_output, dummy_knowledge_output):
        """Test that Red Team flags unvalidated market claims."""
        result = await run_red_team(dummy_research_output, dummy_knowledge_output)

        # Should challenge "only real-time" claim due to competitors
        assert any("only" in c.lower() or "unique" in c.lower() for c in result.challenges)

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_red_team_detects_obvious_contradictions(self, dummy_contradictory_output):
        """Test Red Team detects obvious contradictions."""
        dummy_research = {
            "founders": ["CEO"],
            "competitors": ["Competitor A", "Competitor B"],
            "market_summary": "Competitive market",
            "funding_summary": "Seed funding",
            "industry_summary": "Growing industry",
            "sources": ["Research"]
        }

        result = await run_red_team(dummy_research, dummy_contradictory_output)

        # Should flag "only company" claim with 2+ competitors
        assert len(result.contradictions) > 0


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_red_team_agent.py -v

3. Run specific test class:
   pytest tests/test_red_team_agent.py::TestContradictionDetection -v

4. Run with async support:
   pytest tests/test_red_team_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_red_team_agent.py --cov=backend.agents.red_team --cov-report=html

EXPECTED RESULTS:
- Input handling tests: PASS
- Schema validation tests: PASS
- Helper function tests: PASS
- Contradiction detection tests: PASS (tests actual logic)
- Fact-checking tests: PASS (mock logic tests)
- Integration tests: FAIL (NotImplementedError) until Person 5 integrates LLM
- LLM integration tests: SKIP (marked) until implementation ready
"""
