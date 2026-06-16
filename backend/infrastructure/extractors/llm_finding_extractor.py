"""
VentureMind AI — LLM-Based Finding Extractor
Extracts quantifiable facts and definitive statements from ingested data.

Implements IFindingExtractor using semantic search + LLM-based fact extraction
with strict hallucination prevention via chunk ID validation.
"""

import json
import logging
from typing import Dict, List

from openai import AsyncOpenAI

from backend.core.settings import settings
from backend.domain.interfaces import IFindingExtractor, IRetrievalService
from backend.domain.schemas import Finding, RetrievedChunk, ScoreCategory

logger = logging.getLogger(__name__)


class LlmFindingExtractor(IFindingExtractor):
    """
    Production-ready LLM-based finding extractor for investment scoring.

    Workflow:
    1. Map ScoreCategory to semantic query
    2. Retrieve relevant context from Qdrant
    3. Extract structured findings via LLM (JSON-mode)
    4. Validate chunk IDs to prevent hallucination
    5. Return Finding objects with full traceability

    Features:
    - Category-specific search queries
    - JSON-mode LLM output for deterministic parsing
    - Strict hallucination prevention (chunk ID validation)
    - Comprehensive error handling and logging
    - Full traceability (finding_text + supporting_chunk_ids)
    """

    # Category-to-query mapping for semantic search
    CATEGORY_QUERIES: Dict[ScoreCategory, str] = {
        ScoreCategory.TEAM: (
            "Founders, founding team, team background, prior exits, domain expertise, "
            "technical skills, business experience, leadership history, education background"
        ),
        ScoreCategory.MARKET: (
            "Market size, total addressable market (TAM), market growth, competitive landscape, "
            "market trends, customer segments, market opportunity, market adoption, market dynamics"
        ),
        ScoreCategory.PRODUCT: (
            "Product features, product roadmap, technology, differentiation, innovation, "
            "product strategy, product-market fit, competitive advantage, unique value proposition"
        ),
        ScoreCategory.FINANCIAL: (
            "Revenue, ARR (Annual Recurring Revenue), growth rate, profitability, burn rate, "
            "funding rounds, valuation, unit economics, customer acquisition cost (CAC), "
            "lifetime value (LTV), cash runway"
        ),
        ScoreCategory.RISK: (
            "Risks, challenges, dependencies, threats, market risks, technical risks, "
            "regulatory risks, competitive threats, execution risks, cash flow risks, "
            "team retention risks, litigation, compliance issues"
        ),
    }

    def __init__(
        self,
        retrieval_service: IRetrievalService,
    ):
        """
        Initialize the LLM finding extractor.

        Args:
            retrieval_service: IRetrievalService instance for semantic search.
        """
        self.retrieval_service = retrieval_service
        self.llm_client = AsyncOpenAI(
            api_key=settings.hf_router_api_key,
            base_url=settings.hf_router_base_url,
        )
        # self.llm_model = settings.llm_model_name
        self.llm_model ="meta-llama/Llama-3.1-8B-Instruct:novita"
        logger.info("✓ LLM finding extractor initialized")

    async def extract_findings(
        self, deal_id: str, category: ScoreCategory
    ) -> List[Finding]:
        """
        Extract findings from ingested data for a specific evaluation category.

        Orchestrates the complete extraction pipeline:
        1. Map category to semantic query
        2. Retrieve relevant context chunks
        3. Extract facts via LLM (JSON-mode)
        4. Validate chunk IDs and construct Finding objects
        5. Return with full traceability

        Args:
            deal_id: The deal/startup ID for strict isolation.
            category: The scoring category to extract findings for.

        Returns:
            List[Finding]: Extracted findings with supporting chunk IDs.

        Raises:
            RuntimeError: If extraction fails critically.
        """
        logger.info(
            f"[FindingExtractor] Extracting findings: "
            f"deal_id={deal_id} category={category.value}"
        )

        try:
            # ================================================================
            # Step 1: Map Category to Semantic Query
            # ================================================================
            query = self.CATEGORY_QUERIES[category]
            logger.debug(f"  Query: {query}")

            # ================================================================
            # Step 2: Retrieve Relevant Context
            # ================================================================
            logger.debug("  Retrieving context from Qdrant...")
            retrieval_response = await self.retrieval_service.search(
                query=query,
                deal_id=deal_id,
                top_k=10,  # Get more chunks for comprehensive finding extraction
            )

            retrieved_chunks = retrieval_response.results
            logger.info(f"  ✓ Retrieved {len(retrieved_chunks)} context chunks")

            if not retrieved_chunks:
                logger.warning(f"  ⚠ No context found for category {category.value}")
                return []

            # Build lookup of available chunk IDs for validation
            available_chunk_ids = {chunk.chunk_id for chunk in retrieved_chunks}

            # ================================================================
            # Step 3: Extract Facts via LLM (JSON-mode)
            # ================================================================
            logger.debug("  Calling LLM for fact extraction...")
            findings_data = await self._extract_with_llm(
                category, retrieved_chunks
            )

            if not findings_data:
                logger.warning(f"  ⚠ LLM returned no findings for {category.value}")
                return []

            # ================================================================
            # Step 4: Validate & Construct Finding Objects
            # ================================================================
            logger.debug(f"  Validating {len(findings_data)} extracted findings...")
            findings: List[Finding] = []

            for finding_dict in findings_data:
                try:
                    finding_text = finding_dict.get("finding_text", "").strip()
                    chunk_ids = finding_dict.get("supporting_chunk_ids", [])

                    # Skip empty findings
                    if not finding_text:
                        logger.debug("    Skipping empty finding_text")
                        continue

                    # Validate chunk IDs (strict hallucination prevention)
                    valid_chunk_ids = [
                        cid for cid in chunk_ids if cid in available_chunk_ids
                    ]

                    if not valid_chunk_ids:
                        logger.warning(
                            f"    ⚠ Finding has no valid chunk IDs: {finding_text[:60]}..."
                        )
                        continue

                    if len(valid_chunk_ids) < len(chunk_ids):
                        logger.debug(
                            f"    Some chunk IDs were hallucinated. "
                            f"Valid: {valid_chunk_ids}"
                        )

                    # Create Finding object
                    finding = Finding(
                        finding_text=finding_text,
                        supporting_chunk_ids=valid_chunk_ids,
                    )
                    findings.append(finding)
                    logger.debug(
                        f"    Added finding: {finding_text[:60]}... "
                        f"(chunks: {len(valid_chunk_ids)})"
                    )

                except Exception as e:
                    logger.warning(f"    Failed to process finding: {e}")
                    continue

            logger.info(
                f"  ✓ Extracted {len(findings)} validated findings "
                f"for category {category.value}"
            )
            if findings:
                logger.info(f"  Example finding: {findings[0]}")
            return findings

        except Exception as e:
            logger.error(
                f"  ✗ Finding extraction failed ({type(e).__name__}): {e}",
                exc_info=True,
            )
            raise RuntimeError(f"Finding extraction failed for {category.value}: {e}") from e

    async def _extract_with_llm(
        self, category: ScoreCategory, chunks: List[RetrievedChunk]
    ) -> List[Dict]:
        """
        Call LLM to extract findings from context chunks.

        Uses JSON-mode for deterministic parsing. LLM is instructed to extract
        purely quantifiable facts or definitive statements, avoiding speculation.

        Args:
            category: The scoring category.
            chunks: Retrieved context chunks.

        Returns:
            List of dictionaries with 'finding_text' and 'supporting_chunk_ids'.

        Raises:
            RuntimeError: If LLM call or parsing fails.
        """
        try:
            # Build context string from chunks
            context = self._build_context_string(chunks)

            # Construct system prompt
            system_prompt = (
                "You are a meticulous data extraction specialist. "
                "Extract ONLY quantifiable facts, metrics, and definitive statements "
                "from the provided context. Do NOT speculate or infer. "
                "Do NOT include opinions, estimates, or unclear claims. "
                "\n\n"
                "Return a JSON array of findings. Each finding must have:\n"
                '- "finding_text": A clear, factual statement (max 200 chars)\n'
                '- "supporting_chunk_ids": Array of chunk IDs from the context that support this finding\n'
                "\nExample:\n"
                '[\n'
                '  {\n'
                '    "finding_text": "Company achieved $5M ARR in Q2 2024",\n'
                '    "supporting_chunk_ids": ["chunk_123", "chunk_456"]\n'
                '  }\n'
                ']\n'
                "\nIf you cannot extract any facts, return an empty array []."
            )

            user_prompt = (
                f"Category: {category.value.upper()}\n\n"
                f"Extract factual findings from this context:\n\n{context}"
            )

            logger.debug(f"LLM Input:\nSystem: {system_prompt[:200]}...\nUser: {user_prompt[:200]}...")

            # Call LLM with JSON-mode
            response = await self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.0,  # Deterministic extraction
                max_tokens=4096,
            )

            response_text = response.choices[0].message.content
            logger.info(f"LLM Raw Response: {response_text[:500]}")

            # Parse JSON response
            try:
                findings_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"  ✗ Failed to parse LLM JSON response: {e}")
                raise RuntimeError(f"Invalid JSON from LLM: {e}") from e

            logger.info(f"  ✓ Parsed findings_data type={type(findings_data).__name__}, count={len(findings_data) if isinstance(findings_data, (list, dict)) else 'N/A'}")

            # Ensure it's a list, handling dict responses gracefully
            if isinstance(findings_data, dict):
                # Check for common keys that might contain the list
                for key in ["findings", "results", "data"]:
                    if key in findings_data and isinstance(findings_data[key], list):
                        logger.debug(f"  Extracted findings from dict key '{key}'")
                        findings_data = findings_data[key]
                        break
                else:
                    # No list-containing key found, wrap the dict in a list
                    logger.debug("  Wrapping dict response in a list")
                    findings_data = [findings_data]
            elif not isinstance(findings_data, list):
                logger.error(f"  ✗ LLM response is neither list nor dict: {type(findings_data)}")
                raise RuntimeError(f"LLM response must be a JSON array or object, got {type(findings_data).__name__}")

            return findings_data

        except Exception as e:
            logger.error(f"  ✗ LLM extraction failed: {e}", exc_info=True)
            raise

    def _build_context_string(self, chunks: List[RetrievedChunk]) -> str:
        """
        Build a formatted context string from retrieved chunks.

        Each chunk is numbered and includes its ID for reference.

        Args:
            chunks: List of retrieved chunks.

        Returns:
            Formatted context string for LLM.
        """
        context_parts = []

        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Chunk {i} ID: {chunk.chunk_id}]\n"
                f"{chunk.text}\n"
            )

        return "\n---\n\n".join(context_parts)
