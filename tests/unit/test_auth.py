# tests/unit/test_auth.py
import pytest
from pathlib import Path
from unittest.mock import patch
from ml_agent.auth.manager import AuthManager
from ml_agent.auth.strategies import (
    EnvVarStrategy, FileStrategy, CLIArgStrategy
)
from ml_agent.core.exceptions import AuthenticationError

def test_cli_arg_strategy():
    """Test CLI argument strategy."""
    strategy = CLIArgStrategy(api_key="test-key")
    assert strategy.get_credentials("claude") == "test-key"

def test_env_var_strategy(monkeypatch):
    """Test environment variable strategy."""
    monkeypatch.setenv("CLAUDE_API_KEY", "env-key")
    strategy = EnvVarStrategy()
    assert strategy.get_credentials("claude") == "env-key"

def test_file_strategy(tmp_path):
    """Test file-based strategy."""
    auth_file = tmp_path / "auth.json"
    strategy = FileStrategy(auth_file)
    assert strategy.get_credentials("claude") is None

def test_auth_manager_get_api_key_cli():
    """Test AuthManager with CLI key."""
    manager = AuthManager(cli_api_key="cli-key")
    assert manager.get_api_key("claude") == "cli-key"

def test_auth_manager_no_credentials(tmp_path, monkeypatch):
    """Test error when no credentials found."""
    # Use temp auth file that doesn't exist to avoid interactive strategy
    auth_file = tmp_path / "auth.json"
    manager = AuthManager(auth_file=auth_file, cli_api_key=None)
    # Clear any environment variables
    monkeypatch.delenv("NONEXISTENT_API_KEY", raising=False)
    # Mock the interactive strategy to return None
    with patch("ml_agent.auth.strategies.InteractiveStrategy.get_credentials", return_value=None):
        with pytest.raises(AuthenticationError):
            manager.get_api_key("nonexistent")
