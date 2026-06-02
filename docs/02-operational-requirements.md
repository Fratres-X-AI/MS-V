# 02 — Operational Requirements

## Primary Mission

Squad-level multispectral obscurant to **disrupt UAS observation and targeting** during contact, casualty recovery, and maneuver — employed **with standard visual smoke**, not alone.

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
| Deployment | Hand-thrown, pin-pull |
| Fuze | M201A1 compatible |
| Issue | 1–2 per soldier + standard smoke |
| Temperature | −20°C to +50°C |
| Wind | ≤ 15 mph |
| Throw | ≥ 20 m (≥ 25 m objective) |
| Cost | $75–150 (goal) |

---

## Secondary Requirements

- Survives rough handling, 1.5 m drop, moisture exposure  
- Non-lethal respiratory irritation — documented, minimized where possible  
- Effective in light crosswind for majority of burn  
- Training-safe with standard PPE  
- **Combined with AN-M8/M83** → effective vs FPV and fiber-optic drones  

---

## Measure of Effectiveness

**2–3 MS-V + signal smoke** must defeat or significantly degrade **FPV and fiber-optic** drone observation during casualty movement, break contact, or reposition.

Single-grenade or MS-V-only employment is **not** the acceptance standard.

---

## Sensor Targets

| Sensor | Band | Requirement |
|--------|------|-------------|
| FPV / visible camera | VIS | Degraded in combined employment |
| NVG / low-light | NIR | Degraded |
| Thermal (cooled/uncooled) | MWIR | Degraded |
| **Fused EO/IR (FPV, fiber-optic)** | VIS + IR | **Primary MoE** |

---

## Environment

| Condition | Effect |
|-----------|--------|
| −20°C to +50°C | Full performance |
| 0–15 mph wind | Effective; throw upwind |
| > 15 mph | Not recommended |
| Heavy rain | 30–50% duration reduction |

---

## Verification (Summary)

1. Fill screening (α across bands)  
2. Single-grenade duration and area  
3. **Combined employment vs FPV/fiber-optic surrogate** (MoE gate)  
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

