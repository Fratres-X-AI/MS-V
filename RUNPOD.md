# RunPod Handoff Guide

Run this when you rent a pod. Local work should already be done (`analysis/results/suite_summary.json`).

## Pod Setup

```bash
git clone https://github.com/Fratres-X-AI/MS-V.git
cd MS-V
pip install -r requirements.txt
```

## Recommended Instance

- **CPU:** rent big — 16–32 vCPU. NumPy vectorized; **GPU not required**.
- **RAM:** 4 GB+ (scale with sample count)
- **Storage:** 10 GB

### Parallelism policy

All RunPod runs auto-detect vCPU and use **`workers = vCPU - 1`** (32 → 31, 28 → 27). Scenarios run in parallel across workers; BLAS pinned to 1 thread per worker to avoid oversubscription. Override only for debug: `--workers 4`.

Log line at startup: `[RunPod] vCPU=32 -> workers=31 (max parallel, minus 1)`

## Mega Suite (full sensitivity campaign)

```bash
# 38 jobs, ~140M total samples — baselines + sweeps + convergence
python sim/run_mega_suite.py --workers 31
python analysis/summarize_mega_suite.py
```

Outputs: `analysis/results/mega_suite/` + `analysis/MEGA_SUITE_REPORT.md`

Includes: 10M-sample baselines, visual-smoke/yield/burn/alpha/temp sweeps, 7-seed convergence, adversarial stress.

## Run Full Scale

```bash
# Default: 2M samples × 3 employment scenarios + wind bins
python sim/run_runpod.py

# Custom scale
python sim/run_runpod.py --samples 5000000 --grenades 1 2 3

# Wind only sweep
python sim/run_runpod.py --samples 2000000 --scenarios wind
```

Outputs: `analysis/results/runpod/` + `manifest.json`

## After Run

```bash
python analysis/summarize_results.py
# Copy runpod results into summary manually or extend summarize_results.py
```

## Pull Results Locally

```bash
scp -r user@pod:/workspace/MS-V/analysis/results/runpod ./analysis/results/
```

## Parameter Sweeps to Try on RunPod

1. **Yield factor** — edit `burn_model.py` bounds or add sweep script
2. **α extinction** — tighten/ widen bands in `params.yaml`
3. **Visual smoke factor** — 1.0 to 1.6 sensitivity
4. **5M+ samples** — stable CIs on MoE fractions

## Do Not Claim

- Validation or TRL 4+
- Military readiness
- Empirical obscurant performance

Label all outputs: **literature-parameter sensitivity study**.
