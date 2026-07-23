# 🤖 ML Agent CLI - Interactive REPL (Like pi.dev)

Run an **interactive AI agent** that orchestrates ML workflows autonomously. Just like pi.dev, but for ML workflows on your Claude/OpenAI subscription.

## Quick Start

```bash
export CLAUDE_API_KEY="sk-ant-..."
source venv/bin/activate
python3 run_agent.py
```

Welcome screen:
```
============================================================
🤖 ML Agent CLI
============================================================
Provider: claude
Model: claude-opus-4-8

Commands:
  /workflows - List available workflows
  /status - Show agent status
  /clear - Clear session
  /exit - Exit agent

Examples:
  Collect LaTeX dataset from arXiv
  Fine-tune a model on my dataset
  Deploy model to Hugging Face

Session saved to: ~/.ml-agent/cli_session.json
============================================================
```

## Usage Examples

### 1. Collect Dataset

```
You: Collect 100 papers from arXiv about LaTeX and math

🤖 Agent:
I'll collect 100 papers from arXiv about LaTeX and mathematics.
Starting the arxiv-dataset workflow...
[Executing Python code to fetch papers]
Successfully collected 100 papers! Saved to datasets/latex.jsonl
```

### 2. Fine-tune Model

```
You: Fine-tune flan-t5-base on the LaTeX dataset

🤖 Agent:
I'll fine-tune the model on your dataset.
Loading dataset from datasets/latex.jsonl...
[Training for 3 epochs]
Model saved to models/latex-explainer
Training complete! F1 score: 0.87
```

### 3. Deploy

```
You: Deploy the model to Hugging Face

🤖 Agent:
I'll deploy your model to Hugging Face Hub.
Pushing model to huggingface.co/your-user/latex-explainer...
Model deployed! URL: https://huggingface.co/your-user/latex-explainer
```

---

## Commands

### /workflows
List available workflows.

```
/workflows

Available workflows:
  • arxiv-dataset - Collect papers from arXiv
  • fine-tune - Fine-tune a model
  • deploy - Deploy to Hugging Face Hub
  • evaluate - Evaluate model performance
```

### /status
Show agent status.

```
/status

Status:
  Provider: claude
  Model: claude-opus-4-8
  Conversation turns: 5
  Session: ~/.ml-agent/cli_session.json
```

### /clear
Clear conversation history.

```
/clear
Session cleared ✓
```

### /exit
Exit the agent.

```
/exit
Bye! 👋
```

---

## How It Works

```
┌─────────────────────────────────────┐
│  You (User Input)                   │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  Claude Agent (Multi-turn)          │
│  - Understands request              │
│  - Plans workflow                   │
│  - Makes decisions                  │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  ML Workflows (Executed)            │
│  - Dataset collection               │
│  - Model training                   │
│  - Deployment                       │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  Results & Artifacts                │
│  - Models, datasets, logs           │
└─────────────────────────────────────┘
```

---

## Session Persistence

Every conversation is saved to `~/.ml-agent/cli_session.json`:

```json
{
  "conversation": [
    {
      "role": "user",
      "content": "Collect 100 papers from arXiv"
    },
    {
      "role": "assistant",
      "content": "I'll collect 100 papers... [results]"
    }
  ]
}
```

Resume conversation automatically on next run (context is loaded).

---

## Advanced Usage

### Use Different Provider

```bash
python3 run_agent.py --provider openai
```

### Resume Previous Session

```bash
python3 run_agent.py --resume
```

---

## Workflow Descriptions

### arxiv-dataset
Collect papers from arXiv and extract LaTeX expressions with explanations.

```
You: Collect 50 papers on differential equations from arXiv

🤖 Agent:
Collecting papers from arXiv category: math.AP
Extracting LaTeX expressions...
Generating explanations with Claude...
Saved 50 papers with 1,247 equations to datasets/latex.jsonl
```

### fine-tune
Fine-tune a model on your dataset.

```
You: Fine-tune a model on the collected dataset

🤖 Agent:
Loading dataset: datasets/latex.jsonl
Training flan-t5-base for 3 epochs...
[Training progress]
Final metrics:
  - Loss: 0.12
  - F1: 0.92
  - BLEU: 0.88
Model saved to models/latex-explainer
```

### deploy
Deploy trained model to Hugging Face Hub.

```
You: Deploy the model

🤖 Agent:
Pushing model to Hugging Face Hub...
Model card generated
Access URL: https://huggingface.co/your-user/latex-explainer
```

### evaluate
Evaluate model performance on test set.

```
You: Evaluate the model

🤖 Agent:
Running evaluation on test set...
[Metrics]
```

---

## Tips & Tricks

### 1. Multi-step Workflows
The agent remembers context, so you can do multi-step workflows:

```
You: Collect 100 papers, then fine-tune a model, then deploy

🤖 Agent: (Executes all steps autonomously)
```

### 2. Customize Workflows
Describe exactly what you want:

```
You: Collect papers from categories math.LA and math.AP, 
     extract only equations about linear algebra,
     fine-tune with batch size 64 for 5 epochs
```

### 3. Check Progress
Ask the agent to show progress:

```
You: What's the status of the training?

🤖 Agent: (Reports current status)
```

---

## Cost Estimation

- **Simple query**: ~1-5k tokens (~$0.01)
- **Dataset collection**: ~10-50k tokens (~$0.10-0.50)
- **Full pipeline**: ~50-200k tokens (~$0.50-2.00)

Monitor real-time usage in [Anthropic Console](https://console.anthropic.com/)

---

## Comparison with pi.dev

| Feature | pi.dev | ML Agent |
|---------|--------|----------|
| **Purpose** | Code development | ML workflows |
| **Interaction** | REPL (text input) | REPL (text input) |
| **Agent** | Coding agent | ML orchestrator |
| **Uses** | Your system resources | Claude/OpenAI API |
| **Session** | Saved locally | Saved locally |

Both work the same way: **You type → Agent thinks → Agent executes → You see results**

---

## 🚀 Your Personal ML Assistant

Like pi.dev, but tailored for ML workflows. Just describe what you want, and Claude figures out how to execute it on your subscription.

**It's like having an AI ML engineer on call 24/7!**
