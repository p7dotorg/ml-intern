#!/usr/bin/env python3
"""Run ML Agent Daemon directly"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.agent_daemon import AgentDaemon
from ml_agent.core.logger import setup_logging

async def main():
    setup_logging()

    # Example: Run arxiv-dataset workflow
    daemon = AgentDaemon(provider="claude")

    print("🚀 Starting autonomous workflow...")
    print("📊 Workflow: arxiv-dataset")
    print("💾 Config: Collect 100 LaTeX math papers\n")

    result = await daemon.execute_workflow_autonomous(
        "arxiv-dataset",
        {
            "output_file": "datasets/latex_explanations.jsonl",
            "papers_count": 100,
            "categories": ["math.LA", "math.AP"],
            "max_equations_per_paper": 20,
        }
    )

    print("\n✅ Workflow Result:")
    print(json.dumps(result, indent=2))

    # Show status
    print("\n📊 Daemon Status:")
    print(json.dumps(daemon.get_status(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
