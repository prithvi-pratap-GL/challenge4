from typing import Any, Type, TypeVar, Optional
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel
import json
import re

from backend.config import get_settings

T = TypeVar("T", bound=BaseModel)


class LLMClient:
    """OpenAI-compatible LLM client wrapper supporting multiple providers."""

    def __init__(self):
        """Initialize LLM client from environment configuration."""
        self.settings = get_settings()
        self._init_client()

    def _init_client(self):
        """Initialize appropriate OpenAI client based on configuration."""
        api_key = self.settings.API_KEY
        model_name = self.settings.MODEL_NAME
        base_url = self.settings.BASE_URL
        temperature = self.settings.TEMPERATURE

        self.model_name = model_name
        self.temperature = temperature

        if base_url and "azure" in base_url.lower():
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=base_url,
            )
            self.is_azure = True
        else:
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url or "https://api.openai.com/v1",
            )
            self.is_azure = False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Optional[Type[T]] = None,
    ) -> str | T:
        """
        Generate a response using the LLM.

        Args:
            system_prompt: System context/role for the LLM
            user_prompt: User input/question
            response_model: Optional Pydantic model for structured output

        Returns:
            str if response_model is None, otherwise an instance of response_model
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
                raise ValueError(f"Failed to parse response as {response_model.__name__}: {e}")

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
    """Get singleton LLM client instance."""
    return LLMClient()
