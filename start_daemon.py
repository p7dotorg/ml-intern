#!/usr/bin/env python3
"""
Start ML Agent Daemon Server
Runs 24/7, listening for workflow requests.

Usage:
  python3 start_daemon.py                    # Start on port 8000
  python3 start_daemon.py --port 9000        # Custom port
  python3 start_daemon.py --provider openai  # Use OpenAI
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.daemon_server import start_daemon

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Start ML Agent Daemon Server (runs 24/7)"
    )
    parser.add_argument(
        "--provider",
        default="claude",
        choices=["claude", "openai"],
        help="LLM provider",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Server port (default: 8000)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("🤖 ML Agent Daemon Server")
    print("=" * 60)
    print(f"Provider: {args.provider}")
    print(f"Port: {args.port}")
    print(f"URL: http://localhost:{args.port}")
    print()
    print("API Endpoints:")
    print(f"  POST http://localhost:{args.port}/api/workflow")
    print(f"  GET  http://localhost:{args.port}/api/status")
    print(f"  GET  http://localhost:{args.port}/api/history")
    print(f"  POST http://localhost:{args.port}/api/stop")
    print()
    print("Example:")
    print(f"  curl -X POST http://localhost:{args.port}/api/workflow \\")
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{{"workflow": "arxiv-dataset", "config": {{"papers_count": 100}}}}\'')
    print()
    print("Press Ctrl+C to stop daemon")
    print("=" * 60)
    print()

    start_daemon(provider=args.provider, port=args.port)
