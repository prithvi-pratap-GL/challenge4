"""Application settings from environment variables."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # LLM Configuration
    API_KEY: str = ""
    MODEL_NAME: str = "gpt-4o-mini"
    BASE_URL: str = "https://api.openai.com/v1"
    LLM_TEMPERATURE: float = 0.7

    # Database Configuration
    DATABASE_URL: str = "postgresql://localhost/venturemind"

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = False

    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Environment
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
