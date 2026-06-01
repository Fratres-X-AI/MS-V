# CONOPS Monte Carlo Report — Five Use Cases

> **MATURITY:** Phase 2 full physics + probabilistic MoE — **NOT VALIDATION**
> **Model:** phase2_v1_full_physics · 50,000 samples per case

| Use Case | MS-V | HC | Window (s) | Lock Met | Obscured | Edge Plume | Core | Friendly Blind |
|----------|------|-----|------------|----------|----------|------------|------|----------------|
| Casualty Recovery | 2 | 1 | 15–120 | **19.7%** | 64.6% | 50.9% | 20.6% | 64.2% |
| Break Contact / Exfil | 3 | 2 | 15–120 | **38.9%** | 82.3% | 33.1% | 30.0% | 48.7% |
| Mask Infil / Approach | 2 | 1 | 15–90 | **19.5%** | 65.2% | 50.6% | 20.8% | 64.4% |
| Bounding Overwatch | 2 | 1 | 15–60 | **20.0%** | 65.2% | 50.9% | 20.7% | 64.0% |
| Hasty Defense | 2 | 2 | 12–120 | **62.9%** | 64.7% | 51.0% | 20.6% | 63.8% |

## Interpretation

- **Lock Met** — threat lock broken for ≥ min_lock_s inside CONOPS window with build-up complete
- **Obscured** — v6 probabilistic lock-break at **threat LOS** (Phase 2 microphysics + edge geometry)
- **Edge Plume** — fraction of samples where threat sits at r/R ≥ 0.75
- **Core** — threat inside dense core (r/R ≤ 0.35)
- **Friendly Blind** — squad inside dense MWIR cloud (hard constraint on movement)
- Values **< 100%** indicate hardened MoE is discriminating (A-013 partially addressed)

Source: `sim/conops/kill_chain.py` · `docs/04-conops-use-cases.md`
