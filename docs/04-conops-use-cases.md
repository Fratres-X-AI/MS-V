# 04 — CONOPS / Use Cases

> **Not a drill.** These timelines are sketches. The model’s casualty-recovery lock-met is **14.9%**, and friendly thermal blackout on that case is **70.5%**. Toxicology is unverified. Do not train this. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).

Squad / fireteam **concept** only. Sketches below assume 2–3 MS-V + 1–2 visual smoke. They are not cleared steps.

---

## Use Case 1: Casualty Recovery

**Situation:** Casualty in the open; FPV or loitering drone observing.

| Time | Action |
|------|--------|
| T+0 | Sketch only. Do not throw. |
| T+12–15 s | Model does not show a screen. Do not move to the casualty on this timeline. |
| T+15–120 s | Model lock-met on this case is 14.9%. Not a recovery window. |

**Goal:** Break visual + thermal lock long enough to recover and reach cover.

---

## Use Case 2: Break Contact / Exfil

**Situation:** Squad withdrawing under drone-supported contact.

| Time | Action |
|------|--------|
| T+0 | Sketch only. Do not throw. |
| T+15–120 s | Model lock-met on this case is 31.6%. Not a bound. |
| T+90 s+ | Not a rescreen drill. |

**Goal:** Mask withdrawal; successive screens for multi-bound exfil. One 120 s screen will not cover 300+ m alone.

---

## Use Case 3: Mask Infil / Approach

**Situation:** Open-ground crossing or approach under loitering drone.

| Time | Action |
|------|--------|
| T−60 s | Sketch only. |
| T+0 | Do not throw. |
| T+15–90 s | Model lock-met on this case is 14.9%. Do not move through the cloud. |

**Goal:** A hoped-for shorter observation window. Not shown against fiber-optic or FPV.

---

## Use Case 4: Bounding Overwatch

**Situation:** Repositioning under drone overwatch.

| Time | Action |
|------|--------|
| T+0 | Sketch only. Do not throw. |
| T+15–60 s | Model lock-met on this case is 14.9%. Not a bound. |
| T+60–120 s | Not a second-volley drill. |

**Goal:** Temporary windows of reduced drone effectiveness per bound.

---

## Use Case 5: Hasty Defense

**Situation:** Occupying position under active drone search.

| Time | Action |
|------|--------|
| T+0 | Sketch only. Do not throw. |
| T+12–15 s | Acquisition is not shown to be degraded. |
| T+15–120 s | Model lock-met on this case is 61.1%, and friendly thermal blackout is about 70%. Do not occupy the cloud. |

**Goal:** Buy time to improve position without immediate engagement. Avoid cloud center — friendly thermal degraded inside.

---

## Quick Reference

```
Not a drill. Do not throw. Do not move on these times.
```

| Rule | Detail |
|------|--------|
| Never solo | MS-V alone is not shown to beat FPV or fiber-optic |
| Typical volley | A sketch of 2–3 MS-V + 1–2 visual smoke. Not an issue quantity. |
| Fiber-optic | Not shown. |
| FPV | Not shown. |

See [08 — Layered Defense Integration](08-layered-defense-integration.md).

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

