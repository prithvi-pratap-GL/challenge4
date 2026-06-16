"""
VentureMind — PostgreSQL SQLAlchemy Model Extensions II
Incremental additions to orm.py / orm_extensions.py. ORM definitions only.

New tables:
  - recommendations          (backs RecommendationRepository)
  - benchmark_distributions   (backs BenchmarkRepository.get_distribution /
                                get_percentile_data — domain_extensions_ii.BenchmarkDistribution)

Also documents required relationship additions to DealORM (orm.py).
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    ARRAY,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .orm import Base, DealORM


# ---------------------------------------------------------------------------
# Investment Recommendations
# ---------------------------------------------------------------------------


class RecommendationORM(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    deal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("deals.id", ondelete="CASCADE"), nullable=False
    )
    report_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    verdict: Mapped[str] = mapped_column(String(20), nullable=False)  # invest | watchlist | pass
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    composite_score: Mapped[float] = mapped_column(Float, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    drivers: Mapped[dict] = mapped_column(JSONB, nullable=False)            # list[RecommendationDriver]
    conditions: Mapped[dict] = mapped_column(JSONB, nullable=False)          # RecommendationConditions
    score_factor_refs: Mapped[Optional[list]] = mapped_column(ARRAY(String(150)))
    finding_ids: Mapped[Optional[list]] = mapped_column(ARRAY(UUID(as_uuid=True)))
    risk_flag_ids: Mapped[Optional[list]] = mapped_column(ARRAY(UUID(as_uuid=True)))
    highest_severity_risk: Mapped[Optional[str]] = mapped_column(String(20))
    sections_most_influential: Mapped[Optional[list]] = mapped_column(ARRAY(String(50)))
    generated_by: Mapped[str] = mapped_column(String(100), nullable=False, default="recommendation_engine_v1")
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("deal_id", "report_version", name="uq_recommendation_deal_report_version"),
    )

    deal: Mapped[DealORM] = relationship("DealORM", back_populates="recommendations")


# ---------------------------------------------------------------------------
# Benchmark Distributions
# ---------------------------------------------------------------------------


class BenchmarkDistributionORM(Base):
    __tablename__ = "benchmark_distributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)            # BenchmarkMetricUnit

    # Segmentation (BenchmarkSegment)
    vertical: Mapped[str] = mapped_column(String(50), nullable=False)
    stage: Mapped[str] = mapped_column(String(50), nullable=False)
    geography: Mapped[str] = mapped_column(String(100), nullable=False, default="global")

    source_report: Mapped[str] = mapped_column(String(255), nullable=False)
    source_year: Mapped[int] = mapped_column(Integer, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)

    # Anchors (BenchmarkAnchors)
    p25: Mapped[Optional[float]] = mapped_column(Float)
    p50: Mapped[Optional[float]] = mapped_column(Float)
    p75: Mapped[Optional[float]] = mapped_column(Float)
    p90: Mapped[Optional[float]] = mapped_column(Float)

    mean: Mapped[Optional[float]] = mapped_column(Float)
    stddev: Mapped[Optional[float]] = mapped_column(Float)
    raw_values: Mapped[Optional[list]] = mapped_column(ARRAY(Float))

    as_of: Mapped[date] = mapped_column(Date, nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "metric_name", "vertical", "stage", "geography", "source_report", "source_year",
            name="uq_benchmark_distribution_segment_source",
        ),
    )


# ---------------------------------------------------------------------------
# Required relationship addition to DealORM (orm.py)
# ---------------------------------------------------------------------------
#
#   recommendations: Mapped[list["RecommendationORM"]] = relationship(
#       "RecommendationORM", back_populates="deal", cascade="all, delete-orphan")