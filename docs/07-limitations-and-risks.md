# 07 — Limitations and Risks

## Bottom Line

MS-V is a **tactical enabler**, not a counter-UAS system. It buys **~2 minutes of combined visual-thermal cover** when employed correctly (2–3 grenades + visual smoke). It will not defeat every drone, every condition, or every threat alone.

---

## Hard Limits

| Limit | Reality |
|-------|---------|
| **Not standalone** | MS-V without visual smoke fails MoE vs FPV/fiber-optic |
| **Not instant** | 12–15 s build-up — throw before you move, not during |
| **Not RF defeat** | Jamming is EW's job |
| **Not kinetic kill** | Attack drones need MKFS / kinetic layer |
| **Not all-weather** | > 15 mph wind, heavy rain = degraded |
| **Not friendly-blind** | Degrades own thermal optics in/near cloud |
| **Heavier** | ~850 g; 20–25 m throw; 1.7 kg for two |

---

## Accepted Trades

**Respiratory irritation** — stronger IR fill likely irritates more than M83 TA. Non-lethal, documented, minimized where possible. Mask in dense cloud; brief open-air exposure tolerable with PPE guidance.

**Weight** — 850 g is the price of 120+ s dense multispectral burn. Less comfortable than standard smoke; still within 1–2 per soldier load.

**Build-up** — 12–15 s means the drone may hold lock briefly. Doctrine: employ early.

---

## Threat Matrix

| Threat | MS-V alone | MS-V + visual smoke | Other layer needed |
|--------|------------|---------------------|-------------------|
| FPV (RF + EO/IR) | Partial | **Effective (target)** | EW optional |
| Fiber-optic guided | Partial | **Effective (target)** | None for RF |
| RF-linked observer | Partial | Partial | **EW** |
| Autonomous navigation | None | None | **Kinetic / deception** |
| One-way attack | Obscuration only | Obscuration only | **Kinetic** |
| mm-wave / acoustic | None | None | Other |

---

## Program Risks

| Risk | Mitigation |
|------|------------|
| Fill won't meet 120+ s + MWIR together | 850 g envelope; ECBC fill path; Option C fallback |
| Irritation exceeds acceptable threshold | Early safety testing; reformulate if needed |
| Soldiers skip visual smoke pairing | Doctrine; MoE requires combined employment |
| Cost > $150 | Option C fill; volume scaling |
| Confusion with signal smoke | Distinct markings; training |

---

## What Success Looks Like

A squad under drone overwatch throws 2–3 MS-V + visual smoke, moves for 60–120 seconds under combined cover, and **breaks or degrades** FPV/fiber-optic observation long enough to recover a casualty, break contact, or reach defilade.

What success is **not**: one grenade, no visual smoke, instant opacity, all drone types, all weather, no irritation.

See [08 — Layered Defense Integration](08-layered-defense-integration.md) for system context.

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

