# tests/unit/test_providers_registry.py
import pytest
from ml_agent.providers.registry import ProviderRegistry, get_provider

def test_list_available_providers():
    """Test listing available providers."""
    providers = ProviderRegistry.list_available()
    assert "claude" in providers
    assert "openai" in providers

def test_get_unknown_provider():
    """Test error on unknown provider."""
    with pytest.raises(ValueError, match="Unknown provider"):
        ProviderRegistry.get("unknown", "key")

def test_factory_function():
    """Test factory function."""
    # Should not raise (won't actually connect)
    providers = ProviderRegistry.list_available()
    assert len(providers) > 0
