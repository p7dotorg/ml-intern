#!/usr/bin/env python3
"""
ML Agent Daemon
Runs as an autonomous agent using your Claude/OpenAI subscription.
Executes workflows continuously or on schedule.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from ml_agent.core.agent import MLAgent
from ml_agent.core.config import Config
from ml_agent.core.logger import setup_logging

logger = logging.getLogger(__name__)


class AgentDaemon:
    """Autonomous ML Agent that runs on your subscription."""

    def __init__(self, provider: str = "claude", model: str = "claude-opus-4-8"):
        self.provider = provider
        self.model = model
        self.config = Config()
        self.client = Anthropic()
        self.session_file = Path.home() / ".ml-agent" / "daemon.json"
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_session()

    def _load_session(self) -> None:
        """Load daemon session history."""
        if self.session_file.exists():
            with open(self.session_file) as f:
                self.session = json.load(f)
        else:
            self.session = {"conversation": [], "workflows_completed": []}

    def _save_session(self) -> None:
        """Save daemon session history."""
        with open(self.session_file, "w") as f:
            json.dump(self.session, f, indent=2)

    async def execute_workflow_autonomous(
        self, workflow: str, config: dict | None = None
    ) -> dict:
        """
        Execute a workflow autonomously using Claude API.

        This runs on your subscription - Claude orchestrates the workflow
        and your ml-intern framework executes it.
        """
        config = config or {}
        logger.info(f"Starting autonomous workflow: {workflow}")

        # Build context for Claude
        workflow_context = f"""
You are an autonomous ML workflow executor.

Your task: Execute the {workflow} workflow
Configuration: {json.dumps(config, indent=2)}

The ml-intern framework is available in the user's environment.
You can:
1. Write Python code using ml-agent
2. Ask for status updates
3. Make decisions based on results
4. Execute the workflow step-by-step

Start by understanding what needs to be done, then execute it.
Report progress and final results.
"""

        # Add to conversation history
        self.session["conversation"].append(
            {"role": "user", "content": workflow_context}
        )

        # Call Claude with multi-turn conversation
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system="""You are an autonomous ML workflow executor running on the user's subscription.

Your capabilities:
- Execute Python code using ml-intern framework
- Access local file system
- Make API calls using user's credentials
- Store results and artifacts

Always be explicit about:
1. What you're about to do
2. Progress updates
3. Any errors and how you fixed them
4. Final results and artifact paths

Act autonomously - make decisions and execute without waiting for approval.""",
            messages=self.session["conversation"],
        )

        assistant_response = response.content[0].text
        self.session["conversation"].append(
            {"role": "assistant", "content": assistant_response}
        )

        # Log completion
        self.session["workflows_completed"].append(
            {
                "workflow": workflow,
                "config": config,
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
            }
        )

        self._save_session()
        logger.info(f"Workflow completed: {workflow}")

        return {
            "workflow": workflow,
            "status": "completed",
            "result": assistant_response,
            "timestamp": datetime.now().isoformat(),
        }

    async def run_scheduled_workflows(self, schedule: list[dict]) -> None:
        """
        Run workflows on a schedule.

        Example schedule:
        [
            {"workflow": "arxiv-dataset", "config": {...}, "cron": "0 2 * * *"},
            {"workflow": "fine-tune", "config": {...}, "cron": "0 6 * * 0"}
        ]
        """
        logger.info(f"Starting daemon with {len(schedule)} scheduled workflows")

        for item in schedule:
            workflow = item["workflow"]
            config = item.get("config", {})
            logger.info(f"Executing {workflow} on daemon subscription")

            result = await self.execute_workflow_autonomous(workflow, config)
            logger.info(f"Result: {result}")
            print(json.dumps(result, indent=2))

    def get_status(self) -> dict:
        """Get daemon status."""
        return {
            "provider": self.provider,
            "model": self.model,
            "workflows_completed": len(self.session["workflows_completed"]),
            "conversation_turns": len(self.session["conversation"]),
            "recent_workflows": self.session["workflows_completed"][-5:],
        }


async def main():
    """Example: Run daemon with scheduled workflows."""
    setup_logging()

    daemon = AgentDaemon(provider="claude")

    # Your workflow schedule
    schedule = [
        {
            "workflow": "arxiv-dataset",
            "config": {
                "output_file": "datasets/latex_explanations.jsonl",
                "papers_count": 100,
                "categories": ["math"],
            },
        }
    ]

    # Run workflows
    await daemon.run_scheduled_workflows(schedule)

    # Show status
    print("\n📊 Daemon Status:")
    print(json.dumps(daemon.get_status(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
