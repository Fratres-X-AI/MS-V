# 02 — Operational Requirements

## Primary Mission

Squad-level multispectral obscurant concept to study whether a paired visual + infrared cloud can disrupt UAS observation and targeting. This document is a requirements sketch, not an employment clearance.

---

## Key Performance Parameters

Full definitions: [Annex B](../annexes/B-kpp-targets.md).

| Parameter | Target |
|-----------|--------|
| Weight | ~850 g (~25% larger than AN-M8/M83) |
| Build-up | ≤ 12–15 s to effective density |
| Screening area | 30–40 sq ft/grenade; **2–3 grenade groups** |
| Duration | **120+ s** at good thickness |
| Spectrum | VIS + NIR + MWIR |
| Deployment | Hand-thrown, pin-pull concept; not cleared |
| Fuze | M201A1-compatible target; not tested |
| Issue | Planning target only; KPP-14 not closed |
| Temperature | −20°C to +50°C |
| Wind | ≤ 15 mph |
| Throw | ≥ 20 m (≥ 25 m objective) |
| Cost | $75–150 (goal) |

---

## Secondary Requirements

- Survives rough handling, 1.5 m drop, moisture exposure  
- Respiratory exposure is unverified; no non-lethal claim  
- Wind behavior is not shown; high-wind duration is not evidence of cover  
- No training-safe claim until toxicity, fuze, and range gates close  
- **Combined with AN-M8/M83** remains a hypothesis, not a demonstrated FPV/fiber-optic result  

---

## Measure of Effectiveness

The **2–3 MS-V + signal smoke** case is a model scenario only. It must not be described as defeating FPV or fiber-optic drone observation until an instrumented UAS surrogate range test exists.

Single-grenade or MS-V-only cases are not cleared either.

---

## Sensor Targets

| Sensor | Band | Requirement |
|--------|------|-------------|
| FPV / visible camera | VIS | Targeted; not shown |
| NVG / low-light | NIR | Targeted; not shown |
| Thermal (cooled/uncooled) | MWIR | Targeted; not shown |
| **Fused EO/IR (FPV, fiber-optic)** | VIS + IR | Primary hypothesis; not closed |

---

## Environment

| Condition | Effect |
|-----------|--------|
| −20°C to +50°C | Model duration stays above 120 s. Not measured performance. |
| 0–15 mph wind | Not shown. High-wind duration in the model does not move. |
| > 15 mph | Not a recommendation. The model is not wind-sensitive. |
| Heavy rain | Not measured. Do not use a 30–50% figure. |

---

## Verification (Summary)

1. Fill screening (α across bands)  
2. Single-grenade duration and area  
3. **Paired-plume instrumented test vs FPV/fiber-optic surrogate** (future MoE gate)  
4. Environmental matrix  
5. Respiratory safety characterization

---

## Traceability

- Verification matrix: [rtm/verification_matrix.md](../rtm/verification_matrix.md)
- Requirements CSV: [rtm/requirements_traceability.csv](../rtm/requirements_traceability.csv)
- Assumptions: [rtm/assumption_register.md](../rtm/assumption_register.md)
- Mega suite report: [analysis/MEGA_SUITE_REPORT.md](../analysis/MEGA_SUITE_REPORT.md)
- Sobol sensitivity: [analysis/SOBOL_SENSITIVITY_REPORT.md](../analysis/SOBOL_SENSITIVITY_REPORT.md)
- Reproduce gate: [REPRODUCE.md](../REPRODUCE.md)

---

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION*

