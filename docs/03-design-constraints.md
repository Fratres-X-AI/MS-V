# 03 — Design Constraints

## Physical / Form Factor

| Constraint | Specification |
|------------|---------------|
| Configuration | Hand-thrown grenade with standard pin-pull arming |
| Target weight | **~850 g** (~30 oz) |
| Size envelope | **~25% larger** than AN-M8/M83 (~7.1 × 3.1 in notional) |
| Filler mass | 22–24 oz bispectral composition |
| Throw range | ≥ 20 m by average soldier (≥ 25 m objective) |
| Emission | 4 top + 1 bottom ports (inventory standard) |
| Body | Sheet-metal cylinder |

The ~850 g target allows sufficient fill mass for 2+ minute dense burn while remaining within soldier load limits for 1–2 grenades per soldier (1.7 kg for two MS-V).

---

## Interface / Compatibility

| Constraint | Specification |
|------------|---------------|
| Fuze | M201A1 or direct equivalent — **hard requirement** |
| Fuze delay | 0.7–2.0 seconds |
| Launchers | **None** — no new launchers or complex arming procedures |
| Pouches | Must fit standard grenade pouches (may be snug at ~850 g) |
| Training | Identical basic handling to AN-M8/M18 |

---

## Environmental and Durability

| Constraint | Specification |
|------------|---------------|
| Operating temperature | −20°C to +50°C |
| Drop survival | 1.5 m onto hard surface without functional degradation |
| Moisture | Exposure to rain/humidity without significant performance loss |
| Wind | Effective in light to moderate crosswind (≤ 15 mph) for majority of burn |
| Storage | Standard ammunition storage; ≥ 5 year shelf life target |
| Hazard class | 1.3G target (compatible with current smoke grenade logistics) |

---

## Cost and Producibility

| Constraint | Specification |
|------------|---------------|
| Unit cost target | $75–150 (goal, not hard requirement) |
| Manufacturing | Existing or near-existing processes and materials where possible |
| Fill technology | Proven bispectral/multispectral obscurant (ECBC-validated approaches) — not entirely novel chemistry |
| Production volume | Design for 100,000+ units/year scalability |
| Primary cost driver | Bispectral fill material (estimated 60–70% of unit cost) |

---

## Safety

| Constraint | Specification |
|------------|---------------|
| Respiratory irritation | **Acceptable (non-lethal)** — document and minimize where possible |
| Toxicity | Must not pose unacceptable toxicity or burn risks during normal handling, storage, or deployment with standard PPE |
| Fire hazard | Reduced vs. AN-M8 HC and M15 WP; must not ignite dry vegetation at standard standoff |
| HC / WP content | Zero |
| Safety data | Clear handling procedures and exposure guidelines must be developed before fielding |
| Training | Safe for training with standard protective measures |

MS-V will likely be **more irritating than M83 TA smoke** due to stronger IR obscurant chemistry. This is an accepted trade for multispectral performance.

---

## Logistics and Training

| Constraint | Specification |
|------------|---------------|
| Employment TTPs | Integrate into existing smoke grenade TTPs with **minimal additional training** |
| MS-V-specific training | Identification (markings), combined employment with visual smoke, respiratory guidance, friendly IR impact |
| Packaging | Compatible with current ammunition supply chains; 16 per packing box target |
| Resupply | Company-level, same chain as smoke grenades |
| Markings | Distinct from AN-M8/M18/M83 to prevent employment confusion |

---

## Out of Scope

- RF jamming or detection sensors
- Kinetic defeat mechanisms
- Remote or timed initiation beyond standard fuze delay
- Vehicle mounting or launcher compatibility

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

