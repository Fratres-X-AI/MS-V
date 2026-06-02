# CONOPS Monte Carlo Report — Five Use Cases

> **Generated from:** `analysis/results/conops_summary.json` (regenerate via CONOPS runner when scenarios change)  
> **MATURITY:** Phase 2 full physics + probabilistic MoE — **NOT VALIDATION**  
> **Model:** phase2_v1_full_physics · 1,000,000 samples per case

| Use Case | MS-V | HC | Window (s) | Lock Met | Obscured | Edge Plume | Core | Friendly Blind |
|----------|------|-----|------------|----------|----------|------------|------|----------------|
| Casualty Recovery | 2 | 1 | 15–120 | **14.9%** | 62.9% | 53.1% | 19.7% | 70.5% |
| Break Contact / Exfil | 3 | 2 | 15–120 | **31.6%** | 79.7% | 36.2% | 28.4% | 56.2% |
| Mask Infil / Approach | 2 | 1 | 15–90 | **14.9%** | 63.0% | 53.1% | 19.8% | 70.4% |
| Bounding Overwatch | 2 | 1 | 15–60 | **14.9%** | 63.2% | 53.0% | 19.7% | 70.5% |
| Hasty Defense | 2 | 2 | 12–120 | **61.1%** | 62.9% | 53.0% | 19.7% | 70.4% |

## Interpretation

- **Lock Met** — threat lock broken for ≥ min_lock_s inside CONOPS window with build-up complete
- **Obscured** — v6 probabilistic lock-break at **threat LOS** (Phase 2 microphysics + edge geometry)
- **Edge Plume** — fraction of samples where threat sits at r/R ≥ 0.75
- **Core** — threat inside dense core (r/R ≤ 0.35)
- **Friendly Blind** — squad inside dense MWIR cloud (hard constraint on movement)
- Values **< 100%** indicate hardened MoE is discriminating (A-013 partially addressed)

Source: `sim/conops/kill_chain.py` · `docs/04-conops-use-cases.md`
