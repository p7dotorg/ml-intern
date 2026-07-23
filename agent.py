#!/usr/bin/env python3
"""
ML Agent CLI - Works with Claude API or Codex
Simple. No OAuth. No complexity.

Usage:
  python3 agent.py "collect 100 papers"      # Auto (tries Codex first)
  python3 agent.py --codex "collect papers"  # Force Codex
  python3 agent.py --claude "collect papers" # Force Claude API
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.core.simple_agent import SimpleAgent


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ML Agent - Multi-mode executor")
    parser.add_argument("prompt", nargs="+", help="Task to execute")
    parser.add_argument(
        "--mode",
        choices=["auto", "claude", "codex"],
        default="auto",
        help="Execution mode (default: auto)",
    )

    args = parser.parse_args()
    prompt = " ".join(args.prompt)

    print(f"🤖 Executing: {prompt}\n")

    agent = SimpleAgent(mode=args.mode)

    try:
        result = agent.run(prompt)
        print(result)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
