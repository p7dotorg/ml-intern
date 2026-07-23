# Plugin System

## Creating a Provider Plugin

```python
from ml_agent.plugins.base import ProviderPlugin
from ml_agent.providers.base import BaseProvider

class MyProvider(BaseProvider):
    name = "myprovider"

    async def complete(self, messages, **kwargs):
        # Implementation
        pass

class MyProviderPlugin(ProviderPlugin):
    name = "myprovider-plugin"
    version = "1.0.0"

    def initialize(self, config):
        pass

    def get_provider_class(self):
        return MyProvider
```

Place in `~/.ml-agent/plugins/my_provider.py`
