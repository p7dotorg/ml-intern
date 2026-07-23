#!/usr/bin/env python3
"""Run ML Agent CLI (interactive REPL)"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import asyncio
from ml_agent.agent_cli import main

if __name__ == "__main__":
    asyncio.run(main())
