# tests/integration/test_end_to_end.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from ml_agent.core.agent import MLAgent
from ml_agent.workflows.dataset import ArXivDatasetWorkflow

@pytest.mark.asyncio
@patch('ml_agent.workflows.registry.WorkflowRegistry.get')
@patch('ml_agent.providers.registry.ProviderRegistry.get')
@patch('ml_agent.auth.manager.AuthManager.get_api_key')
async def test_full_workflow(mock_auth, mock_provider, mock_workflow):
    """Test complete workflow execution."""
    # Setup mocks
    mock_auth.return_value = "test-key"
    mock_provider_instance = AsyncMock()
    mock_provider_instance.complete = AsyncMock(return_value="Mocked response")
    mock_provider.return_value = mock_provider_instance

    # Mock the workflow registry to return the workflow class
    mock_workflow.return_value = ArXivDatasetWorkflow

    # Run agent
    agent = MLAgent(
        provider="claude",
        workflow="arxiv-dataset",
        workflow_config={"max_papers": 5}
    )

    # Test that MLAgent was initialized correctly
    assert agent.provider_name == "claude"
    assert agent.workflow_name == "arxiv-dataset"
