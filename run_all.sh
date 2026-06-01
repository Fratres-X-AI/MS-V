#!/usr/bin/env bash
# MS-V one-step regeneration — local or RunPod
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ ! -d .venv ]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements-lock.txt

echo "=== MS-V run_all.sh ==="
python -m sim.reproduce
python sim/run_suite_local.py
python sim/validate_stress.py
python sim/run_mega_suite.py --workers "${WORKERS:-31}"
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py
python sim/run_sobol.py --n-base "${SOBOL_N:-8192}" --workers "${WORKERS:-31}"
python analysis/summarize_sobol.py
python analysis/patch_assumption_register_sobol.py
python analysis/generate_figures.py
echo "=== Complete. See analysis/MEGA_SUITE_REPORT.md and analysis/SOBOL_SENSITIVITY_REPORT.md ==="
