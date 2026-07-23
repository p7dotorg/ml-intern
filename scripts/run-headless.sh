#!/bin/bash
# Run ml-intern workflows via Claude CLI headless mode

set -e

WORKFLOW="${1:?Usage: run-headless.sh <workflow> [workflow_config_json]}"
WORKFLOW_CONFIG="${2:-{}}"

# Build the prompt for Claude to execute the workflow
read -r -d '' PROMPT << 'EOF' || true
You are an ML workflow executor. Your task is to run the following workflow using the ml-intern framework.

WORKFLOW: {WORKFLOW}
CONFIG: {CONFIG}

Steps:
1. Set up Python environment with ml-intern installed
2. Create a Python script to execute the workflow
3. Run the workflow and capture results
4. Return the final output/artifacts path

Respond with:
- Workflow status (SUCCESS/FAILED)
- Artifacts path (if any)
- Summary of what was executed
EOF

PROMPT="${PROMPT//\{WORKFLOW\}/$WORKFLOW}"
PROMPT="${PROMPT//\{CONFIG\}/$WORKFLOW_CONFIG}"

# Run Claude Code in headless mode
echo "🚀 Executing workflow: $WORKFLOW"
echo "📝 Config: $WORKFLOW_CONFIG"
echo ""

claude -p --output-format json \
  --add-dir /Users/lucianfialho/Code/latex \
  --allowed-tools "Bash,Read,Write" \
  "$PROMPT"
