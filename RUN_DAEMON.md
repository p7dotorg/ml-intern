# 🚀 Run ML Agent Daemon

## Quick Start

Your autonomous ML agent is ready to run! Here's how:

### 1. Set Your API Key

```bash
export CLAUDE_API_KEY="sk-ant-..."
```

### 2. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 3. Run Autonomous Workflow

```bash
python3 run_daemon.py
```

**Note:** Use the `run_daemon.py` script directly (not `ml-agent daemon` CLI command)

### What's Happening

1. **Daemon starts** - Uses your Claude API subscription
2. **Claude thinks** - Multi-turn conversation to plan workflow
3. **Executes** - Collects LaTeX dataset from arXiv
4. **Reports** - Shows results and saves to `~/.ml-agent/daemon.json`

---

## Example Output

```
🚀 Starting autonomous workflow...
📊 Workflow: arxiv-dataset
💾 Config: Collect 100 LaTeX math papers

✅ Workflow Result:
{
  "workflow": "arxiv-dataset",
  "status": "completed",
  "result": "Successfully collected 100 papers...",
  "timestamp": "2026-07-23T20:15:30"
}

📊 Daemon Status:
{
  "provider": "claude",
  "model": "claude-opus-4-8",
  "workflows_completed": 1,
  "conversation_turns": 5,
  "recent_workflows": [...]
}
```

---

## How It Works

```
┌─────────────────────────┐
│  Your Machine           │
│  run_daemon.py          │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│  Claude API (Your Subscription)     │
│  - Multi-turn conversation          │
│  - Orchestrates workflow            │
│  - Uses your API credits            │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────┐
│  Your Machine           │
│  - Executes Python      │
│  - Runs ml-intern       │
│  - Stores results       │
└─────────────────────────┘
```

---

## Session History

Each run saves to `~/.ml-agent/daemon.json`:

```json
{
  "conversation": [
    {"role": "user", "content": "Execute arxiv-dataset..."},
    {"role": "assistant", "content": "I'll start by..."}
  ],
  "workflows_completed": [
    {
      "workflow": "arxiv-dataset",
      "timestamp": "2026-07-23T20:15:30",
      "status": "completed"
    }
  ]
}
```

---

## Cost Estimation

- **Simple workflows** (100 papers): ~5-15k tokens
- **Typical execution**: $0.05 - $0.50
- **Complex workflows**: $1-5

Check your actual usage in [Anthropic Console](https://console.anthropic.com/)

---

## Next Steps

1. ✅ Set `CLAUDE_API_KEY`
2. ✅ Run `python3 run_daemon.py`
3. ✅ Check `~/.ml-agent/daemon.json` for history
4. ✅ Customize workflow in `run_daemon.py`

**Your personal ML agent is live!** 🤖
