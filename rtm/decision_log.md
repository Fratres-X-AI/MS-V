# MS-V Decision Log

| ID | Date | Decision | Rationale | Status | Source |
|----|------|----------|-----------|--------|--------|
| D-001 | v2 | Weight ~850 g | Density + 120+ s burn requires fill mass | **Locked** | User / Annex C |
| D-002 | v2 | Build-up ≤ 12–15 s (moderate priority) | Trade for multispectral + duration | **Locked** | User / Annex C |
| D-003 | v2 | Employment: 2–3 MS-V + visual smoke | FPV/fiber-optic MoE | **Locked** | docs/04, doc 07 |
| D-004 | v2 | Fill Option A (unified bispectral) baseline | ECBC precedent | **Open** — pending Phase 1 sensitivity |
| D-005 | v2 | Respiratory irritation acceptable (non-lethal) | IR performance trade | **Locked** | docs/03, doc 07 |
| D-006 | 2026-05-24 | Phase 1 before external engagement | Highest internal leverage | **Locked** | MasterPlan |
| D-007 | 2026-05-24 | Parallel Phase 0 audit + Phase 1 skeleton | Don't block modeling on perfect audit | **Accepted** | MasterPlan |
| D-008 | 2026-05-24 | CL-threshold duration (v2) | Remove arbitrary thickness fractions | **Superseded by D-009** | sim/engine.py |
| D-009 | 2026-06-01 | CL-ramp duration model (v3) | Duration starts at spectral threshold crossing during linear CL build-up | **Locked** | `phase1_v3_cl_ramp` |
| D-010 | 2026-06-01 | Burn rate cap 4.2 g/s | Align to 680 g / 120+ s design; OAT + Sobol rank #1 driver | **Locked** | params.yaml, A-002 |
| D-011 | 2026-06-01 | Mega suite 38 jobs / 140M samples | Full sensitivity campaign on RunPod CPU | **Locked** | `sim/config/seeds.yaml` |
| D-012 | 2026-06-01 | Fixed PRNG seeds via seeds.yaml | Python `hash()` non-portable — config control | **Locked** | seeds.yaml |
| D-013 | 2026-06-01 | Saltelli Sobol global sensitivity | Quantify variance drivers for TRL 3 prioritization | **Locked** | `sim/run_sobol.py` |
| D-014 | 2026-06-01 | MoE surrogate saturation disclosed | 100% lock-break pass non-discriminative (A-013) | **Locked** | verification_matrix |
| D-015 | 2026-06-01 | v4 band-integrated sensor path | Contrast-based degradation vs scalar transmittance | **Active** | `models/sensors/degradation.py` |
| D-016 | 2026-06-01 | CI must not overwrite 140M manifest | Quick mega → `mega_suite_quick/` | **Locked** | `.github/workflows/ci.yml` |

## Open Trades

| Trade | Options | Blocker |
|-------|---------|---------|
| Fill chemistry | Option A / B / C (Annex C) | No literature α calibration for MS-V fill |
| Cost vs performance | $75–150 vs Option A fill | Phase 4 cost model |
| Throw accuracy at 850 g | Accept vs reduce weight | Phase 2 human-factors; no data |
