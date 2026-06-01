#!/usr/bin/env bash
# MS-V — single-pass submission pipeline (local or RunPod)
# Usage: bash one_pass.sh [workers] [sobol_n_base]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
# 32 vCPU pod -> 31 workers (n-1). Override: RUNPOD_CPU_COUNT=32 bash one_pass.sh
export RUNPOD_CPU_COUNT="${RUNPOD_CPU_COUNT:-32}"
WORKERS="${1:-$((RUNPOD_CPU_COUNT - 1))}"
SOBOL_N="${2:-8192}"
LOG="${ROOT}/analysis/one_pass.log"

exec > >(tee -a "$LOG") 2>&1
echo "=== MS-V ONE PASS $(date -u +%Y-%m-%dT%H:%M:%SZ) workers=$WORKERS sobol_N=$SOBOL_N ==="

if [ ! -d .venv ]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements-lock.txt

python -m sim.reproduce
python sim/run_suite_local.py
python sim/validate_stress.py
python sim/run_mega_suite.py --workers "$WORKERS"
python sim/run_sobol.py --n-base "$SOBOL_N" --workers "$WORKERS"
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py
python analysis/summarize_sobol.py
python analysis/patch_assumption_register_sobol.py
python analysis/generate_figures.py
python analysis/generate_form_factor_assets.py
python sim/run_conops.py --samples "${CONOPS_SAMPLES:-100000}"
python analysis/summarize_conops.py

# Write completion stamp for pull verification
python - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path
p = Path("analysis/results/one_pass_complete.json")
p.parent.mkdir(parents=True, exist_ok=True)
mega = json.loads(Path("analysis/results/mega_suite/manifest.json").read_text())
sobol = json.loads(Path("analysis/results/sobol/sobol_results.json").read_text())
p.write_text(json.dumps({
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "mega_jobs_pass": mega.get("jobs_pass"),
    "mega_total_samples": mega.get("total_samples"),
    "sobol_n_base": sobol.get("n_base"),
    "sobol_n_evaluations": sobol.get("n_evaluations"),
    "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY - NOT VALIDATION",
}, indent=2))
print(f"Wrote {p}")
PY

echo "=== ONE PASS COMPLETE ==="
