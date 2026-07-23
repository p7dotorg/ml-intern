# src/ml_agent/providers/claude.py
import anthropic
from typing import Optional
from ml_agent.providers.base import BaseProvider, Message
from ml_agent.core.exceptions import AuthenticationError, ProviderException

class ClaudeProvider(BaseProvider):
    """Anthropic Claude provider."""

    name = "claude"
    default_model = "claude-3-5-sonnet-20241022"

    def __init__(self, api_key: str, model: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.model = model or self.default_model
        self.client = anthropic.Anthropic(api_key=api_key)

    async def complete(
        self,
        messages: list[Message],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion using Claude."""
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=formatted_messages,
                **kwargs
            )

            return response.content[0].text

        except anthropic.AuthenticationError as e:
            raise AuthenticationError(f"Claude authentication failed: {e}")
        except anthropic.RateLimitError as e:
            raise ProviderException(f"Claude rate limited: {e}")
        except Exception as e:
            raise ProviderException(f"Claude error: {e}")

    def validate_credentials(self) -> bool:
        """Validate API key."""
        try:
            # Try to make a minimal request
            self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False
