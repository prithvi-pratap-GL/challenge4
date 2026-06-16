import os
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings loaded from environment variables.
    Uses Pydantic BaseSettings for validation and type coercion.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Embedding Configuration
    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        description="The sentence-transformers model to use for embeddings.",
    )
    embedding_device: str = Field(
        default="cpu",
        description="Device to run the embedding model on ('cpu' or 'cuda').",
    )

    # Vector Store Configuration
    qdrant_url: str = Field(
        ...,
        description="The URL of the Qdrant vector database server.",
    )
    qdrant_api_key: str | None = Field(
        default=None,
        description="API key for Qdrant authentication (optional).",
    )

    # Vision / LLM Configuration
    hf_router_api_key: str = Field(
        ...,
        description="API key for the Hugging Face Router.",
    )
    hf_router_base_url: str = Field(
        default="https://router.huggingface.co/v1",
        description="Base URL for the Hugging Face Router API.",
    )

    # Groq Configuration
    groq_api_key: str = Field(
        ...,
        description="API key for Groq.",
    )
    groq_base_url: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Base URL for Groq API.",
    )

    vision_model: str = Field(
        default="meta-llama/llama-4-scout-17b-16e-instruct",
        description="The vision-language model to use for PDF page analysis (via Groq).",
    )
    llm_model_name: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.2",
        description="The LLM model to use for page classification and general tasks.",
    )

    # Web Crawling Configuration
    firecrawl_api_key: str = Field(
        ...,
        description="API key for the Firecrawl web crawling service.",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    This ensures environment variables are only read once per application lifecycle.
    """
    return Settings()


# Export a singleton instance for easy importing
settings = get_settings()