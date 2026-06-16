"""
VentureMind AI — Website Ingestion Service
Orchestrates the complete website crawl -> classify -> chunk -> embed -> store pipeline.

Implements clean separation of concerns through dependency injection of crawlers,
classifiers, embeddings, and repositories. No direct API calls to external services.
"""

import asyncio
import logging
import re
import uuid
from typing import List, Protocol

from pydantic import BaseModel, Field
from qdrant_client import AsyncQdrantClient

from backend.domain.interfaces import IPageClassifier, IWebCrawler
from backend.domain.schemas import CrawledPage, Evidence, Source
from backend.infrastructure.embeddings.provider import get_embedding_provider
from backend.infrastructure.vectorstore.qdrant_client import (
    ensure_collections_exist,
    get_async_qdrant_client,
)

logger = logging.getLogger(__name__)


class SourceRepository(Protocol):
    """Protocol for Source persistence operations."""

    async def save(self, source: Source) -> None: ...


class EvidenceRepository(Protocol):
    """Protocol for Evidence persistence operations."""

    async def save(self, evidence: Evidence) -> None: ...


class WebsiteIngestionResult(BaseModel):
    """Result of website ingestion containing traceability and statistics."""

    source_id: str = Field(..., description="Unique identifier of the source")
    total_chunks_created: int = Field(
        ..., description="Total number of chunks created from the website"
    )
    total_pages_crawled: int = Field(..., description="Total number of pages crawled")


class WebsiteIngestionService:
    """
    Orchestrates the complete website ingestion pipeline.

    Pipeline flow:
    1. Create Source entity for traceability
    2. Crawl website (Firecrawl or BeautifulSoup)
    3. Concurrently classify all pages (LLM)
    4. Chunk classified pages semantically
    5. Vectorize context-enriched chunks
    6. Upsert to Qdrant
    7. Create Evidence entities linked to Source

    Features:
    - Dependency injection of crawler, classifier, embeddings, repositories
    - Concurrent classification with asyncio.gather
    - Semantic chunking by headers and character limit
    - Context-enriched chunk vectors (URL, category, title)
    - Graceful error handling with transaction-like rollback logging
    - Production-ready logging at each step
    """

    def __init__(
        self,
        crawler: IWebCrawler,
        classifier: IPageClassifier,
        source_repo: SourceRepository,
        evidence_repo: EvidenceRepository,
    ):
        """
        Initialize the website ingestion service with dependency injection.

        Args:
            crawler: IWebCrawler implementation (e.g., FirecrawlWebCrawler)
            classifier: IPageClassifier implementation (e.g., LlmPageClassifier)
            source_repo: Repository for persisting Source entities
            evidence_repo: Repository for persisting Evidence entities
        """
        self.crawler = crawler
        self.classifier = classifier
        self.source_repo = source_repo
        self.evidence_repo = evidence_repo
        self.embedding_provider = get_embedding_provider()
        self.qdrant_client: AsyncQdrantClient = get_async_qdrant_client()
        self.semaphore = asyncio.Semaphore(5)

    async def initialize(self) -> None:
        """Ensure vector store collections are provisioned before ingestion."""
        await ensure_collections_exist()

    def _split_by_headers(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """
        Split Markdown text into semantic chunks by headers and character limit.

        Strategy:
        1. Split by Markdown headers (# , ## , ### , etc.)
        2. For each section, further split by character limit if needed
        3. Preserve header context for each chunk

        Args:
            text: The Markdown text to chunk
            max_chunk_size: Target chunk size in characters

        Returns:
            List of semantic chunks
        """
        chunks: List[str] = []
        header_pattern = r"^(#{1,6}\s+.+)$"
        lines = text.split("\n")

        current_chunk = []
        current_header = ""

        for line in lines:
            if re.match(header_pattern, line):
                if current_chunk:
                    chunk_text = "\n".join(current_chunk).strip()
                    if chunk_text:
                        if current_header:
                            chunk_text = f"{current_header}\n\n{chunk_text}"
                        chunks.append(chunk_text)
                    current_chunk = []

                current_header = line
            else:
                current_chunk.append(line)
                chunk_text = "\n".join(current_chunk).strip()
                if len(chunk_text) > max_chunk_size:
                    if current_header:
                        chunk_text = f"{current_header}\n\n{chunk_text}"
                    chunks.append(chunk_text)
                    current_chunk = []

        if current_chunk:
            chunk_text = "\n".join(current_chunk).strip()
            if chunk_text:
                if current_header:
                    chunk_text = f"{current_header}\n\n{chunk_text}"
                chunks.append(chunk_text)

        return chunks if chunks else [text] if text else []

    async def _classify_page_safely(self, page: CrawledPage) -> CrawledPage:
        """
        Classify a single page with concurrency control via semaphore.

        Args:
            page: The CrawledPage to classify

        Returns:
            The same page object with updated category
        """
        async with self.semaphore:
            category = await self.classifier.classify_page(page.text)
            page.category = category
            return page

    async def ingest_website(
        self, base_url: str, deal_id: str
    ) -> WebsiteIngestionResult:
        """
        Execute the complete website ingestion pipeline.

        Flow:
        1. Create Source entity for traceability
        2. Crawl website
        3. Concurrently classify pages
        4. Chunk classified pages semantically
        5. Vectorize context-enriched chunks
        6. Upsert to Qdrant
        7. Create Evidence entities

        Args:
            base_url: The website URL to crawl
            deal_id: The deal/startup ID for association

        Returns:
            WebsiteIngestionResult with source_id and total_chunks_created

        Raises:
            RuntimeError: If critical pipeline steps fail
        """
        logger.info("=" * 80)
        logger.info("Starting website ingestion pipeline for: %s", base_url)
        logger.info("=" * 80)

        source_id = str(uuid.uuid4())

        try:
            # ================================================================
            # Step 1: Traceability (Source Creation)
            # ================================================================
            logger.info("\n[Step 1] Creating Source entity for traceability...")
            source = Source(
                id=source_id,
                document_type="website",
                file_path=base_url,
                startup_id=deal_id,
            )
            await self.source_repo.save(source)
            logger.info(f"  ✓ Source created: {source_id}")

            # ================================================================
            # Step 2: Crawl Website
            # ================================================================
            logger.info("\n[Step 2] Crawling website...")
            await self.initialize()
            crawled_pages = await self.crawler.crawl_website(base_url)
            logger.info(f"  ✓ Crawled {len(crawled_pages)} pages")

            if not crawled_pages:
                logger.error("  ✗ No pages crawled from website")
                raise RuntimeError(f"Failed to crawl website: {base_url}")

            # ================================================================
            # Step 3: Concurrent Classification
            # ================================================================
            logger.info("\n[Step 3] Classifying pages concurrently...")
            classification_tasks = [
                self._classify_page_safely(page) for page in crawled_pages
            ]
            classified_pages = await asyncio.gather(*classification_tasks)
            logger.info(f"  ✓ Classified {len(classified_pages)} pages")

            category_counts = {}
            for page in classified_pages:
                cat = page.category.value
                category_counts[cat] = category_counts.get(cat, 0) + 1
            for cat, count in sorted(category_counts.items()):
                logger.debug(f"    {cat}: {count}")

            # ================================================================
            # Step 4: Semantic Chunking
            # ================================================================
            logger.info("\n[Step 4] Chunking classified pages...")
            chunks_data: List[tuple[str, str, str, str, str, str]] = []

            for page in classified_pages:
                semantic_chunks = self._split_by_headers(page.text)
                for chunk_text in semantic_chunks:
                    context_header = (
                        f"Source: {page.url} | "
                        f"Category: {page.category.value} | "
                        f"Title: {page.title or 'Untitled'}"
                    )
                    enriched_chunk = f"{context_header}\n\n{chunk_text}"
                    chunks_data.append(
                        (
                            page.url,
                            page.category.value,
                            page.title or "Untitled",
                            chunk_text,
                            context_header,
                            enriched_chunk,
                        )
                    )

            logger.info(f"  ✓ Created {len(chunks_data)} semantic chunks")

            # ================================================================
            # Step 5: Vectorization & Storage
            # ================================================================
            logger.info("\n[Step 5] Vectorizing and upserting chunks to Qdrant...")
            points = []

            for url, category, title, chunk_text, context_header, enriched_chunk in chunks_data:
                try:
                    vector = self.embedding_provider.embed(enriched_chunk)
                    point_id = f"website_{deal_id}_{uuid.uuid4().hex[:12]}"
                    points.append(
                        {
                            "id": point_id,
                            "vector": vector,
                            "payload": {
                                "source_id": source_id,
                                "startup_id": deal_id,
                                "document_id": base_url,
                                "url": url,
                                "category": category,
                                "title": title,
                                "text": chunk_text,
                                "context": context_header,
                            },
                        }
                    )
                except Exception as e:
                    logger.warning(f"Failed to vectorize chunk from {url}: {e}")
                    continue

            if points:
                await self.qdrant_client.upsert(
                    collection_name="startup_website_chunks", points=points
                )
                logger.info(f"  ✓ Upserted {len(points)} vectors to Qdrant")
            else:
                logger.warning("  ⚠ No vectors to upsert (all chunks failed)")

            # ================================================================
            # Step 6: Traceability (Evidence Creation)
            # ================================================================
            logger.info("\n[Step 6] Creating Evidence entities for traceability...")
            evidence_count = 0

            for url, category, title, chunk_text, context_header, _ in chunks_data:
                try:
                    evidence = Evidence(
                        id=str(uuid.uuid4()),
                        source_id=source_id,
                        content=chunk_text,
                        page_number=None,
                        metadata={
                            "url": url,
                            "category": category,
                            "title": title,
                            "context": context_header,
                        },
                    )
                    await self.evidence_repo.save(evidence)
                    evidence_count += 1
                except Exception as e:
                    logger.warning(f"Failed to save evidence for chunk from {url}: {e}")
                    continue

            logger.info(f"  ✓ Created {evidence_count} Evidence entities")

            # ================================================================
            # Summary
            # ================================================================
            result = WebsiteIngestionResult(
                source_id=source_id,
                total_chunks_created=len(points),
                total_pages_crawled=len(crawled_pages),
            )

            logger.info("\n" + "=" * 80)
            logger.info("✓ Website ingestion pipeline completed successfully")
            logger.info(f"  Source ID: {result.source_id}")
            logger.info(f"  Pages crawled: {result.total_pages_crawled}")
            logger.info(f"  Chunks created: {result.total_chunks_created}")
            logger.info("=" * 80)

            return result

        except Exception as e:
            logger.error(
                f"✗ Website ingestion pipeline failed at critical step: {type(e).__name__}: {e}",
                exc_info=True,
            )
            raise RuntimeError(f"Website ingestion failed for {base_url}: {e}") from e
