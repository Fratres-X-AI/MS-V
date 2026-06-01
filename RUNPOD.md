# RunPod Handoff Guide

Run this when you rent a pod. Local work should already be done (`analysis/results/suite_summary.json`).

## Pod Setup

```bash
git clone https://github.com/Fratres-X-AI/MS-V.git
cd MS-V
pip install -r requirements.txt
```

## Recommended Instance

- **CPU:** 8+ vCPU sufficient (NumPy vectorized — GPU optional unless we add CuPy later)
- **RAM:** 4 GB+
- **Storage:** 10 GB

GPU not required for current Phase 1 engine.

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
