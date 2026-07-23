# src/ml_agent/workflows/dataset.py
import json
from pathlib import Path
from typing import Any, Dict
from ml_agent.workflows.base import Workflow, WorkflowStep
from ml_agent.workflows.registry import WorkflowRegistry

class ArXivDatasetWorkflow(Workflow):
    """Workflow to collect dataset from arXiv papers."""

    name = "arxiv-dataset"
    description = "Collect LaTeX expressions and explanations from arXiv"

    async def execute(self) -> Dict[str, Any]:
        """Execute dataset collection workflow."""
        output_file = Path(self.config.get("output_file", "dataset.jsonl"))

        self.logger.info("Starting dataset collection", output=str(output_file))

        # Step 1: Download papers (simulated)
        step1 = WorkflowStep(
            name="download_papers",
            task="List 10 popular math papers from arXiv in 2024"
        )
        papers = await self.run_step(step1)
        self._save_state("papers", papers)

        # Step 2: Extract equations
        step2 = WorkflowStep(
            name="extract_equations",
            task=f"From these papers: {papers[:200]}... extract LaTeX equations"
        )
        equations = await self.run_step(step2)
        self._save_state("equations", equations)

        # Step 3: Generate explanations
        step3 = WorkflowStep(
            name="generate_explanations",
            task=f"Generate Portuguese explanations for: {equations[:200]}..."
        )
        explanations = await self.run_step(step3)
        self._save_state("explanations", explanations)

        # Step 4: Validate dataset
        step4 = WorkflowStep(
            name="validate",
            task=f"Validate dataset quality: {explanations[:200]}..."
        )
        validation = await self.run_step(step4)

        self.logger.info("Dataset collection complete", validation=validation)

        return {
            "status": "success",
            "papers_processed": len(papers),
            "equations_found": len(equations),
            "explanations_generated": len(explanations),
            "output_file": str(output_file)
        }

# Register the workflow
WorkflowRegistry.register("arxiv-dataset", ArXivDatasetWorkflow)
