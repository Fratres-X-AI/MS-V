# Tail Risk & Parameter Sensitivity Analysis

> Derived from `analysis/results/mega_suite/summary.csv` (140M-sample campaign).
> **Not validation** — ranks sensitivity inside literature-assumed bounds only.

## Headline

- **Jobs analyzed:** 38
- **All-KPP pass (within assumed bounds):** 38/38
- **MoE lock-break fraction range:** **55.1%–98.5%** (phase2/v6 — discriminative)
- **Tightest duration p10 margin:** 32.3 s above 120 s KPP
- **Throw p10 range (phase2 HF):** 20.0–20.0 m

## Duration p10 — Ranked (worst first)

| Rank | Job | Dur p10 (s) | Dur p50 (s) | Margin vs 120 s |
|------|-----|-------------|-------------|-----------------|
| 1 | baseline_10M_adversarial_g3_n10000000 | 152.3 | 156.7 | 32.3 |
| 2 | sweep_burn_hi_4.4_g3_n2000000 | 161.9 | 187.1 | 41.9 |
| 3 | sweep_temp_hot_g3_n2000000 | 162.6 | 186.9 | 42.6 |
| 4 | sweep_temp_nominal_g3_n2000000 | 169.6 | 195.3 | 49.6 |
| 5 | baseline_10M_single_g1_duration_n10000000 | 169.7 | 197.4 | 49.7 |
| 6 | baseline_10M_g1_n10000000 | 169.7 | 197.4 | 49.7 |
| 7 | baseline_10M_wind_high_g3_n10000000 | 169.8 | 197.5 | 49.8 |
| 8 | sweep_yield_lo_0.18_g3_n2000000 | 169.8 | 197.5 | 49.8 |
| 9 | sweep_yield_lo_0.22_g3_n2000000 | 169.9 | 197.6 | 49.9 |
| 10 | sweep_burn_hi_4.2_g3_n2000000 | 169.9 | 197.6 | 49.9 |
| 11 | sweep_vis_smoke_1.0_g3_n2000000 | 169.9 | 197.6 | 49.9 |
| 12 | baseline_10M_g3_n10000000 | 169.9 | 197.6 | 49.9 |
| 13 | sweep_vis_smoke_1.1_g3_n2000000 | 169.9 | 197.6 | 49.9 |
| 14 | sweep_alpha_wide_g3_n2000000 | 169.9 | 197.6 | 49.9 |
| 15 | convergence_seed_2027_g3_n2000000 | 169.9 | 197.6 | 49.9 |

## MoE lock-break — Ranked (lowest first)

| Rank | Job | MoE frac | Dur p10 |
|------|-----|----------|---------|
| 1 | baseline_10M_adversarial_g3_n10000000 | 55.1% | 152.3s |
| 2 | baseline_10M_g1_n10000000 | 58.3% | 169.7s |
| 3 | baseline_10M_single_g1_duration_n10000000 | 58.4% | 169.7s |
| 4 | baseline_10M_wind_high_g3_n10000000 | 59.7% | 169.8s |
| 5 | baseline_10M_g2_n10000000 | 63.6% | 170.0s |
| 6 | sweep_yield_lo_0.18_g3_n2000000 | 79.3% | 169.8s |
| 7 | sweep_yield_lo_0.22_g3_n2000000 | 79.5% | 169.9s |
| 8 | sweep_burn_hi_3.6_g3_n2000000 | 79.8% | 194.3s |
| 9 | sweep_alpha_pessimistic_g3_n2000000 | 79.8% | 169.9s |
| 10 | sweep_temp_hot_g3_n2000000 | 79.8% | 162.6s |

## Parameter sensitivity (inferred from sweep jobs)

| Driver | Observation | Tail-risk note |
|--------|-------------|----------------|
| **Burn rate (upper bound)** | Dominant — 4.4 g/s max → ~152 s p10; 3.6 → ~183 s | Formulation must hold ≤4.2 g/s design cap |
| **Temperature (hot)** | 35–50°C bin → ~153 s p10 | High ambient shortens screen; doctrine/timing |
| **Adversarial stack** | 10M stacked corners → lowest MoE ~55% | Worst modeled envelope still passes duration KPP |
| **Yield (lower bound)** | 0.18–0.34 sweeps: modest MoE spread | Duration flat; MoE varies ~79–80% |
| **Visual smoke factor** | 1.0–1.6: negligible duration spread | Partner smoke affects MoE definition |
| **Alpha (extinction)** | tight/wide/pessimistic: stable duration | v6 band-integrated — see MoE Sobol phase2 |
| **Seed convergence** | 7 seeds, 2M each: stable ±0.03 s p10 | MC numerical stability confirmed |

## What this does NOT show

- p1 / empirical worst-case (no fill chemistry data)
- Per-wavelength extinction measurement uncertainty
- FPV ISP / AGC / fiber-optic link budget effects (partially in v6)
- Empirical throw under live-fire stress
- Toxicology or cost (KPP-12/13)

## Required before interpreting as design confirmation

1. Empirical α(λ) and particle size for candidate fill
2. Sensor transmittance curves with degradation thresholds
3. Geometry/settling model coupled to employment doctrine
4. External lab/range campaign (TRL 3→4 gate)
