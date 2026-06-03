# Test & Evaluation Master Plan (TEMP) Outline — MS-V Veil

> **Status:** Outline for TRL 3 transition — **not executed**  
> **Maturity ceiling:** Analytical TRL 3 after phase2/v6 M&S freeze; empirical TRL 4 requires external lab/range  
> **Budget / schedule:** TBD pending funding — placeholders below are planning order-of-magnitude only

## 1. Purpose

Define the empirical test program required to convert the literature-parameter sensitivity model into a validated obscurant characterization suitable for prototype down-select.

## 2. Test objectives (priority order from OAT sensitivity)

| Priority | Objective | Closes assumption | Method |
|----------|-----------|-------------------|--------|
| **P0** | Burn rate vs temperature/humidity | A-002, A-015, A-016 | Burn cup gravimetric, 20–95% RH, −20 to +50 °C |
| **P0** | Mass extinction α(λ) VIS/NIR/MWIR | A-001, A-005, A-006 | Laboratory spectrometry on MS-V fill aerosol |
| **P0** | Combined MS-V + AN-M8 plume MoE | A-009, A-013 | Instrumented UAS FPV + thermal surrogate |
| **P0** | Respiratory irritation margin | A-010 | Toxicology panel per program safety plan |
| **P1** | Build-up time to effective density | A-003, A-020 | High-speed video + lidar |
| **P1** | Cloud geometry / screening area | A-004, A-018 | Lidar transects, wind tunnel or range |
| **P1** | Particle size / settling | A-017 | Cascade impactor |
| **P2** | Throw range / human factors | A-012, KPP-08 | HF range with 850 g form factor |
| **P2** | Fuze interface | A-011 | M201A1 compatibility test |

## 3. P0 test cards (TRL 3 critical path)

### P0-1 — Fill burn cup (Gate **2A** / E-1)

| Field | Detail |
|-------|--------|
| **Resources** | Gravimetric burn cup, environmental chamber (RH/temp), fill batch from Annex C down-select |
| **Duration** | 3–6 weeks lab (matrix: 3 temps × 3 RH × replicates) |
| **Procedure** | ASTM-style cup per [`analysis/fill_physics_test_plan.md`](../../analysis/fill_physics_test_plan.md) T-01 |
| **Pass** | p10 duration ≥ **120 s** at nominal loading; burn rate within model bounds for MC update |
| **Fail** | Cannot meet KPP-03 at any bound without reformulation |
| **Artifacts** | Raw mass-time CSV, RH/temp log, `partner_validation_results.json` → `fill_burn_cup` |
| **Gate link** | [DOC-11 §2A](../../docs/11-partner-validation-and-trl-gates.md) |

### P0-2 — Spectral extinction α(λ) (Gate **2B** / E-1)

| Field | Detail |
|-------|--------|
| **Resources** | FTIR / transmissometer, aerosol generation from P0-1 pass batch |
| **Duration** | 2–4 weeks |
| **Procedure** | VIS/NIR/MWIR vs mass loading (fill plan T-02) |
| **Pass** | Measured bands within ±20% of model mid at design loading; MWIR supports fused lock-break concept |
| **Fail** | MWIR insufficient vs planning surrogate |
| **Artifacts** | α(λ) curves, calibration certs, JSON → `spectral_extinction` |
| **Gate link** | [DOC-11 §2B](../../docs/11-partner-validation-and-trl-gates.md) |

### P0-3 — Combined plume MoE (Gate **2D** / E-4)

| Field | Detail |
|-------|--------|
| **Resources** | Range or chamber with MS-V + AN-M8 employment; fused EO/IR rig; safety officer |
| **Duration** | 4–8 weeks (setup + n≥20 instrumented trials) |
| **Procedure** | Nominal vs adversarial sensor stacks; measure lock-break duration vs smoke-only baseline |
| **Pass** | **Directional** consistency with M&S — measurable lock-break under instrumented conditions; **do not require** match to MC ~80% nominal / ~55% adversarial **surrogate lock-met** fractions (A-013) |
| **Fail** | No measurable lock-break vs smoke-only baseline |
| **Artifacts** | Trial video, sensor logs, JSON → `uas_surrogate`; update matrix MOE-01 row with **measured** status |
| **Gate link** | [DOC-11 §2D](../../docs/11-partner-validation-and-trl-gates.md) |
| **M&S reference** | Matrix MOE-01: `baseline_10M_g3_n10000000` (nominal), `baseline_10M_adversarial_g3_n10000000` (stress) — planning only |

### P0-4 — Respiratory / irritation (KPP-12)

| Field | Detail |
|-------|--------|
| **Resources** | Program safety office, toxicology contractor |
| **Duration** | 8–16 weeks (program-dependent) |
| **Procedure** | Panel per non-lethal obscurant requirements; compare to TA-25 / IR fill literature |
| **Pass** | Meets program non-lethal criteria |
| **Fail** | Exceeds acceptable exposure → formulation or employment change |
| **Artifacts** | Tox report (controlled distribution), matrix row KPP-12 update |
| **Gate link** | E-1 closure in [`trl_gate_external.md`](../trl_gate_external.md) |

## 4. P1 test cards

### P1-1 — Build-up time (supports KPP-02)

| Field | Detail |
|-------|--------|
| **Resources** | High-speed video, lidar or structured light |
| **Duration** | 2–3 weeks |
| **Pass** | p90 build-up ≤ **15 s** |
| **Fail** | p90 > 15 s without port/yield trade |
| **Artifacts** | Time-series density proxy, gate note in partner JSON |
| **Gate link** | Supports matrix KPP-02; no separate DOC-11 ID |

### P1-2 — Cloud geometry / screening (KPP-04)

| Field | Detail |
|-------|--------|
| **Resources** | Lidar transects, controlled wind (0–15 mph) |
| **Duration** | 3–4 weeks |
| **Pass** | Screening area 30–40 sq ft at p10 single-grenade |
| **Fail** | Below 30 sq ft at design loading |
| **Artifacts** | Lidar plots, wind log |

### P1-3 — Particle size / settling (A-017)

| Field | Detail |
|-------|--------|
| **Resources** | Cascade impactor, microscopy |
| **Duration** | 2 weeks |
| **Pass** | D50/D90 within literature bounds used in phase2 PSD |
| **Fail** | Settling faster than model → duration risk |
| **Artifacts** | PSD report, optional MC parameter update |

## 5. P2 test cards

### P2-1 — Throw range (Gate **2C** / E-2)

| Field | Detail |
|-------|--------|
| **Resources** | HF range, inert **850 g** round, DOC-10 1D screening complete |
| **Duration** | 1–2 weeks (n≥30 throws) |
| **Pass** | p10 ≥ **20 m** under stress posture per [`human_factors.yaml`](../../models/system/human_factors.yaml) |
| **Fail** | p10 < 18 m without envelope change |
| **Artifacts** | Distance grid, posture log, JSON → `throw_range` |
| **Gate link** | [DOC-11 §2C](../../docs/11-partner-validation-and-trl-gates.md) |

### P2-2 — Fuze interface (KPP-07)

| Field | Detail |
|-------|--------|
| **Resources** | M201A1 lot, inert body |
| **Duration** | 1 week |
| **Pass** | Function within 0.7–2.0 s spec |
| **Fail** | Out-of-tolerance lot or fit |
| **Artifacts** | Fuze test record |

## 6. Success criteria (TRL 3)

| Metric | Model prediction (sensitivity) | Empirical accept |
|--------|-------------------------------|------------------|
| Duration p10 | ≥ 120 s at good thickness | Measured ≥ 120 s at 10th percentile conditions |
| Build-up p90 | ≤ 15 s | Measured ≤ 15 s |
| α(λ) bands | Literature bounds | Measured within ±20% of model mid |
| MoE lock-break | Surrogate non-binding when saturation off | ≥ 60 s in ≥ 80% of instrumented trials (directional) |
| Throw p10 | ≥ 20 m stressed MC | Measured p10 ≥ 20 m (n≥30) |

## 7. Resource and staffing estimates (planning — notional)

Order-of-magnitude for funded TRL 3 program planning. **Not a cost proposal** — KPP-13 remains PLANNED.

| Element | P0 lab | P0 range/chamber | P1 | P2 HF |
|---------|--------|------------------|-----|-------|
| **Calendar** | 3–6 mo | 3–6 mo (overlap) | 2–4 mo | 1–2 mo |
| **Staff (FTE)** | 1–2 pyro/chem + 0.5 safety | 1 test director + 2 range techs | 1 optical + 1 lidar | 1 HF lead + 2 throwers |
| **Major equipment** | Burn cup, chamber, FTIR | UAS rig, smoke baseline | Lidar, wind source | Grid, inert 850 g rounds |
| **Notional $ (USD)** | $150k–400k | $250k–600k | $80k–200k | $40k–80k |

Assumes government or prime facility access; university lab may reduce burn-cup cost, not range MoE.

## 8. Risk register

| Risk | Likelihood | Impact | Mitigation | RTM |
|------|------------|--------|------------|-----|
| Fill cannot meet duration + tox | Med | High | Annex C trades; P0-1 before P0-3 | A-002, KPP-12 |
| MWIR α insufficient | Med | High | P0-2 before P0-3 | A-005, KPP-06 |
| **Surrogate MoE misread as validation** | **High** | **High** | A-013 on all briefings; matrix `surrogate_saturated`; no LinkedIn % without caveat | A-013, MOE-01 |
| v3-era 100% MoE saturation confusion | Med | High | Disclose v6 spread (~80%/55%) is still **not** field MoE | A-013 |
| Throw fails at 850 g | Med | Med | P2-1 before down-select; envelope trade only if p10 < 18 m | KPP-08, E-2 |
| Export / ITAR on range data | Med | Med | CEL review; partner JSON template only | — |
| Schedule slip (funding) | High | Med | Phased gates 2A→2B→2C→2D→2E | — |
| Public over-claim before E-1 | High | High | [`linkedin-posting-guide.md`](../../docs/linkedin-posting-guide.md); Option C only | GOV |

## 9. MoE / sensor surrogate disclosure (mandatory in test reports)

All TEMP reports referencing M&S must include:

1. **A-013:** v6 `lock_break_probability` is a **planning surrogate**, not a validated UAS defeat model.
2. **`surrogate_saturated`:** When true in archived jobs, tri-band/MoE MC pass is non-discriminative.
3. **No equivalence:** Empirical gate **2D** pass/fail is **not** required to reproduce MC percentages.

Cite: [`rtm/assumption_register.md`](../../rtm/assumption_register.md) · [`models/sensors/INTEGRATION.md`](../../models/sensors/INTEGRATION.md).

## 10. Budget and schedule (TBD pending funding)

| Phase | Duration (planning) | Budget | Deliverable |
|-------|---------------------|--------|-------------|
| TRL 3a — Lab | 3–6 mo | **TBD** | P0-1, P0-2, P1-3 |
| TRL 3b — Chamber/range | 3–6 mo | **TBD** | P0-3, P1-1, P1-2 |
| TRL 3c — HF / fuze | 1–2 mo | **TBD** | P2-1, P2-2 |
| TRL 4 — Relevant environment | 6–12 mo | **TBD** | Full E-1..E-5 closure |

## 11. Configuration control

- Baseline params: `models/cloud_physics/params.yaml`
- Form factor authority: `models/system/form_factor.yaml` (`v2_kpp`)
- Seed manifest: `sim/config/seeds.yaml`
- Reproduce: `bash run_all.sh` or `make reproduce`
- Locked deps: `requirements-lock.txt` / `environment.yml`

## 12. Traceability

- Verification matrix: [`rtm/verification_matrix.md`](../../rtm/verification_matrix.md)
- Fill physics plan: [`analysis/fill_physics_test_plan.md`](../../analysis/fill_physics_test_plan.md)
- Human factors: [`analysis/human_factors_notes.md`](../../analysis/human_factors_notes.md)
- TRL gate: [`proposals/trl_gate_external.md`](../trl_gate_external.md)
- Partner gates: [`docs/11-partner-validation-and-trl-gates.md`](../../docs/11-partner-validation-and-trl-gates.md)

## 13. References

- [`rtm/verification_matrix.md`](../../rtm/verification_matrix.md)
- [`rtm/assumption_register.md`](../../rtm/assumption_register.md)
- [`analysis/tail_risk_analysis.md`](../../analysis/tail_risk_analysis.md)
- [`proposals/srd/MS-V-SRD.md`](../srd/MS-V-SRD.md)
