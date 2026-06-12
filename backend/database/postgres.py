"""PostgreSQL database connection and session management.

Person 5 owns this module.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.config import get_settings

settings = get_settings()

# Database URL
DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    from backend.database.models import Base

    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables."""
    from backend.database.models import Base

    Base.metadata.drop_all(bind=engine)
