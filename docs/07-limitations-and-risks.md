# 07 — Limitations and Risks

## Bottom Line

Read [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md) first.

MS-V is a **model of a concept**, not a counter-UAS system and not a cleared grenade. The ~170 s figure is a model p10. It is not two minutes of cover. No soldier is cleared to throw, breathe, or move through this cloud.

---

## Hard Limits

| Limit | Reality |
|-------|---------|
| **Not standalone** | MS-V without visual smoke fails MoE vs FPV/fiber-optic |
| **Not instant** | Model build-up is about 12–15 s. That is not an order to throw, then move. |
| **Not RF defeat** | Jamming is EW's job |
| **Not kinetic kill** | Attack drones need MKFS / kinetic layer |
| **Not all-weather** | > 15 mph wind, heavy rain = degraded |
| **Friendly thermal blackout** | Model puts own troops in a dense MWIR cloud about 70% of the time on most use cases. Unvalidated. Do not enter the cloud. |
| **Heavier** | ~850 g on paper. Throw distance is not closed. |

---

## Accepted Trades

**Respiratory exposure** — not characterized. KPP-12 is unverified. Do not call it non-lethal. Do not call a short exposure tolerable. No mask drill is cleared, because there is no fill and no dose.

**Weight** — 850 g is the design target for a model duration above 120 s. Less comfortable than standard smoke. Issue quantity is a planning target only, not authorized.

**Build-up** — 12–15 s is a model build-up target. It is not an order to employ early.

---

## Threat Matrix

| Threat | MS-V alone | MS-V + visual smoke | Other layer needed |
|--------|------------|---------------------|-------------------|
| FPV (RF + EO/IR) | Not shown | Design target only — not measured | EW optional |
| Fiber-optic guided | Not shown | Design target only — not measured | None for RF |
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
| Paired-cloud hypothesis fails | Future paired-plume test; do not call visual-smoke pairing doctrine |
| Cost > $150 | Option C fill; volume scaling |
| Confusion with signal smoke | Distinct markings; training |

---

## What Success Looks Like

Not this: a squad throws 2–3 grenades and moves for 60–120 seconds under cover. The model’s casualty-recovery case meets its own lock test about **15%** of the time, and friendlies are thermally blacked out about **70%** of the time. That is not a success case.

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

