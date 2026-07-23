# 🤖 ML Agent Daemon - 24/7 Server

Run your ML agent **continuously** like pi.dev, listening for workflow requests and executing them autonomously on your Claude/OpenAI subscription.

## Quick Start

### Terminal 1: Start Daemon (Runs 24/7)

```bash
export CLAUDE_API_KEY="sk-ant-..."
source venv/bin/activate
python3 start_daemon.py
```

Output:
```
============================================================
🤖 ML Agent Daemon Server
============================================================
Provider: claude
Port: 8000
URL: http://localhost:8000

API Endpoints:
  POST http://localhost:8000/api/workflow
  GET  http://localhost:8000/api/status
  GET  http://localhost:8000/api/history
  POST http://localhost:8000/api/stop

Press Ctrl+C to stop daemon
```

### Terminal 2: Send Workflow Requests

```bash
# Submit workflow
python3 client_daemon.py workflow \
  --workflow arxiv-dataset \
  --papers 100 \
  --categories "math.LA,math.AP"

# Check status
python3 client_daemon.py status

# View history
python3 client_daemon.py history

# Stop daemon
python3 client_daemon.py stop
```

---

## API Endpoints

### POST /api/workflow
Submit a workflow to execute.

```bash
curl -X POST http://localhost:8000/api/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "arxiv-dataset",
    "config": {
      "papers_count": 100,
      "categories": ["math.LA"],
      "output_file": "datasets/latex.jsonl"
    }
  }'
```

Response:
```json
{
  "status": "completed",
  "result": {
    "workflow": "arxiv-dataset",
    "status": "completed",
    "result": "Successfully collected 100 papers...",
    "timestamp": "2026-07-23T21:30:00"
  }
}
```

### GET /api/status
Get daemon status and statistics.

```bash
curl http://localhost:8000/api/status
```

Response:
```json
{
  "provider": "claude",
  "model": "claude-opus-4-8",
  "workflows_completed": 5,
  "conversation_turns": 23,
  "recent_workflows": [...]
}
```

### GET /api/history
Get workflow execution history.

```bash
curl "http://localhost:8000/api/history?limit=10"
```

### POST /api/stop
Gracefully stop daemon.

```bash
curl -X POST http://localhost:8000/api/stop
```

---

## Architecture

```
┌─────────────────────────────────────┐
│  Daemon Server (Runs 24/7)          │
│  - HTTP API on port 8000            │
│  - Listens for workflow requests    │
│  - Executes on your subscription    │
│  - Stores history locally           │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      ↓             ↓
  ┌─────────┐  ┌──────────┐
  │ Client  │  │ External │
  │ Script  │  │ Services │
  │  (CLI)  │  │ (Webhooks)
  └─────────┘  └──────────┘
```

---

## Use Cases

### 1. Scheduled Dataset Collection

```bash
# Run daily at 2 AM (via cron)
0 2 * * * python3 client_daemon.py workflow \
  --workflow arxiv-dataset \
  --papers 100
```

### 2. CI/CD Integration

```bash
# In your GitHub Actions
curl -X POST http://your-machine:8000/api/workflow \
  -d '{"workflow": "fine-tune", "config": {...}}'
```

### 3. Web Hook Triggers

```python
# Your web service triggers ML workflows
import requests

requests.post(
    "http://localhost:8000/api/workflow",
    json={
        "workflow": "deploy",
        "config": {"model_path": "models/latex-explainer"}
    }
)
```

### 4. Always-On ML Agent

Just leave it running! Like pi.dev:
- Accepts requests 24/7
- Uses your subscription credits
- Persists session history
- Autonomous decision making

---

## Session Persistence

History stored in `~/.ml-agent/daemon.json`:

```json
{
  "conversation": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "workflows_completed": [
    {
      "workflow": "arxiv-dataset",
      "config": {...},
      "timestamp": "2026-07-23T21:30:00",
      "status": "completed"
    }
  ]
}
```

---

## Deployment Options

### Option 1: Local Machine (Development)
```bash
python3 start_daemon.py
```

### Option 2: Background Process (Production)
```bash
nohup python3 start_daemon.py > daemon.log 2>&1 &
```

### Option 3: Systemd Service (Linux)
```ini
[Unit]
Description=ML Agent Daemon
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/ml-intern
ExecStart=/path/to/ml-intern/venv/bin/python3 start_daemon.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option 4: Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -e .
ENV CLAUDE_API_KEY=$CLAUDE_API_KEY
CMD ["python3", "start_daemon.py"]
```

---

## Monitoring

### Check if daemon is running
```bash
curl http://localhost:8000/api/status
```

### View logs
```bash
tail -f daemon.log
```

### Monitor API usage
Check [Anthropic Console](https://console.anthropic.com/) for real-time usage.

---

## Cost Control

- Each workflow uses Claude API tokens from your subscription
- Estimate: ~$0.05-0.50 per workflow
- Monitor usage in Anthropic/OpenAI console
- Set budget alerts if needed

---

## Troubleshooting

### Port already in use
```bash
python3 start_daemon.py --port 9000  # Use different port
```

### API key not found
```bash
export CLAUDE_API_KEY="sk-ant-..."
python3 start_daemon.py
```

### Daemon crashed
Check logs and restart:
```bash
python3 start_daemon.py
```

---

## 🚀 Your Personal ML Agent

The daemon is your **always-on ML orchestrator** running on your Claude/OpenAI subscription. Submit workflows, let Claude decide execution, and get results back via the API.

**It's like having a personal ML engineer working 24/7!**
