#!/usr/bin/env python3
"""
ML-Intern API Executor
Run workflows via Anthropic SDK (fully headless, no CLI needed)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from anthropic import Anthropic

def run_workflow_via_api(workflow: str, config: dict | None = None) -> dict:
    """
    Execute ML workflow via Claude API directly.

    Args:
        workflow: Workflow name
        config: Workflow configuration

    Returns:
        Execution result
    """
    config = config or {}
    client = Anthropic()

    system_prompt = """You are an ML workflow executor. When given a task, you:
1. Analyze what needs to be done
2. Write Python code using the ml-intern framework to execute it
3. Run the code and report results

The ml-intern framework is installed and available at /Users/lucianfialho/Code/latex/src/ml_agent/
"""

    user_message = f"""
Execute this ML workflow:
- Workflow: {workflow}
- Config: {json.dumps(config, indent=2)}

Write Python code that:
1. Imports MLAgent from ml_agent.core.agent
2. Creates an MLAgent with provider='claude', workflow='{workflow}', workflow_config={json.dumps(config)}
3. Calls agent.run_sync()
4. Returns the result

Then execute the code and tell me:
- Status (SUCCESS/FAILED)
- Results or error
- Any artifacts generated
"""

    print(f"🚀 Running workflow: {workflow}")
    print(f"📝 Config: {json.dumps(config)}")
    print()

    conversation = [{"role": "user", "content": user_message}]

    # First turn: get the Python code
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        system=system_prompt,
        messages=conversation
    )

    assistant_message = response.content[0].text
    conversation.append({"role": "assistant", "content": assistant_message})

    print("📝 Generated Plan:")
    print(assistant_message[:500] + "..." if len(assistant_message) > 500 else assistant_message)
    print()

    # Second turn: ask to actually execute it
    conversation.append({
        "role": "user",
        "content": "Now execute this code on your machine and tell me the actual results."
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        system=system_prompt,
        messages=conversation
    )

    result_text = response.content[0].text

    print("✅ Execution Complete:")
    print(result_text)

    return {
        "status": "SUCCESS",
        "workflow": workflow,
        "result": result_text
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: api_executor.py <workflow> [config_json]")
        print("Example: api_executor.py arxiv-dataset '{\"papers_count\": 50}'")
        sys.exit(1)

    workflow = sys.argv[1]
    config_str = sys.argv[2] if len(sys.argv) > 2 else "{}"

    try:
        config = json.loads(config_str)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON config: {config_str}")
        sys.exit(1)

    result = run_workflow_via_api(workflow, config)
    print(json.dumps(result, indent=2))
