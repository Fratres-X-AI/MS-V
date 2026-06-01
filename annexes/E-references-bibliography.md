# Annex E — References and Bibliography

Sources used in the MS-V design package. MS-V performance targets reflect **revision v2** (density + duration priority, ~850 g form factor, combined employment with visual smoke).

---

## Primary US Military Sources

| Document | Title | Relevance |
|----------|-------|-----------|
| TM 43-0001-29 | Army Ammunition Data Sheets: Grenades | Baseline grenade specs (AN-M8, M18, M83, M15) |
| FM 23-30 | Grenades and Pyrotechnic Signals | Hand grenade employment procedures |
| FM 3-50 Ch. 7 | Visual-Infrared Obscurants | VI obscurant doctrine; transmittance/Pd planning |
| FM 3-50 App G | Smoke Operations — Cloud Phases | Streamer, build-up, uniform, terminal |
| JPEO PM CCS | Smoke Grenades product page | Current M83/M18 fielding data |

URLs: see v1 bibliography entries in project history; primary TM at [militarynewbie.com TM 43-0001-29 PDF](https://www.militarynewbie.com/wp-content/uploads/2013/11/TM-43-0001-29-Army-Ammunition-Data-Sheets-for-Grenades.pdf).

---

## Bispectral / Multispectral Obscurant Research

| Source | Relevance |
|--------|-----------|
| US Army ECBC (2014) — Bispectral Obscurant Grenade | Primary technical precedent; fill testing metrics |
| US Army ARL (2014) — Smokes/obscurants transmittance measurement | EETRANS spectrometer; VIS–FIR measurement |
| DTIC VPOS paper | Vehicle-scale multispectral obscurant context |
| DTIC COMBIC/XSCALE | Smoke modeling; mass extinction coefficient |

---

## Counter-UAS Layered Defense (Context)

| Source | Relevance |
|--------|-----------|
| DVIDS — IonStrike interceptor assessment | Kinetic layer (MKFS) analog |
| Northrop Grumman JCREW/DRAKE | EW layer for RF-linked drones |
| Rheinmetall ROSY | Vehicle multispectral obscurant; not squad-portable |

---

## MS-V Internal Documents

| Document | Path |
|----------|------|
| Executive Brief | [docs/00-executive-brief.md](../docs/00-executive-brief.md) |
| Concept Overview | [docs/01-concept-overview.md](../docs/01-concept-overview.md) |
| Operational Requirements | [docs/02-operational-requirements.md](../docs/02-operational-requirements.md) |
| Design Constraints | [docs/03-design-constraints.md](../docs/03-design-constraints.md) |
| CONOPS / Use Cases | [docs/04-conops-use-cases.md](../docs/04-conops-use-cases.md) |
| Key Design Trades | [docs/05-key-design-trades.md](../docs/05-key-design-trades.md) |
| System Description | [docs/06-system-description.md](../docs/06-system-description.md) |
| Limitations and Risks | [docs/07-limitations-and-risks.md](../docs/07-limitations-and-risks.md) |
| Layered Defense Integration | [docs/08-layered-defense-integration.md](../docs/08-layered-defense-integration.md) |
| Annex A — Baseline Comparison | [A-baseline-grenade-comparison.md](A-baseline-grenade-comparison.md) |
| Annex B — KPP Targets (v2) | [B-kpp-targets.md](B-kpp-targets.md) |
| Annex C — Trades Matrix (v2) | [C-trades-matrix.md](C-trades-matrix.md) |
| Annex D — Spectrum and Cloud Model (v2) | [D-spectrum-and-cloud-model.md](D-spectrum-and-cloud-model.md) |
| Baseline Data (JSON) | [data/baseline_grenades.json](../data/baseline_grenades.json) |

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| v1 | Initial build | 500 g, ≤8 s build-up, 60–90 s duration |
| v2 | Spec revision | ~850 g, 12–15 s build-up, 120+ s duration, density+duration priority, combined employment MoE |
| v2.1 | Tightening pass | Executive brief, sharper README/concept/CONOPS/limitations for external sharing |

---

## Disclaimer

MS-V is a conceptual design document. Proposed KPP targets are design goals — not fielded military requirements. Baseline grenade specifications sourced from TM 43-0001-29. All MS-V performance targets require validation through the test framework in Annex B.
