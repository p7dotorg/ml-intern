# tests/unit/test_config.py
import pytest
from pathlib import Path
from ml_agent.core.config import Config, ProviderConfig

def test_config_defaults():
    """Test default configuration values."""
    config = Config()
    assert config.log_level == "INFO"
    assert config.debug is False
    assert isinstance(config.home_dir, Path)

def test_provider_config():
    """Test provider configuration."""
    provider = ProviderConfig(api_key="test-key")
    assert provider.api_key == "test-key"
    assert provider.timeout == 30
    assert provider.max_retries == 3

def test_ensure_directories(tmp_path):
    """Test directory creation."""
    config = Config(home_dir=tmp_path / ".ml-agent")
    config.ensure_directories()
    assert config.home_dir.exists()
    assert config.log_dir.exists()
