"""OpenAI-compatible LLM client wrapper.

Supports: OpenAI, Azure, OpenRouter, Ollama, local models
"""

from typing import Any, Type, TypeVar, Optional
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel
import json
import re
import os

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """OpenAI-compatible LLM client."""

    def __init__(self, api_key: str = None, model_name: str = None, base_url: str = None, temperature: float = 0.7):
        """
        Initialize LLM client.

        Args:
            api_key: LLM API key (defaults to env var)
            model_name: Model name (defaults to env var)
            base_url: API endpoint (defaults to env var)
            temperature: Response temperature
        """
        self.api_key = api_key or os.getenv("API_KEY", "")
        self.model_name = model_name or os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.base_url = base_url or os.getenv("BASE_URL", "https://api.openai.com/v1")
        self.temperature = temperature

        self._init_client()

    def _init_client(self):
        """Initialize appropriate OpenAI client."""
        if "azure" in self.base_url.lower():
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=self.base_url,
            )
            self.is_azure = True
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
            self.is_azure = False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Optional[Type[T]] = None,
    ) -> str | T:
        """
        Generate response from LLM.

        Args:
            system_prompt: System context
            user_prompt: User query
            response_model: Optional Pydantic model for structured output

        Returns:
            Generated text or structured response
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        kwargs = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
        }

        if response_model:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__,
                    "schema": response_model.model_json_schema(),
                    "strict": True,
                },
            }

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        if response_model:
            try:
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    data = json.loads(json_str)
                    return response_model(**data)
                return response_model(**json.loads(content))
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Failed to parse response: {e}")

        return content

    def generate_with_temperature(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        response_model: Optional[Type[T]] = None,
    ) -> str | T:
        """Generate with custom temperature."""
        original_temp = self.temperature
        self.temperature = temperature
        try:
            return self.generate(system_prompt, user_prompt, response_model)
        finally:
            self.temperature = original_temp

    def stream(self, system_prompt: str, user_prompt: str):
        """Stream response tokens."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        with self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=self.temperature,
            stream=True,
        ) as stream:
            for text in stream.text_stream:
                yield text


def get_llm_client() -> LLMClient:
    """Get LLM client instance."""
    return LLMClient()
