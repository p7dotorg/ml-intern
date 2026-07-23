# src/ml_agent/core/config.py
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class ProviderConfig(BaseModel):
    """Configuration for a specific LLM provider."""
    api_key: Optional[str] = Field(None, description="API key for provider")
    base_url: Optional[str] = Field(None, description="Custom base URL")
    timeout: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum retry attempts")

class WorkflowConfig(BaseModel):
    """Configuration for a workflow execution."""
    name: str
    provider: str
    steps: dict = Field(default_factory=dict)
    max_iterations: int = 300
    timeout_minutes: int = 120

class Config(BaseSettings):
    """Main configuration for ML Agent."""

    # Directories
    home_dir: Path = Field(default_factory=lambda: Path.home() / ".ml-agent")
    log_dir: Path = Field(default_factory=lambda: Path.home() / ".ml-agent" / "logs")
    config_file: Path = Field(default_factory=lambda: Path.home() / ".ml-agent" / "config.yaml")
    auth_file: Path = Field(default_factory=lambda: Path.home() / ".ml-agent" / "auth.json")

    # Logging
    log_level: str = Field("INFO", description="Log level")
    log_format: str = Field("json", description="json or text")

    # Providers
    providers: dict[str, ProviderConfig] = Field(default_factory=dict)

    # General
    debug: bool = False

    class Config:
        env_prefix = "ML_AGENT_"
        yaml_file = None

    def ensure_directories(self):
        """Create necessary directories."""
        self.home_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        """Load config from YAML file."""
        import yaml
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
