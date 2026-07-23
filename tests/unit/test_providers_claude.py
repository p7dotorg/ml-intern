# tests/unit/test_providers_claude.py
import pytest
from unittest.mock import Mock, AsyncMock, patch
from ml_agent.providers.claude import ClaudeProvider
from ml_agent.providers.base import Message

@pytest.fixture
def claude_provider():
    with patch('anthropic.Anthropic'):
        return ClaudeProvider(api_key="sk-ant-test")

def test_claude_initialization(claude_provider):
    """Test Claude provider initialization."""
    assert claude_provider.name == "claude"
    assert claude_provider.api_key == "sk-ant-test"
    assert claude_provider.model == ClaudeProvider.default_model

def test_claude_repr(claude_provider):
    """Test provider string representation."""
    assert "***" in repr(claude_provider)
    assert "claude" in repr(claude_provider).lower()
