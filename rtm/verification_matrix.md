# Verification Matrix — MS-V Phase 1 M&S

> **MATURITY:** Sensitivity Study Complete (140M samples) — **NOT VALIDATION**
> **Model (campaign):** phase1_v3_cl_ramp · **Current engine:** phase1_v4_sensor
> **Evidence index:** `analysis/results/mega_suite/manifest.json` · **Seeds:** `sim/config/seeds.yaml`

## Limitations (read first)

- All results are **literature-parameter bounds** only — no MS-V fill empirical data.
- MoE and tri-band checks **saturate at 100%** in current surrogate — pass is **non-discriminative**.
- Duration margin is **real for burn/temp sweeps**; yield/alpha sweeps do not bind in v3/v4.

## KPP / MoE Summary

| Req | Criterion | Primary Job ID | Seed | Observed | Pass | Quantified Margin |
|-----|-----------|----------------|------|----------|------|-------------------|
| KPP-02 | Build-up p90 ≤ 15 s | `baseline_10M_g3_n10000000` | 45 | 12.583557869368104 | YES | 16.1% headroom below 15.0s cap (p90=12.6s) |
| KPP-03 | Duration p10 ≥ 120 s at good thickness | `baseline_10M_g3_n10000000` | 45 | 159.98264316091925 | YES | +33.3% above 120.0s threshold (p10=160.0s) |
| KPP-04 | Screening area p10 ≥ 30 sq ft (single grenade) | `baseline_10M_g1_n10000000` | 43 | p10 ≈ 31.0 sq ft | YES | +3.4% above 30 sq ft threshold at p10 |
| KPP-06 | VIS + NIR + MWIR attenuation (tri-band) | `baseline_10M_g3_n10000000` | 45 | T_p50 ≪ 0.15 all bands | YES | Surrogate saturates — **not discriminative**; TRL 3 spectrometer required |
| MOE-01 | Fused EO/IR lock-break ≥ 60 s (2–3 MS-V + visual smoke) | `baseline_10M_g3_n10000000` | 45 | 1.0 | YES* | 100% in all 38 jobs — **surrogate non-binding**; see A-013 |

*YES with surrogate saturation caveat on KPP-06 and MOE-01.

## Full Job Registry (38 jobs → evidence)

| Job ID | Seed | Samples | Grenades | Dur p10 | Pass | Category |
|--------|------|---------|----------|---------|------|----------|
| `baseline_10M_adversarial_g3_n10000000` | 999 | 10,000,000 | 3 | 143.6s | YES | stress_adversarial |
| `baseline_10M_g1_n10000000` | 43 | 10,000,000 | 1 | 159.9s | YES | baseline_employment |
| `baseline_10M_g2_n10000000` | 44 | 10,000,000 | 2 | 160.0s | YES | baseline_employment |
| `baseline_10M_g3_n10000000` | 45 | 10,000,000 | 3 | 160.0s | YES | baseline_employment |
| `baseline_10M_single_g1_duration_n10000000` | 51 | 10,000,000 | 1 | 159.9s | YES | baseline_employment |
| `baseline_10M_wind_calm_g3_n10000000` | 217 | 10,000,000 | 3 | 160.0s | YES | baseline_wind |
| `baseline_10M_wind_high_g3_n10000000` | 208 | 10,000,000 | 3 | 160.0s | YES | baseline_wind |
| `baseline_10M_wind_moderate_g3_n10000000` | 210 | 10,000,000 | 3 | 160.0s | YES | baseline_wind |
| `convergence_seed_137_g3_n2000000` | 137 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_2027_g3_n2000000` | 2027 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_271_g3_n2000000` | 271 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_4099_g3_n2000000` | 4099 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_42_g3_n2000000` | 42 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_8191_g3_n2000000` | 8191 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `convergence_seed_999_g3_n2000000` | 999 | 2,000,000 | 3 | 160.0s | YES | convergence |
| `sweep_alpha_pessimistic_g3_n2000000` | 603 | 2,000,000 | 3 | 159.9s | YES | sweep_alpha |
| `sweep_alpha_tight_g3_n2000000` | 601 | 2,000,000 | 3 | 160.0s | YES | sweep_alpha |
| `sweep_alpha_wide_g3_n2000000` | 602 | 2,000,000 | 3 | 160.0s | YES | sweep_alpha |
| `sweep_burn_hi_3.6_g3_n2000000` | 536 | 2,000,000 | 3 | 182.9s | YES | sweep_burn_rate |
| `sweep_burn_hi_3.8_g3_n2000000` | 538 | 2,000,000 | 3 | 174.7s | YES | sweep_burn_rate |
| `sweep_burn_hi_4.0_g3_n2000000` | 540 | 2,000,000 | 3 | 167.0s | YES | sweep_burn_rate |
| `sweep_burn_hi_4.2_g3_n2000000` | 542 | 2,000,000 | 3 | 160.0s | YES | sweep_burn_rate |
| `sweep_burn_hi_4.4_g3_n2000000` | 544 | 2,000,000 | 3 | 152.4s | YES | sweep_burn_rate |
| `sweep_temp_cold_g3_n2000000` | 680 | 2,000,000 | 3 | 169.9s | YES | sweep_temperature |
| `sweep_temp_hot_g3_n2000000` | 735 | 2,000,000 | 3 | 152.9s | YES | sweep_temperature |
| `sweep_temp_nominal_g3_n2000000` | 705 | 2,000,000 | 3 | 159.5s | YES | sweep_temperature |
| `sweep_vis_smoke_1.0_g3_n2000000` | 310 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.1_g3_n2000000` | 311 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.2_g3_n2000000` | 312 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.3_g3_n2000000` | 313 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.4_g3_n2000000` | 314 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.5_g3_n2000000` | 315 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.6_g3_n2000000` | 316 | 2,000,000 | 3 | 160.0s | YES | sweep_visual_smoke |
| `sweep_yield_lo_0.18_g3_n2000000` | 418 | 2,000,000 | 3 | 159.9s | YES | sweep_yield |
| `sweep_yield_lo_0.22_g3_n2000000` | 422 | 2,000,000 | 3 | 160.0s | YES | sweep_yield |
| `sweep_yield_lo_0.26_g3_n2000000` | 426 | 2,000,000 | 3 | 160.0s | YES | sweep_yield |
| `sweep_yield_lo_0.30_g3_n2000000` | 430 | 2,000,000 | 3 | 160.0s | YES | sweep_yield |
| `sweep_yield_lo_0.34_g3_n2000000` | 434 | 2,000,000 | 3 | 160.0s | YES | sweep_yield |

## Tail-risk jobs (lowest duration p10)

- **Tightest overall:** `sweep_burn_hi_4.4_g3_n2000000` — +27.0% above 120.0s threshold (p10=152.4s)
- **Adversarial stack:** `baseline_10M_adversarial_g3_n10000000` — +19.7% above 120.0s threshold (p10=143.6s)

## TRL 3 physical verification required

| Req | Empirical test | Closes assumption |
|-----|----------------|-------------------|
| KPP-03 | Burn cup duration vs T/RH | A-002, burn_rate_g_s |
| KPP-06 | α(λ) transmissometry | A-001, A-005 |
| MOE-01 | Surrogate UAS FPV + thermal | A-008, A-013 |
| KPP-04 | Cloud geometry / lidar | A-004 |

Auto-generated by `analysis/generate_verification_matrix.py`.
