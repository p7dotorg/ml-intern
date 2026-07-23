# src/ml_agent/auth/manager.py
from pathlib import Path
from typing import Optional
from ml_agent.auth.strategies import (
    AuthStrategy, EnvVarStrategy, FileStrategy,
    CLIArgStrategy, InteractiveStrategy
)
from ml_agent.auth.oauth import OAuthManager, SubscriptionAuthStrategy
from ml_agent.core.exceptions import AuthenticationError

class AuthManager:
    """Manages authentication across providers (API keys + OAuth subscriptions)."""

    def __init__(self, auth_file: Path = None, cli_api_key: Optional[str] = None):
        self.auth_file = auth_file or Path.home() / ".ml-agent" / "auth.json"
        self.oauth_manager = OAuthManager()
        self.subscription_strategy = SubscriptionAuthStrategy()

        self.strategies = [
            CLIArgStrategy(cli_api_key),
            FileStrategy(self.auth_file),
            EnvVarStrategy(),
            InteractiveStrategy(save_to_file=True, auth_file=self.auth_file),
        ]

    def get_api_key(self, provider: str) -> str:
        """Get API key for provider using resolution order.

        Priority:
        1. CLI argument
        2. OAuth subscription (Claude Pro, ChatGPT Plus)
        3. auth.json file
        4. Environment variables
        5. Interactive prompt
        """
        # Check for OAuth subscription first
        if self.subscription_strategy.is_subscribed(provider):
            if key := self.subscription_strategy.get_api_key(provider):
                return key

        # Fall back to traditional API key resolution
        for strategy in self.strategies:
            if key := strategy.get_credentials(provider):
                return key

        raise AuthenticationError(
            f"No credentials found for provider '{provider}'. "
            f"Options:\n"
            f"  1. Login: ml-agent login {provider}\n"
            f"  2. API Key: ANTHROPIC_API_KEY=... or --api-key\n"
            f"  3. auth.json: {self.auth_file}"
        )

    def validate_provider_auth(self, provider_instance) -> bool:
        """Validate provider credentials."""
        return provider_instance.validate_credentials()

    def get_subscription_status(self, provider: str) -> dict:
        """Get subscription status for provider."""
        if self.subscription_strategy.is_subscribed(provider):
            return self.subscription_strategy.get_subscription_info(provider)

        return {"provider": provider, "authenticated": False, "type": "api_key"}

    def list_subscriptions(self) -> list:
        """List all active subscriptions."""
        subscriptions = []
        for provider in ["claude", "openai", "google", "xai"]:
            if self.subscription_strategy.is_subscribed(provider):
                info = self.subscription_strategy.get_subscription_info(provider)
                subscriptions.append(info)

        return subscriptions
