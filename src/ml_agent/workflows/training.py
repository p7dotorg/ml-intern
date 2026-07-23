# src/ml_agent/workflows/training.py
from typing import Any, Dict
from ml_agent.workflows.base import Workflow, WorkflowStep
from ml_agent.workflows.registry import WorkflowRegistry

class FineTuneWorkflow(Workflow):
    """Workflow to fine-tune a model."""

    name = "fine-tune"
    description = "Fine-tune a model on custom dataset"

    async def execute(self) -> Dict[str, Any]:
        """Execute fine-tuning workflow."""
        dataset_file = self.config.get("dataset_file", "dataset.jsonl")
        model_name = self.config.get("model", "google/flan-t5-small")

        self.logger.info("Starting fine-tuning", model=model_name, dataset=dataset_file)

        # Step 1: Prepare dataset
        step1 = WorkflowStep(
            name="prepare_dataset",
            task=f"Prepare and validate dataset from {dataset_file}"
        )
        prep = await self.run_step(step1)
        self._save_state("prep", prep)

        # Step 2: Setup training
        step2 = WorkflowStep(
            name="setup_training",
            task=f"Setup training environment for {model_name} on prepared dataset"
        )
        setup = await self.run_step(step2)
        self._save_state("setup", setup)

        # Step 3: Train model
        step3 = WorkflowStep(
            name="train",
            task=f"Train {model_name} with learning_rate=5e-5, epochs=3"
        )
        training = await self.run_step(step3)
        self._save_state("training", training)

        # Step 4: Evaluate
        step4 = WorkflowStep(
            name="evaluate",
            task="Evaluate trained model on test set and report metrics"
        )
        evaluation = await self.run_step(step4)

        self.logger.info("Fine-tuning complete")

        return {
            "status": "success",
            "model": model_name,
            "training_metrics": evaluation,
            "output_path": "./models/fine-tuned"
        }

# Register the workflow
WorkflowRegistry.register("fine-tune", FineTuneWorkflow)
