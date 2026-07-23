#!/usr/bin/env python3
"""
Run complete LaTeX dataset pipeline
Collect → Train → Deploy
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.workflows.latex_pipeline import run_latex_pipeline


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LaTeX Dataset Pipeline")
    parser.add_argument(
        "--papers", type=int, default=100, help="Number of papers to collect"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=["math.LA", "math.AP"],
        help="arXiv categories",
    )
    parser.add_argument(
        "--epochs", type=int, default=3, help="Training epochs"
    )
    parser.add_argument(
        "--model",
        default="google/flan-t5-base",
        help="Base model for fine-tuning",
    )
    parser.add_argument(
        "--no-deploy",
        action="store_true",
        help="Skip deployment to Hub",
    )

    args = parser.parse_args()

    # Run pipeline
    result = run_latex_pipeline(
        max_papers=args.papers,
        categories=args.categories,
        model_name=args.model,
        epochs=args.epochs,
        deploy=not args.no_deploy,
    )

    # Exit with status
    sys.exit(0 if result["status"] == "completed" else 1)
