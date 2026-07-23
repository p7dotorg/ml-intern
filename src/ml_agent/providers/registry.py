# src/ml_agent/providers/registry.py
from typing import Dict, Type
from ml_agent.providers.base import BaseProvider
from ml_agent.providers.claude import ClaudeProvider
from ml_agent.providers.openai import OpenAIProvider

class ProviderRegistry:
    """Registry for available LLM providers."""

    _providers: Dict[str, Type[BaseProvider]] = {
        "claude": ClaudeProvider,
        "openai": OpenAIProvider,
    }

    @classmethod
    def register(cls, name: str, provider_class: Type[BaseProvider]):
        """Register a new provider."""
        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str, api_key: str, **kwargs) -> BaseProvider:
        """Get provider instance."""
        if name not in cls._providers:
            raise ValueError(f"Unknown provider: {name}")
        return cls._providers[name](api_key=api_key, **kwargs)

    @classmethod
    def list_available(cls) -> list[str]:
        """List all available providers."""
        return list(cls._providers.keys())

def get_provider(name: str, api_key: str, **kwargs) -> BaseProvider:
    """Factory function to get provider instance."""
    return ProviderRegistry.get(name, api_key, **kwargs)
