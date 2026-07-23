# ML Agent Framework

Multi-provider ML workflow automation framework supporting Claude, OpenAI, and more via plugins.

## Installation

```bash
pip install ml-agent
```

## Quick Start

```bash
# List providers
ml-agent list-providers

# Validate credentials
ml-agent validate-auth --provider claude

# Run workflow
ml-agent run \
  --provider claude \
  --workflow arxiv-dataset \
  --config config.yaml
```

## Documentation

- [API Reference](docs/API_REFERENCE.md)
- [Plugin System](docs/PLUGINS.md)
- [Examples](examples/)

## License

Apache 2.0
