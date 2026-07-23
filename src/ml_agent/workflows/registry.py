# src/ml_agent/workflows/registry.py
from typing import Dict, Type
from ml_agent.workflows.base import Workflow

class WorkflowRegistry:
    """Registry for available workflows."""

    _workflows: Dict[str, Type[Workflow]] = {}

    @classmethod
    def register(cls, name: str, workflow_class: Type[Workflow]):
        """Register a workflow."""
        cls._workflows[name] = workflow_class

    @classmethod
    def get(cls, name: str) -> Type[Workflow]:
        """Get workflow class."""
        if name not in cls._workflows:
            raise ValueError(f"Unknown workflow: {name}")
        return cls._workflows[name]

    @classmethod
    def list_available(cls) -> list[str]:
        """List all available workflows."""
        return list(cls._workflows.keys())
