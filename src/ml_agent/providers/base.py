# src/ml_agent/providers/base.py
from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
import structlog

@dataclass
class Message:
    """LLM message format."""
    role: str  # "user", "assistant", "system"
    content: str

class BaseProvider(ABC):
    """Abstract base for LLM providers."""

    name: str  # Must be defined by subclass

    def __init__(self, api_key: str, **kwargs):
        """Initialize provider."""
        self.api_key = api_key
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.config = kwargs

    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        max_tokens: int = 2048,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion from messages."""
        pass

    @abstractmethod
    def validate_credentials(self) -> bool:
        """Validate API credentials."""
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(api_key=***)"
