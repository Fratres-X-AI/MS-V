#!/usr/bin/env bash
# Pod Round 3 — tail-risk deep dives (120M+ focused samples)
set -euo pipefail
cd "$(dirname "$0")/.."
export RUNPOD_CPU_COUNT="${RUNPOD_CPU_COUNT:-32}"
WORKERS="${WORKERS:-3}"

echo "=== POD ROUND 3 $(date -u +%Y-%m-%dT%H:%M:%SZ) deep-dive workers=$WORKERS ==="
source .venv/bin/activate

echo "--- Tail-risk deep dives (50M burn-worst + 20M adversarial + 50M baseline + 2x10M burn seeds) ---"
python sim/run_deep_dive.py --workers "$WORKERS"
python analysis/summarize_deep_dive.py

echo "--- Regenerate tail-risk + verification matrix ---"
python analysis/rebuild_mega_manifest.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py
python analysis/generate_figures.py

python - <<'PY'
import json
from datetime import datetime, timezone
from pathlib import Path
dd = json.loads(Path("analysis/results/deep_dive/manifest.json").read_text())
Path("analysis/results/pod_round3_complete.json").write_text(json.dumps({
    "completed_at": datetime.now(timezone.utc).isoformat(),
    "deep_dive_samples": dd.get("total_samples"),
    "deep_dive_jobs": len(dd.get("jobs", [])),
    "elapsed_s": dd.get("elapsed_s"),
    "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY - NOT VALIDATION",
}, indent=2))
print("Wrote analysis/results/pod_round3_complete.json")
PY

echo "=== POD ROUND 3 COMPLETE ==="
