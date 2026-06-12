"""Analysis repository for database access.

Person 5 owns this module.
"""

from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from backend.database.models import AnalysisRecord


class AnalysisRepository:
    """Repository for analysis records."""

    def __init__(self, db: Session):
        """Initialize repository."""
        self.db = db

    def create(
        self,
        startup_name: str,
        website_url: Optional[str] = None,
        pitch_deck_path: Optional[str] = None,
    ) -> AnalysisRecord:
        """Create new analysis record."""
        record = AnalysisRecord(
            startup_name=startup_name,
            website_url=website_url,
            pitch_deck_path=pitch_deck_path,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, analysis_id: UUID) -> Optional[AnalysisRecord]:
        """Get analysis by ID."""
        return self.db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()

    def update_status(self, analysis_id: UUID, status: str, current_agent: str = None, progress: int = None):
        """Update analysis status."""
        record = self.get_by_id(analysis_id)
        if record:
            record.status = status
            if current_agent:
                record.current_agent = current_agent
            if progress is not None:
                record.progress_percent = progress
            self.db.commit()
            self.db.refresh(record)
        return record

    def update_output(
        self,
        analysis_id: UUID,
        output_type: str,
        output_data: dict,
    ):
        """Update specific output in analysis."""
        record = self.get_by_id(analysis_id)
        if record:
            if output_type == "research":
                record.research_output = output_data
            elif output_type == "knowledge":
                record.knowledge_output = output_data
            elif output_type == "bull":
                record.bull_output = output_data
            elif output_type == "bear":
                record.bear_output = output_data
            elif output_type == "review":
                record.review_output = output_data
            elif output_type == "red_team":
                record.red_team_output = output_data
            elif output_type == "committee":
                record.committee_decision = output_data
            elif output_type == "simulation":
                record.simulation_output = output_data
            elif output_type == "final_report":
                record.final_report = output_data

            self.db.commit()
            self.db.refresh(record)
        return record

    def mark_completed(self, analysis_id: UUID, final_report: dict):
        """Mark analysis as completed."""
        record = self.get_by_id(analysis_id)
        if record:
            record.status = "completed"
            record.final_report = final_report
            record.progress_percent = 100
            self.db.commit()
            self.db.refresh(record)
        return record

    def mark_failed(self, analysis_id: UUID, error_message: str):
        """Mark analysis as failed."""
        record = self.get_by_id(analysis_id)
        if record:
            record.status = "failed"
            record.error_message = error_message
            self.db.commit()
            self.db.refresh(record)
        return record
