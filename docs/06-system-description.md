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

| Phase | Time | Event |
|-------|------|-------|
| Employment | T+0 | Pin pull; throw 20–25 m; seek cover ≥ 5 m |
| Fuze delay | T+0–2 s | Striker → primer → delay → ignition |
| Ignition | T+2 s | Starter ignites fill; port tape blown off |
| Streamer | T+2–5 s | Initial emission jets |
| Build-up | T+5–12 s | Streamers merge; density increasing |
| **Effective density** | **T+12–15 s** | **Combined multispectral screen operational** |
| Uniform | T+15–135 s | 120+ s at good thickness |
| Terminal | T+135 s+ | Density declining; rescreen if needed |

---

## Combined Employment

MS-V is designed for **combined use with standard visual smoke**:

| Grenade | Quantity (typical) | Function |
|---------|-------------------|----------|
| MS-V | 2–3 | Multispectral core (VIS + NIR + MWIR) |
| AN-M8 or M83 | 1–2 | Visual opacity; FPV video degradation |

**Throw pattern:** Overlapping triangular or linear layout upwind of protected position. MS-V and visual smoke may be thrown at same point or offset 5–10 m for coverage extension.

---

## Basic Employment

1. Identify drone observation axis
2. Select MS-V (by marking) and visual smoke from load
3. Pull pins; throw 2–3 MS-V + 1–2 visual smoke in pattern
4. Wait for effective density (~12–15 s)
5. Execute maneuver under combined screen
6. Rescreen if action exceeds 120 s

### Throw Technique

| Parameter | Guidance |
|-----------|----------|
| Distance | 20–25 m (heavier than standard smoke) |
| Direction | Between friendly force and threat sensor; upwind |
| Arc | Low arc preferred for ground-hugging cloud |
| Standoff | ≥ 5 m from ignition point |

---

## Safety Features and Guidance

| Topic | Guidance |
|-------|----------|
| Respiratory irritation | Acceptable non-lethal; **mask in dense cloud** |
| Brief exposure | Tolerable in open terrain at ≥ 10 m standoff |
| Friendly thermal | Degraded inside/near cloud — employment doctrine mitigates |
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
| Issue | 1–2 per soldier, plus standard signal smoke |

---

## Training Requirements

| Event | Content |
|-------|---------|
| Familiarization (30 min) | ID, handling, irritation, friendly IR impact |
| Combined employment (1 hr) | MS-V + visual smoke patterns; CONOPS scenarios |
| Layered defense (1 hr) | EW, kinetic coordination |
| Live throw | Per unit SOP; 2 throws minimum |

Basic fuze operation requires no training beyond standard smoke grenade qualification (FM 23-30).

See [Annex B](../annexes/B-kpp-targets.md) for KPP acceptance criteria.
