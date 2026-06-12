from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Environment configuration for VentureMind AI backend."""

    # LLM Configuration
    MODEL_NAME: str = "gpt-4o-mini"
    BASE_URL: Optional[str] = None
    API_KEY: str
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 4096

    # Qdrant Configuration
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # PostgreSQL Configuration
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "venturemind_ai"

    # External APIs
    TAVILY_API_KEY: str
    CRUNCHBASE_API_KEY: Optional[str] = None
    LINKEDIN_API_KEY: Optional[str] = None

    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings from environment variables."""
    return Settings()
