#!/usr/bin/env python3
"""
ML-Intern Headless Executor
Run workflows via Claude CLI in non-interactive mode
"""

import json
import subprocess
import sys
from pathlib import Path

def run_workflow_headless(workflow: str, config: dict | None = None) -> dict:
    """
    Execute an ML workflow via Claude CLI headless mode.

    Args:
        workflow: Workflow name (e.g., 'arxiv-dataset', 'fine-tune', 'deploy')
        config: Workflow configuration dict

    Returns:
        dict with status, artifacts, and summary
    """
    config = config or {}

    prompt = f"""
You are an ML workflow executor. Execute the following ML workflow:

Workflow: {workflow}
Config: {json.dumps(config, indent=2)}

Use Python with the ml-intern framework (already installed locally).

Execute this Python code:
```python
import sys
sys.path.insert(0, '/Users/lucianfialho/Code/latex/src')

from ml_agent.core.agent import MLAgent

try:
    agent = MLAgent(
        provider='claude',
        workflow='{workflow}',
        workflow_config={json.dumps(config)}
    )
    result = agent.run_sync()
    print(json.dumps({{
        "status": "SUCCESS",
        "result": str(result),
        "workflow": "{workflow}"
    }}))
except Exception as e:
    print(json.dumps({{
        "status": "FAILED",
        "error": str(e),
        "workflow": "{workflow}"
    }}))
```

Run this Python code and return the JSON output.
"""

    print(f"🚀 Running workflow in headless mode: {workflow}")
    print(f"📝 Config: {json.dumps(config)}")
    print()

    # Run Claude CLI in headless mode
    result = subprocess.run(
        [
            "claude",
            "-p",
            "--output-format", "json",
            "--add-dir", "/Users/lucianfialho/Code/latex",
            prompt
        ],
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode != 0:
        print(f"❌ Workflow execution failed")
        print(f"STDERR: {result.stderr}")
        return {
            "status": "FAILED",
            "error": result.stderr
        }

    try:
        output = json.loads(result.stdout)
        print(f"✅ Workflow completed: {workflow}")
        print(json.dumps(output, indent=2))
        return output
    except json.JSONDecodeError:
        return {
            "status": "SUCCESS",
            "output": result.stdout
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: headless_executor.py <workflow> [config_json]")
        print("Example: headless_executor.py arxiv-dataset '{\"papers_count\": 50}'")
        sys.exit(1)

    workflow = sys.argv[1]
    config_str = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        config = json.loads(config_str)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON config: {config_str}")
        sys.exit(1)

    result = run_workflow_headless(workflow, config)
    sys.exit(0 if result.get("status") == "SUCCESS" else 1)
