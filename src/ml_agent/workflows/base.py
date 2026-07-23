# src/ml_agent/workflows/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
import structlog

@dataclass
class WorkflowStep:
    """Single step in a workflow."""
    name: str
    task: str  # Task for LLM
    validation: Optional[callable] = None

class Workflow(ABC):
    """Base class for all workflows."""

    name: str
    description: str

    def __init__(self, provider, config: Dict[str, Any] = None):
        self.provider = provider
        self.config = config or {}
        self.logger = structlog.get_logger(self.__class__.__name__)
        self.state = {}

    @abstractmethod
    async def execute(self) -> Dict[str, Any]:
        """Execute the workflow."""
        pass

    async def run_step(
        self,
        step: WorkflowStep,
        context: Dict = None
    ) -> str:
        """Execute a single workflow step."""
        context = context or {}

        self.logger.info(
            "Running step",
            step=step.name,
            task=step.task[:50]
        )

        # Get LLM response
        from ml_agent.providers.base import Message

        messages = [
            Message(role="user", content=step.task)
        ]

        response = await self.provider.complete(messages)

        # Validate if needed
        if step.validation:
            if not step.validation(response):
                raise ValueError(f"Validation failed for step {step.name}")

        return response

    def _save_state(self, key: str, value: Any):
        """Save state for later steps."""
        self.state[key] = value

    def _load_state(self, key: str) -> Any:
        """Load saved state."""
        return self.state.get(key)
