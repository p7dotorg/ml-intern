# src/ml_agent/providers/openai.py
import openai
from typing import Optional
from ml_agent.providers.base import BaseProvider, Message
from ml_agent.core.exceptions import AuthenticationError, ProviderException

class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider."""

    name = "openai"
    default_model = "gpt-4-turbo"

    def __init__(self, api_key: str, model: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.model = model or self.default_model
        self.client = openai.OpenAI(api_key=api_key)

    async def complete(
        self,
        messages: list[Message],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion using OpenAI."""
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=formatted_messages,
                **kwargs
            )

            return response.choices[0].message.content

        except openai.AuthenticationError as e:
            raise AuthenticationError(f"OpenAI authentication failed: {e}")
        except openai.RateLimitError as e:
            raise ProviderException(f"OpenAI rate limited: {e}")
        except Exception as e:
            raise ProviderException(f"OpenAI error: {e}")

    def validate_credentials(self) -> bool:
        """Validate API key."""
        try:
            self.client.chat.completions.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False
