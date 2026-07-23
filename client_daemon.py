#!/usr/bin/env python3
"""
ML Agent Daemon Client
Send workflow requests to running daemon server.

Usage:
  # Start daemon (separate terminal)
  python3 start_daemon.py

  # Submit workflow (in another terminal)
  python3 client_daemon.py --workflow arxiv-dataset --papers 100
  python3 client_daemon.py status
  python3 client_daemon.py history
  python3 client_daemon.py stop
"""

import json
import sys
from pathlib import Path

import requests

BASE_URL = "http://localhost:8000/api"


def submit_workflow(workflow: str, config: dict) -> None:
    """Submit workflow to daemon."""
    print(f"📤 Submitting {workflow}...")

    response = requests.post(
        f"{BASE_URL}/workflow",
        json={"workflow": workflow, "config": config},
        timeout=300,
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ {result['status'].upper()}")
        if "result" in result:
            print(json.dumps(result["result"], indent=2))
    else:
        print(f"❌ Error: {response.text}")


def get_status() -> None:
    """Get daemon status."""
    print("📊 Daemon Status:")

    response = requests.get(f"{BASE_URL}/status", timeout=5)

    if response.status_code == 200:
        status = response.json()
        print(json.dumps(status, indent=2))
    else:
        print(f"❌ Error: {response.text}")


def get_history(limit: int = 10) -> None:
    """Get workflow history."""
    print(f"📜 Workflow History (last {limit}):")

    response = requests.get(f"{BASE_URL}/history?limit={limit}", timeout=5)

    if response.status_code == 200:
        history = response.json()
        for workflow in history["workflows"]:
            print(f"  • {workflow['workflow']} - {workflow['status']}")
    else:
        print(f"❌ Error: {response.text}")


def stop_daemon() -> None:
    """Stop daemon."""
    print("⏹️  Stopping daemon...")

    response = requests.post(f"{BASE_URL}/stop", timeout=5)

    if response.status_code == 200:
        print("✅ Daemon stopped")
    else:
        print(f"❌ Error: {response.text}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ML Agent Daemon Client")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Workflow command
    workflow_parser = subparsers.add_parser("workflow", help="Submit workflow")
    workflow_parser.add_argument(
        "--workflow", required=True, help="Workflow name (arxiv-dataset, fine-tune, deploy)"
    )
    workflow_parser.add_argument("--papers", type=int, help="Number of papers (for arxiv-dataset)")
    workflow_parser.add_argument("--categories", help="Comma-separated categories")

    # Other commands
    subparsers.add_parser("status", help="Show daemon status")
    subparsers.add_parser("history", help="Show workflow history")
    subparsers.add_parser("stop", help="Stop daemon")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "workflow":
            config = {}
            if args.papers:
                config["papers_count"] = args.papers
            if args.categories:
                config["categories"] = args.categories.split(",")

            submit_workflow(args.workflow, config)

        elif args.command == "status":
            get_status()

        elif args.command == "history":
            get_history()

        elif args.command == "stop":
            stop_daemon()

    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to daemon at {BASE_URL}")
        print("Start daemon with: python3 start_daemon.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
