#!/usr/bin/env python3
"""
ML Agent CLI - Interactive REPL Agent (like pi.dev)
Run workflows interactively with Claude orchestrating execution.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

from anthropic import Anthropic

from ml_agent.core.config import Config
from ml_agent.core.logger import setup_logging


class AgentCLI:
    """Interactive CLI Agent - like pi.dev but for ML workflows."""

    def __init__(self, provider: str = "claude"):
        self.provider = provider
        self.client = Anthropic()
        self.config = Config()
        self.conversation = []
        self.model = "claude-opus-4-8"
        self.session_file = Path.home() / ".ml-agent" / "cli_session.json"
        self.session_file.parent.mkdir(parents=True, exist_ok=True)

    def _load_session(self) -> None:
        """Load previous conversation."""
        if self.session_file.exists():
            with open(self.session_file) as f:
                data = json.load(f)
                self.conversation = data.get("conversation", [])
        else:
            self.conversation = []

    def _save_session(self) -> None:
        """Save conversation."""
        with open(self.session_file, "w") as f:
            json.dump({"conversation": self.conversation}, f, indent=2)

    async def chat(self, user_input: str) -> str:
        """Send message to Claude and get response."""
        self.conversation.append({"role": "user", "content": user_input})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system="""You are an autonomous ML workflow agent.

Your capabilities:
- Execute ML workflows (arxiv-dataset, fine-tune, deploy)
- Write and run Python code using ml-intern framework
- Make decisions about workflow execution
- Process data and generate results
- Store artifacts locally

When the user asks you to do something:
1. Understand the request
2. Plan the approach
3. Execute step-by-step
4. Report results

Always be explicit about what you're doing and provide progress updates.
Use code blocks when executing Python.""",
            messages=self.conversation,
        )

        assistant_response = response.content[0].text
        self.conversation.append({"role": "assistant", "content": assistant_response})
        self._save_session()

        return assistant_response

    def print_welcome(self) -> None:
        """Print welcome message."""
        print("\n" + "=" * 60)
        print("🤖 ML Agent CLI")
        print("=" * 60)
        print(f"Provider: {self.provider}")
        print(f"Model: {self.model}")
        print()
        print("Commands:")
        print("  /workflows - List available workflows")
        print("  /status - Show agent status")
        print("  /clear - Clear session")
        print("  /exit - Exit agent")
        print()
        print("Examples:")
        print("  Collect LaTeX dataset from arXiv")
        print("  Fine-tune a model on my dataset")
        print("  Deploy model to Hugging Face")
        print()
        print("Session saved to: ~/.ml-agent/cli_session.json")
        print("=" * 60)
        print()

    def handle_command(self, command: str) -> Optional[str]:
        """Handle special commands."""
        if command == "/workflows":
            return """Available workflows:
  • arxiv-dataset - Collect papers from arXiv
  • fine-tune - Fine-tune a model
  • deploy - Deploy to Hugging Face Hub
  • evaluate - Evaluate model performance"""

        elif command == "/status":
            return f"""Status:
  Provider: {self.provider}
  Model: {self.model}
  Conversation turns: {len(self.conversation) // 2}
  Session: {self.session_file}"""

        elif command == "/clear":
            self.conversation = []
            self._save_session()
            return "Session cleared ✓"

        elif command == "/exit":
            return None

        return None

    async def run_repl(self) -> None:
        """Run interactive REPL."""
        self._load_session()
        self.print_welcome()

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.startswith("/"):
                    result = self.handle_command(user_input)
                    if result is None:
                        print("Bye! 👋")
                        break
                    print(f"\n{result}\n")
                    continue

                # Send to Claude
                print("\n🤖 Agent:")
                response = await self.chat(user_input)
                print(response)
                print()

            except KeyboardInterrupt:
                print("\n\nBye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")


async def main():
    """Run agent CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="ML Agent CLI - Interactive workflow executor"
    )
    parser.add_argument(
        "--provider",
        default="claude",
        choices=["claude", "openai"],
        help="LLM provider",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume previous session",
    )

    args = parser.parse_args()

    setup_logging()
    agent = AgentCLI(provider=args.provider)

    await agent.run_repl()


if __name__ == "__main__":
    asyncio.run(main())
