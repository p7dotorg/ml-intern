# tests/unit/test_workflows.py
import pytest
from ml_agent.workflows.base import Workflow, WorkflowStep
from ml_agent.workflows.registry import WorkflowRegistry

class TestWorkflow(Workflow):
    name = "test"
    description = "Test workflow"

    async def execute(self):
        return {"status": "success"}

def test_workflow_step():
    """Test workflow step creation."""
    step = WorkflowStep(name="test_step", task="Test task")
    assert step.name == "test_step"

def test_workflow_registry():
    """Test workflow registry."""
    WorkflowRegistry.register("test", TestWorkflow)
    assert "test" in WorkflowRegistry.list_available()
    assert WorkflowRegistry.get("test") == TestWorkflow

def test_workflow_unknown():
    """Test error on unknown workflow."""
    with pytest.raises(ValueError):
        WorkflowRegistry.get("unknown")
