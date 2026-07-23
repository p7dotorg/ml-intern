# tests/unit/test_plugins.py
from ml_agent.plugins.base import Plugin, ProviderPlugin, WorkflowPlugin

class MockPlugin(Plugin):
    name = "mock"
    version = "1.0.0"

    def initialize(self, config):
        pass

def test_plugin_base():
    """Test plugin base class."""
    plugin = MockPlugin()
    assert plugin.name == "mock"
    assert plugin.version == "1.0.0"
