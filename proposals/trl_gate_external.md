# TRL Gate — External Verification Package

> **Purpose:** Define evidence required to advance MS-V from TRL 2–3 (M&S) to TRL 4 (component validation).

## Current status (M&S)

| Gate | Evidence | Status |
|------|----------|--------|
| G0 | Literature sensitivity 140M | **Complete** — [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) |
| G1 | Reproducibility harness | **Complete** — `python -m sim.reproduce` (v4 golden profile) |
| G2 | Global sensitivity Sobol | **Complete** — [`analysis/SOBOL_SENSITIVITY_REPORT.md`](../analysis/SOBOL_SENSITIVITY_REPORT.md) |
| G3 | Form factor design authority | **Complete** — Annex F + STL |
| G4 | CONOPS timeline | **Complete** — MOE-02 in matrix |

## TRL 3 → 4 gates (external)

| Gate | Deliverable | Owner | Closes |
|------|-------------|-------|--------|
| E-1 | Fill physics bench ([`analysis/fill_physics_test_plan.md`](../analysis/fill_physics_test_plan.md)) | Lab | KPP-03, KPP-06, KPP-12 |
| E-2 | Throw range under load (n≥30) | HF range | KPP-08 |
| E-3 | Prototype mass / balance | Prototype | KPP-01 |
| E-4 | UAS surrogate FPV + thermal lock-break | Range | MOE-01, A-013 |
| E-5 | Environmental chamber (−20/+50°C) | Lab | KPP-10 confirmation |

## Forbidden claims before E-1..E-5

- Field validation, military ready, empirical MS-V fill performance
- MoE 100% pass as lock-break confirmation when `surrogate_saturated=true`

## Submission cross-refs

- SRD: [`proposals/srd/MS-V-SRD.md`](srd/MS-V-SRD.md)
- TEMP outline: [`proposals/temp/MS-V-TEMP-outline.md`](temp/MS-V-TEMP-outline.md)
- Partner validation plan: [`docs/11-partner-validation-and-trl-gates.md`](../docs/11-partner-validation-and-trl-gates.md)
- Licensing: [`docs/licensing-and-partnership.md`](../docs/licensing-and-partnership.md)
