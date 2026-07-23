import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from ml_agent.core.agent import MLAgent
from ml_agent.core.config import Config

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization."""
    with patch('ml_agent.auth.manager.AuthManager.get_api_key', return_value="test-key"):
        with patch('ml_agent.providers.registry.ProviderRegistry.get') as mock_get:
            with patch('ml_agent.workflows.registry.WorkflowRegistry.get') as mock_workflow:
                mock_provider = AsyncMock()
                mock_get.return_value = mock_provider
                mock_workflow_class = MagicMock()
                mock_workflow.return_value = mock_workflow_class

                agent = MLAgent(
                    provider="claude",
                    workflow="arxiv-dataset",
                )

                assert agent.provider_name == "claude"
                assert agent.workflow_name == "arxiv-dataset"
