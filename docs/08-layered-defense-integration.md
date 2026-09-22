# 08 — Layered Defense Integration

MS-V is a **modeled concept**, not a fielded layer. Nothing below is a cleared integration. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).

```
Detect → EW (optional) → MS-V + Signal Smoke → Kinetic (MKFS)
```

| Layer | MS-V role |
|-------|-----------|
| Detection | MS-V does not detect. No throw is cleared. |
| EW | Jams RF; MS-V's EO/IR effect is not measured |
| Visual smoke | A modeled pairing, not a required partner — no MoE closed |
| Kinetic | Not shown to buy time |

Not shown against FPV or fiber-optic drones specifically. This is a target hypothesis, not a result.

---

## Layer 1: Detection

MS-V does **not** detect threats. Detection would cue a future test scenario only after the concept passes safety and range gates.

| System | Would cue future test scenario when... |
|--------|------------------------------|
| Acoustic | Drone audible overhead |
| RF detector | Control link detected (paired-cloud test case) |
| Soldier observation | Visual contact with UAS |
| EO/IR spotter | Thermal signature of orbiting UAS |

---

## Layer 2: Non-Kinetic — Electronic Warfare

| Aspect | Detail |
|--------|--------|
| EW role | Jam RF datalink; degrade RF-controlled drones |
| MS-V role | Hypothesized EO/IR obscuration; not measured |
| Combined | Future test case only |
| Fiber-optic drones | EW ineffective; MS-V + visual smoke remains unproven |
| Redundancy | Conceptual complement only |

---

## Layer 2: Non-Kinetic — Signal Smoke + MS-V (Paired-Cloud Hypothesis)

MS-V is **never the sole obscurant** in the model. There is no standard employment pair:

| Component | System | Function |
|-----------|--------|----------|
| Multispectral core | 2–3 × MS-V | Modeled VIS + NIR + MWIR attenuation |
| Visual supplement | 1–2 × AN-M8 / M83 | Modeled visible-opacity supplement |
| Combined MoE | Both | Future UAS surrogate test; not closed |

### Why Both Are Required

| Drone Type | Visual Smoke Alone | MS-V Alone | Combined |
|------------|-------------------|------------|----------|
| FPV (visible + thermal) | Partial | Not shown | Not shown |
| Fiber-optic guided | Partial (VIS) | Not shown | Not shown |
| Thermal-only loitering | None | Not shown | Not shown |
| Visible-only commercial | Effective | Overkill | Not an MS-V claim |

AN-M8/M18/M83 remain in the basic load for signaling, marking, and visual screening. MS-V adds the IR channel inventory smoke cannot provide.

---

## Layer 2: Non-Kinetic — MS-V Unique Contribution

| Capability | Signal Smoke | MS-V | Combined |
|------------|-------------|------|----------|
| Defeat visible camera | Yes | Partial | Yes |
| Defeat thermal imager | **No** | Yes | Yes |
| 120+ s dense multispectral | No | Yes | Yes |
| FPV / fiber-optic MoE | No | Partial | **Yes** |
| Squad-portable | Yes | Yes | Yes |
| Signaling / marking | Yes | No | Via signal smoke |

---

## Layer 3: Kinetic (MKFS)

| Aspect | Detail |
|--------|--------|
| Role | Physically defeat UAS threats |
| MS-V relationship | MS-V creates obscuration window; kinetic closes kill chain |
| Sequence | MS-V + smoke deployed → lock degraded → kinetic engages if threat persists or attacks |
| Analog | IonStrike-class interceptors integrated with FAAD/IBCS C2 |
| CONOPS | Kinetic handoff not in standard MS-V CONOPS — reserved for attack profiles |

MS-V does not replace kinetic defeat. It buys time and degrades sensors so kinetic layers engage more effectively.

---

## Integration Matrix

| Threat Profile | Detection | EW | Visual Smoke | MS-V | Kinetic |
|---------------|-----------|-----|-------------|------|---------|
*Not a cleared table. MS-V is not shown against any of these threats. No throw quantity is authorized.*

| FPV drone (RF + EO/IR) | Not shown | Not shown | Not shown | Not shown | N/A |
| Fiber-optic guided | Not shown | N/A | Not shown | Not shown | N/A |
| Observation UAS (EO/IR) | Not shown | Not shown | Not shown | Not shown | N/A |
| Loitering munition | Not shown | Not shown | Not shown | Not shown | N/A |
| CASEVAC under UAS | Not shown | Not shown | Not shown | Not shown | N/A |
| Break contact | Not shown | Not shown | Not shown | Not shown | N/A |

---

## Issue and Employment — Not Written

There is no issue quantity, employment authority, or mission procedure. MS-V is not a fielded item. KPP-14 (issue quantity) is not closed while KPP-12 (toxicology) is open. Writing a load table or a mission checklist here would read as authorization that does not exist.

See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md) and [04 — CONOPS / Use Cases](04-conops-use-cases.md), which is also marked not a drill.

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

