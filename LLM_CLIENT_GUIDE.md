# LLM Client & Configuration Guide

## Overview

The LLM Client is an OpenAI-compatible wrapper that supports multiple LLM providers. All configuration is managed through environment variables, making it flexible for different deployment scenarios.

## Architecture

### Components

1. **`backend/config/settings.py`** - Environment configuration management using Pydantic
2. **`backend/llm/client.py`** - OpenAI-compatible LLM wrapper
3. **`backend/contracts/schemas.py`** - Shared data contracts for all modules

## Configuration

### Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update with your credentials:
   ```
   MODEL_NAME=gpt-4o-mini
   BASE_URL=https://api.openai.com/v1
   API_KEY=your_api_key_here
   TEMPERATURE=0.7
   ```

### Supported Providers

#### OpenAI
```env
MODEL_NAME=gpt-4o-mini
BASE_URL=https://api.openai.com/v1
API_KEY=sk-...
```

#### Azure OpenAI
```env
MODEL_NAME=gpt-4
BASE_URL=https://your-resource.openai.azure.com/
API_KEY=your_azure_key
```

#### OpenRouter
```env
MODEL_NAME=openai/gpt-4
BASE_URL=https://openrouter.ai/api/v1
API_KEY=sk-...
```

#### Ollama (Local)
```env
MODEL_NAME=mistral
BASE_URL=http://localhost:11434/v1
API_KEY=not-needed
```

## Usage

### Basic Text Generation

```python
from backend.llm import get_llm_client

client = get_llm_client()

response = client.generate(
    system_prompt="You are a VC analyst evaluating startups.",
    user_prompt="What are the key metrics for evaluating a SaaS startup?"
)
print(response)
```

### Structured Output (JSON Schema)

```python
from pydantic import BaseModel
from backend.llm import get_llm_client

class InvestmentAnalysis(BaseModel):
    verdict: str
    confidence: int
    reasoning: str

client = get_llm_client()

response = client.generate(
    system_prompt="You are a VC analyst.",
    user_prompt="Should we invest in this startup?",
    response_model=InvestmentAnalysis
)

# response is an InvestmentAnalysis instance
print(f"Verdict: {response.verdict}")
print(f"Confidence: {response.confidence}%")
```

### Custom Temperature

```python
client = get_llm_client()

# More creative response
creative = client.generate_with_temperature(
    system_prompt="You are a creative strategist.",
    user_prompt="What's an unconventional marketing approach?",
    temperature=1.2
)

# More deterministic response
deterministic = client.generate_with_temperature(
    system_prompt="You are a financial analyst.",
    user_prompt="Calculate ROI...",
    temperature=0.1
)
```

### Streaming

```python
client = get_llm_client()

for chunk in client.stream(
    system_prompt="You are a VC analyst.",
    user_prompt="Analyze this startup..."
):
    print(chunk, end="", flush=True)
```

## Settings Reference

### Required Environment Variables

- `API_KEY` - LLM API key
- `QDRANT_URL` - Qdrant vector database URL
- `QDRANT_API_KEY` - Qdrant API key
- `POSTGRES_USER` - PostgreSQL username
- `POSTGRES_PASSWORD` - PostgreSQL password
- `TAVILY_API_KEY` - Tavily research API key

### Optional Environment Variables

- `MODEL_NAME` - LLM model (default: `gpt-4o-mini`)
- `BASE_URL` - LLM endpoint (default: OpenAI)
- `TEMPERATURE` - Response temperature (default: `0.7`)
- `MAX_TOKENS` - Max response tokens (default: `4096`)
- `DEBUG` - Enable debug mode (default: `False`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## Contracts

All modules communicate using shared Pydantic models. These are frozen contracts that enable parallel development.

### Core Contracts

**StartupInput** (Input)
- `startup_name: str`
- `website_url: Optional[str]`
- `pitch_deck_path: Optional[str]`

**AnalysisState** (Workflow State)
Tracks all intermediate outputs during analysis pipeline.

See `backend/contracts/schemas.py` for complete contract definitions.

## Testing

Run tests:
```bash
pytest backend/tests/test_llm_client.py -v
```

## Integration Points

### Person 2 - Research Layer
Uses `get_llm_client()` to generate research queries and process results.

### Person 3 - RAG Layer
Uses `get_llm_client()` with embeddings and retrieval.

### Person 4 - Agent Intelligence
Uses `get_llm_client()` with structured outputs for agent outputs.

### Person 5 - Platform & Orchestration
Manages all LLM initialization and configuration. Other modules only call `get_llm_client()`.

## Error Handling

```python
from backend.llm import get_llm_client

client = get_llm_client()

try:
    response = client.generate(
        system_prompt="...",
        user_prompt="...",
        response_model=MyModel
    )
except ValueError as e:
    # Structured output parsing failed
    print(f"Parsing error: {e}")
except Exception as e:
    # API error
    print(f"API error: {e}")
```

## Performance Notes

- The LLM client is initialized once and reused
- Streaming is recommended for long generations
- Custom temperature should match the task (higher for creativity, lower for precision)
- Structured outputs add ~20% latency due to JSON schema validation
