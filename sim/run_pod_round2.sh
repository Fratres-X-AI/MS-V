#!/usr/bin/env bash
# Pod Round 2 — heavier CONOPS + MoE Sobol + wind deep-dive + full mega refresh
set -euo pipefail
cd "$(dirname "$0")/.."
export RUNPOD_CPU_COUNT="${RUNPOD_CPU_COUNT:-32}"
WORKERS="${WORKERS:-31}"
LOG="${PWD}/pod_round2.log"

exec > >(tee -a "$LOG") 2>&1
echo "=== POD ROUND 2 $(date -u +%Y-%m-%dT%H:%M:%SZ) workers=$WORKERS ==="

source .venv/bin/activate

echo "--- Full mega suite refresh (phase2/v6, 140M) ---"
python sim/run_mega_suite.py --workers "$WORKERS"
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py

echo "--- CONOPS 1M samples ---"
python sim/run_conops.py --samples 1000000
python analysis/summarize_conops.py

echo "--- Wind scenario deep-dive (2M x 3 wind bins, parallel) ---"
python sim/run_runpod.py --samples 2000000 --scenarios wind --grenades 3 --workers "$WORKERS"

echo "--- MoE Sobol phase2 N=8192 mc_n=5000 ---"
python sim/run_sobol_moe_phase2.py --n-base 8192 --mc-n 5000 --workers "$WORKERS"
python analysis/summarize_sobol_moe_phase2.py

echo "--- Duration Sobol N=32768 ---"
python sim/run_sobol.py --n-base 32768 --workers "$WORKERS"
python analysis/summarize_sobol.py
python analysis/patch_assumption_register_sobol.py

python analysis/generate_figures.py

python - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path
mega = json.loads(Path("analysis/results/mega_suite/manifest.json").read_text())
moe = json.loads(Path("analysis/results/sobol_moe_phase2/sobol_moe_phase2_results.json").read_text())
conops = json.loads(Path("analysis/results/conops/conops_summary.json").read_text())
Path("analysis/results/pod_round2_complete.json").write_text(json.dumps({
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "mega_samples": mega.get("total_samples"),
    "mega_model": mega.get("model_version"),
    "moe_sobol_n_base": moe.get("n_base"),
    "moe_sobol_mc_n": moe.get("mc_n_per_row"),
    "moe_sobol_evaluations": moe.get("n_evaluations"),
    "conops_use_cases": len(conops.get("use_cases", [])),
    "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY - NOT VALIDATION",
}, indent=2))
print("Wrote analysis/results/pod_round2_complete.json")
PY

echo "=== POD ROUND 2 COMPLETE ==="
