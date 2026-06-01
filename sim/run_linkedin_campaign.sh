#!/usr/bin/env bash
# LinkedIn / submission campaign — RunPod (31 workers)
set -euo pipefail
cd "$(dirname "$0")/.."
export RUNPOD_CPU_COUNT="${RUNPOD_CPU_COUNT:-32}"
WORKERS="${WORKERS:-31}"

echo "=== MS-V LinkedIn Campaign $(date -u +%Y-%m-%dT%H:%M:%SZ) workers=$WORKERS ==="

source .venv/bin/activate

# Refresh reports from committed mega manifest
python analysis/summarize_mega_suite.py
python analysis/generate_verification_matrix.py

# High-sample CONOPS for MOE-02 confidence
CONOPS_SAMPLES="${CONOPS_SAMPLES:-500000}"
echo "--- CONOPS n=$CONOPS_SAMPLES ---"
python sim/run_conops.py --samples "$CONOPS_SAMPLES"
python analysis/summarize_conops.py

# Standard duration Sobol (12-param lumped — burn rate ranking)
echo "--- Duration Sobol N=16384 ---"
python sim/run_sobol.py --n-base 16384 --workers "$WORKERS"
python analysis/summarize_sobol.py
python analysis/patch_assumption_register_sobol.py

# Phase2 MoE Sobol (6-param engine-backed — discriminative MoE)
echo "--- MoE Sobol phase2 N=4096 mc_n=3000 ---"
python sim/run_sobol_moe_phase2.py --n-base 4096 --mc-n 3000 --workers "$WORKERS"
python analysis/summarize_sobol_moe_phase2.py

python analysis/analyze_tail_risk.py
python analysis/generate_figures.py

python - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path
mega = json.loads(Path("analysis/results/mega_suite/manifest.json").read_text())
conops = json.loads(Path("analysis/results/conops/conops_summary.json").read_text())
moe_sobol = json.loads(Path("analysis/results/sobol_moe_phase2/sobol_moe_phase2_results.json").read_text())
Path("analysis/results/linkedin_campaign.json").write_text(json.dumps({
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "mega_model": mega.get("model_version"),
    "mega_samples": mega.get("total_samples"),
    "conops_samples": conops.get("n_samples"),
    "moe_sobol_n_base": moe_sobol.get("n_base"),
    "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
}, indent=2))
print("Wrote analysis/results/linkedin_campaign.json")
PY

echo "=== LINKEDIN CAMPAIGN COMPLETE ==="
