# src/ml_agent/auth/manager.py
from pathlib import Path
from typing import Optional
from ml_agent.auth.strategies import (
    AuthStrategy, EnvVarStrategy, FileStrategy,
    CLIArgStrategy, InteractiveStrategy
)
from ml_agent.core.exceptions import AuthenticationError

class AuthManager:
    """Manages authentication across providers."""

    def __init__(self, auth_file: Path = None, cli_api_key: Optional[str] = None):
        self.auth_file = auth_file or Path.home() / ".ml-agent" / "auth.json"
        self.strategies = [
            CLIArgStrategy(cli_api_key),
            FileStrategy(self.auth_file),
            EnvVarStrategy(),
            InteractiveStrategy(save_to_file=True, auth_file=self.auth_file),
        ]

    def get_api_key(self, provider: str) -> str:
        """Get API key for provider using resolution order."""
        for strategy in self.strategies:
            if key := strategy.get_credentials(provider):
                return key

        raise AuthenticationError(
            f"No credentials found for provider '{provider}'. "
            f"Please provide via CLI, env var, or auth.json"
        )

    def validate_provider_auth(self, provider_instance) -> bool:
        """Validate provider credentials."""
        return provider_instance.validate_credentials()
