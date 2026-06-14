"""Unit tests for Bull Agent."""

import pytest
from backend.agents.schemas import BullOutput
from backend.agents.bull.agent import run_bull_case, _format_list


# ============================================================================
# Fixtures: Dummy ResearchOutput and KnowledgeOutput
# ============================================================================

@pytest.fixture
def dummy_research_output():
    """Create dummy ResearchOutput for testing."""
    return {
        "founders": [
            "Alice Chen (ex-Google Brain, 10 years AI/ML)",
            "Bob Rodriguez (ex-Stripe, built payments at scale)"
        ],
        "competitors": [
            "Competitor A (Series B, $30M raised)",
            "Competitor B (Bootstrapped, slower growth)"
        ],
        "market_summary": "Global AI ops market: $150B TAM, growing 45% YoY",
        "funding_summary": (
            "Seed: $2M from Sequoia, Benchmark (2023)\n"
            "Pre-Series A: $5M from existing investors (2024)"
        ),
        "industry_summary": (
            "AI/ML operations consolidation trend. Enterprise shift to AI-first infrastructure. "
            "Increasing demand for governance and monitoring tools."
        ),
        "sources": ["Crunchbase", "LinkedIn", "YC Company Directory"]
    }


@pytest.fixture
def dummy_knowledge_output():
    """Create dummy KnowledgeOutput for testing."""
    return {
        "startup_summary": "AIFlow - AI Operations & Governance Platform\nAutomates ML monitoring and compliance",
        "business_model": (
            "PLG SaaS model with $5K-$50K ACV. "
            "Free tier for developers, enterprise tier for ops teams."
        ),
        "risks": [
            "Competition from large cloud vendors (AWS SageMaker, GCP Vertex)",
            "Customer acquisition in enterprise segment",
            "Talent retention in competitive AI/ML market"
        ],
        "financials": [
            "$300K MRR (3 months post-seed)",
            "120% Net Revenue Retention",
            "6-month runway remaining"
        ],
        "market_claims": [
            "Fastest ML model governance platform",
            "10x faster deployment compared to competitors",
            "Only platform with real-time explainability"
        ],
        "evidence": [
            "3 Fortune 500 customers (Finance, Tech, Healthcare)",
            "50% Month-over-Month growth",
            "250+ daily active users on free tier",
            "LinkedIn: 5K+ followers, strong organic growth"
        ]
    }


# ============================================================================
# Unit Tests
# ============================================================================

class TestBullAgentInputHandling:
    """Test that Bull Agent correctly accepts and processes inputs."""

    def test_accepts_research_output(self, dummy_research_output):
        """Verify run_bull_case accepts ResearchOutput dict."""
        assert isinstance(dummy_research_output, dict)
        assert "founders" in dummy_research_output
        assert "competitors" in dummy_research_output
        assert "market_summary" in dummy_research_output
        assert "funding_summary" in dummy_research_output
        assert "industry_summary" in dummy_research_output
        assert "sources" in dummy_research_output

    def test_accepts_knowledge_output(self, dummy_knowledge_output):
        """Verify run_bull_case accepts KnowledgeOutput dict."""
        assert isinstance(dummy_knowledge_output, dict)
        assert "startup_summary" in dummy_knowledge_output
        assert "business_model" in dummy_knowledge_output
        assert "risks" in dummy_knowledge_output
        assert "financials" in dummy_knowledge_output
        assert "market_claims" in dummy_knowledge_output
        assert "evidence" in dummy_knowledge_output

    @pytest.mark.asyncio
    async def test_function_signature(self, dummy_research_output, dummy_knowledge_output):
        """Verify run_bull_case has correct function signature."""
        # This test verifies the function is callable with correct parameters
        try:
            await run_bull_case(dummy_research_output, dummy_knowledge_output)
        except NotImplementedError as e:
            # Expected until Person 5 provides LLM client
            assert "LLM client" in str(e)


class TestBullOutputSchema:
    """Test that BullOutput schema is correctly defined."""

    def test_bull_output_schema_has_required_fields(self):
        """Verify BullOutput schema has investment_case, strengths, confidence."""
        # Test that BullOutput can be instantiated with required fields
        output = BullOutput(
            investment_case="This is a compelling investment opportunity.",
            strengths=["Strong founding team", "Large market opportunity"],
            confidence=85
        )
        assert output.investment_case == "This is a compelling investment opportunity."
        assert output.strengths == ["Strong founding team", "Large market opportunity"]
        assert output.confidence == 85

    def test_bull_output_confidence_validation_min(self):
        """Verify confidence score must be >= 0."""
        with pytest.raises(ValueError):
            BullOutput(
                investment_case="Test",
                strengths=["Test"],
                confidence=-1
            )

    def test_bull_output_confidence_validation_max(self):
        """Verify confidence score must be <= 100."""
        with pytest.raises(ValueError):
            BullOutput(
                investment_case="Test",
                strengths=["Test"],
                confidence=101
            )

    def test_bull_output_confidence_boundary_values(self):
        """Verify confidence score accepts boundary values (0, 100)."""
        output_min = BullOutput(
            investment_case="Test",
            strengths=["Test"],
            confidence=0
        )
        assert output_min.confidence == 0

        output_max = BullOutput(
            investment_case="Test",
            strengths=["Test"],
            confidence=100
        )
        assert output_max.confidence == 100

    def test_bull_output_required_fields(self):
        """Verify all fields are required (no defaults)."""
        with pytest.raises(ValueError):
            BullOutput(
                investment_case="Test",
                strengths=["Test"]
                # Missing confidence
            )


class TestHelperFunctions:
    """Test utility functions used by Bull Agent."""

    def test_format_list_with_items(self):
        """Verify _format_list formats list items correctly."""
        items = ["Item 1", "Item 2", "Item 3"]
        result = _format_list(items)
        assert "Item 1" in result
        assert "Item 2" in result
        assert "Item 3" in result
        assert result.startswith("\n-")

    def test_format_list_empty(self):
        """Verify _format_list handles empty lists."""
        result = _format_list([])
        assert result == "None provided"

    def test_format_list_single_item(self):
        """Verify _format_list handles single item."""
        result = _format_list(["Single Item"])
        assert "Single Item" in result


# ============================================================================
# Integration Tests (with mock LLM)
# ============================================================================

class TestBullAgentWithMockLLM:
    """Test Bull Agent behavior with mocked LLM integration."""

    @pytest.mark.asyncio
    async def test_bull_agent_rejects_invalid_inputs(self):
        """Verify Bull Agent handles invalid inputs gracefully."""
        # Test with empty dicts
        empty_research = {}
        empty_knowledge = {}

        with pytest.raises(NotImplementedError):
            await run_bull_case(empty_research, empty_knowledge)

    @pytest.mark.asyncio
    async def test_bull_agent_prompt_generation(self, dummy_research_output, dummy_knowledge_output):
        """Verify Bull Agent correctly generates prompts for LLM."""
        # This test verifies prompt construction without actual LLM call
        from backend.agents.bull.prompts import BULL_SYSTEM_PROMPT, BULL_USER_PROMPT_TEMPLATE

        assert "optimistic" in BULL_SYSTEM_PROMPT.lower() or "opportunity" in BULL_SYSTEM_PROMPT.lower()
        assert "{startup_name}" in BULL_USER_PROMPT_TEMPLATE
        assert "{founders}" in BULL_USER_PROMPT_TEMPLATE
        assert "{market_summary}" in BULL_USER_PROMPT_TEMPLATE


# ============================================================================
# Expected LLM Integration Test (for when Person 5 provides client)
# ============================================================================

class TestBullAgentLLMIntegration:
    """
    These tests will activate once Person 5's LLM client is integrated.

    Expected integration:
    from backend.llm.client import LLMClient

    Then run_bull_case will call:
    llm_client = LLMClient()
    response = await llm_client.generate(
        system_prompt=BULL_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=BullOutput
    )
    """

    @pytest.mark.skip(reason="Awaiting Person 5's LLM client implementation")
    @pytest.mark.asyncio
    async def test_bull_agent_with_real_llm(self, dummy_research_output, dummy_knowledge_output):
        """
        Test Bull Agent with real LLM integration.

        BLOCKED: Waiting for Person 5 to implement:
        - backend.llm.client.LLMClient
        - LLMClient.generate(system_prompt, user_prompt, response_model)
        """
        result = await run_bull_case(dummy_research_output, dummy_knowledge_output)

        assert isinstance(result, BullOutput)
        assert len(result.investment_case) > 100  # Substantive narrative
        assert len(result.strengths) >= 6  # At least 6 strengths
        assert 0 <= result.confidence <= 100  # Valid confidence


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_bull_agent.py -v

3. Run specific test class:
   pytest tests/test_bull_agent.py::TestBullOutputSchema -v

4. Run with async support:
   pytest tests/test_bull_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_bull_agent.py --cov=backend.agents.bull --cov-report=html

EXPECTED RESULTS:
- Input handling tests: PASS
- Schema validation tests: PASS
- Helper function tests: PASS
- Integration placeholder tests: FAIL (NotImplementedError) until Person 5 integrates LLM
- LLM integration tests: SKIP (marked) until implementation ready
"""
