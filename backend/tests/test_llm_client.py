import pytest
from pydantic import BaseModel
from backend.llm import LLMClient
from backend.contracts import ResearchOutput


class MockResponse(BaseModel):
    """Test response model."""

    message: str
    status: str


class TestLLMClient:
    """Test LLM client initialization and methods."""

    def test_llm_client_initialization(self):
        """Test that LLM client initializes without errors."""
        client = LLMClient()
        assert client is not None
        assert client.model_name
        assert client.temperature >= 0.0
        assert client.temperature <= 2.0

    def test_llm_client_has_required_methods(self):
        """Test that LLM client has required methods."""
        client = LLMClient()
        assert hasattr(client, "generate")
        assert hasattr(client, "generate_with_temperature")
        assert hasattr(client, "stream")
        assert callable(client.generate)
        assert callable(client.generate_with_temperature)
        assert callable(client.stream)

    def test_generate_signature(self):
        """Test generate method accepts required parameters."""
        client = LLMClient()
        # Just check the method signature is correct
        import inspect

        sig = inspect.signature(client.generate)
        params = list(sig.parameters.keys())
        assert "system_prompt" in params
        assert "user_prompt" in params
        assert "response_model" in params

    def test_research_output_contract(self):
        """Test ResearchOutput contract structure."""
        output = ResearchOutput(
            founders=["Founder 1"],
            competitors=["Competitor 1"],
            market_summary="Test market",
            funding_summary="Test funding",
            industry_summary="Test industry",
            sources=["source1"],
        )
        assert output.founders == ["Founder 1"]
        assert output.market_summary == "Test market"
        assert len(output.sources) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
