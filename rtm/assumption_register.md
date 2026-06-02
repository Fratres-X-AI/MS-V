# MS-V Assumption Register (Formal)

> **MATURITY:** Sensitivity Study Complete — literature-parameter bounds only  
> **NOT VALIDATION** — no MS-V fill empirical data exists  
> **Campaign evidence:** 140M samples, 38 jobs — `analysis/results/mega_suite/manifest.json`  
> **Sensitivity method:** OAT (38-job mega suite) + **Saltelli Sobol** (N=256, 6,656 evals, seed=4242) — see `analysis/SOBOL_SENSITIVITY_REPORT.md`

| ID | Assumption | Source / Standard | Bound used in MC | OAT sensitivity rank | KPP impact | TRL 3 test priority | Status |
|----|------------|-------------------|------------------|----------------------|------------|---------------------|--------|
| A-001 | MS-V unified bispectral fill achieves VIS+NIR+MWIR attenuation | ECBC bispectral grenade program (2014); Annex E | α VIS 4–12, NIR 3–10, MWIR 2–9 m²/g | **Low** (saturates surrogate) | KPP-06 High | **P0** — spectrometer α(λ) | LITERATURE |
| A-002 | 624–680 g fill burns 120+ s at good thickness | Design target v2; baseline_grenades.json | burn 2.9–4.2 g/s | **Rank 1** (Δdur p10 up to −27% at 4.4 g/s) | KPP-03 High | **P0** — burn cup vs T | UNVALIDATED |
| A-003 | Build-up to effective density 8–15 s | Annex B/D; HC baseline 10–20 s | uniform 8–15 s × burn coupling | **Low** (p90 ~12.6 s stable) | KPP-02 Medium | P1 — high-speed video | UNVALIDATED |
| A-004 | Screening area 30–40 sq ft per grenade | Annex B; scaled from AN-M8 | uniform 30–40 sq ft × overlap^0.72 | **Low** in duration; Medium area | KPP-04 Medium | P1 — lidar / geometry | UNVALIDATED |
| A-005 | Beer-Lambert T=exp(−α·CL) planning adequate | FM 3-50 App G; Annex D | CL-threshold duration model | **Medium** (defines KPP-03 clock) | KPP-03,06 Medium | P1 — compare to line-of-sight meters | LITERATURE |
| A-006 | Mass extinction α literature applies to MS-V fill | COMBIC/ECBC open literature | see A-001 bands | **Low** in OAT sweeps | KPP-06 High | **P0** with A-001 | LITERATURE |
| A-007 | Wind 0–15 mph operating envelope | User req; FM 3-50 planning | uniform 0–15 mph | **Low** on duration (v3) | KPP-11 Medium | P2 — range plume | VALIDATED (req) |
| A-008 | FPV + fiber-optic threats fuse VIS + thermal | Open-source UAS reporting; Annex D | fused MoE mask | N/A (threat model) | MOE-01 High | P1 — threat spec review | LITERATURE |
| A-009 | Combined MS-V + AN-M8 required for MoE | docs/04, 07; Annex D | visual_smoke_factor 1.3 (sweep 1.0–1.6) | **Low** on duration/MoE fraction | MOE-01 High | **P0** — combined plume test | VALIDATED (doctrine) |
| A-010 | Respiratory irritation acceptable non-lethal | Design acceptance | not in MC | N/A | KPP-12 High | **P0** — tox panel | UNVALIDATED |
| A-011 | M201A1 fuze compatible | Inventory commonality | fuze delay 0.7–2 s (not MC) | N/A | KPP-07 Medium | P2 — fuze interface | UNVALIDATED |
| A-012 | Throw 20–25 m for 850 g under stress | KPP-08; heavier than AN-M8 | not in MC | N/A | KPP-08 High | **P0** — HF range test | UNVALIDATED |
| A-013 | Surrogate MoE / v6 probabilistic lock-break | Planning surrogate only; **not** field defeat rate | v6: ~**80%** nominal / ~**55%** adversarial lock-met (phase2 mega); v3 tier often **saturated** | **Discriminative in v6** when `surrogate_saturated=false`; still UNVALIDATED empirically | MOE-01 **Critical gap** | **P0** — UAS surrogate test (gate 2D) | UNVALIDATED |
| A-014 | Aerosol yield fraction 0.22–0.52 | Literature order-of-magnitude; burn model | uniform yield; humidity penalty | **Low** (no MoE variance) | MoE Medium | P0 — gravimetric yield | UNVALIDATED |
| A-015 | Temperature ±0.2%/°C burn rate coupling | Arrhenius-lite surrogate | −20 to +50 °C | **Rank 2** (hot bin −7 s p10 vs nominal) | KPP-03,10 Medium | P0 — burn cup | UNVALIDATED |
| A-016 | Humidity yield penalty above 50% RH | Hygroscopic agglomeration (surrogate) | 20–95% RH | **Low** in OAT | KPP-03 Low | P1 — chamber | UNVALIDATED |
| A-017 | Particle settling 0.02 m/s | Order-of-magnitude; not in duration v3 | params only | Not yet modeled | KPP-03 Medium | P1 — particle sizing | UNVALIDATED |
| A-018 | Cloud depth 2–4 m representative LOS | Annex D planning | uniform 2–4 m | **Medium** (CL magnitude) | KPP-04,06 Medium | P1 — geometry | UNVALIDATED |
| A-019 | Multi-grenade overlap efficiency 0.85 | Engineering estimate | fixed 0.85 | **Low** on duration | MOE Medium | P1 — range geometry | UNVALIDATED |
| A-020 | CL ramp linear during build-up | Annex D streamer→build-up | exponent 1.0 | **Medium** (duration clock) | KPP-02,03 Medium | P1 — time-resolved CL | UNVALIDATED |
| A-021 | Phase 1B geometry + combined HC plume | `geometry_settling.py`; docs/04 | throw offset 0–4 m, HC fill 539 g | **Medium** (coverage) | KPP-04, MOE High | P1 — range geometry | UNVALIDATED |
| A-022 | v5 band-integrated MoE + NETD floor | `fpv_thermal.py` | NETD 50 mK surrogate | **High** — lock_met discriminates | MOE-01 High | P0 — UAS surrogate | UNVALIDATED |
| A-023 | Edge-of-plume threat geometry | `geometry_settling.py` | orbit 0–1.05×R, spread 3.2×R, signed throw | **High** — obscured ~74–85% (binds) | MOE-01 High | P0 — range plume + UAS orbit | UNVALIDATED |
| A-024 | Squad thermal exposure at plume edge | `kill_chain.py` | squad radial 0.65–1.05×R, CL thresh 5.5 | **Medium** — friendly blind ~68% | MOE-01 Medium | P1 — HF / movement | UNVALIDATED |
| A-025 | Phase 2 aerosol microphysics (PSD/settling) | `aerosol_microphysics.py` | log-normal PSD, Stokes settling | **Medium** — duration tails | KPP-03 Medium | P0 — particle sizing | UNVALIDATED |
| A-026 | Phase 2 atmospheric + spectral corrections | `atmospheric_coupling.py`, `spectral_extinction.py` | washout, multi-scatter | **Low–Med** | MoE Medium | P1 — chamber/field | UNVALIDATED |
| A-027 | v6 probabilistic lock-break sensor | `lock_break.py` | logistic P(lock break) + fiber/RF | **High** — MoE discriminates | MOE-01 High | P0 — UAS surrogate | UNVALIDATED |

## OAT sensitivity ranking (duration p10, 38-job campaign)

| Rank | Parameter | Evidence job | Δ vs nominal |
|------|-----------|--------------|--------------|
| 1 | Burn rate upper bound | `sweep_burn_hi_4.4_g3` | 152.4 s p10 (−4.7% vs 160 s) |
| 2 | Hot temperature (35–50°C) | `sweep_temp_hot_g3` | 152.9 s p10 |
| 3 | Adversarial stack | `baseline_10M_adversarial_g3` | 143.6 s p10 |
| — | Yield lower bound | all yield sweeps | **No binding change** |
| — | α tight/wide/pessimistic | alpha sweeps | **No binding change** |
| — | Visual smoke factor | vis 1.0–1.6 | **No binding change** |

## Explicit non-assumptions (out of MC scope)

- Form factor throw dynamics (850 g, 7.1×3.1 in) — Phase 2
- Combined plume spatial interaction — Phase 1B
- Atmospheric stability classes — not modeled
- Sensor ISP/AGC/auto-gain — not modeled

## References

- FM 3-50 / COMBIC obscurant planning
- ECBC bispectral grenade (2014) — Annex E
- TM 43-0001-29 — baseline grenade masses/durations
- `rtm/uncertainty_register.md` — quantitative bounds
- `analysis/tail_risk_analysis.md` — tail statistics

## Sobol global sensitivity (duration ST rank)

> Campaign: `analysis\results\sobol\sobol_results.json` · generated 2026-06-01T19:04:22.274178+00:00

| Rank | Parameter | ST | S1 | TRL 3 focus |
|------|-----------|-----|-----|-------------|
| 1 | `burn_rate_g_s` | 0.8322 | 0.8272 | see verification matrix |
| 2 | `temp_c` | 0.1231 | 0.1219 | see verification matrix |
| 3 | `filler_mass_g` | 0.0453 | 0.0484 | see verification matrix |
| 4 | `alpha_mwir` | 0.0000 | -0.0003 | see verification matrix |
| 5 | `yield_factor` | 0.0000 | -0.0001 | see verification matrix |
| 6 | `cloud_depth_m` | 0.0000 | 0.0000 | see verification matrix |
| 7 | `wind_mph` | 0.0000 | -0.0000 | see verification matrix |
| 8 | `build_up_time_s` | 0.0000 | -0.0002 | see verification matrix |
| 9 | `alpha_nir` | 0.0000 | -0.0002 | see verification matrix |
| 10 | `screening_area_sqft` | 0.0000 | 0.0000 | see verification matrix |
| 11 | `alpha_vis` | 0.0000 | 0.0000 | see verification matrix |
| 12 | `humidity_rh` | 0.0000 | 0.0000 | see verification matrix |
| — | moe_met | DEGENERATE | — | A-013 surrogate saturation |
