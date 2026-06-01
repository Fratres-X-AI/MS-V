# Verification Matrix — MS-V Phase 1 M&S

> **MATURITY:** Sensitivity Study Complete (140M samples) — **NOT VALIDATION**
> **Campaign model:** `phase2_v1_full_physics` · **physics_tier:** `phase2` · **sensor:** `unknown`
> **Evidence index:** `analysis/results/mega_suite/manifest.json` · **Seeds:** `sim/config/seeds.yaml`

## Limitations (read first)

- All results are **literature-parameter bounds** only — no MS-V fill empirical data.
- KPP-12 (toxicology) and KPP-13 (cost) require Phase 4 verification — not closed by M&S.
- When `surrogate_saturated=true`, MoE/tri-band pass is **non-discriminative** (A-013).

## KPP / MoE Summary

| Req | Criterion | Primary Job ID | Seed | Observed | Pass | Quantified Margin |
|-----|-----------|----------------|------|----------|------|-------------------|
| KPP-01 | Total weight ~850 g | `N/A (design authority)` | — | 850 g (v2_kpp envelope) | YES | Form-factor design authority — `models/system/form_factor.yaml`; TRL 3 mass measurement |
| KPP-02 | Build-up p90 ≤ 15 s | `baseline_10M_g3_n10000000` | 45 | 12.58481854456294 | YES | 16.1% headroom below 15.0s cap (p90=12.6s) |
| KPP-03 | Duration p10 ≥ 120 s at good thickness | `baseline_10M_g3_n10000000` | 45 | 169.9150843689387 | YES | +41.6% above 120.0s threshold (p10=169.9s) |
| KPP-04 | Screening area p10 ≥ 30 sq ft (single grenade) | `baseline_10M_g1_n10000000` | 43 | p10 = 31.00 sq ft | YES | + margin vs 30 sq ft at p10 (single grenade job) |
| KPP-05 | Employment group 2–3 grenades | `baseline_10M_g2_n10000000; baseline_10M_g3_n10000000` | 44;45 | g2 dur_p10=170.0s; g3 dur_p10=169.9s | YES | Doctrine — combined MS-V + visual smoke in groups |
| KPP-06 | VIS + NIR + MWIR attenuation (tri-band) | `baseline_10M_g3_n10000000` | 45 | {'VIS_p50': 1.0239761503873761e-54, 'NIR_p50': 3.7920314032287445e-41, 'MWIR_p50': 2.507193846885407e-34, 'fraction_below_threshold': 0.8005475} | YES | v6 band-integrated transmittance — see sensor_diagnostics |
| KPP-07 | Fuze delay M201A1 (0.7–2.0 s) | `baseline_10M_g3_n10000000` | 45 | {'p10': 0.829991823333638, 'p50': 1.3503545284840563, 'p90': 1.8699703657287716} | YES | M201A1 band enforced in deployment_kinematics MC |
| KPP-08 | Throw range ≥ 20 m (stressed) | `baseline_10M_g3_n10000000` | 45 | 20.0 | YES | +0.0% above 20.0 m threshold (p10=20.0 m) |
| KPP-09 | Form factor ~7.1 × 3.1 in (v2 KPP) | `N/A (design authority)` | — | v2_kpp envelope in form_factor.yaml | YES | Annex F + STL assets — not physics MC |
| KPP-10 | Operating temp −20°C to +50°C | `sweep_temp_cold_g3_n2000000; sweep_temp_hot_g3_n2000000` | 680;735 | cold p10=180.6s; hot p10=162.6s | YES | +35.5% above 120.0s threshold (p10=162.6s) (hot bin tightest) |
| KPP-11 | Wind tolerance ≤ 15 mph | `baseline_10M_wind_high_g3_n10000000` | 208 | wind_high dur_p10=169.8s | YES | FM 3-50 planning band — duration not wind-bound in campaign |
| KPP-12 | Respiratory irritation acceptable (non-lethal) | `N/A` | — | Literature bounds only | NO | UNVERIFIED — Phase 4 toxicology; stronger IR fill vs TA (Annex B) |
| KPP-13 | Unit cost $75–150 at scale | `N/A` | — | Cost model not in MC | NO | PLANNED — Phase 4 manufacturing study |
| KPP-14 | Issue quantity 1–2 per soldier | `N/A (doctrine)` | — | 1–2 per soldier (Annex B) | YES | Logistics doctrine — not physics MC |
| MOE-01 | Fused EO/IR lock-break ≥ 60 s (2–3 MS-V + visual smoke) | `baseline_10M_g3_n10000000` | 45 | 0.8005475 | YES | 80.1% lock-break ≥60 s (v6 probabilistic — discriminative) |
| MOE-02 | CASEVAC / movement window T+15–135 s | `sim/run_conops.py` | 4242 | casualty_recovery: lock_met=0.149 | YES | CONOPS Monte Carlo — see analysis/CONOPS_REPORT.md |

*YES* = pass with surrogate saturation caveat. PARTIAL = design authority or planned verification.

## Limitations (program)

| Req | Statement | Source | Status |
|-----|-----------|--------|--------|
| LIM-01 | Requires visual smoke (not standalone) | `docs/07-limitations-and-risks.md` | ACCEPTED |
| LIM-02 | Obscuration only — not RF defeat | `docs/07-limitations-and-risks.md` | ACCEPTED |
| LIM-03 | TRL 2–3 ceiling — no empirical MS-V fill validation | `MasterPlan.md` | ACCEPTED |

## Full Job Registry (38 jobs → evidence)

| Job ID | Seed | Samples | Grenades | Dur p10 | Throw p10 | Pass | Category |
|--------|------|---------|----------|---------|-----------|------|----------|
| `baseline_10M_adversarial_g3_n10000000` | 999 | 10,000,000 | 3 | 152.3s | 20.0m | YES | stress_adversarial |
| `baseline_10M_g1_n10000000` | 43 | 10,000,000 | 1 | 169.7s | 20.0m | YES | baseline_employment |
| `baseline_10M_g2_n10000000` | 44 | 10,000,000 | 2 | 170.0s | 20.0m | YES | baseline_employment |
| `baseline_10M_g3_n10000000` | 45 | 10,000,000 | 3 | 169.9s | 20.0m | YES | baseline_employment |
| `baseline_10M_single_g1_duration_n10000000` | 51 | 10,000,000 | 1 | 169.7s | 20.0m | YES | baseline_employment |
| `baseline_10M_wind_calm_g3_n10000000` | 217 | 10,000,000 | 3 | 170.0s | 20.0m | YES | baseline_wind |
| `baseline_10M_wind_high_g3_n10000000` | 208 | 10,000,000 | 3 | 169.8s | 20.0m | YES | baseline_wind |
| `baseline_10M_wind_moderate_g3_n10000000` | 210 | 10,000,000 | 3 | 169.9s | 20.0m | YES | baseline_wind |
| `convergence_seed_137_g3_n2000000` | 137 | 2,000,000 | 3 | 169.9s | 20.0m | YES | convergence |
| `convergence_seed_2027_g3_n2000000` | 2027 | 2,000,000 | 3 | 169.9s | 20.0m | YES | convergence |
| `convergence_seed_271_g3_n2000000` | 271 | 2,000,000 | 3 | 170.0s | 20.0m | YES | convergence |
| `convergence_seed_4099_g3_n2000000` | 4099 | 2,000,000 | 3 | 170.0s | 20.0m | YES | convergence |
| `convergence_seed_42_g3_n2000000` | 42 | 2,000,000 | 3 | 169.9s | 20.0m | YES | convergence |
| `convergence_seed_8191_g3_n2000000` | 8191 | 2,000,000 | 3 | 169.9s | 20.0m | YES | convergence |
| `convergence_seed_999_g3_n2000000` | 999 | 2,000,000 | 3 | 169.9s | 20.0m | YES | convergence |
| `sweep_alpha_pessimistic_g3_n2000000` | 603 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_alpha |
| `sweep_alpha_tight_g3_n2000000` | 601 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_alpha |
| `sweep_alpha_wide_g3_n2000000` | 602 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_alpha |
| `sweep_burn_hi_3.6_g3_n2000000` | 536 | 2,000,000 | 3 | 194.3s | 20.0m | YES | sweep_burn_rate |
| `sweep_burn_hi_3.8_g3_n2000000` | 538 | 2,000,000 | 3 | 185.5s | 20.0m | YES | sweep_burn_rate |
| `sweep_burn_hi_4.0_g3_n2000000` | 540 | 2,000,000 | 3 | 177.4s | 20.0m | YES | sweep_burn_rate |
| `sweep_burn_hi_4.2_g3_n2000000` | 542 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_burn_rate |
| `sweep_burn_hi_4.4_g3_n2000000` | 544 | 2,000,000 | 3 | 161.9s | 20.0m | YES | sweep_burn_rate |
| `sweep_temp_cold_g3_n2000000` | 680 | 2,000,000 | 3 | 180.6s | 20.0m | YES | sweep_temperature |
| `sweep_temp_hot_g3_n2000000` | 735 | 2,000,000 | 3 | 162.6s | 20.0m | YES | sweep_temperature |
| `sweep_temp_nominal_g3_n2000000` | 705 | 2,000,000 | 3 | 169.6s | 20.0m | YES | sweep_temperature |
| `sweep_vis_smoke_1.0_g3_n2000000` | 310 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.1_g3_n2000000` | 311 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.2_g3_n2000000` | 312 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.3_g3_n2000000` | 313 | 2,000,000 | 3 | 170.0s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.4_g3_n2000000` | 314 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.5_g3_n2000000` | 315 | 2,000,000 | 3 | 170.0s | 20.0m | YES | sweep_visual_smoke |
| `sweep_vis_smoke_1.6_g3_n2000000` | 316 | 2,000,000 | 3 | 170.0s | 20.0m | YES | sweep_visual_smoke |
| `sweep_yield_lo_0.18_g3_n2000000` | 418 | 2,000,000 | 3 | 169.8s | 20.0m | YES | sweep_yield |
| `sweep_yield_lo_0.22_g3_n2000000` | 422 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_yield |
| `sweep_yield_lo_0.26_g3_n2000000` | 426 | 2,000,000 | 3 | 169.9s | 20.0m | YES | sweep_yield |
| `sweep_yield_lo_0.30_g3_n2000000` | 430 | 2,000,000 | 3 | 170.0s | 20.0m | YES | sweep_yield |
| `sweep_yield_lo_0.34_g3_n2000000` | 434 | 2,000,000 | 3 | 170.0s | 20.0m | YES | sweep_yield |

## Tail-risk jobs (lowest duration p10)

- **Tightest burn sweep:** `sweep_burn_hi_4.4_g3_n2000000` — +34.9% above 120.0s threshold (p10=161.9s)
- **Adversarial stack:** `baseline_10M_adversarial_g3_n10000000` — +26.9% above 120.0s threshold (p10=152.3s)

## TRL 3 physical verification required

| Req | Empirical test | Closes assumption |
|-----|----------------|-------------------|
| KPP-01 | Mass / balance | Form factor prototype |
| KPP-03 | Burn cup duration vs T/RH | A-002, burn_rate_g_s |
| KPP-06 | α(λ) transmissometry | A-001, A-005 |
| KPP-08 | Throw range under load | human_factors.yaml |
| MOE-01 | Surrogate UAS FPV + thermal | A-008, A-013 |
| KPP-04 | Cloud geometry / lidar | A-004 |
| KPP-12 | Irritation characterization | Toxicology panel |

## Traceability links

- Assumptions: [`rtm/assumption_register.md`](assumption_register.md)
- CSV export: [`rtm/requirements_traceability.csv`](requirements_traceability.csv)
- Human factors: [`analysis/human_factors_notes.md`](../analysis/human_factors_notes.md)

Auto-generated by `analysis/generate_verification_matrix.py`.
