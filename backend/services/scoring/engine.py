"""
VentureMind AI — Deterministic Scoring Engine
Production-grade rules-based evaluation of startup investment potential.

Implements IScoringEngine using deterministic logic exclusively.
LLM extracts findings (non-deterministic), Python assigns scores (deterministic).
"""

import asyncio
import logging
import re
from pathlib import Path
from typing import List, Optional

from backend.domain.interfaces import IFindingExtractor, IScoringEngine
from backend.domain.schemas import (
    CategoryScore,
    FactorScore,
    Finding,
    InvestmentRecommendation,
    RecommendationStatus,
    ScoreCategory,
)

logger = logging.getLogger(__name__)


class DeterministicScoringService(IScoringEngine):
    """
    Production-ready deterministic scoring engine for investment decisions.

    Architecture:
    - Separates LLM-based finding extraction (non-deterministic) from
      deterministic scoring logic (Python rules)
    - Uses a Rules Engine pattern with category-specific evaluators
    - Each rule is pure logic with no external dependencies
    - Fully auditable: score → factor → finding → chunk_id → source

    Scoring tiers:
    - 0-40: Weak (red flags, significant concerns)
    - 41-60: Adequate (some concerns, moderate potential)
    - 61-75: Strong (good fundamentals, opportunity)
    - 76-100: Excellent (outstanding potential, best-in-class)

    Investment Logic:
    - INVEST: All core categories > 75 AND risk < 40
    - WATCHLIST: 2+ core categories > 60 AND risk < 60
    - PASS: Otherwise
    """

    def __init__(self, finding_extractor: IFindingExtractor):
        """
        Initialize the deterministic scoring service.

        Args:
            finding_extractor: IFindingExtractor for fact extraction.
        """
        self.finding_extractor = finding_extractor
        self.upload_dir = Path("storage/uploads")
        logger.info("✓ Deterministic scoring service initialized")

    def _find_pdf_url(self, deal_id: str) -> Optional[str]:
        """
        Find the uploaded PDF for a deal and return its public URL.

        Args:
            deal_id: The deal ID to search for.

        Returns:
            The public /uploads/ URL if found, None otherwise.
        """
        if not self.upload_dir.exists():
            return None

        for pdf_file in self.upload_dir.glob(f"{deal_id}_*"):
            if pdf_file.is_file() and pdf_file.suffix.lower() == ".pdf":
                return f"/uploads/{pdf_file.name}"

        return None

    async def evaluate_startup(self, deal_id: str) -> InvestmentRecommendation:
        """
        Evaluate a startup and produce an investment recommendation.

        Orchestrates the complete scoring pipeline:
        1. Concurrently extract findings across all categories
        2. Apply deterministic factor rules to each category
        3. Aggregate factor scores to category scores
        4. Apply final deterministic logic for recommendation
        5. Generate executive reasoning

        Args:
            deal_id: The deal/startup ID to evaluate.

        Returns:
            InvestmentRecommendation: Complete scoring and recommendation.

        Raises:
            RuntimeError: If evaluation fails critically.
        """
        logger.info("=" * 80)
        logger.info(f"[ScoringEngine] Evaluating startup: deal_id={deal_id}")
        logger.info("=" * 80)

        try:
            # ================================================================
            # Step 1: Concurrently Extract Findings
            # ================================================================
            logger.info("\n[Step 1] Extracting findings across all categories...")
            extraction_tasks = {
                category: self.finding_extractor.extract_findings(deal_id, category)
                for category in ScoreCategory
            }

            findings_by_category = await asyncio.gather(
                *extraction_tasks.values(), return_exceptions=True
            )

            category_findings = {}
            for category, result in zip(extraction_tasks.keys(), findings_by_category):
                if isinstance(result, Exception):
                    logger.warning(
                        f"  ⚠ Failed to extract findings for {category.value}: {result}"
                    )
                    category_findings[category] = []
                else:
                    category_findings[category] = result
                    logger.info(
                        f"  ✓ Extracted {len(result)} findings for {category.value}"
                    )
                    if result:
                        for finding in result:
                            logger.debug(f"    - {finding.finding_text[:80]}... (chunks: {len(finding.supporting_chunk_ids)})")

            # ================================================================
            # Step 2: Apply Deterministic Factor Rules
            # ================================================================
            logger.info("\n[Step 2] Applying deterministic scoring rules...")
            category_scores: List[CategoryScore] = []

            for category in ScoreCategory:
                findings = category_findings[category]
                factor_scores = self._evaluate_category(category, findings)
                aggregate_score = self._aggregate_factors(factor_scores)

                category_score = CategoryScore(
                    category=category,
                    factors=factor_scores,
                    aggregate_score=aggregate_score,
                )
                category_scores.append(category_score)

                logger.info(
                    f"  ✓ {category.value.upper()}: score={aggregate_score} "
                    f"(factors: {len(factor_scores)})"
                )

            # ================================================================
            # Step 3: Apply Final Deterministic Logic
            # ================================================================
            logger.info("\n[Step 3] Applying final recommendation logic...")
            status = self._determine_recommendation(category_scores)
            reasoning = self._generate_reasoning(category_scores, status)

            logger.info(f"  ✓ Recommendation: {status.value.upper()}")

            # ================================================================
            # Return Final Recommendation
            # ================================================================
            pdf_url = self._find_pdf_url(deal_id)
            recommendation = InvestmentRecommendation(
                deal_id=deal_id,
                status=status,
                reasoning=reasoning,
                category_scores=category_scores,
                pdf_url=pdf_url,
            )

            logger.info("\n" + "=" * 80)
            logger.info("✓ Evaluation completed successfully")
            logger.info(f"  Status: {status.value.upper()}")

            # Log sample findings for verification
            for cat_score in category_scores:
                total_findings = sum(len(f.findings) for f in cat_score.factors)
                logger.info(f"  {cat_score.category.value.upper()}: {total_findings} findings across {len(cat_score.factors)} factors")
                if cat_score.factors:
                    first_factor = cat_score.factors[0]
                    logger.info(f"    Example factor '{first_factor.factor_name}': {len(first_factor.findings)} findings")
                    if first_factor.findings:
                        logger.info(f"      Example: {first_factor.findings[0]}")

            logger.info("=" * 80)

            return recommendation

        except Exception as e:
            logger.error(
                f"✗ Evaluation failed ({type(e).__name__}): {e}",
                exc_info=True,
            )
            raise RuntimeError(f"Startup evaluation failed: {e}") from e

    def _evaluate_category(
        self, category: ScoreCategory, findings: List[Finding]
    ) -> List[FactorScore]:
        """
        Evaluate a category using category-specific deterministic rules.

        Args:
            category: The scoring category.
            findings: Extracted findings for this category.

        Returns:
            List of FactorScore objects.
        """
        if category == ScoreCategory.TEAM:
            return self._evaluate_team_factors(findings)
        elif category == ScoreCategory.MARKET:
            return self._evaluate_market_factors(findings)
        elif category == ScoreCategory.PRODUCT:
            return self._evaluate_product_factors(findings)
        elif category == ScoreCategory.FINANCIAL:
            return self._evaluate_financial_factors(findings)
        elif category == ScoreCategory.RISK:
            return self._evaluate_risk_factors(findings)
        else:
            return []

    def _evaluate_team_factors(self, findings: List[Finding]) -> List[FactorScore]:
        """
        Deterministic evaluation of TEAM category.

        Factors:
        - Domain Expertise: Founders with prior success in same domain
        - Leadership Experience: Track record of leading companies/teams
        - Diversity: Mix of skills (technical, business, domain)

        Args:
            findings: Team-related findings.

        Returns:
            List of FactorScore objects.
        """
        factors = []
        logger.info(f"[_evaluate_team_factors] Input findings count: {len(findings)}")
        if findings:
            logger.info(f"  Sample input: {findings[0].finding_text[:100]}")

        # Factor 1: Domain Expertise
        domain_expertise_score = self._score_domain_expertise(findings)
        domain_expertise_findings = self._filter_findings_for_factor(findings, ["domain", "expertise"])
        logger.info(f"[Domain Expertise] Before filter: {len(findings)}, After filter: {len(domain_expertise_findings)}")
        factors.append(
            FactorScore(
                factor_name="Domain Expertise",
                score=domain_expertise_score,
                findings=domain_expertise_findings,
            )
        )

        # Factor 2: Leadership Experience
        leadership_score = self._score_leadership_experience(findings)
        factors.append(
            FactorScore(
                factor_name="Leadership Experience",
                score=leadership_score,
                findings=self._filter_findings_for_factor(findings, ["founder", "ceo", "leader", "exit"]),
            )
        )

        # Factor 3: Team Composition
        team_diversity_score = self._score_team_diversity(findings)
        factors.append(
            FactorScore(
                factor_name="Team Composition",
                score=team_diversity_score,
                findings=self._filter_findings_for_factor(findings, ["team", "background", "experience"]),
            )
        )

        return factors

    def _evaluate_market_factors(self, findings: List[Finding]) -> List[FactorScore]:
        """
        Deterministic evaluation of MARKET category.

        Factors:
        - Market Size: TAM > $1B (excellent), > $100M (good), etc.
        - Market Growth: Annual growth > 20% (strong)
        - Competitive Position: Limited competitors or clear differentiation

        Args:
            findings: Market-related findings.

        Returns:
            List of FactorScore objects.
        """
        factors = []

        # Factor 1: Market Size
        market_size_score = self._score_market_size(findings)
        factors.append(
            FactorScore(
                factor_name="Market Size & TAM",
                score=market_size_score,
                findings=self._filter_findings_for_factor(findings, ["market", "tam", "addressable"]),
            )
        )

        # Factor 2: Market Growth
        market_growth_score = self._score_market_growth(findings)
        factors.append(
            FactorScore(
                factor_name="Market Growth",
                score=market_growth_score,
                findings=self._filter_findings_for_factor(findings, ["growth", "trend", "adoption"]),
            )
        )

        # Factor 3: Competitive Position
        competitive_position_score = self._score_competitive_position(findings)
        factors.append(
            FactorScore(
                factor_name="Competitive Position",
                score=competitive_position_score,
                findings=self._filter_findings_for_factor(findings, ["competitive", "differentiation", "advantage"]),
            )
        )

        return factors

    def _evaluate_product_factors(self, findings: List[Finding]) -> List[FactorScore]:
        """
        Deterministic evaluation of PRODUCT category.

        Factors:
        - Product-Market Fit: Customer traction, adoption signals
        - Innovation: Unique technology or approach
        - Roadmap Clarity: Clear vision for product evolution

        Args:
            findings: Product-related findings.

        Returns:
            List of FactorScore objects.
        """
        factors = []

        # Factor 1: Product-Market Fit
        pmf_score = self._score_product_market_fit(findings)
        factors.append(
            FactorScore(
                factor_name="Product-Market Fit",
                score=pmf_score,
                findings=self._filter_findings_for_factor(findings, ["product-market fit", "traction", "adoption"]),
            )
        )

        # Factor 2: Innovation
        innovation_score = self._score_innovation(findings)
        factors.append(
            FactorScore(
                factor_name="Innovation & Differentiation",
                score=innovation_score,
                findings=self._filter_findings_for_factor(findings, ["innovation", "technology", "unique"]),
            )
        )

        # Factor 3: Roadmap
        roadmap_score = self._score_roadmap(findings)
        factors.append(
            FactorScore(
                factor_name="Roadmap Clarity",
                score=roadmap_score,
                findings=self._filter_findings_for_factor(findings, ["roadmap", "feature", "vision"]),
            )
        )

        return factors

    def _evaluate_financial_factors(self, findings: List[Finding]) -> List[FactorScore]:
        """
        Deterministic evaluation of FINANCIAL category.

        Factors:
        - Revenue & Growth: ARR > $10M (excellent), growth > 100% YoY (excellent)
        - Unit Economics: LTV:CAC ratio > 3 (strong)
        - Profitability Path: Clear path to positive unit economics or EBITDA

        Args:
            findings: Financial-related findings.

        Returns:
            List of FactorScore objects.
        """
        factors = []

        # Factor 1: Revenue & Growth
        revenue_score = self._score_revenue_and_growth(findings)
        factors.append(
            FactorScore(
                factor_name="Revenue & Growth",
                score=revenue_score,
                findings=self._filter_findings_for_factor(findings, ["revenue", "arr", "growth", "mrr"]),
            )
        )

        # Factor 2: Unit Economics
        unit_econ_score = self._score_unit_economics(findings)
        factors.append(
            FactorScore(
                factor_name="Unit Economics",
                score=unit_econ_score,
                findings=self._filter_findings_for_factor(findings, ["ltv", "cac", "payback", "unit economics"]),
            )
        )

        # Factor 3: Profitability Path
        profitability_score = self._score_profitability_path(findings)
        factors.append(
            FactorScore(
                factor_name="Profitability Path",
                score=profitability_score,
                findings=self._filter_findings_for_factor(findings, ["ebitda", "burn", "runway", "profitability"]),
            )
        )

        return factors

    def _evaluate_risk_factors(self, findings: List[Finding]) -> List[FactorScore]:
        """
        Deterministic evaluation of RISK category.

        Factors:
        - Execution Risk: Team stability, tech debt, complexity
        - Market Risk: Market dependency, regulatory risk
        - Operational Risk: Key person dependencies, operational maturity

        Lower scores in RISK category are BETTER (inverse scoring).

        Args:
            findings: Risk-related findings.

        Returns:
            List of FactorScore objects.
        """
        factors = []

        # Factor 1: Execution Risk
        execution_risk_score = self._score_execution_risk(findings)
        factors.append(
            FactorScore(
                factor_name="Execution Risk",
                score=execution_risk_score,
                findings=self._filter_findings_for_factor(findings, ["execution", "risk", "challenge"]),
            )
        )

        # Factor 2: Market Risk
        market_risk_score = self._score_market_risk(findings)
        factors.append(
            FactorScore(
                factor_name="Market Risk",
                score=market_risk_score,
                findings=self._filter_findings_for_factor(findings, ["market risk", "regulatory", "threat"]),
            )
        )

        # Factor 3: Operational Risk
        operational_risk_score = self._score_operational_risk(findings)
        factors.append(
            FactorScore(
                factor_name="Operational Risk",
                score=operational_risk_score,
                findings=self._filter_findings_for_factor(findings, ["operational", "dependency", "key person"]),
            )
        )

        return factors

    # ========================================================================
    # Deterministic Scoring Rules (Pure Logic, No Side Effects)
    # ========================================================================

    def _score_domain_expertise(self, findings: List[Finding]) -> int:
        """Score domain expertise based on findings."""
        if not findings:
            return 30  # Low baseline if no evidence

        keywords = ["founder", "domain", "expertise", "background", "experience"]
        relevant_findings = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if len(relevant_findings) >= 2:
            return 75
        elif len(relevant_findings) == 1:
            return 50
        return 30

    def _score_leadership_experience(self, findings: List[Finding]) -> int:
        """Score leadership experience (exits, prior companies)."""
        keywords = ["exit", "founder", "ceo", "led", "founded", "started"]
        relevant_findings = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        # Look for successful exits
        if any("exit" in f.finding_text.lower() for f in relevant_findings):
            return 85
        elif len(relevant_findings) >= 2:
            return 65
        elif len(relevant_findings) == 1:
            return 45
        return 25

    def _score_team_diversity(self, findings: List[Finding]) -> int:
        """Score team diversity and composition."""
        if not findings:
            return 35

        # More findings = more evidence of diverse team
        num_findings = len(findings)
        if num_findings >= 3:
            return 70
        elif num_findings == 2:
            return 50
        elif num_findings == 1:
            return 35
        return 25

    def _score_market_size(self, findings: List[Finding]) -> int:
        """Score market size based on TAM/revenue figures."""
        # Look for specific numbers
        for finding in findings:
            text = finding.finding_text.lower()
            # Check for billion-dollar markets
            if re.search(r'\$\d+\s*(?:b|billion)', text, re.IGNORECASE):
                return 90
            # Check for hundred-million markets
            if re.search(r'\$\d+\d{1,3}\s*(?:m|million)', text, re.IGNORECASE):
                return 70

        return 40 if findings else 20

    def _score_market_growth(self, findings: List[Finding]) -> int:
        """Score market growth rate."""
        for finding in findings:
            text = finding.finding_text.lower()
            # Check for high growth percentages
            if re.search(r'(?:100|[5-9]\d)%\s*(?:growth|cagr)', text):
                return 85
            if re.search(r'(?:20|[3-4]\d)%\s*(?:growth|cagr)', text):
                return 65
            if re.search(r'\d+%\s*(?:growth|cagr)', text):
                return 45

        return 40 if findings else 20

    def _score_competitive_position(self, findings: List[Finding]) -> int:
        """Score competitive differentiation."""
        keywords = ["competitive", "advantage", "differentiation", "unique", "moat"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if len(relevant) >= 2:
            return 75
        elif len(relevant) == 1:
            return 55
        return 35

    def _score_product_market_fit(self, findings: List[Finding]) -> int:
        """Score product-market fit signals."""
        keywords = ["traction", "adoption", "customers", "pmf", "growth", "retention"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if len(relevant) >= 3:
            return 80
        elif len(relevant) >= 1:
            return 50
        return 30

    def _score_innovation(self, findings: List[Finding]) -> int:
        """Score innovation and differentiation."""
        keywords = ["innovation", "technology", "unique", "proprietary", "patent"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if len(relevant) >= 2:
            return 75
        elif len(relevant) == 1:
            return 50
        return 35

    def _score_roadmap(self, findings: List[Finding]) -> int:
        """Score roadmap clarity."""
        keywords = ["roadmap", "feature", "vision", "plan"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        return 60 if len(relevant) >= 1 else 40

    def _score_revenue_and_growth(self, findings: List[Finding]) -> int:
        """Score revenue and growth metrics."""
        for finding in findings:
            text = finding.finding_text.lower()
            # High revenue
            if re.search(r'\$\d+\s*(?:m|million)', text):
                # Check growth rate
                if re.search(r'100%|growth', text):
                    return 90
                return 75
            # Some revenue
            if re.search(r'\$\d+(?:k|000)', text):
                return 50

        return 30 if findings else 10

    def _score_unit_economics(self, findings: List[Finding]) -> int:
        """Score unit economics quality."""
        keywords = ["ltv", "cac", "payback", "ratio", "unit economics"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if len(relevant) >= 2:
            return 75
        elif len(relevant) == 1:
            return 55
        return 35

    def _score_profitability_path(self, findings: List[Finding]) -> int:
        """Score path to profitability."""
        keywords = ["ebitda", "profitable", "positive", "runway", "burn"]
        relevant = [f for f in findings if any(kw in f.finding_text.lower() for kw in keywords)]

        if any("profitable" in f.finding_text.lower() or "ebitda" in f.finding_text.lower()
               for f in relevant):
            return 80
        elif len(relevant) >= 1:
            return 50
        return 35

    def _score_execution_risk(self, findings: List[Finding]) -> int:
        """Score execution risk (LOWER is BETTER in risk category)."""
        risk_keywords = ["technical debt", "complexity", "dependency", "bottleneck"]
        risks = [f for f in findings if any(kw in f.finding_text.lower() for kw in risk_keywords)]

        # Fewer risks = higher score (100 = no risk)
        if not risks:
            return 85
        elif len(risks) == 1:
            return 60
        else:
            return 40

    def _score_market_risk(self, findings: List[Finding]) -> int:
        """Score market risk (LOWER is BETTER)."""
        risk_keywords = ["regulatory", "compliance", "threat", "market risk"]
        risks = [f for f in findings if any(kw in f.finding_text.lower() for kw in risk_keywords)]

        if not risks:
            return 85
        elif len(risks) == 1:
            return 60
        else:
            return 40

    def _score_operational_risk(self, findings: List[Finding]) -> int:
        """Score operational risk (LOWER is BETTER)."""
        risk_keywords = ["key person", "dependency", "operational", "maturity"]
        risks = [f for f in findings if any(kw in f.finding_text.lower() for kw in risk_keywords)]

        if not risks:
            return 80
        elif len(risks) == 1:
            return 55
        else:
            return 35

    # ========================================================================
    # Aggregation & Recommendation Logic
    # ========================================================================

    def _aggregate_factors(self, factors: List[FactorScore]) -> int:
        """
        Aggregate factor scores to category score.

        Uses weighted average: all factors equally weighted.

        Args:
            factors: List of factor scores.

        Returns:
            Aggregate score (0-100).
        """
        if not factors:
            return 0

        total = sum(f.score for f in factors)
        return int(total / len(factors))

    def _determine_recommendation(
        self, category_scores: List[CategoryScore]
    ) -> RecommendationStatus:
        """
        Determine investment recommendation based on category scores.

        Rules:
        - INVEST: All core categories (TEAM, MARKET, PRODUCT, FINANCIAL) > 75
                  AND risk < 40
        - WATCHLIST: 2+ core categories > 60 AND risk < 60
        - PASS: Otherwise

        Args:
            category_scores: List of category scores.

        Returns:
            RecommendationStatus.
        """
        # Extract scores by category
        scores_by_category = {cs.category: cs.aggregate_score for cs in category_scores}

        core_categories = [ScoreCategory.TEAM, ScoreCategory.MARKET, ScoreCategory.PRODUCT, ScoreCategory.FINANCIAL]
        core_scores = [scores_by_category.get(cat, 0) for cat in core_categories]
        risk_score = scores_by_category.get(ScoreCategory.RISK, 50)

        # INVEST: All core > 75 AND risk < 40
        if all(score > 75 for score in core_scores) and risk_score < 40:
            return RecommendationStatus.INVEST

        # WATCHLIST: 2+ core > 60 AND risk < 60
        strong_core_count = sum(1 for score in core_scores if score > 60)
        if strong_core_count >= 2 and risk_score < 60:
            return RecommendationStatus.WATCHLIST

        # PASS: Otherwise
        return RecommendationStatus.PASS

    def _generate_reasoning(
        self, category_scores: List[CategoryScore], status: RecommendationStatus
    ) -> str:
        """
        Generate executive summary reasoning for the recommendation.

        Args:
            category_scores: Detailed category scores.
            status: Final recommendation status.

        Returns:
            Human-readable reasoning string.
        """
        scores_by_category = {cs.category: cs.aggregate_score for cs in category_scores}

        strengths = []
        weaknesses = []

        for cat in ScoreCategory:
            score = scores_by_category.get(cat, 0)
            if cat == ScoreCategory.RISK:
                # Inverse scoring for risk
                if score < 40:
                    strengths.append(f"Low risk profile ({score})")
                elif score > 60:
                    weaknesses.append(f"Elevated risk ({score})")
            else:
                if score > 75:
                    strengths.append(f"Strong {cat.value} ({score})")
                elif score < 50:
                    weaknesses.append(f"Weak {cat.value} ({score})")

        reasoning_parts = [
            f"Recommendation: {status.value.upper()}."
        ]

        if strengths:
            reasoning_parts.append(f"Strengths: {', '.join(strengths)}.")
        if weaknesses:
            reasoning_parts.append(f"Concerns: {', '.join(weaknesses)}.")

        reasoning_parts.append(
            "See detailed category scores and factor analysis for complete evaluation."
        )

        return " ".join(reasoning_parts)

    def _filter_findings_for_factor(
        self, findings: List[Finding], keywords: List[str]
    ) -> List[Finding]:
        """
        Filter findings by keywords.

        If no findings match keywords, returns all findings as fallback to prevent
        empty factors when LLM output doesn't use exact keyword terminology.

        Args:
            findings: List of findings.
            keywords: Keywords to match (case-insensitive).

        Returns:
            Filtered findings, or all findings if none match keywords.
        """
        filtered = [
            f for f in findings
            if any(kw.lower() in f.finding_text.lower() for kw in keywords)
        ]
        logger.debug(
            f"  Filtering {len(findings)} findings by keywords {keywords}: "
            f"kept {len(filtered)}"
        )
        if findings and not filtered:
            logger.debug(f"    No findings matched keywords, using all {len(findings)} as fallback")
            return findings
        return filtered
