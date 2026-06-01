# Sobol Global Sensitivity Report — MS-V Phase 1

> **MATURITY:** Literature-parameter deterministic physics — **NOT VALIDATION**
> **Method:** Saltelli + Sobol (SALib) · N=8,192 · evaluations=212,992
> **Scenario:** 3 grenades · seed=4242

## Interpretation

- **S1** = first-order Sobol index (direct effect share of variance)
- **ST** = total-order index (direct + interaction effects)
- Duration indices are **actionable** for TRL 3 burn-cup / chamber testing
- MoE indices may be **depressed** when surrogate saturates (see A-013)

## KPP-03 Duration — ranked by ST

| Rank | Parameter | S1 | ST | TRL 3 priority |
|------|-----------|-----|-----|----------------|
| 1 | `burn_rate_g_s` | 0.8321 | 0.8340 | P0 burn cup |
| 2 | `temp_c` | 0.1212 | 0.1227 | P0 chamber T |
| 3 | `filler_mass_g` | 0.0446 | 0.0452 | P0 burn cup |
| 4 | `alpha_mwir` | 0.0000 | 0.0000 | P0 spectrometry |
| 5 | `yield_factor` | 0.0000 | 0.0000 | P0 gravimetric yield |
| 6 | `cloud_depth_m` | 0.0000 | 0.0000 | P1 geometry |
| 7 | `build_up_time_s` | 0.0000 | 0.0000 | P1 high-speed video |
| 8 | `wind_mph` | 0.0000 | 0.0000 | P2 range plume |
| 9 | `alpha_nir` | 0.0000 | 0.0000 | P0 spectrometry |
| 10 | `screening_area_sqft` | 0.0000 | 0.0000 | P1 lidar geometry |
| 11 | `alpha_vis` | -0.0000 | 0.0000 | P0 spectrometry |
| 12 | `humidity_rh` | 0.0000 | 0.0000 | P1 chamber RH |

- Duration Y: mean=187.7s p10=159.9s p50=185.6s p90=218.7s

## KPP-02 Build-up — top 5 by ST

| Parameter | S1 | ST |
|-----------|-----|-----|
| `build_up_time_s` | 1.0000 | 1.0000 |
| `wind_mph` | 0.0000 | 0.0000 |
| `temp_c` | 0.0000 | 0.0000 |
| `humidity_rh` | 0.0000 | 0.0000 |
| `filler_mass_g` | 0.0000 | 0.0000 |

## MOE-01 lock-break (binary surrogate) — top 5 by ST

| Parameter | S1 | ST | Note |
|-----------|-----|-----|------|
| — | — | — | **DEGENERATE** — 100% pass, surrogate saturation (A-013) |

## TRL 3 test plan (Sobol-driven)

1. **Burn rate + filler mass** — highest expected ST on duration; burn cup DOE
2. **Temperature** — coupled to burn; environmental chamber
3. **Build-up time** — if ST > 0.1, prioritize streamer imaging
4. **α(λ) bands** — spectrometry regardless of low ST (surrogate limitation)

Auto-generated from `analysis/results/sobol/sobol_results.json`.
