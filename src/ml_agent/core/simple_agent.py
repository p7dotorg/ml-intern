"""
Simple ML Agent - Works with Claude API or Codex (Claude Code)
No OAuth, no complexity. Just works.
"""

import subprocess
import json
from typing import Optional
from anthropic import Anthropic


class SimpleAgent:
    """ML Agent that uses Claude API or Codex."""

    def __init__(self, mode: str = "auto"):
        """
        Initialize agent.

        Modes:
        - "claude": Use Claude API
        - "codex": Use Codex (Claude Code)
        - "auto": Try Codex first, fallback to Claude
        """
        self.mode = mode
        self.client = Anthropic()
        self.conversation = []

    def _use_codex(self, prompt: str) -> Optional[str]:
        """Use Codex (Claude Code) via subprocess."""
        try:
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=300,
            )
            return result.stdout if result.returncode == 0 else None
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None

    def _use_claude_api(self, prompt: str) -> str:
        """Use Claude API directly."""
        self.conversation.append({"role": "user", "content": prompt})

        response = self.client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            system="""You are an ML workflow executor.
Execute tasks autonomously, write code when needed, report results.
Be direct and concise.""",
            messages=self.conversation,
        )

        assistant_response = response.content[0].text
        self.conversation.append({"role": "assistant", "content": assistant_response})

        return assistant_response

    def run(self, prompt: str) -> str:
        """Run prompt using configured mode."""
        if self.mode == "codex":
            result = self._use_codex(prompt)
            if result:
                return result
            raise RuntimeError("Codex not available")

        elif self.mode == "claude":
            return self._use_claude_api(prompt)

        elif self.mode == "auto":
            # Try Codex first
            result = self._use_codex(prompt)
            if result:
                return result

            # Fall back to Claude API
            return self._use_claude_api(prompt)

        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def chat(self, prompt: str) -> str:
        """Run and return response."""
        return self.run(prompt)


# Easy to use
def run_workflow(workflow: str, config: dict, mode: str = "auto") -> str:
    """Run a workflow."""
    agent = SimpleAgent(mode=mode)

    prompt = f"""Execute workflow: {workflow}
Config: {json.dumps(config, indent=2)}

Steps:
1. Understand the task
2. Execute it
3. Return results"""

    return agent.run(prompt)
