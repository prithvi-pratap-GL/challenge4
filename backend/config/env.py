"""Environment variable management."""

import os
from backend.config.settings import settings


def load_env() -> dict:
    """Load and validate environment variables."""
    return {
        'api_key': settings.API_KEY,
        'model_name': settings.MODEL_NAME,
        'base_url': settings.BASE_URL,
        'llm_temperature': settings.LLM_TEMPERATURE,
        'database_url': settings.DATABASE_URL,
        'api_host': settings.API_HOST,
        'api_port': settings.API_PORT,
        'api_debug': settings.API_DEBUG,
        'log_level': settings.LOG_LEVEL,
        'environment': settings.ENVIRONMENT,
    }


def get_llm_config() -> dict:
    """Get LLM configuration."""
    return {
        'api_key': settings.API_KEY,
        'model_name': settings.MODEL_NAME,
        'base_url': settings.BASE_URL,
        'temperature': settings.LLM_TEMPERATURE,
    }


def get_database_url() -> str:
    """Get database connection URL."""
    return settings.DATABASE_URL


def get_api_config() -> dict:
    """Get API configuration."""
    return {
        'host': settings.API_HOST,
        'port': settings.API_PORT,
        'debug': settings.API_DEBUG,
    }
