# CONOPS Kill-Chain Simulation — Phase 1B

Five use cases from [`docs/04-conops-use-cases.md`](../../docs/04-conops-use-cases.md).

## Run

```bash
python sim/run_conops.py --samples 100000
python analysis/summarize_conops.py
```

Output: `analysis/CONOPS_REPORT.md` · `analysis/results/conops/conops_summary.json`

## Model stack

| Layer | Module |
|-------|--------|
| Combined MS-V + HC plumes | `models/cloud_physics/geometry_settling.py` |
| Settling + duration | `duration_until_cl_below_threshold` |
| Hardened MoE | `models/sensors/fpv_thermal.py` (v5) |
| Time windows | `sim/conops/kill_chain.py` |

## Key metrics

- **Lock Met** — operational MoE inside doctrine window (discriminates ~20–99% across use cases)
- **Obscured** — threat sensor cannot maintain fused lock at LOS CL
- **Friendly Blind** — squad thermal masking inside dense cloud (hard constraint)

> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION
