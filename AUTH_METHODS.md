# 🔐 Authentication Methods

ML-Agent supports **both API keys AND subscription-based OAuth** (like pi.dev).

---

## Method 1: API Keys (Simple)

Use your API keys directly from Claude/OpenAI.

### Claude API Key

```bash
export CLAUDE_API_KEY="sk-ant-..."
python3 run_agent.py
```

### OpenAI API Key

```bash
export OPENAI_API_KEY="sk-..."
python3 run_agent.py
```

---

## Method 2: Subscription-Based OAuth (Like pi.dev)

Use your **Claude Pro**, **ChatGPT Plus**, or other subscriptions!

### Login

```bash
ml-agent login claude      # Login to Claude Pro
ml-agent login openai      # Login to ChatGPT Plus
```

This opens OAuth flow:
1. Redirects to Claude.ai / ChatGPT login
2. You authenticate and grant permission
3. Token saved to `~/.ml-agent/auth.json`
4. Auto-refreshes when expired

### Check Subscriptions

```bash
ml-agent status
```

Output:
```
Active Subscriptions:
  ✓ Claude Pro (claude)
  ✓ ChatGPT Plus (openai)

Credentials:
  API Keys: 0
  OAuth Subscriptions: 2
```

---

## Method 3: auth.json File

Manual configuration with both API keys and subscriptions:

```json
{
  "api_keys": {
    "claude": "sk-ant-...",
    "openai": "sk-..."
  },
  "oauth": {
    "claude": {
      "auth_code": "...",
      "subscription": "claude-pro",
      "type": "oauth"
    },
    "openai": {
      "auth_code": "...",
      "subscription": "chatgpt-plus",
      "type": "oauth"
    }
  }
}
```

Location: `~/.ml-agent/auth.json` (chmod 600)

---

## Authentication Priority

When running ml-agent, it checks credentials in this order:

1. **CLI flag**: `--api-key "sk-ant-..."`
2. **OAuth subscription**: `~/.ml-agent/auth.json` (if logged in)
3. **Environment variables**: `CLAUDE_API_KEY`, `OPENAI_API_KEY`
4. **auth.json file**: API keys section
5. **Interactive prompt**: Ask user

---

## Comparison

| Method | Setup | Cost | Renewal |
|--------|-------|------|---------|
| **API Key** | `export CLAUDE_API_KEY=...` | Pay-as-you-go | Manual |
| **Subscription OAuth** | `ml-agent login claude` | Monthly subscription | Auto |

---

## Examples

### Example 1: Use Claude Pro (subscription)

```bash
# First time
ml-agent login claude
# → Opens claude.ai, you authenticate
# → Token saved to auth.json

# Next runs
python3 run_agent.py
# → Automatically uses Claude Pro
```

### Example 2: Use ChatGPT Plus (subscription)

```bash
ml-agent login openai
python3 run_agent.py
```

### Example 3: Mix API Keys + Subscriptions

```bash
export CLAUDE_API_KEY="sk-ant-..."  # API key
ml-agent login openai               # Subscription

python3 run_agent.py
# → Uses ChatGPT Plus (subscription) first
# → Falls back to Claude API key if needed
```

---

## Troubleshooting

### "No credentials found"

Check what you have configured:

```bash
ml-agent status

# If nothing, do:
export CLAUDE_API_KEY="sk-ant-..."  # OR
ml-agent login claude
```

### "OAuth token expired"

Auto-refreshes on next run. If issues persist:

```bash
rm ~/.ml-agent/auth.json
ml-agent login claude  # Re-authenticate
```

### "Permission denied on auth.json"

Fix permissions:

```bash
chmod 600 ~/.ml-agent/auth.json
```

---

## Security

✅ **Safe:**
- Credentials stored locally (not cloud)
- `auth.json` has chmod 600 (owner only)
- OAuth tokens auto-refresh
- No telemetry or logging of credentials

⚠️ **Be careful:**
- Don't commit `auth.json` to git
- Don't share API keys in messages
- Use subscription auth over API keys when possible

---

## Cost Comparison

### API Key Method
- **Cost**: Pay Claude/OpenAI directly per token
- **Example**: 1M tokens ≈ $3-15 depending on model
- **Best for**: Occasional use, testing

### Subscription Method (Claude Pro / ChatGPT Plus)
- **Cost**: $20/month (Claude Pro) or $20/month (ChatGPT Plus)
- **Benefit**: Unlimited usage within allowances
- **Best for**: Regular/heavy usage

**For ML workflows, subscription usually cheaper!**

---

**Choose your auth method and start using ml-agent! 🚀**
