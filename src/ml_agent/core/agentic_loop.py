"""
Agentic Loop - Iterates until task completion
Similar to Hugging Face ml-intern's submission loop
"""

import json
import re
from typing import Dict, Optional
from anthropic import Anthropic
from ml_agent.core.context_manager import ContextManager
from ml_agent.core.tool_router import ToolRouter


class DoomLoopDetector:
    """Detects repeated patterns that indicate doom loops."""

    def __init__(self, window_size: int = 5):
        self.window_size = window_size
        self.action_history = []

    def add_action(self, action: str) -> None:
        """Add action to history."""
        self.action_history.append(action)

    def is_doom_loop(self) -> bool:
        """Check if we're in a doom loop."""
        if len(self.action_history) < self.window_size:
            return False

        # Check if last N actions are identical
        recent = self.action_history[-self.window_size:]
        return len(set(recent)) == 1

    def get_latest_actions(self, n: int = 5) -> list:
        """Get latest N actions."""
        return self.action_history[-n:]


class AgenticLoop:
    """Main agent loop - iterates until task completion."""

    def __init__(self, provider: str = "claude"):
        self.client = Anthropic()
        self.context = ContextManager()
        self.router = ToolRouter()
        self.doom_detector = DoomLoopDetector()
        self.max_iterations = 300
        self.iteration = 0

    def get_system_prompt(self) -> str:
        """System prompt for the agent."""
        return f"""You are an autonomous ML research agent.

Your task: Collect LaTeX datasets, train models, and deploy them to Hugging Face Hub.

Available tools:
{self.router.get_tool_specs()}

For each turn:
1. Analyze the current state
2. Decide the next action
3. Call a tool with: <tool_call>
{{
  "tool": "tool_name",
  "params": {{"key": "value"}}
}}
</tool_call>
4. Interpret results and continue

Guidelines:
- Be autonomous - make decisions without asking
- Iterate until completion
- Report progress after each step
- Handle failures gracefully
- Stop when task is complete"""

    async def run(self, task: str, max_iterations: int = 300) -> Dict:
        """Run the agentic loop."""
        self.max_iterations = max_iterations
        self.iteration = 0

        # Initial prompt
        self.context.add_message("user", task)

        print(f"\n🤖 Starting agentic loop...")
        print(f"📋 Task: {task}\n")

        while self.iteration < self.max_iterations:
            self.iteration += 1
            print(f"[Iteration {self.iteration}/{self.max_iterations}]")

            # Get response from Claude
            response = self.client.messages.create(
                model="claude-opus-4-8",
                max_tokens=2048,
                system=self.get_system_prompt(),
                messages=self.context.get_messages(),
            )

            assistant_message = response.content[0].text
            self.context.add_message("assistant", assistant_message)

            print(f"Agent: {assistant_message[:200]}...\n")

            # Check for doom loop
            if self.doom_detector.is_doom_loop():
                print("⚠️ Doom loop detected! Injecting recovery prompt...")
                recovery = "You seem to be repeating the same action. Try a different approach."
                self.context.add_message("system", recovery)
                continue

            # Parse and execute tool calls
            tool_calls = self._parse_tool_calls(assistant_message)

            if not tool_calls:
                # No tool calls - might be done
                if "complete" in assistant_message.lower() or "done" in assistant_message.lower():
                    print("✓ Task appears complete!")
                    break
                continue

            # Execute tools
            for tool_name, params in tool_calls:
                print(f"  → Calling: {tool_name}({params})")

                result = await self.router.route(tool_name, params)
                self.context.add_action(tool_name, tool_name, result)
                self.doom_detector.add_action(tool_name)

                # Add result to context
                self.context.add_message("user", f"Tool result:\n{result}")

                print(f"    Result: {result[:100]}...\n")

        # Final summary
        return {
            "status": "completed" if self.iteration < self.max_iterations else "max_iterations_reached",
            "iterations": self.iteration,
            "messages": len(self.context.messages),
            "tokens": self.context.estimate_tokens(),
            "context": self.context.get_summary(),
        }

    def _parse_tool_calls(self, text: str) -> list:
        """Parse tool calls from agent response."""
        # Look for <tool_call>...</tool_call> blocks
        pattern = r"<tool_call>\s*(.*?)\s*</tool_call>"
        matches = re.findall(pattern, text, re.DOTALL)

        tool_calls = []
        for match in matches:
            try:
                data = json.loads(match)
                tool_calls.append((data["tool"], data.get("params", {})))
            except json.JSONDecodeError:
                continue

        return tool_calls


async def run_agent(task: str) -> Dict:
    """Convenience function to run agent."""
    loop = AgenticLoop()
    return await loop.run(task)
