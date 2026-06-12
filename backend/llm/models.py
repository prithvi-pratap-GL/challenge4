"""LLM model configurations and prompts."""

from enum import Enum


class ModelProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    AZURE = "azure"
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"
    LOCAL = "local"


class LLMModel(str, Enum):
    """Available LLM models."""

    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_35_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    MISTRAL = "mistral"
    LLAMA2 = "llama2"


class TemperatureSetting(float, Enum):
    """Standard temperature presets."""

    PRECISE = 0.1  # For factual, deterministic outputs
    BALANCED = 0.7  # Default balanced setting
    CREATIVE = 1.2  # For creative, diverse outputs
    VERY_CREATIVE = 1.5  # Maximum creativity
