"""
Complete LaTeX Dataset Pipeline
Orchestrates: Collection → Training → Deployment
"""

from ml_agent.workflows.arxiv_collector import run_arxiv_workflow
from ml_agent.workflows.model_trainer import run_training_workflow
from ml_agent.workflows.hub_deployer import run_deployment_workflow


def run_latex_pipeline(
    max_papers: int = 100,
    categories: list = None,
    model_name: str = "google/flan-t5-base",
    epochs: int = 3,
    deploy: bool = True,
):
    """Run complete LaTeX dataset pipeline."""
    if categories is None:
        categories = ["math.LA", "math.AP"]

    print("=" * 60)
    print("🚀 LaTeX Dataset Pipeline")
    print("=" * 60)

    # Step 1: Collect dataset
    print("\n[1/3] Collecting dataset from arXiv...")
    print("-" * 60)

    collection_result = run_arxiv_workflow(categories, max_papers)

    if collection_result["status"] != "completed":
        print(f"❌ Collection failed: {collection_result}")
        return collection_result

    dataset_path = collection_result["dataset_path"]
    print(f"\n✓ Dataset collected: {dataset_path}")

    # Step 2: Train model
    print("\n[2/3] Training model...")
    print("-" * 60)

    training_result = run_training_workflow(
        dataset_path, model_name=model_name, epochs=epochs
    )

    if training_result["status"] != "completed":
        print(f"❌ Training failed: {training_result}")
        return training_result

    model_path = training_result["model_path"]
    print(f"\n✓ Model trained: {model_path}")

    # Step 3: Deploy (optional)
    if deploy:
        print("\n[3/3] Deploying to Hugging Face Hub...")
        print("-" * 60)

        deployment_result = run_deployment_workflow(model_path)

        if deployment_result["status"] != "completed":
            print(f"❌ Deployment failed: {deployment_result}")
            return deployment_result

        print(f"\n✓ Model deployed: {deployment_result['hub_url']}")
    else:
        deployment_result = {"status": "skipped"}

    # Summary
    print("\n" + "=" * 60)
    print("✓ Pipeline completed successfully!")
    print("=" * 60)
    print(f"\nResults:")
    print(f"  📊 Dataset: {dataset_path}")
    print(f"  🤖 Model: {model_path}")
    if deploy:
        print(f"  🌐 Hub: {deployment_result['hub_url']}")

    return {
        "status": "completed",
        "dataset": dataset_path,
        "model": model_path,
        "deployment": deployment_result,
    }
