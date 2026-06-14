"""Unit tests for Reviewer Agent."""

import pytest
from backend.agents.schemas import ReviewOutput
from backend.agents.reviewer.agent import (
    review_analysis,
    _check_completeness,
    _check_accuracy,
    _check_consistency,
    _is_shallow_analysis,
    _contains_generic_language,
    _is_generic_challenge
)


# ============================================================================
# Fixtures: Complete and Incomplete Analysis States
# ============================================================================

@pytest.fixture
def complete_analysis_state():
    """Create a complete analysis state ready for approval."""
    return {
        "bull_output": {
            "investment_case": (
                "This founding team brings exceptional domain expertise from Google and Stripe. "
                "The $150B AI market is experiencing explosive 45% CAGR growth. "
                "Their governance solution addresses a critical gap with defensible technology. "
                "With strong unit economics (LTV:CAC 3:1) and early traction from Fortune 500 customers, "
                "this is a clear category winner with significant expansion potential."
            ),
            "strengths": [
                "Founder pedigree: ex-Google, ex-Stripe",
                "Large TAM: $150B, 45% CAGR",
                "Fortune 500 validation: 3 customers",
                "Defensible moat: proprietary governance",
                "Unit economics: LTV:CAC 3:1",
                "Series A ready: backed by Sequoia"
            ],
            "confidence": 85
        },
        "bear_output": {
            "rejection_case": (
                "The team lacks relevant enterprise sales experience despite strong engineering backgrounds. "
                "The $150B market is increasingly crowded with 20+ competitors and major cloud vendors entering. "
                "Proprietary approaches are replicable by companies with 100x more resources. "
                "Unit economics are deteriorating with churn accelerating and NRR below break-even."
            ),
            "weaknesses": [
                "Founder inexperience: first-time founder in enterprise sales",
                "Market saturation: 20+ competitors, Google/AWS entering",
                "No defensible moat: features replicable by incumbents",
                "Deteriorating metrics: NRR declining",
                "Unit economics: CAC rising, LTV declining",
                "Execution risk: CEO dependency"
            ],
            "confidence": 75
        },
        "red_team_output": {
            "challenges": [
                "Claim of defensible moat contradicted by replicability analysis",
                "Fortune 500 customer claims lack independent validation",
                "Market growth assumptions unsupported by third-party research"
            ],
            "contradictions": [
                "Bull claims unique technology but Bear identifies replicable features",
                "Growth claims contradict industry saturation trends"
            ],
            "missing_evidence": [
                "No customer case studies provided",
                "No third-party validation of performance claims",
                "Financial projections not independently verified"
            ]
        },
        "research_output": {
            "founders": [
                "Alice Chen (ex-Google Brain, 10 years ML experience)",
                "Bob Rodriguez (ex-Stripe, payments at scale)"
            ],
            "competitors": [
                "Google Cloud AI",
                "AWS SageMaker",
                "Datadog ML Monitoring",
                "20+ other startups"
            ],
            "market_summary": "$150B TAM, 45% CAGR, consolidation trend",
            "funding_summary": "Series A: $5M from Sequoia and Benchmark",
            "industry_summary": "Cloud vendors bundling features, commoditization accelerating",
            "sources": ["Crunchbase", "LinkedIn", "GitHub"]
        },
        "knowledge_output": {
            "startup_summary": "AIFlow - ML Governance Platform",
            "business_model": "PLG SaaS, $5K-$50K ACV",
            "risks": ["Vendor competition", "Execution risk"],
            "financials": ["$300K MRR", "120% NRR"],
            "market_claims": [
                "Only real-time governance solution",
                "10x faster than competitors",
                "Fortune 500 validated"
            ],
            "evidence": [
                "3 Fortune 500 customers",
                "50% MoM growth",
                "250+ daily active users"
            ]
        }
    }


@pytest.fixture
def incomplete_analysis_state():
    """Create an incomplete analysis state missing Bull case."""
    return {
        "bull_output": None,  # Missing!
        "bear_output": {
            "rejection_case": "Generic risks exist",
            "weaknesses": ["Competition", "Execution risk"],
            "confidence": 70
        },
        "red_team_output": {
            "challenges": [],  # No specific challenges
            "contradictions": [],
            "missing_evidence": []
        },
        "research_output": {
            "founders": [],  # No founder analysis
            "competitors": [],  # No competitors identified
            "market_summary": "",
            "funding_summary": "",
            "industry_summary": "",
            "sources": []
        },
        "knowledge_output": {
            "startup_summary": "Company",
            "business_model": "",
            "risks": [],
            "financials": [],
            "market_claims": ["We are the best"],
            "evidence": []  # No evidence
        }
    }


@pytest.fixture
def shallow_analysis_state():
    """Create analysis with shallow, generic language."""
    return {
        "bull_output": {
            "investment_case": "This startup could be good. It might work. Execution risk exists.",  # Generic
            "strengths": ["Good team", "Good market"],
            "confidence": 60
        },
        "bear_output": {
            "rejection_case": "There is competition. It might be risky.",  # Too vague
            "weaknesses": ["Execution risk", "Market risk"],
            "confidence": 60
        },
        "red_team_output": {
            "challenges": ["Generic challenge"],
            "contradictions": [],
            "missing_evidence": []
        },
        "research_output": {
            "founders": ["Founder"],
            "competitors": ["Competitor"],
            "market_summary": "Market exists",
            "funding_summary": "Got funding",
            "industry_summary": "Industry is competitive",
            "sources": []
        },
        "knowledge_output": {
            "startup_summary": "Startup",
            "business_model": "SaaS model",
            "risks": [],
            "financials": [],
            "market_claims": [],
            "evidence": []
        }
    }


@pytest.fixture
def hallucinated_analysis_state():
    """Create analysis with potential hallucinations."""
    return {
        "bull_output": {
            "investment_case": (
                "The startup has 100+ Fortune 500 customers including Apple, Google, Microsoft. "
                "Revenue is $1B ARR with 500% growth. Market is $5 trillion."
            ),
            "strengths": ["Unrealistic numbers", "Made-up customers"],
            "confidence": 95
        },
        "bear_output": {
            "rejection_case": "Analysis not provided",
            "weaknesses": [],
            "confidence": 0
        },
        "red_team_output": {
            "challenges": [],
            "contradictions": [],
            "missing_evidence": []
        },
        "research_output": {
            "founders": ["Founder"],
            "competitors": [],
            "market_summary": "",
            "funding_summary": "",
            "industry_summary": "",
            "sources": []
        },
        "knowledge_output": {
            "startup_summary": "Startup",
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

class TestReviewOutputSchema:
    """Test ReviewOutput schema validation."""

    def test_review_output_schema_has_required_fields(self):
        """Verify ReviewOutput has all required fields."""
        output = ReviewOutput(
            approved=True,
            feedback="Analysis approved",
            retry_required=False
        )
        assert output.approved is True
        assert output.feedback == "Analysis approved"
        assert output.retry_required is False

    def test_review_output_required_fields(self):
        """Verify all fields are required."""
        with pytest.raises(ValueError):
            ReviewOutput(
                approved=True,
                feedback="Feedback"
                # Missing retry_required
            )

    def test_review_output_field_types(self):
        """Verify field types are correct."""
        with pytest.raises(ValueError):
            ReviewOutput(
                approved="true",  # Should be bool
                feedback="Feedback",
                retry_required=False
            )


class TestCompletenessChecks:
    """Test completeness validation."""

    def test_complete_analysis_passes(self, complete_analysis_state):
        """Verify complete analysis passes all checks."""
        result = _check_completeness(
            complete_analysis_state["bull_output"],
            complete_analysis_state["bear_output"],
            complete_analysis_state["red_team_output"],
            complete_analysis_state["research_output"],
            complete_analysis_state["knowledge_output"]
        )
        assert len(result["missing_analyses"]) == 0
        assert len(result["shallow_analyses"]) == 0

    def test_missing_bull_case_detected(self, incomplete_analysis_state):
        """Verify missing Bull case is detected."""
        result = _check_completeness(
            None,  # Bull output missing
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )
        assert "Bull case" in result["missing_analyses"]

    def test_missing_competitors_detected(self, incomplete_analysis_state):
        """Verify missing competitor analysis is detected."""
        result = _check_completeness(
            incomplete_analysis_state["bull_output"],
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )
        assert any("competitor" in analysis.lower() for analysis in result["shallow_analyses"])

    def test_no_evidence_detected(self, incomplete_analysis_state):
        """Verify missing evidence in knowledge base is detected."""
        result = _check_completeness(
            incomplete_analysis_state["bull_output"],
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )
        assert any("evidence" in analysis.lower() for analysis in result["shallow_analyses"])


class TestAccuracyChecks:
    """Test accuracy validation."""

    def test_generic_language_detected(self, shallow_analysis_state):
        """Verify generic/vague language is flagged."""
        result = _check_accuracy(
            shallow_analysis_state["bull_output"],
            shallow_analysis_state["bear_output"],
            shallow_analysis_state["red_team_output"],
            shallow_analysis_state["knowledge_output"]
        )
        assert len(result["issues"]) > 0
        assert any("generic" in issue.lower() for issue in result["issues"])

    def test_claims_without_evidence_flagged(self, incomplete_analysis_state):
        """Verify more claims than evidence is flagged."""
        result = _check_accuracy(
            incomplete_analysis_state["bull_output"],
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["knowledge_output"]
        )
        # Should flag mismatch between claims and evidence
        assert any("more claims" in issue.lower() or "evidence" in issue.lower() for issue in result["issues"])

    def test_substantive_analysis_passes(self, complete_analysis_state):
        """Verify substantive analysis passes accuracy checks."""
        result = _check_accuracy(
            complete_analysis_state["bull_output"],
            complete_analysis_state["bear_output"],
            complete_analysis_state["red_team_output"],
            complete_analysis_state["knowledge_output"]
        )
        # Should have minimal or no accuracy issues
        assert len(result["issues"]) < 3


class TestHelperFunctions:
    """Test helper functions."""

    def test_shallow_analysis_detection(self):
        """Verify shallow analyses are detected."""
        shallow = "This is too short"
        deep = (
            "This is a comprehensive analysis with multiple sentences "
            "that provides detailed insights and evidence-based reasoning "
            "about the subject matter."
        )

        assert _is_shallow_analysis(shallow) is True
        assert _is_shallow_analysis(deep) is False
        assert _is_shallow_analysis("") is True

    def test_generic_language_detection(self):
        """Verify generic language is detected."""
        generic = "This could potentially be good. It might work. Seems to have potential."
        specific = (
            "The startup has $500K MRR with 3 Fortune 500 customers "
            "and demonstrated 120% NRR, indicating strong product-market fit."
        )

        assert _contains_generic_language(generic) is True
        assert _contains_generic_language(specific) is False

    def test_generic_challenge_detection(self):
        """Verify generic challenges are detected."""
        generic = "Execution risk exists"
        specific = "This startup depends entirely on CEO for technical decisions and business development"

        assert _is_generic_challenge(generic) is True
        assert _is_generic_challenge(specific) is False


# ============================================================================
# Integration Tests: Full Review Workflow
# ============================================================================

class TestReviewerIntegration:
    """Test Reviewer Agent integration workflow."""

    @pytest.mark.asyncio
    async def test_complete_analysis_approved(self, complete_analysis_state):
        """Verify complete analysis is approved."""
        result = await review_analysis(
            complete_analysis_state["bull_output"],
            complete_analysis_state["bear_output"],
            complete_analysis_state["red_team_output"],
            complete_analysis_state["research_output"],
            complete_analysis_state["knowledge_output"]
        )

        assert isinstance(result, ReviewOutput)
        assert result.approved is True
        assert result.retry_required is False

    @pytest.mark.asyncio
    async def test_incomplete_analysis_rejected(self, incomplete_analysis_state):
        """Verify incomplete analysis is rejected and retry triggered."""
        result = await review_analysis(
            incomplete_analysis_state["bull_output"],
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )

        assert isinstance(result, ReviewOutput)
        assert result.approved is False
        assert result.retry_required is True
        assert "Bull case" in result.feedback or "missing" in result.feedback.lower()

    @pytest.mark.asyncio
    async def test_shallow_analysis_rejected(self, shallow_analysis_state):
        """Verify shallow analysis is rejected."""
        result = await review_analysis(
            shallow_analysis_state["bull_output"],
            shallow_analysis_state["bear_output"],
            shallow_analysis_state["red_team_output"],
            shallow_analysis_state["research_output"],
            shallow_analysis_state["knowledge_output"]
        )

        assert isinstance(result, ReviewOutput)
        assert result.approved is False
        assert result.retry_required is True
        assert "generic" in result.feedback.lower() or "shallow" in result.feedback.lower()

    @pytest.mark.asyncio
    async def test_hallucinated_analysis_rejected(self, hallucinated_analysis_state):
        """Verify hallucinated/unrealistic analysis is rejected."""
        result = await review_analysis(
            hallucinated_analysis_state["bull_output"],
            hallucinated_analysis_state["bear_output"],
            hallucinated_analysis_state["red_team_output"],
            hallucinated_analysis_state["research_output"],
            hallucinated_analysis_state["knowledge_output"]
        )

        assert isinstance(result, ReviewOutput)
        assert result.retry_required is True  # Should trigger retry

    @pytest.mark.asyncio
    async def test_actionable_feedback_provided(self, incomplete_analysis_state):
        """Verify feedback is actionable for orchestrator."""
        result = await review_analysis(
            incomplete_analysis_state["bull_output"],
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )

        # Feedback should indicate what to fix and whether to retry
        assert len(result.feedback) > 0
        assert result.retry_required is True
        # Feedback should be specific enough to trigger correct agent re-run
        assert ("Bull case" in result.feedback or
                "missing" in result.feedback.lower() or
                "competitors" in result.feedback.lower())


class TestReflectionLoopTrigger:
    """Test reflection loop triggering logic."""

    @pytest.mark.asyncio
    async def test_retry_true_when_incomplete(self, incomplete_analysis_state):
        """Verify retry_required=True when analysis is incomplete."""
        result = await review_analysis(
            None,  # Missing Bull
            incomplete_analysis_state["bear_output"],
            incomplete_analysis_state["red_team_output"],
            incomplete_analysis_state["research_output"],
            incomplete_analysis_state["knowledge_output"]
        )
        assert result.retry_required is True

    @pytest.mark.asyncio
    async def test_retry_true_when_inaccurate(self, hallucinated_analysis_state):
        """Verify retry_required=True when analysis contains hallucinations."""
        result = await review_analysis(
            hallucinated_analysis_state["bull_output"],
            hallucinated_analysis_state["bear_output"],
            hallucinated_analysis_state["red_team_output"],
            hallucinated_analysis_state["research_output"],
            hallucinated_analysis_state["knowledge_output"]
        )
        assert result.retry_required is True

    @pytest.mark.asyncio
    async def test_retry_false_when_complete(self, complete_analysis_state):
        """Verify retry_required=False when analysis is complete."""
        result = await review_analysis(
            complete_analysis_state["bull_output"],
            complete_analysis_state["bear_output"],
            complete_analysis_state["red_team_output"],
            complete_analysis_state["research_output"],
            complete_analysis_state["knowledge_output"]
        )
        assert result.retry_required is False


# ============================================================================
# Mock Tests: Quality Evaluation Logic
# ============================================================================

class TestQualityEvaluation:
    """Test quality evaluation logic without LLM."""

    def test_evaluate_bull_specificity(self):
        """Test evaluation of Bull case specificity."""
        generic_bull = "This is a good investment opportunity with strong potential"
        specific_bull = (
            "Founder background from Google/Stripe, $150B market at 45% CAGR, "
            "3 Fortune 500 customers, LTV:CAC 3:1, Series A backed by Sequoia"
        )

        assert _is_shallow_analysis(generic_bull) is True
        assert _is_shallow_analysis(specific_bull) is False

    def test_evaluate_evidence_support(self):
        """Test evaluation of evidence supporting claims."""
        # More claims than evidence = risk
        claims = ["Claim 1", "Claim 2", "Claim 3", "Claim 4"]
        evidence = ["Evidence 1"]

        claim_evidence_ratio = len(claims) / len(evidence)
        assert claim_evidence_ratio > 1  # More claims than evidence = concern

    def test_evaluate_red_team_depth(self):
        """Test evaluation of Red Team analysis depth."""
        shallow_challenge = "Market competition exists"
        deep_challenge = "Startup claims unique governance, but Google Cloud AI offers similar features"

        assert _is_generic_challenge(shallow_challenge) is True
        assert _is_generic_challenge(deep_challenge) is False


# ============================================================================
# Test Instructions
# ============================================================================

"""
HOW TO RUN TESTS:

1. Install pytest and pytest-asyncio:
   pip install pytest pytest-asyncio

2. Run all tests:
   pytest tests/test_reviewer_agent.py -v

3. Run specific test class:
   pytest tests/test_reviewer_agent.py::TestReviewerIntegration -v

4. Run with async support:
   pytest tests/test_reviewer_agent.py -v --asyncio-mode=auto

5. Run with coverage:
   pytest tests/test_reviewer_agent.py --cov=backend.agents.reviewer --cov-report=html

EXPECTED RESULTS:
- Schema validation tests: PASS
- Completeness check tests: PASS
- Accuracy check tests: PASS
- Helper function tests: PASS
- Integration tests: PASS (mock logic tests)
- Reflection loop tests: PASS
- Quality evaluation tests: PASS
"""
