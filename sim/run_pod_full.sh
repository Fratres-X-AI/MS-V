#!/usr/bin/env bash
# Full RunPod compute campaign — MS-V Phase 1 v4
set -euo pipefail
cd "$(dirname "$0")/.."
WORKERS="${1:-31}"

echo "=== MS-V Pod Full Run (workers=$WORKERS) ==="
pip install -q -r requirements-lock.txt

echo "--- Reproduce harness ---"
python -m sim.reproduce

echo "--- Local suite 100k ---"
python sim/run_suite_local.py

echo "--- Stress validation ---"
python sim/validate_stress.py

echo "--- Mega suite 140M ---"
python sim/run_mega_suite.py --workers "$WORKERS"

echo "--- Summaries ---"
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py

echo "--- Tail risk ---"
python analysis/analyze_tail_risk.py

echo "=== DONE ==="
