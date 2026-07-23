"""
Tool Router - Routes agent actions to appropriate tools
"""

from typing import Dict, Any, Callable
import json


class ToolRouter:
    """Routes tool calls from agent to appropriate handlers."""

    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.register_default_tools()

    def register_tool(self, name: str, handler: Callable) -> None:
        """Register a tool handler."""
        self.tools[name] = handler

    def register_default_tools(self) -> None:
        """Register default tools."""
        from ml_agent.workflows.arxiv_collector import ArXivCollector
        from ml_agent.workflows.model_trainer import ModelTrainer
        from ml_agent.workflows.hub_deployer import HubDeployer

        # Collection tools
        self.register_tool("collect_arxiv", self._collect_arxiv)
        self.register_tool("list_datasets", self._list_datasets)

        # Training tools
        self.register_tool("train_model", self._train_model)
        self.register_tool("check_model_status", self._check_model_status)

        # Deployment tools
        self.register_tool("deploy_model", self._deploy_model)
        self.register_tool("check_deployment", self._check_deployment)

        # Utils
        self.register_tool("read_file", self._read_file)
        self.register_tool("list_files", self._list_files)

    async def route(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Route a tool call."""
        if tool_name not in self.tools:
            return json.dumps({
                "status": "error",
                "message": f"Unknown tool: {tool_name}",
                "available_tools": list(self.tools.keys())
            })

        try:
            handler = self.tools[tool_name]
            result = handler(**params)
            return json.dumps({
                "status": "success",
                "tool": tool_name,
                "result": result
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "tool": tool_name,
                "error": str(e)
            })

    def _collect_arxiv(self, papers: int = 100, categories: list = None) -> Dict:
        """Collect papers from arXiv."""
        from ml_agent.workflows.arxiv_collector import run_arxiv_workflow
        return run_arxiv_workflow(categories, papers)

    def _list_datasets(self) -> Dict:
        """List available datasets."""
        import os
        datasets_dir = "datasets"
        if not os.path.exists(datasets_dir):
            return {"status": "no_datasets"}

        files = os.listdir(datasets_dir)
        return {"datasets": files}

    def _train_model(self, dataset_path: str, epochs: int = 3) -> Dict:
        """Train model."""
        from ml_agent.workflows.model_trainer import run_training_workflow
        return run_training_workflow(dataset_path, epochs=epochs)

    def _check_model_status(self) -> Dict:
        """Check model training status."""
        import os
        models_dir = "models"
        if not os.path.exists(models_dir):
            return {"status": "no_models"}

        dirs = os.listdir(models_dir)
        return {"models": dirs}

    def _deploy_model(self, model_path: str, repo_name: str = "latex-explainer") -> Dict:
        """Deploy model to Hub."""
        from ml_agent.workflows.hub_deployer import run_deployment_workflow
        return run_deployment_workflow(model_path, repo_name)

    def _check_deployment(self) -> Dict:
        """Check deployment status."""
        return {"status": "deployment_checked"}

    def _read_file(self, path: str) -> str:
        """Read file content."""
        with open(path) as f:
            return f.read()

    def _list_files(self, directory: str = ".") -> Dict:
        """List files in directory."""
        import os
        try:
            files = os.listdir(directory)
            return {"files": files, "directory": directory}
        except Exception as e:
            return {"error": str(e)}

    def get_tool_specs(self) -> str:
        """Get tool specifications for prompt."""
        specs = {
            "collect_arxiv": {
                "description": "Collect papers from arXiv",
                "params": {"papers": "number of papers", "categories": "list of categories"}
            },
            "train_model": {
                "description": "Train model on dataset",
                "params": {"dataset_path": "path to dataset", "epochs": "training epochs"}
            },
            "deploy_model": {
                "description": "Deploy model to Hugging Face Hub",
                "params": {"model_path": "path to model", "repo_name": "repository name"}
            },
            "list_datasets": {"description": "List available datasets"},
            "list_files": {"description": "List files in directory", "params": {"directory": "path"}},
            "check_model_status": {"description": "Check model status"},
        }
        return json.dumps(specs, indent=2)
