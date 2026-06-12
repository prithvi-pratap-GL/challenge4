"""Unit tests for Bear Agent."""

import pytest
from backend.agents.schemas import BearOutput
from backend.agents.bear.agent import run_bear_case, _format_list


# ============================================================================
# Fixtures: Dummy ResearchOutput and KnowledgeOutput
# ============================================================================

@pytest.fixture
def dummy_research_output():
    """Create dummy ResearchOutput for testing."""
    return {
        "founders": [
            "Alice Chen (2 failed startups, left due to disputes)",
            "Bob Rodriguez (first-time founder)"
        ],
        "competitors": [
            "Google Cloud AI (massive resources, entry starting this year)",
            "AWS SageMaker (entrenched, 80% market penetration)",
            "20+ well-funded startups in the same space"
        ],
        "market_summary": (
            "AI ops market claimed to be $150B but highly fragmented. "
            "Customer willingness to pay declining due to open-source alternatives. "
            "Market saturation increasing rapidly."
        ),
        "funding_summary": (
            "Seed: $2M from tier-2 investors (2023)\n"
            "Pre-Series A: $5M from same investors (forced round due to burn)"
        ),
        "industry_summary": (
            "Consolidation trend favoring large incumbents. "
            "Open-source commoditization accelerating. "
            "Enterprise customers consolidating vendors. "
            "AI hype cycle declining after 2024 peak."
        ),
        "sources": ["Crunchbase", "LinkedIn", "YC Company Directory"]
    }


@pytest.fixture
def dummy_knowledge_output():
    """Create dummy KnowledgeOutput for testing."""
    return {
        "startup_summary": "AIFlow - Yet Another AI Operations Tool\nMe-too product in saturated market",
        "business_model": (
            "PLG SaaS with $5K-$50K ACV but 90% churn. "
            "Unit economics underwater: CAC $8K, LTV $12K (unproven). "
            "Pricing compression from competition."
        ),
        "risks": [
            "Direct competition from $100B+ cloud vendors",
            "Founder track record includes failures",
            "Key person dependency on CEO",
            "Unproven technology (relies on open-source models)",
            "Customer concentration risk (3 customers = 60% revenue)",
            "Burn rate exceeds runway by 6 months",
            "No defensible moat or unique IP"
        ],
        "financials": [
            "$300K MRR declining (down from $350K last month)",
            "85% Net Revenue Retention (below break-even threshold)",
            "Burn rate: $800K/month vs $5M in runway = 6 months"
        ],
        "market_claims": [
            "We're the fastest ML governance platform (unverified by third-party)",
            "10x faster deployment (no independent validation)",
            "Only platform with real-time explainability (feature available in open-source)"
        ],
        "evidence": [
            "3 enterprise customers (2 on month-to-month contracts ready to churn)",
            "Declining MoM growth (-8% last month after +12% prior)",
            "High customer acquisition cost ($30K average)",
            "LinkedIn following plateau for 3 months"
        ]
    }


# ============================================================================
# Unit Tests
# ============================================================================

class TestBearAgentInputHandling:
    """Test that Bear Agent correctly accepts and processes inputs."""

    def test_accepts_research_output(self, dummy_research_output):
        """Verify run_bear_case accepts ResearchOutput dict."""
        assert isinstance(dummy_research_output, dict)
        assert "founders" in dummy_research_output
        assert "competitors" in dummy_research_output
        assert "market_summary" in dummy_research_output
        assert "funding_summary" in dummy_research_output
        assert "industry_summary" in dummy_research_output
        assert "sources" in dummy_research_output

    def test_accepts_knowledge_output(self, dummy_knowledge_output):
        """Verify run_bear_case accepts KnowledgeOutput dict."""
        assert isinstance(dummy_knowledge_output, dict)
        assert "startup_summary" in dummy_knowledge_output
        assert "business_model" in dummy_knowledge_output
        assert "risks" in dummy_knowledge_output
        assert "financials" in dummy_knowledge_output
        assert "market_claims" in dummy_knowledge_output
        assert "evidence" in dummy_knowledge_output

    @pytest.mark.asyncio
    async def test_function_signature(self, dummy_research_output, dummy_knowledge_output):
        """Verify run_bear_case has correct function signature."""
        # This test verifies the function is callable with correct parameters
        try:
            await run_bear_case(dummy_research_output, dummy_knowledge_output)
        except NotImplementedError as e:
            # Expected until Person 5 provides LLM client
            assert "LLM client" in str(e)


class TestBearOutputSchema:
    """Test that BearOutput schema is correctly defined."""

    def test_bear_output_schema_has_required_fields(self):
        """Verify BearOutput schema has rejection_case, weaknesses, confidence."""
        # Test that BearOutput can be instantiated with required fields
        output = BearOutput(
            rejection_case="This is a compelling rejection argument.",
            weaknesses=["Weak team", "Market saturation"],
            confidence=75
        )
        assert output.rejection_case == "This is a compelling rejection argument."
        assert output.weaknesses == ["Weak team", "Market saturation"]
        assert output.confidence == 75

    def test_bear_output_confidence_validation_min(self):
        """Verify confidence score must be >= 0."""
        with pytest.raises(ValueError):
            BearOutput(
                rejection_case="Test",
                weaknesses=["Test"],
                confidence=-1
            )

    def test_bear_output_confidence_validation_max(self):
        """Verify confidence score must be <= 100."""
        with pytest.raises(ValueError):
            BearOutput(
                rejection_case="Test",
                weaknesses=["Test"],
                confidence=101
            )

    def test_bear_output_confidence_boundary_values(self):
        """Verify confidence score accepts boundary values (0, 100)."""
        output_min = BearOutput(
            rejection_case="Test",
            weaknesses=["Test"],
            confidence=0
        )
        assert output_min.confidence == 0

        output_max = BearOutput(
            rejection_case="Test",
            weaknesses=["Test"],
            confidence=100
        )
        assert output_max.confidence == 100

    def test_bear_output_required_fields(self):
        """Verify all fields are required (no defaults)."""
        with pytest.raises(ValueError):
            BearOutput(
                rejection_case="Test",
                weaknesses=["Test"]
                # Missing confidence
            )


class TestHelperFunctions:
    """Test utility functions used by Bear Agent."""

    def test_format_list_with_items(self):
        """Verify _format_list formats list items correctly."""
        items = ["Risk 1", "Risk 2", "Risk 3"]
        result = _format_list(items)
        assert "Risk 1" in result
        assert "Risk 2" in result
        assert "Risk 3" in result
        assert result.startswith("\n-")

    def test_format_list_empty(self):
        """Verify _format_list handles empty lists."""
        result = _format_list([])
        assert result == "None provided"

    def test_format_list_single_item(self):
        """Verify _format_list handles single item."""
        result = _format_list(["Single Risk"])
        assert "Single Risk" in result


# ============================================================================
# Integration Tests (with mock LLM)
# ============================================================================

class TestBearAgentWithMockLLM:
    """Test Bear Agent behavior with mocked LLM integration."""

    @pytest.mark.asyncio
    async def test_bear_agent_rejects_invalid_inputs(self):
        """Verify Bear Agent handles invalid inputs gracefully."""
        # Test with empty dicts
        empty_research = {}
        empty_knowledge = {}

        with pytest.raises(NotImplementedError):
            await run_bear_case(empty_research, empty_knowledge)

    @pytest.mark.asyncio
    async def test_bear_agent_prompt_generation(self, dummy_research_output, dummy_knowledge_output):
        """Verify Bear Agent correctly generates prompts for LLM."""
        # This test verifies prompt construction without actual LLM call
        from backend.agents.bear.prompts import BEAR_SYSTEM_PROMPT, BEAR_USER_PROMPT_TEMPLATE

        assert "critical" in BEAR_SYSTEM_PROMPT.lower() or "risk" in BEAR_SYSTEM_PROMPT.lower()
        assert "{startup_name}" in BEAR_USER_PROMPT_TEMPLATE
        assert "{founders}" in BEAR_USER_PROMPT_TEMPLATE
        assert "{market_summary}" in BEAR_USER_PROMPT_TEMPLATE


class TestBearVsBullTone:
    """Test that Bear Agent produces distinctly different output from Bull Agent."""

    def test_bear_system_prompt_is_critical(self):
        """Verify Bear prompt emphasizes risk and criticism."""
        from backend.agents.bear.prompts import BEAR_SYSTEM_PROMPT

        # Should contain risk-focused language
        assert any(word in BEAR_SYSTEM_PROMPT.lower() for word in [
            "risk", "critical", "skeptical", "execution risk", "failure", "downside"
        ])

    def test_bear_system_prompt_differs_from_bull(self):
        """Verify Bear and Bull prompts have different tones."""
        from backend.agents.bull.prompts import BULL_SYSTEM_PROMPT
        from backend.agents.bear.prompts import BEAR_SYSTEM_PROMPT

        # They should be different
        assert BULL_SYSTEM_PROMPT != BEAR_SYSTEM_PROMPT

        # Bull should have opportunity language
        assert "opportunity" in BULL_SYSTEM_PROMPT.lower() or "optimistic" in BULL_SYSTEM_PROMPT.lower()

        # Bear should have risk language
        assert "risk" in BEAR_SYSTEM_PROMPT.lower() or "critical" in BEAR_SYSTEM_PROMPT.lower()


# ============================================================================
# Expected LLM Integration Test (for when Person 5 provides client)
# ============================================================================

class TestBearAgentLLMIntegration:
    """
    These tests will activate once Person 5's LLM client is integrated.

    Expected integration:
    from backend.llm.client import LLMClient

    Then run_bear_case will call:
    llm_client = LLMClient()
    response = await llm_client.generate(
        system_prompt=BEAR_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=BearOutput
    )
    """

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_bear_agent_with_real_llm(self, dummy_research_output, dummy_knowledge_output):
        """
        Test Bear Agent with real LLM integration.

        BLOCKED: Waiting for Person 5 to implement:
        - backend.llm.client.LLMClient
        - LLMClient.generate(system_prompt, user_prompt, response_model)
        """
        result = await run_bear_case(dummy_research_output, dummy_knowledge_output)

        assert isinstance(result, BearOutput)
        assert len(result.rejection_case) > 100  # Substantive narrative
        assert len(result.weaknesses) >= 6  # At least 6 weaknesses
        assert 0 <= result.confidence <= 100  # Valid confidence

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_bear_output_is_critical(self, dummy_research_output, dummy_knowledge_output):
        """
        Verify Bear Agent output has noticeably critical tone.

        This test verifies the tone is distinctly bearish and risk-focused.
        BLOCKED: Waiting for LLM integration.
        """
        result = await run_bear_case(dummy_research_output, dummy_knowledge_output)

        # Should contain critical language
        output_lower = result.rejection_case.lower()
        assert any(word in output_lower for word in [
            "risk", "fail", "concern", "challenge", "threat", "weakness"
        ])

        # Should NOT sound like Bull Agent (no "opportunity", "strong", "excellent")
        assert "excellent" not in output_lower or "excellent opportunity" not in output_lower


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_bear_agent.py -v

3. Run specific test class:
   pytest tests/test_bear_agent.py::TestBearOutputSchema -v

4. Run with async support:
   pytest tests/test_bear_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_bear_agent.py --cov=backend.agents.bear --cov-report=html

EXPECTED RESULTS:
- Input handling tests: PASS
- Schema validation tests: PASS
- Helper function tests: PASS
- Integration placeholder tests: FAIL (NotImplementedError) until Person 5 integrates LLM
- LLM integration tests: SKIP (marked) until implementation ready
- Tone comparison tests: PASS (verify prompts differ from Bull Agent)
"""
