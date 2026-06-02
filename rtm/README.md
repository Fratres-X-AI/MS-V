# Requirements Traceability Matrix (RTM)

Submission-grade audit trail for MS-V Phase 1 M&S.

| Artifact | Purpose |
|----------|---------|
| [`requirements_traceability.csv`](requirements_traceability.csv) | Req → job ID → seed → pass status |
| [`verification_matrix.md`](verification_matrix.md) | KPP/MoE with quantified margins + 38 jobs |
| [`verification_matrix.csv`](verification_matrix.csv) | Machine-readable job registry |
| [`assumption_register.md`](assumption_register.md) | Literature bounds + OAT + **Sobol** ranks |
| [`uncertainty_register.md`](uncertainty_register.md) | Quantitative bound definitions |
| [`decision_log.md`](decision_log.md) | Modeling decisions D-001–D-016 |
| [`audit_log.md`](audit_log.md) | Phase 0 doc cross-check |
| [`human_factors_notes.md`](../analysis/human_factors_notes.md) | KPP-08 throw ballistics |
| [`fill_physics_test_plan.md`](../analysis/fill_physics_test_plan.md) | TRL 3 bench test plan |

## Reviewer quick path (< 2 min)

1. Open `verification_matrix.md` → find KPP row → job ID + margin  
2. Open `assumption_register.md` → find assumption → TRL 3 test priority  
3. Run `python -m sim.reproduce` → golden checksum gate  
4. Sobol: `analysis/SOBOL_SENSITIVITY_REPORT.md`

## Partner / prime handoff

| Artifact | Purpose |
|----------|---------|
| [Licensing & partnership](../docs/licensing-and-partnership.md) | IP tiers, PCA, diligence index |
| [DOC-11 partner validation](../docs/11-partner-validation-and-trl-gates.md) | Bench/range gates |
| [partner_validation_results.template.json](../data/partner_validation_results.template.json) | Partner data schema (`status: pending`) |

## Seeds & config control

- `sim/config/seeds.yaml` — 38 mega-suite jobs  
- `sim/config/sobol.yaml` — Sobol campaign settings  
- `models/cloud_physics/params.yaml` — literature bounds (SHA in manifests)
