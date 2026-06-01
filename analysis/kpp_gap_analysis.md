# KPP Gap Analysis — Phase 1 M&S (v3 CL-Ramp Model)

> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION  
> Model: `phase1_v3_cl_ramp` — Beer-Lambert threshold + CL ramp during build-up.

## Summary (100k samples)

| KPP | Target | Sim Result (3 grenade, nominal) | Adversarial stress | Status |
|-----|--------|--------------------------------|--------------------|--------|
| Build-up p90 | ≤ 15 s | ~12.6 s | PASS | **PASS** |
| Duration p10 | ≥ 120 s | ~148 s | ~144 s | **PASS** |
| Duration p50 | ≥ 120 s | ~170 s | ~147 s | **PASS** |
| Screening area p10 | ≥ 30 sq ft | ~68 sq ft | PASS | **PASS** |
| MoE lock ≥ 60 s | Primary MoE | **100%** | **100%** | **PASS** |

All four automated KPP checks **PASS** for nominal envelope (0–15 mph), all wind bins, and **adversarial stress** (`sim/validate_stress.py`).

## v3 Improvements over v2

1. **CL ramp timing** — duration starts when spectral threshold is first crossed during linear CL build-up, not when an arbitrary build-up clock expires. Adds ~10–15 s of honest screening time when peak CL exceeds threshold by wide margin.
2. **Burn rate cap 4.2 g/s** — aligned to 680 g / 162 s raw design objective (sustained bispectral fill, not HC rate).
3. **Symmetric temperature coupling** — cold slows burn, heat accelerates (±0.2%/°C from 20°C reference).

## Physics traceability

| Parameter | Value | Basis |
|-----------|-------|-------|
| Fill mass | 624–680 g | `baseline_grenades.json` MS-V_target |
| Burn rate | 2.9–4.2 g/s | Design trade 1 — density + duration |
| Duration | `t_burn − t(CL≥τ)` | Annex B KPP-03, ECBC CL metrics |
| MoE | VIS+NIR+MWIR < 0.15 | KPP-06 + combined visual smoke factor |

## Honest External Statement

> "Physics-informed sensitivity modeling (CL-ramp v3) indicates the v2 concept meets proposed KPPs and the primary operational MoE under literature-bound parameters across the 0–15 mph operating envelope and under stacked adversarial stress. **Not validated experimentally.**"

## RunPod

Re-validate at scale: `python sim/run_runpod.py --workers 31 --out analysis/results/runpod_v3`
