# Tail Risk & Parameter Sensitivity Analysis

> Derived from `analysis/results/mega_suite/summary.csv` (140M-sample campaign).
> **Not validation** — ranks sensitivity inside literature-assumed bounds only.

## Headline

- **Jobs analyzed:** 38
- **All-KPP pass (within assumed bounds):** 38/38
- **Minimum MoE lock-break fraction:** 100.0% (current surrogate saturates at 100%)
- **Tightest duration p10 margin:** 23.6 s above 120 s KPP

## Duration p10 — Ranked (worst first)

| Rank | Job | Dur p10 (s) | Dur p50 (s) | Margin vs 120 s |
|------|-----|-------------|-------------|-----------------|
| 1 | baseline_10M_adversarial_g3_n10000000 | 143.6 | 147.1 | 23.6 |
| 2 | sweep_burn_hi_4.4_g3_n2000000 | 152.4 | 175.7 | 32.4 |
| 3 | sweep_temp_hot_g3_n2000000 | 152.9 | 175.6 | 32.9 |
| 4 | sweep_temp_nominal_g3_n2000000 | 159.5 | 183.5 | 39.5 |
| 5 | sweep_alpha_pessimistic_g3_n2000000 | 159.9 | 185.5 | 39.9 |
| 6 | baseline_10M_single_g1_duration_n10000000 | 159.9 | 185.5 | 39.9 |
| 7 | baseline_10M_g1_n10000000 | 159.9 | 185.5 | 39.9 |
| 8 | sweep_yield_lo_0.18_g3_n2000000 | 159.9 | 185.5 | 39.9 |
| 9 | baseline_10M_wind_high_g3_n10000000 | 160.0 | 185.6 | 40.0 |
| 10 | sweep_yield_lo_0.22_g3_n2000000 | 160.0 | 185.6 | 40.0 |
| 11 | baseline_10M_g2_n10000000 | 160.0 | 185.6 | 40.0 |
| 12 | sweep_burn_hi_4.2_g3_n2000000 | 160.0 | 185.6 | 40.0 |
| 13 | sweep_vis_smoke_1.0_g3_n2000000 | 160.0 | 185.6 | 40.0 |
| 14 | sweep_vis_smoke_1.1_g3_n2000000 | 160.0 | 185.5 | 40.0 |
| 15 | baseline_10M_g3_n10000000 | 160.0 | 185.6 | 40.0 |

## Parameter sensitivity (inferred from sweep jobs)

| Driver | Observation | Tail-risk note |
|--------|-------------|----------------|
| **Burn rate (upper bound)** | Dominant — 4.4 g/s max → ~152 s p10; 3.6 → ~183 s | Formulation must hold ≤4.2 g/s design cap |
| **Temperature (hot)** | 35–50°C bin → ~153 s p10 | High ambient shortens screen; doctrine/timing |
| **Adversarial stack** | 10M stacked corners → ~144 s p10 | Worst modeled envelope still passes; **outside envelope unmodeled** |
| **Yield (lower bound)** | 0.18–0.34 sweeps: no duration/MoE separation | CL surrogate saturates — **sensor model upgrade required** |
| **Visual smoke factor** | 1.0–1.6: negligible duration spread | Partner smoke affects MoE definition, not burn clock |
| **Alpha (extinction)** | tight/wide/pessimistic: ~160 s p10 flat | Uncertainty in α does not bind until sensor curves added |
| **Seed convergence** | 7 seeds, 2M each: stable ±0.03 s p10 | MC numerical stability confirmed |

## What this does NOT show

- p1 / empirical worst-case (no fill chemistry data)
- Per-wavelength extinction measurement uncertainty
- FPV ISP / AGC / fiber-optic link budget effects
- Cloud geometry, settling, or combined plume interaction
- Throw range, load, or human-factors failure modes

## Required before interpreting as design confirmation

1. Empirical α(λ) and particle size for candidate fill
2. Sensor transmittance curves with degradation thresholds
3. Geometry/settling model coupled to employment doctrine
4. External lab/range campaign (TRL 3→4 gate)
