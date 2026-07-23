# tests/unit/test_providers_base.py
import pytest
from ml_agent.providers.base import BaseProvider, Message

class MockProvider(BaseProvider):
    name = "mock"

    async def complete(self, messages, max_tokens=2048, temperature=0.7, **kwargs):
        return "Mock response"

    def validate_credentials(self):
        return True

def test_base_provider_initialization():
    """Test provider initialization."""
    provider = MockProvider(api_key="test-key")
    assert provider.api_key == "test-key"
    assert provider.name == "mock"

def test_message_creation():
    """Test message creation."""
    msg = Message(role="user", content="Hello")
    assert msg.role == "user"
    assert msg.content == "Hello"
