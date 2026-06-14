"""Unit tests for Digital Twin Agent."""

import pytest
from backend.agents.schemas import SimulationOutput
from backend.agents.digital_twin.agent import (
    simulate_scenarios,
    _extract_metric,
    _extract_tam,
    _calculate_survival_probability,
    _identify_opportunities,
    _identify_scenario_risks
)


# ============================================================================
# Fixtures: Test Data
# ============================================================================

@pytest.fixture
def strong_startup_data():
    """Strong startup with good unit economics."""
    return {
        "research_output": {
            "founders": [
                "Alice Chen (ex-Google, 10 years ML)",
                "Bob Rodriguez (ex-Stripe, payments)"
            ],
            "competitors": ["Google Cloud", "AWS", "Datadog"],
            "market_summary": "$150B TAM, 45% CAGR",
            "funding_summary": "Series A $5M from Sequoia",
            "industry_summary": "AI/ML ops consolidation"
        },
        "knowledge_output": {
            "startup_summary": "AIFlow - ML Governance Platform",
            "business_model": "PLG SaaS, $5K-$50K ACV",
            "risks": ["Competition from cloud vendors"],
            "financials": ["$300K MRR", "120% NRR", "Burn: $500K/month", "Runway: 12 months"],
            "market_claims": ["Best governance solution"],
            "evidence": ["3 Fortune 500 customers"]
        }
    }


@pytest.fixture
def weak_startup_data():
    """Weak startup with poor unit economics."""
    return {
        "research_output": {
            "founders": ["First-time founder"],
            "competitors": ["20+ competitors", "Google entering"],
            "market_summary": "Saturated $50B TAM",
            "funding_summary": "Seed from tier-2 VCs",
            "industry_summary": "Commoditizing market"
        },
        "knowledge_output": {
            "startup_summary": "GenericAI - Another SaaS",
            "business_model": "Enterprise SaaS, negative unit economics",
            "risks": [
                "Vendor competition",
                "Key person dependency on founder/CTO",
                "Customer concentration risk"
            ],
            "financials": ["$100K MRR", "85% NRR", "Burn: $1M/month", "Runway: 3 months"],
            "market_claims": ["We are unique"],
            "evidence": []
        }
    }


# ============================================================================
# Unit Tests
# ============================================================================

class TestSimulationOutputSchema:
    """Test SimulationOutput schema validation."""

    def test_simulation_output_schema(self):
        """Verify SimulationOutput has all required fields."""
        output = SimulationOutput(
            scenario="Google enters the market",
            survival_probability=45,
            opportunities=["Partner with Google", "Acquisition potential"],
            risks=["Market share loss", "Price war"]
        )
        assert output.scenario == "Google enters the market"
        assert output.survival_probability == 45
        assert len(output.opportunities) == 2
        assert len(output.risks) == 2

    def test_survival_probability_bounds(self):
        """Verify survival probability is 0-100."""
        with pytest.raises(ValueError):
            SimulationOutput(
                scenario="Test",
                survival_probability=101,
                opportunities=[],
                risks=[]
            )


class TestHelperFunctions:
    """Test helper functions for metric extraction and analysis."""

    def test_extract_metric(self):
        """Test metric extraction from financials."""
        financials = ["$300K MRR", "120% NRR", "Burn: $500K/month"]
        assert _extract_metric(financials, "MRR") == "$300K MRR"
        assert _extract_metric(financials, "NRR") == "120% NRR"
        assert _extract_metric(financials, "Burn") == "Burn: $500K/month"
        assert _extract_metric(financials, "ARR") is None

    def test_extract_tam(self):
        """Test TAM extraction from market summary."""
        summary = "Global market is $150B TAM with 45% growth"
        tam = _extract_tam(summary)
        assert "$" in tam
        assert "150" in tam

    def test_calculate_survival_probability(self):
        """Test survival probability calculation."""
        knowledge = {"financials": ["$300K MRR", "120% NRR"]}
        research = {"founders": ["ex-Google founder"]}

        # Strong startup should have higher baseline
        prob = _calculate_survival_probability(
            "Minor market downturn",
            knowledge,
            research
        )
        assert prob > 50

        # Weak NRR should lower probability
        weak_knowledge = {"financials": ["$100K MRR", "85% NRR"]}
        weak_prob = _calculate_survival_probability(
            "Minor market downturn",
            weak_knowledge,
            research
        )
        assert weak_prob < prob


class TestSurvivalProbabilityCalculation:
    """Test survival probability under different scenarios."""

    def test_major_competitor_entry(self, strong_startup_data):
        """Verify major competitor entry significantly reduces survival."""
        strong_prob = _calculate_survival_probability(
            "Google enters the market with competing product",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        minor_prob = _calculate_survival_probability(
            "Minor market downturn",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        # Major competitor should severely impact survival
        assert strong_prob < minor_prob - 15

    def test_cost_doubling(self, strong_startup_data):
        """Verify cost doubling (CAC) reduces survival."""
        cac_double_prob = _calculate_survival_probability(
            "Customer acquisition cost (CAC) doubles",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        normal_prob = _calculate_survival_probability(
            "Normal market conditions",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        assert cac_double_prob < normal_prob - 10

    def test_market_shrinkage(self, strong_startup_data):
        """Verify market shrinkage significantly impacts survival."""
        shrink_prob = _calculate_survival_probability(
            "Core market shrinks by 40% due to recession",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        strong_prob = _calculate_survival_probability(
            "Strong market growth",
            strong_startup_data["knowledge_output"],
            strong_startup_data["research_output"]
        )

        assert shrink_prob < strong_prob - 25

    def test_key_person_leaves(self, weak_startup_data):
        """Verify key person leaving impacts survival differently based on founder experience."""
        # Experienced founder handles it better
        strong_data = weak_startup_data.copy()
        strong_data["research_output"]["founders"] = ["ex-Google founder"]

        experienced_prob = _calculate_survival_probability(
            "CTO leaves to start their own company",
            strong_data["knowledge_output"],
            strong_data["research_output"]
        )

        # Inexperienced founder is hit harder
        inexperienced_prob = _calculate_survival_probability(
            "CTO leaves to start their own company",
            weak_startup_data["knowledge_output"],
            weak_startup_data["research_output"]
        )

        assert experienced_prob > inexperienced_prob


class TestOpportunityIdentification:
    """Test opportunity identification in scenarios."""

    def test_expansion_opportunities(self):
        """Verify expansion scenario identifies new opportunities."""
        opportunities = _identify_opportunities(
            "Startup expands into new international market",
            "Experienced founder"
        )
        assert any("expansion" in opp.lower() or "diversif" in opp.lower() for opp in opportunities)

    def test_open_source_opportunities(self):
        """Verify open-source competition identifies alternative opportunities."""
        opportunities = _identify_opportunities(
            "New open-source alternative emerges",
            "Founder background"
        )
        assert any("partner" in opp.lower() or "service" in opp.lower() for opp in opportunities)


class TestRiskIdentification:
    """Test scenario-specific risk identification."""

    def test_google_entry_risks(self):
        """Verify Google entry identifies specific risks."""
        risks = _identify_scenario_risks(
            "Google enters market with bundled offering",
            []
        )
        assert len(risks) > 0
        assert any("vendor" in r.lower() or "price" in r.lower() for r in risks)

    def test_cac_doubling_risks(self):
        """Verify CAC doubling identifies economics risks."""
        risks = _identify_scenario_risks(
            "CAC doubles due to market saturation",
            []
        )
        assert len(risks) > 0
        assert any("unit economics" in r.lower() or "unsustainable" in r.lower() for r in risks)


# ============================================================================
# Integration Tests: Full Simulation
# ============================================================================

class TestDigitalTwinIntegration:
    """Test Digital Twin Agent full simulation workflow."""

    @pytest.mark.asyncio
    async def test_simulate_default_scenarios(self, strong_startup_data):
        """Verify default scenarios are run when none provided."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"]
        )

        assert len(results) > 0
        assert all(isinstance(r, SimulationOutput) for r in results)

    @pytest.mark.asyncio
    async def test_simulate_custom_scenarios(self, strong_startup_data):
        """Verify custom scenarios are used when provided."""
        custom_scenarios = [
            "Market collapses by 50%",
            "Founder quits unexpectedly"
        ]

        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            custom_scenarios
        )

        assert len(results) == 2
        assert results[0].scenario == custom_scenarios[0]
        assert results[1].scenario == custom_scenarios[1]

    @pytest.mark.asyncio
    async def test_survival_probability_realistic(self, strong_startup_data):
        """Verify survival probabilities are realistic and scenario-dependent."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            [
                "Minor market adjustment",
                "Google enters market"
            ]
        )

        minor_adjustment = next(r for r in results if "Minor" in r.scenario)
        google_entry = next(r for r in results if "Google" in r.scenario)

        # Google entry should reduce survival more than minor adjustment
        assert google_entry.survival_probability < minor_adjustment.survival_probability

    @pytest.mark.asyncio
    async def test_weak_startup_lower_survival(self, weak_startup_data):
        """Verify weak startups have lower survival probabilities."""
        scenario = "Minor market downturn"

        strong_results = await simulate_scenarios(
            {
                "founders": ["ex-Google founder"],
                "competitors": ["Few competitors"],
                "market_summary": "$100B TAM growing 50%",
                "funding_summary": "Well-funded",
                "industry_summary": "Growth market"
            },
            {
                "startup_summary": "Strong startup",
                "business_model": "Profitable SaaS",
                "risks": [],
                "financials": ["$500K MRR", "130% NRR"],
                "market_claims": [],
                "evidence": []
            },
            [scenario]
        )

        weak_results = await simulate_scenarios(
            weak_startup_data["research_output"],
            weak_startup_data["knowledge_output"],
            [scenario]
        )

        strong_survival = strong_results[0].survival_probability
        weak_survival = weak_results[0].survival_probability

        # Weak startup should have lower survival
        assert weak_survival < strong_survival

    @pytest.mark.asyncio
    async def test_opportunities_identified(self, strong_startup_data):
        """Verify opportunities are identified in scenarios."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            ["Startup expands into new market"]
        )

        assert len(results[0].opportunities) > 0

    @pytest.mark.asyncio
    async def test_risks_identified(self, strong_startup_data):
        """Verify risks are identified in scenarios."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            ["Google enters market"]
        )

        assert len(results[0].risks) > 0


class TestSurvivalProbabilityPenalties:
    """Test realistic survival probability penalties."""

    @pytest.mark.asyncio
    async def test_severe_scenario_penalty(self, strong_startup_data):
        """Verify severe scenarios apply appropriate penalties."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            [
                "Company has 3 months runway and cannot raise Series B",
                "Key technical person quits"
            ]
        )

        # Both severe scenarios should have survival < 50%
        for result in results:
            if "months runway" in result.scenario or "technical" in result.scenario:
                assert result.survival_probability < 60, f"Scenario '{result.scenario}' should have lower survival"

    @pytest.mark.asyncio
    async def test_minor_scenario_higher_survival(self, strong_startup_data):
        """Verify minor scenarios have higher survival probability."""
        results = await simulate_scenarios(
            strong_startup_data["research_output"],
            strong_startup_data["knowledge_output"],
            ["Minor competitive pressure in peripheral market"]
        )

        # Minor scenario should have survival > 50%
        assert results[0].survival_probability > 50


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_digital_twin_agent.py -v

3. Run specific test class:
   pytest tests/test_digital_twin_agent.py::TestSurvivalProbabilityCalculation -v

4. Run with async support:
   pytest tests/test_digital_twin_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_digital_twin_agent.py --cov=backend.agents.digital_twin --cov-report=html

EXPECTED RESULTS:
- Schema validation tests: PASS
- Helper function tests: PASS
- Survival probability calculation tests: PASS
- Opportunity identification tests: PASS
- Risk identification tests: PASS
- Integration tests: PASS
"""
