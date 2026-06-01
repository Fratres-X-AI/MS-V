# Test & Evaluation Master Plan (TEMP) Outline — MS-V Veil

> **Status:** Outline for TRL 3 transition — **not executed**  
> **Maturity ceiling:** Analytical TRL 3 after Phase 1B freeze; empirical TRL 4 requires external lab/range

## 1. Purpose

Define the empirical test program required to convert the literature-parameter sensitivity model into a validated obscurant characterization suitable for prototype down-select.

## 2. Test Objectives (priority order from OAT sensitivity)

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

## 3. Success Criteria (TRL 3)

| Metric | Model prediction (sensitivity) | Empirical accept |
|--------|-------------------------------|------------------|
| Duration p10 | ≥ 120 s at good thickness | Measured ≥ 120 s at 10th percentile conditions |
| Build-up p90 | ≤ 15 s | Measured ≤ 15 s |
| α(λ) bands | Literature bounds | Measured within ±20% of model mid |
| MoE lock-break | Surrogate non-binding | ≥ 60 s in ≥ 80% of instrumented trials |

## 4. Configuration Control

- Baseline params: `models/cloud_physics/params.yaml`
- Seed manifest: `sim/config/seeds.yaml`
- Reproduce: `bash run_all.sh` or `make reproduce`
- Locked deps: `requirements-lock.txt` / `environment.yml`

## 5. Schedule (external funding)

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| TRL 3a — Lab | 3–6 mo | α(λ), burn cup, particle sizing |
| TRL 3b — Chamber | 3–6 mo | Combined plume, MoE surrogate |
| TRL 4 — Range | 6–12 mo | Relevant-environment validation |

## 6. Traceability

- Verification matrix: [`rtm/verification_matrix.md`](../../rtm/verification_matrix.md)
- Fill physics plan: [`analysis/fill_physics_test_plan.md`](../../analysis/fill_physics_test_plan.md)
- Human factors: [`analysis/human_factors_notes.md`](../../analysis/human_factors_notes.md)
- TRL gate: [`proposals/trl_gate_external.md`](../trl_gate_external.md)

## 7. References

- [`rtm/verification_matrix.md`](../rtm/verification_matrix.md)
- [`rtm/assumption_register.md`](../rtm/assumption_register.md)
- [`analysis/tail_risk_analysis.md`](../analysis/tail_risk_analysis.md)
