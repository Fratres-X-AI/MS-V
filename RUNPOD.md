# RunPod Handoff Guide

Run this when you rent a pod. Local work should already pass `make reproduce`.

## One-Step Full Pipeline

```bash
git clone https://github.com/Fratres-X-AI/MS-V.git
cd MS-V
bash run_all.sh                    # venv + reproduce + suite + mega + reports
# Or: WORKERS=31 bash run_all.sh
```

`run_all.sh` executes: `sim.reproduce` → local suite → stress → mega suite → manifest rebuild → tail-risk → verification matrix.

## Pod Setup (manual)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-lock.txt
# Or: conda env create -f environment.yml
```

## Recommended Instance

- **CPU:** 16–32 vCPU. NumPy vectorized; **GPU not required**.
- **RAM:** 4 GB+ (scale with sample count)
- **Storage:** 10 GB

### Parallelism policy

All RunPod runs use **`workers = vCPU - 1`** (32 → **31**). Set `RUNPOD_CPU_COUNT=32` on the pod when `nproc` reports the host (e.g. 256) instead of rented vCPU. Override: `--workers 4`.

## Mega Suite (140M sensitivity campaign)

```bash
python sim/run_mega_suite.py --workers 31
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
python analysis/generate_verification_matrix.py
```

**Configuration control:** All 38 jobs defined in [`sim/config/seeds.yaml`](sim/config/seeds.yaml) — seeds, sample counts, sweep mutations.

Outputs: `analysis/results/mega_suite/manifest.json` + `rtm/verification_matrix.md`

## Reproducibility

| File | Purpose |
|------|---------|
| `requirements-lock.txt` | Pinned Python deps with hashes |
| `environment.yml` | Conda env (Python 3.10–3.12) |
| `sim/config/seeds.yaml` | Per-job PRNG seeds |
| `sim/reproduce.py` | Golden checksum validation |

## Pull Results Locally

```bash
scp -r user@pod:/workspace/MS-V/analysis/results/mega_suite ./analysis/results/
scp user@pod:/workspace/MS-V/rtm/verification_matrix.md ./rtm/
```

## Do Not Claim

- Validation or TRL 4+
- Military readiness
- Empirical obscurant performance
- MoE 100% pass as lock-break confirmation (surrogate saturates)

## RunPod Instance Log

| Campaign | Host | vCPU | RAM | Workers | Samples | Wall time |
|----------|------|------|-----|---------|---------|-----------|
| Initial 2M | 213.173.107.24:36432 | 32 | — | 31 | 12M | ~1 s |
| Mega 140M | 213.173.107.24:36432 | 32 | — | 31 | 140M | ~9 s |
| Full refresh + Sobol N=8192 | 91.199.227.82:15218 | 32 | 125 GiB | **31** | 140M + 212k Sobol | see pod log |

Document local vs pod: NumPy vectorized MC is CPU-bound; pod wall time scales with workers until memory bandwidth limits.
