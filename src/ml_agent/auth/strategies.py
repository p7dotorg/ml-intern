# src/ml_agent/auth/strategies.py
from abc import ABC, abstractmethod
from pathlib import Path
import os
import json
from typing import Optional

class AuthStrategy(ABC):
    """Base authentication strategy."""

    @abstractmethod
    def get_credentials(self, provider: str) -> Optional[str]:
        """Get credentials for provider."""
        pass

class EnvVarStrategy(AuthStrategy):
    """Get credentials from environment variables."""

    def get_credentials(self, provider: str) -> Optional[str]:
        """Look for {PROVIDER}_API_KEY or similar."""
        env_keys = [
            f"{provider.upper()}_API_KEY",
            f"{provider.upper().replace('-', '_')}_API_KEY",
        ]
        for key in env_keys:
            if value := os.getenv(key):
                return value
        return None

class FileStrategy(AuthStrategy):
    """Get credentials from auth.json file."""

    def __init__(self, auth_file: Path):
        self.auth_file = auth_file

    def get_credentials(self, provider: str) -> Optional[str]:
        """Read from auth.json."""
        if not self.auth_file.exists():
            return None

        try:
            with open(self.auth_file) as f:
                data = json.load(f)
            return data.get("providers", {}).get(provider, {}).get("api_key")
        except (json.JSONDecodeError, KeyError):
            return None

class CLIArgStrategy(AuthStrategy):
    """Get credentials from CLI arguments."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_credentials(self, provider: str) -> Optional[str]:
        """Return CLI-provided key if matches provider."""
        return self.api_key

class InteractiveStrategy(AuthStrategy):
    """Prompt user for credentials."""

    def __init__(self, save_to_file: bool = False, auth_file: Path = None):
        self.save_to_file = save_to_file
        self.auth_file = auth_file

    def get_credentials(self, provider: str) -> Optional[str]:
        """Prompt user for API key."""
        import getpass
        key = getpass.getpass(f"Enter {provider.upper()} API key: ")

        if self.save_to_file and self.auth_file and key:
            self._save_to_file(provider, key)

        return key if key else None

    def _save_to_file(self, provider: str, key: str):
        """Save credentials to auth.json."""
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)

        data = {}
        if self.auth_file.exists():
            with open(self.auth_file) as f:
                data = json.load(f)

        if "providers" not in data:
            data["providers"] = {}
        data["providers"][provider] = {"api_key": key}

        with open(self.auth_file, "w") as f:
            json.dump(data, f, indent=2)
        os.chmod(self.auth_file, 0o600)
