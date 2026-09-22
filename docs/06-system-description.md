# 06 — System Description

High-level description of MS-V components, functioning, and employment. Conceptual design — not manufacturing drawings.

---

## System Overview

MS-V is a burning-type hand grenade (~850 g, ~25% larger than standard smoke) that generates a multispectral aerosol cloud upon ignition. Architecture matches inventory smoke grenades (AN-M8/M18/M83) with bispectral fill and enlarged body for extended dense burn.

```
┌─────────────────────────────────────┐
│           M201A1 Fuze              │  Pull ring / safety lever
│         (0.7–2.0 s delay)          │
├─────────────────────────────────────┤
│         Starter Mixture              │
├─────────────────────────────────────┤
│                                     │
│   Bispectral Aerosol Fill           │  22–24 oz
│   (VIS + NIR + MWIR)                │
│                                     │
├─────────────────────────────────────┤
│  ○   ○   ○   ○   (4 top ports)     │
│              ○   (1 bottom port)    │
└─────────────────────────────────────┘
   ~7.1 × 3.1 in sheet metal body
   ~850 g total weight
```

---

## Components

| Component | Specification |
|-----------|---------------|
| Body | Sheet steel cylinder, ~7.1 × 3.1 in, olive drab with MS-V marking band |
| Fuze | M201A1-compatible, pyrotechnic delay-igniting, 0.7–2.0 s |
| Starter | Ignites bispectral fill; may differ slightly from HC starter |
| Fill | 22–24 oz unified bispectral pyrotechnic composition |
| Ports | 4 top + 1 bottom; pressure-sensitive tape |
| Markings | "MS-V" stencil; distinctive top band (not white/color like AN-M8/M18) |

---

## Functioning Sequence

> Model sketch. Not a functioning round. Fuze, ignition, and screen times below are design hopes. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).

| Phase | Time | Event |
|-------|------|-------|
| Employment | T+0 | Not cleared. Published 20 m throw was floored. |
| Fuze delay | T+0–2 s | Not a fuze test. Delays in the model are drawn inside the pass band. |
| Ignition | T+2 s | No fill has been burned. |
| Build-up | T+5–15 s | Model p90 only. Not a screen. |
| Duration | ~170 s model p10 | Not cover time. |

---

## Paired-Cloud Model Scenario

MS-V is modeled with standard visual smoke. This is not a cleared employment method:

| Grenade | Quantity (model) | Function |
|---------|-------------------|----------|
| MS-V | 2–3 | Multispectral core hypothesis (VIS + NIR + MWIR) |
| AN-M8 or M83 | 1–2 | Visual-opacity supplement hypothesis |

There is no cleared throw pattern.

---

## Basic Employment

Not written. Toxicology is open, the throw number was floored, and the CONOPS model does not clear a movement. Do not pull a pin on this concept.

---

## Safety Features and Guidance

| Topic | Guidance |
|-------|----------|
| Respiratory irritation | Unverified. No exposure is tolerable. |
| Brief exposure | Not cleared at any standoff. |
| Friendly thermal | Model blackout about 70% on most use cases. Do not enter the cloud. |
| Fire hazard | Reduced vs HC; avoid dry grass at minimum standoff |
| Identification | MS-V marking band + stencil — do not confuse with signal smoke |
| Storage | 1.3G; standard ammunition storage |

---

## Packaging and Logistics

| Parameter | Specification |
|-----------|---------------|
| Individual container | 1 per container |
| Packing box | 16 per box (target) |
| Hazard class | 1.3G |
| Issue | Not authorized. KPP-14 is not closed. |

---

## Training Requirements

| Event | Content |
|-------|---------|
No training course. There is no round to throw and no fuze that has been tested. Do not teach FM 23-30 as if it covers MS-V.

See [Annex B](../annexes/B-kpp-targets.md) for KPP acceptance criteria.

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

