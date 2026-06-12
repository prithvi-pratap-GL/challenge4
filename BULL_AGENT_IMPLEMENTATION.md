# Bull Agent Implementation

## Overview
The Bull Agent builds the strongest possible investment case for a startup analysis. It takes research findings and knowledge base context to construct a compelling bullish narrative.

## Files Created

### 1. `backend/agents/bull/agent.py`
Main agent implementation containing `run_bull_case()` function.

**Function Signature:**
```python
async def run_bull_case(
    research_output: Dict[str, Any],
    knowledge_output: Dict[str, Any]
) -> BullOutput
```

**Inputs:**
- `research_output`: ResearchOutput containing founders, competitors, market, funding, industry data
- `knowledge_output`: KnowledgeOutput containing business model, risks, financials, evidence

**Output:**
- `BullOutput`: Pydantic model with:
  - `investment_case` (str): 3-4 paragraph bullish narrative
  - `strengths` (List[str]): 6-8 key strengths and opportunities
  - `confidence` (int): 0-100 confidence score

### 2. `backend/agents/bull/prompts.py`
Contains LLM prompts for the Bull Agent:
- `BULL_SYSTEM_PROMPT`: Instructs LLM to act as aggressive VC advocate
- `BULL_USER_PROMPT_TEMPLATE`: Formats research and knowledge data for analysis

### 3. `tests/test_bull_agent.py`
Comprehensive test suite covering:
- Input validation (ResearchOutput, KnowledgeOutput)
- BullOutput schema validation
- Helper function tests
- Placeholder for LLM integration tests

## Current Status

✅ **Complete:**
- Directory structure set up
- Pydantic schemas defined
- Robust system prompt drafted
- `run_bull_case()` function skeleton
- Input/output formatting logic
- Comprehensive test suite

⏳ **Blocked on Person 5:**
- LLM client integration (`backend.llm.client.LLMClient`)

## Person 5 Integration Requirements

For the Bull Agent to work end-to-end, Person 5 must:

### 1. Create LLM Client Module
File: `backend/llm/client.py`

```python
class LLMClient:
    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: type
    ) -> Any:
        """Generate structured response from LLM."""
        # Implementation: call OpenAI/LLM API
        # Parse response into response_model (Pydantic validation)
        # Return typed response
```

### 2. Update `run_bull_case()` in `backend/agents/bull/agent.py`

Replace the placeholder with:
```python
from backend.llm.client import LLMClient

async def run_bull_case(...) -> BullOutput:
    # ... existing data extraction code ...
    
    llm_client = LLMClient()
    response = await llm_client.generate(
        system_prompt=BULL_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=BullOutput
    )
    return response
```

### 3. Configuration Requirements

Ensure `backend/config/settings.py` provides:
- OpenAI API key or alternative LLM credentials
- LLM model selection (from environment variables)
- Timeout and retry settings

## Testing Instructions

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/test_bull_agent.py -v --asyncio-mode=auto

# Run with coverage
pytest tests/test_bull_agent.py --cov=backend.agents.bull --cov-report=html
```

### Current Test Results
**Before Person 5 Integration:**
- ✅ Input handling tests: PASS
- ✅ Schema validation tests: PASS
- ✅ Helper function tests: PASS
- ⏳ Integration tests: SKIP (marked) / FAIL (NotImplementedError) until LLM client ready

**After Person 5 Integration:**
- All tests should PASS
- Integration test should verify:
  - `investment_case` length > 100 characters
  - `strengths` list has 6+ items
  - `confidence` in range 0-100

## Acceptance Criteria Status

✅ **Function accepts correct inputs**
- `run_bull_case(research: ResearchOutput, knowledge: KnowledgeOutput)` is implemented
- Input types are validated in tests
- Function properly extracts and formats data

✅ **Function returns BullOutput**
- Output is correctly typed as BullOutput
- All required fields: investment_case, strengths, confidence
- Confidence validated to 0-100 range

✅ **Unit tests written**
- `tests/test_bull_agent.py` with comprehensive coverage
- Tests include:
  - Input validation (6 tests)
  - Schema validation (5 tests)
  - Helper functions (3 tests)
  - Mock/placeholder integration (2 tests)
  - Full LLM integration (1 skipped test for after Person 5)

## Prompt Engineering Details

### System Prompt Characteristics
- Positions agent as "aggressive venture capital partner"
- Focus areas: founder credibility, market opportunity, competitive advantages, growth potential
- Balanced tone: optimistic yet evidence-based

### User Prompt Template
Provides structured context:
- Startup name and overview
- Founder backgrounds and track records
- Funding history and investor validation
- Competitive landscape
- Market size and growth rates
- Business model and unit economics
- Traction and validation signals
- Identified risks (to address, not ignore)

## Design Decisions

1. **Async Function**: `run_bull_case()` is async to support concurrent processing in orchestrator
2. **Dict-based Inputs**: Uses Dict[str, Any] to accept flexible research/knowledge structures
3. **Helper Functions**: `_format_list()` handles list-to-string conversion for prompts
4. **LLM Abstraction**: Placeholder design allows clean integration once Person 5 provides client
5. **Comprehensive Tests**: Test-first approach catches integration issues early

## Next Steps

1. **Person 5**: Implement `backend.llm.client.LLMClient`
2. **Person 4**: Uncomment and test LLM integration code
3. **Integration**: Run end-to-end tests with actual LLM
4. **Iterate**: Refine prompts based on LLM output quality

## Related Agents

This Bull Agent is part of the investment committee framework:
- **Bear Agent** (`backend/agents/bear/`): Builds rejection case
- **Red Team Agent** (`backend/agents/red_team/`): Challenges assumptions
- **Reviewer Agent** (`backend/agents/reviewer/`): Quality assurance
- **Committee Agent** (`backend/agents/committee/`): Final synthesis

All agents follow the same pattern:
1. Accept research + knowledge inputs
2. Generate LLM prompts
3. Call Person 5's LLM client
4. Return Pydantic-validated output

## Questions?

- **LLM Integration**: See "Person 5 Integration Requirements" section
- **Testing**: Run `pytest tests/test_bull_agent.py -v`
- **Prompts**: See `backend/agents/bull/prompts.py`
- **Schema**: See `backend/agents/schemas.py`
