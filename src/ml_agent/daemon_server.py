#!/usr/bin/env python3
"""
ML Agent Daemon Server
Runs 24/7, listening for workflow requests via HTTP API or CLI.
Like pi.dev but for ML workflows on your subscription.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

from ml_agent.agent_daemon import AgentDaemon
from ml_agent.core.logger import setup_logging

logger = logging.getLogger(__name__)

app = FastAPI(title="ML Agent Daemon", version="1.0.0")


class DaemonServer:
    """24/7 running ML Agent Daemon Server."""

    def __init__(self, provider: str = "claude", port: int = 8000):
        self.provider = provider
        self.port = port
        self.daemon = AgentDaemon(provider=provider)
        self.running = False
        self.queue: list[dict] = []

    @app.post("/api/workflow")
    async def submit_workflow(self, request: dict) -> dict:
        """Submit a workflow to execute."""
        workflow = request.get("workflow")
        config = request.get("config", {})

        if not workflow:
            raise HTTPException(status_code=400, detail="workflow required")

        logger.info(f"Received workflow: {workflow}", extra={"config": config})

        # Execute immediately (or queue if busy)
        try:
            result = await self.daemon.execute_workflow_autonomous(workflow, config)
            return {"status": "completed", "result": result}
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return {"status": "failed", "error": str(e)}

    @app.get("/api/status")
    async def get_status(self) -> dict:
        """Get daemon status."""
        return self.daemon.get_status()

    @app.get("/api/history")
    async def get_history(self, limit: int = 10) -> dict:
        """Get workflow history."""
        history = self.daemon.session.get("workflows_completed", [])
        return {"workflows": history[-limit:]}

    @app.post("/api/stop")
    async def stop_daemon(self) -> dict:
        """Stop daemon gracefully."""
        self.running = False
        return {"status": "stopped"}

    async def run(self) -> None:
        """Run daemon server."""
        self.running = True
        logger.info(f"Starting daemon on port {self.port}")
        logger.info(f"Provider: {self.provider}")
        logger.info("API endpoints:")
        logger.info("  POST /api/workflow - Submit workflow")
        logger.info("  GET  /api/status - Get daemon status")
        logger.info("  GET  /api/history - Get workflow history")
        logger.info("  POST /api/stop - Stop daemon")

        config = uvicorn.Config(
            app=app,
            host="127.0.0.1",
            port=self.port,
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()


def start_daemon(provider: str = "claude", port: int = 8000) -> None:
    """Start the daemon server."""
    setup_logging()
    server = DaemonServer(provider=provider, port=port)
    asyncio.run(server.run())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ML Agent Daemon Server")
    parser.add_argument(
        "--provider", default="claude", help="LLM provider (claude, openai)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    args = parser.parse_args()

    start_daemon(provider=args.provider, port=args.port)
