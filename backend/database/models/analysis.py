"""Analysis record model.

Person 5 owns this module.
Stores analysis execution records in PostgreSQL.
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import json

from backend.database.models import Base


class AnalysisRecord(Base):
    """Stores analysis execution record."""

    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    startup_name = Column(String(255), nullable=False, index=True)
    website_url = Column(String(2048), nullable=True)
    pitch_deck_path = Column(String(2048), nullable=True)
    status = Column(String(50), nullable=False, default="pending", index=True)
    current_agent = Column(String(100), nullable=True)
    progress_percent = Column(Integer, default=0)

    # Store intermediate outputs
    research_output = Column(JSON, nullable=True)
    knowledge_output = Column(JSON, nullable=True)
    bull_output = Column(JSON, nullable=True)
    bear_output = Column(JSON, nullable=True)
    review_output = Column(JSON, nullable=True)
    red_team_output = Column(JSON, nullable=True)
    committee_decision = Column(JSON, nullable=True)
    simulation_output = Column(JSON, nullable=True)
    final_report = Column(JSON, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String(2048), nullable=True)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "startup_name": self.startup_name,
            "website_url": self.website_url,
            "status": self.status,
            "current_agent": self.current_agent,
            "progress": self.progress_percent,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
