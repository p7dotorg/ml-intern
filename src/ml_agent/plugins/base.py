# src/ml_agent/plugins/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any

class Plugin(ABC):
    """Base class for all plugins."""

    name: str
    version: str

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin with config."""
        pass

class ProviderPlugin(Plugin):
    """Plugin for adding a new LLM provider."""

    @abstractmethod
    def get_provider_class(self):
        """Return provider class."""
        pass

class WorkflowPlugin(Plugin):
    """Plugin for adding a new workflow."""

    @abstractmethod
    def get_workflow_class(self):
        """Return workflow class."""
        pass
