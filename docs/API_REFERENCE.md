# ML Agent Framework - API Reference

## Core Classes

### MLAgent
Main orchestrator for ML workflows.

```python
from ml_agent.core.agent import MLAgent

agent = MLAgent(
    provider="claude",
    workflow="arxiv-dataset",
    workflow_config={"output_file": "dataset.jsonl"}
)

result = agent.run_sync()
```

### Workflow
Base class for workflows.

```python
from ml_agent.workflows.base import Workflow

class MyWorkflow(Workflow):
    name = "my-workflow"

    async def execute(self):
        step = WorkflowStep(...)
        await self.run_step(step)
```

## Providers

- `claude` - Anthropic Claude
- `openai` - OpenAI GPT
- `deepseek` - DeepSeek (via plugins)
- `mistral` - Mistral AI (via plugins)

## Workflows

- `arxiv-dataset` - Collect dataset from arXiv
- `fine-tune` - Fine-tune model
- `deploy-hub` - Deploy to Hugging Face Hub
