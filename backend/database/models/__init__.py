"""Database models.

Person 5 owns this module.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()


# Import all models here
from .analysis import AnalysisRecord

__all__ = ["Base", "AnalysisRecord"]
