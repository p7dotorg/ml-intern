# src/ml_agent/plugins/loader.py
from pathlib import Path
from typing import List
import importlib.util
import structlog
from ml_agent.plugins.base import Plugin, ProviderPlugin, WorkflowPlugin
from ml_agent.providers.registry import ProviderRegistry
from ml_agent.workflows.registry import WorkflowRegistry

class PluginLoader:
    """Loads and manages plugins."""

    def __init__(self, plugin_dir: Path = None):
        self.plugin_dir = plugin_dir or Path.home() / ".ml-agent" / "plugins"
        self.logger = structlog.get_logger("PluginLoader")
        self.loaded_plugins = {}

    def load_plugins(self) -> List[Plugin]:
        """Load all plugins from plugin directory."""
        if not self.plugin_dir.exists():
            return []

        plugins = []
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue

            try:
                plugin = self._load_plugin_file(plugin_file)
                if plugin:
                    plugins.append(plugin)
                    self.logger.info("Loaded plugin", name=plugin.name)
            except Exception as e:
                self.logger.error("Failed to load plugin", file=plugin_file, error=str(e))

        return plugins

    def _load_plugin_file(self, path: Path) -> Plugin:
        """Load single plugin file."""
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Find Plugin class
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Plugin) and attr != Plugin:
                plugin = attr()

                # Register appropriately
                if isinstance(plugin, ProviderPlugin):
                    provider_class = plugin.get_provider_class()
                    ProviderRegistry.register(plugin.name, provider_class)

                elif isinstance(plugin, WorkflowPlugin):
                    workflow_class = plugin.get_workflow_class()
                    WorkflowRegistry.register(plugin.name, workflow_class)

                return plugin

        return None
