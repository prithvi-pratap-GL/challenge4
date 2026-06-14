"""Unit tests for Committee Agent."""

import pytest
from backend.agents.schemas import CommitteeDecision
from backend.agents.committee.agent import (
    run_committee,
    _analyze_bull_vs_bear,
    _evaluate_red_team_challenges,
    _assess_analysis_completeness,
    _make_investment_decision
)


# ============================================================================
# Fixtures: Different Analysis Scenarios
# ============================================================================

@pytest.fixture
def strong_bull_case():
    """Strong Bull case scenario."""
    return {
        "bull_output": {
            "investment_case": (
                "Exceptional founding team from Google/Stripe. "
                "$150B TAM with 45% CAGR. 3 Fortune 500 customers validating product. "
                "LTV:CAC 3:1 with path to profitability. Series A backed by Sequoia."
            ),
            "strengths": [
                "Founder pedigree and execution track record",
                "Large addressable market with strong growth",
                "Early customer validation from Fortune 500s",
                "Sustainable unit economics",
                "Experienced institutional backing"
            ],
            "confidence": 85
        },
        "bear_output": {
            "rejection_case": "Competitive threats from Google, AWS. Some execution risk.",
            "weaknesses": ["Competition", "Execution risk"],
            "confidence": 45
        },
        "red_team_output": {
            "challenges": ["Verify Fortune 500 customer commitment"],
            "contradictions": [],
            "missing_evidence": []
        },
        "research_output": {
            "founders": ["Alice Chen (ex-Google)", "Bob Rodriguez (ex-Stripe)"],
            "competitors": ["Google Cloud", "AWS"],
            "market_summary": "$150B TAM, 45% CAGR",
            "funding_summary": "Series A $5M Sequoia",
            "industry_summary": "Growing market"
        },
        "knowledge_output": {
            "startup_summary": "AI Governance",
            "business_model": "PLG SaaS",
            "risks": [],
            "financials": ["$300K MRR", "120% NRR"],
            "market_claims": ["Best governance platform"],
            "evidence": ["3 Fortune 500 customers", "50% MoM growth"]
        }
    }


@pytest.fixture
def strong_bear_case():
    """Strong Bear case scenario."""
    return {
        "bull_output": {
            "investment_case": "Market opportunity exists but faces challenges.",
            "strengths": ["Market size"],
            "confidence": 40
        },
        "bear_output": {
            "rejection_case": (
                "20+ competitors including Google/AWS. "
                "Founder inexperience in enterprise. Unit economics deteriorating. "
                "Market consolidating around incumbents."
            ),
            "weaknesses": [
                "Market saturation with well-funded competitors",
                "Founder lacks enterprise sales experience",
                "Deteriorating metrics (NRR declining)",
                "Execution risk with key person dependency",
                "Commoditization of features"
            ],
            "confidence": 80
        },
        "red_team_output": {
            "challenges": [
                "Fortune 500 claims lack independent validation",
                "Market growth assumptions unsupported"
            ],
            "contradictions": [
                "Bull claims unique solution but features are replicable"
            ],
            "missing_evidence": [
                "No customer case studies",
                "No independent verification of performance"
            ]
        },
        "research_output": {
            "founders": ["First-time founder"],
            "competitors": ["20+ direct competitors", "Google entering", "AWS bundling"],
            "market_summary": "Saturated market, commoditization accelerating",
            "funding_summary": "Tier-2 investors, follow-on forced",
            "industry_summary": "Consolidation favoring incumbents"
        },
        "knowledge_output": {
            "startup_summary": "Another SaaS tool",
            "business_model": "Unsustainable burn",
            "risks": ["Vendor competition", "Team risk"],
            "financials": ["$300K MRR declining", "85% NRR"],
            "market_claims": ["Only governance solution"],
            "evidence": []
        }
    }


@pytest.fixture
def balanced_case():
    """Balanced scenario with mixed signals."""
    return {
        "bull_output": {
            "investment_case": "Good team, large market, but faces competition.",
            "strengths": ["Team", "Market size", "Early traction"],
            "confidence": 65
        },
        "bear_output": {
            "rejection_case": "Competition and execution risk present.",
            "weaknesses": ["Competition", "Execution risk"],
            "confidence": 60
        },
        "red_team_output": {
            "challenges": ["Market claims need validation"],
            "contradictions": ["Growth rate claims vs competitor saturation"],
            "missing_evidence": ["Customer retention data"]
        },
        "research_output": {
            "founders": ["Mixed experience"],
            "competitors": ["5-10 competitors"],
            "market_summary": "$50B TAM, growing",
            "funding_summary": "Series A recent",
            "industry_summary": "Competitive but growing"
        },
        "knowledge_output": {
            "startup_summary": "Growth-stage startup",
            "business_model": "SaaS with improving economics",
            "risks": ["Execution", "Market"],
            "financials": ["$200K MRR", "110% NRR"],
            "market_claims": ["Strong position"],
            "evidence": ["2 large customers", "40% growth"]
        }
    }


@pytest.fixture
def incomplete_analysis():
    """Incomplete analysis missing evidence."""
    return {
        "bull_output": {
            "investment_case": "Looks promising",
            "strengths": ["Team"],
            "confidence": 50
        },
        "bear_output": {
            "rejection_case": "Some risk",
            "weaknesses": ["Risk"],
            "confidence": 50
        },
        "red_team_output": {
            "challenges": [],
            "contradictions": [],
            "missing_evidence": []
        },
        "research_output": {
            "founders": [],
            "competitors": [],
            "market_summary": "",
            "funding_summary": "",
            "industry_summary": ""
        },
        "knowledge_output": {
            "startup_summary": "Company",
            "business_model": "",
            "risks": [],
            "financials": [],
            "market_claims": [],
            "evidence": []
        }
    }


# ============================================================================
# Unit Tests
# ============================================================================

class TestCommitteeDecisionSchema:
    """Test CommitteeDecision schema validation."""

    def test_committee_decision_schema(self):
        """Verify CommitteeDecision has all required fields."""
        decision = CommitteeDecision(
            verdict="INVEST",
            confidence=85,
            reasoning="Bull case compelling with strong team and market."
        )
        assert decision.verdict == "INVEST"
        assert decision.confidence == 85
        assert "Bull" in decision.reasoning

    def test_verdict_options(self):
        """Verify valid verdict options."""
        for verdict in ["INVEST", "PASS", "CONDITIONAL"]:
            decision = CommitteeDecision(
                verdict=verdict,
                confidence=70,
                reasoning="Test"
            )
            assert decision.verdict == verdict

    def test_confidence_bounds(self):
        """Verify confidence is 0-100."""
        with pytest.raises(ValueError):
            CommitteeDecision(
                verdict="INVEST",
                confidence=101,
                reasoning="Test"
            )


class TestBullVsBearAnalysis:
    """Test Bull vs Bear debate analysis."""

    def test_bull_stronger_scenario(self, strong_bull_case):
        """Verify Bull case detected as stronger."""
        result = _analyze_bull_vs_bear(
            strong_bull_case["bull_output"],
            strong_bull_case["bear_output"],
            strong_bull_case["red_team_output"]
        )
        assert result["bull_stronger"] is True
        assert result["confidence_gap"] == 40

    def test_bear_stronger_scenario(self, strong_bear_case):
        """Verify Bear case detected as stronger."""
        result = _analyze_bull_vs_bear(
            strong_bear_case["bull_output"],
            strong_bear_case["bear_output"],
            strong_bear_case["red_team_output"]
        )
        assert result["bull_stronger"] is False
        assert result["confidence_gap"] == 40

    def test_balanced_scenario(self, balanced_case):
        """Verify balanced case detected."""
        result = _analyze_bull_vs_bear(
            balanced_case["bull_output"],
            balanced_case["bear_output"],
            balanced_case["red_team_output"]
        )
        assert result["confidence_gap"] == 5


class TestRedTeamSeverityEvaluation:
    """Test Red Team challenge severity assessment."""

    def test_low_severity(self, strong_bull_case):
        """Verify low severity Red Team issues."""
        result = _evaluate_red_team_challenges(strong_bull_case["red_team_output"])
        assert result["severity"] == "LOW"
        assert result["total_issues"] == 1

    def test_high_severity(self, strong_bear_case):
        """Verify high severity Red Team issues."""
        result = _evaluate_red_team_challenges(strong_bear_case["red_team_output"])
        assert result["severity"] == "HIGH"
        assert result["total_issues"] >= 5

    def test_critical_severity(self):
        """Verify critical severity detection."""
        red_team = {
            "challenges": ["C1", "C2", "C3"],
            "contradictions": ["X1", "X2", "X3"],
            "missing_evidence": ["E1", "E2", "E3"]
        }
        result = _evaluate_red_team_challenges(red_team)
        assert result["severity"] == "CRITICAL"


class TestCompletenessAssessment:
    """Test analysis completeness evaluation."""

    def test_complete_analysis(self, strong_bull_case):
        """Verify complete analysis detected."""
        result = _assess_analysis_completeness(
            strong_bull_case["research_output"],
            strong_bull_case["knowledge_output"],
            strong_bull_case["red_team_output"]
        )
        assert result["is_complete"] is True
        assert len(result["gaps"]) == 0

    def test_incomplete_analysis(self, incomplete_analysis):
        """Verify incomplete analysis detected."""
        result = _assess_analysis_completeness(
            incomplete_analysis["research_output"],
            incomplete_analysis["knowledge_output"],
            incomplete_analysis["red_team_output"]
        )
        assert result["is_complete"] is False
        assert len(result["gaps"]) > 0


# ============================================================================
# Integration Tests: Full Committee Decision
# ============================================================================

class TestCommitteeIntegration:
    """Test Committee Agent full decision workflow."""

    @pytest.mark.asyncio
    async def test_invest_decision_strong_bull(self, strong_bull_case):
        """Verify INVEST recommendation for strong Bull case."""
        result = await run_committee(
            strong_bull_case["bull_output"],
            strong_bull_case["bear_output"],
            strong_bull_case["red_team_output"],
            strong_bull_case["research_output"],
            strong_bull_case["knowledge_output"]
        )

        assert isinstance(result, CommitteeDecision)
        assert result.verdict == "INVEST"
        assert result.confidence >= 75
        assert "Bull" in result.reasoning or "bull" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_pass_decision_strong_bear(self, strong_bear_case):
        """Verify PASS recommendation for strong Bear case."""
        result = await run_committee(
            strong_bear_case["bull_output"],
            strong_bear_case["bear_output"],
            strong_bear_case["red_team_output"],
            strong_bear_case["research_output"],
            strong_bear_case["knowledge_output"]
        )

        assert isinstance(result, CommitteeDecision)
        assert result.verdict == "PASS"
        assert result.confidence <= 45
        assert "Bear" in result.reasoning or "bear" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_conditional_decision_balanced(self, balanced_case):
        """Verify CONDITIONAL recommendation for balanced case."""
        result = await run_committee(
            balanced_case["bull_output"],
            balanced_case["bear_output"],
            balanced_case["red_team_output"],
            balanced_case["research_output"],
            balanced_case["knowledge_output"]
        )

        assert isinstance(result, CommitteeDecision)
        assert result.verdict == "CONDITIONAL"
        assert 50 <= result.confidence <= 70

    @pytest.mark.asyncio
    async def test_pass_decision_incomplete(self, incomplete_analysis):
        """Verify PASS recommendation for incomplete analysis."""
        result = await run_committee(
            incomplete_analysis["bull_output"],
            incomplete_analysis["bear_output"],
            incomplete_analysis["red_team_output"],
            incomplete_analysis["research_output"],
            incomplete_analysis["knowledge_output"]
        )

        assert isinstance(result, CommitteeDecision)
        assert result.verdict == "PASS"
        assert result.confidence <= 40
        assert "incomplete" in result.reasoning.lower()


class TestReasoningQuality:
    """Test reasoning quality and references to all perspectives."""

    @pytest.mark.asyncio
    async def test_reasoning_references_bull(self, strong_bull_case):
        """Verify reasoning references Bull case."""
        result = await run_committee(
            strong_bull_case["bull_output"],
            strong_bull_case["bear_output"],
            strong_bull_case["red_team_output"],
            strong_bull_case["research_output"],
            strong_bull_case["knowledge_output"]
        )

        assert "Bull" in result.reasoning or "bull" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_reasoning_references_bear(self, strong_bear_case):
        """Verify reasoning references Bear case."""
        result = await run_committee(
            strong_bear_case["bull_output"],
            strong_bear_case["bear_output"],
            strong_bear_case["red_team_output"],
            strong_bear_case["research_output"],
            strong_bear_case["knowledge_output"]
        )

        assert "Bear" in result.reasoning or "bear" in result.reasoning.lower()

    @pytest.mark.asyncio
    async def test_reasoning_references_red_team(self, balanced_case):
        """Verify reasoning references Red Team findings."""
        result = await run_committee(
            balanced_case["bull_output"],
            balanced_case["bear_output"],
            balanced_case["red_team_output"],
            balanced_case["research_output"],
            balanced_case["knowledge_output"]
        )

        reasoning_lower = result.reasoning.lower()
        # Should mention Red Team, challenges, or contradictions
        assert any(term in reasoning_lower for term in ["red team", "challenge", "contradiction", "issue"])

    @pytest.mark.asyncio
    async def test_reasoning_substantive(self, strong_bull_case):
        """Verify reasoning is substantive and specific."""
        result = await run_committee(
            strong_bull_case["bull_output"],
            strong_bull_case["bear_output"],
            strong_bull_case["red_team_output"],
            strong_bull_case["research_output"],
            strong_bull_case["knowledge_output"]
        )

        # Reasoning should be detailed, not generic
        assert len(result.reasoning) > 100
        assert "founder" in result.reasoning.lower() or "market" in result.reasoning.lower()


class TestDecisionLogic:
    """Test decision logic implementation."""

    @pytest.mark.asyncio
    async def test_default_to_pass_when_uncertain(self, incomplete_analysis):
        """Verify defaults to PASS when analysis incomplete."""
        result = await run_committee(
            incomplete_analysis["bull_output"],
            incomplete_analysis["bear_output"],
            incomplete_analysis["red_team_output"],
            incomplete_analysis["research_output"],
            incomplete_analysis["knowledge_output"]
        )
        assert result.verdict == "PASS"

    @pytest.mark.asyncio
    async def test_invest_requires_bull_stronger(self, strong_bull_case):
        """Verify INVEST only when Bull is stronger."""
        result = await run_committee(
            strong_bull_case["bull_output"],
            strong_bull_case["bear_output"],
            strong_bull_case["red_team_output"],
            strong_bull_case["research_output"],
            strong_bull_case["knowledge_output"]
        )
        # Bull is stronger (85 vs 45), so INVEST is possible
        assert result.verdict in ["INVEST", "CONDITIONAL"]

    @pytest.mark.asyncio
    async def test_pass_for_critical_red_team(self, strong_bear_case):
        """Verify PASS when Red Team issues critical."""
        result = await run_committee(
            strong_bear_case["bull_output"],
            strong_bear_case["bear_output"],
            strong_bear_case["red_team_output"],
            strong_bear_case["research_output"],
            strong_bear_case["knowledge_output"]
        )
        # High Red Team severity should lead to PASS
        assert result.verdict == "PASS"


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_committee_agent.py -v

3. Run specific test class:
   pytest tests/test_committee_agent.py::TestCommitteeIntegration -v

4. Run with async support:
   pytest tests/test_committee_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_committee_agent.py --cov=backend.agents.committee --cov-report=html

EXPECTED RESULTS:
- Schema validation tests: PASS
- Bull vs Bear analysis tests: PASS
- Red Team severity tests: PASS
- Completeness assessment tests: PASS
- Committee integration tests: PASS
- Reasoning quality tests: PASS
- Decision logic tests: PASS
"""
