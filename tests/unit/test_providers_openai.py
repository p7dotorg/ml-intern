# tests/unit/test_providers_openai.py
import pytest
from unittest.mock import patch
from ml_agent.providers.openai import OpenAIProvider

@pytest.fixture
def openai_provider():
    with patch('openai.OpenAI'):
        return OpenAIProvider(api_key="sk-test")

def test_openai_initialization(openai_provider):
    """Test OpenAI provider initialization."""
    assert openai_provider.name == "openai"
    assert openai_provider.model == OpenAIProvider.default_model
