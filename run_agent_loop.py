#!/usr/bin/env python3
"""
Run ML Agent with Agentic Loop
Autonomous agent that collects, trains, and deploys LaTeX models
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.core.agentic_loop import run_agent


async def main():
    task = """
    Complete the LaTeX ML pipeline:

    1. Collect 20 papers from arXiv with LaTeX expressions (math.LA, math.AP categories)
    2. Extract and create dataset (latex_explanations.jsonl)
    3. Fine-tune google/flan-t5-base on the dataset (3 epochs)
    4. Save the trained model to models/latex-explainer/

    Report progress after each major step.
    """

    print("=" * 60)
    print("🤖 ML Agent - Autonomous LaTeX Pipeline")
    print("=" * 60)

    result = await run_agent(task)

    print("\n" + "=" * 60)
    print("📊 Final Summary")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Total tokens: {result['tokens']}")
    print(f"Context: {result['context']}")


if __name__ == "__main__":
    asyncio.run(main())
