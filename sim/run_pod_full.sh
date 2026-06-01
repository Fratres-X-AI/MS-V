#!/usr/bin/env bash
# Full RunPod compute campaign — mega suite + Sobol GSA
set -euo pipefail
cd "$(dirname "$0")/.."
WORKERS="${1:-255}"
SOBOL_N="${2:-8192}"

echo "=== MS-V Pod Full Run (workers=$WORKERS sobol_N=$SOBOL_N) ==="
if [ ! -d .venv ]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements-lock.txt

echo "--- Reproduce harness ---"
python -m sim.reproduce

echo "--- Local suite 100k ---"
python sim/run_suite_local.py

echo "--- Stress validation ---"
python sim/validate_stress.py

echo "--- Mega suite 140M ---"
python sim/run_mega_suite.py --workers "$WORKERS"

echo "--- Sobol global sensitivity (Saltelli) ---"
python sim/run_sobol.py --n-base "$SOBOL_N" --workers "$WORKERS"

echo "--- Summaries ---"
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py
python analysis/summarize_sobol.py
python analysis/patch_assumption_register_sobol.py
python analysis/generate_figures.py

echo "=== DONE — see analysis/MEGA_SUITE_REPORT.md and analysis/SOBOL_SENSITIVITY_REPORT.md ==="
