# ML Agent Daemon - Autonomous Agent on Your Subscription

Run ML workflows autonomously on **your Claude/OpenAI subscription**. The daemon acts as a personal ML agent, executing workflows using your own API credits.

## Quick Start

```bash
# Run a single workflow autonomously
ml-agent daemon --workflow arxiv-dataset --config-file examples/daemon-config.json

# Check daemon status and history
ml-agent daemon-status
```

## How It Works

1. **You provide**: Workflow name + configuration
2. **Daemon does**: Uses Claude API with multi-turn conversation to execute workflows
3. **Claude orchestrates**: Decides steps, handles errors, reports progress
4. **On your subscription**: Uses your API keys and credits

### Architecture

```
┌─────────────────────────────┐
│   Your Local Machine        │
│  ml-agent daemon --workflow │
└──────────────┬──────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│   Claude API (Your Subscription)        │
│  - Multi-turn conversation              │
│  - Autonomous decision making           │
│  - Workflow orchestration               │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────┐
│   Your Machine              │
│  - Execute Python code      │
│  - Access ml-intern         │
│  - Store artifacts locally  │
└─────────────────────────────┘
```

## Usage Examples

### Single Workflow Execution

```bash
# Collect LaTeX dataset from arXiv
ml-agent daemon \
  --workflow arxiv-dataset \
  --config-file configs/arxiv.json

# Fine-tune a model
ml-agent daemon \
  --workflow fine-tune \
  --config-file configs/training.json

# Deploy to Hugging Face
ml-agent daemon \
  --workflow deploy \
  --config-file configs/deploy.json
```

### Configuration File Format

```json
{
  "workflow": "arxiv-dataset",
  "config": {
    "output_file": "datasets/latex_explanations.jsonl",
    "papers_count": 100,
    "categories": ["math"],
    "max_equations_per_paper": 50
  }
}
```

### Check Daemon History

```bash
ml-agent daemon-status
```

Output:
```json
{
  "provider": "claude",
  "model": "claude-opus-4-8",
  "workflows_completed": 5,
  "conversation_turns": 23,
  "recent_workflows": [
    {
      "workflow": "arxiv-dataset",
      "timestamp": "2026-07-23T20:15:30",
      "status": "completed"
    }
  ]
}
```

## Advanced Features

### Custom Provider

```bash
ml-agent daemon \
  --workflow arxiv-dataset \
  --provider openai \
  --config-file config.json
```

### Programmatic Usage

```python
import asyncio
from ml_agent.agent_daemon import AgentDaemon

async def main():
    daemon = AgentDaemon(provider="claude")
    result = await daemon.execute_workflow_autonomous(
        "arxiv-dataset",
        {"papers_count": 100}
    )
    print(result)

asyncio.run(main())
```

## What's Stored Locally

The daemon keeps a session file at `~/.ml-agent/daemon.json`:

```json
{
  "conversation": [
    {"role": "user", "content": "Execute arxiv-dataset workflow..."},
    {"role": "assistant", "content": "I'll start by..."}
  ],
  "workflows_completed": [
    {
      "workflow": "arxiv-dataset",
      "config": {...},
      "timestamp": "2026-07-23T20:15:30",
      "status": "completed"
    }
  ]
}
```

## Cost Estimation

Each workflow execution uses Claude API tokens:

- **Simple workflows** (status checks, validation): ~1-5k tokens
- **Medium workflows** (dataset collection): ~10-50k tokens
- **Complex workflows** (training): ~50-200k tokens

Check your actual usage in [Anthropic Console](https://console.anthropic.com/).

## Troubleshooting

### "No credentials found"
```bash
export CLAUDE_API_KEY="sk-ant-..."
ml-agent daemon --workflow arxiv-dataset
```

### "Workflow failed"
Check `~/.ml-agent/daemon.json` for the conversation history and error messages.

### "Rate limited"
The daemon includes automatic retry logic with exponential backoff.

## Best Practices

1. **Start small**: Test with a single workflow before chaining multiple
2. **Monitor costs**: Check your Anthropic account for API usage
3. **Log output**: Redirect to file for monitoring
   ```bash
   ml-agent daemon ... > workflow.log 2>&1
   ```
4. **Version control**: Keep config files in your repo for reproducibility

## Security Notes

- API keys stored in environment variables (not in code)
- Session file stored locally in `~/.ml-agent/` (not cloud)
- No data sent to third parties beyond Anthropic API
- All conversations encrypted in transit (HTTPS)

---

**Your personal ML agent is ready!** 🚀
