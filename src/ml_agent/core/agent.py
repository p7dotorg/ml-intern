import asyncio
from typing import Any, Dict, Optional
import structlog
from ml_agent.core.config import Config
from ml_agent.auth.manager import AuthManager
from ml_agent.providers.registry import ProviderRegistry
from ml_agent.workflows.registry import WorkflowRegistry
from ml_agent.core.exceptions import MLAgentException

class MLAgent:
    """Main orchestrator for ML workflows."""

    def __init__(
        self,
        provider: str,
        workflow: str,
        config: Config = None,
        api_key: Optional[str] = None,
        workflow_config: Dict[str, Any] = None,
    ):
        self.provider_name = provider
        self.workflow_name = workflow
        self.config = config or Config()
        self.workflow_config = workflow_config or {}
        self.logger = structlog.get_logger("MLAgent")

        # Setup
        self.config.ensure_directories()

        # Auth
        self.auth_manager = AuthManager(
            auth_file=self.config.auth_file,
            cli_api_key=api_key
        )

        # Get provider
        provider_key = self.auth_manager.get_api_key(provider)
        self.provider = ProviderRegistry.get(provider, provider_key)

        # Get workflow
        self.workflow_class = WorkflowRegistry.get(workflow)

    async def run(self) -> Dict[str, Any]:
        """Run the workflow."""
        self.logger.info(
            "Starting workflow",
            provider=self.provider_name,
            workflow=self.workflow_name
        )

        try:
            # Instantiate and execute workflow
            workflow = self.workflow_class(
                provider=self.provider,
                config=self.workflow_config
            )

            result = await workflow.execute()

            self.logger.info("Workflow complete", result=result)
            return result

        except Exception as e:
            self.logger.error("Workflow failed", error=str(e))
            raise

    def run_sync(self) -> Dict[str, Any]:
        """Run workflow synchronously."""
        return asyncio.run(self.run())
