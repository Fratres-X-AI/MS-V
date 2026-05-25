# MS-V — Multispectral Obscurant Grenade (Veil)

**Squad-layer tool for drone manipulation.** MS-V is a hand-thrown, pin-pull multispectral obscurant grenade that generates a dense visual and infrared screening cloud to disrupt UAS observation, break thermal and visual locks, and create uncertainty during contact, casualty recovery, and small unit movement.

Carried **in addition to** standard signal smoke. Always employed in **groups of 2–3 with visual smoke** for best effect against FPV and fiber-optic guided drones.

> **Disclaimer:** Conceptual design document. Proposed performance targets are design goals (v2) — not fielded military requirements.

---

## Quick Spec Card

| Parameter | AN-M8 HC | M83 TA | **MS-V (proposed v2)** |
|-----------|----------|--------|------------------------|
| Weight | 680 g (24 oz) | 454 g (16 oz) | **~850 g (~30 oz)** |
| Size vs baseline | Standard | Standard | **~25% larger envelope** |
| Filler | 19 oz HC (VIS only) | 11 oz TA (VIS only) | **22–24 oz bispectral** |
| Duration | 105–150 s | 25–90 s | **120+ s at good thickness** |
| Build-up | ~10–20 s | ~10–15 s | **≤ 12–15 s** |
| Spectrum | VIS only | VIS only | **VIS + NIR + MWIR** |
| IR defeat | No | No | **Yes** |
| Employment | Single or multiple | Single or multiple | **2–3 MS-V + visual smoke** |
| Fuze | M201A1 | M201A1 | **M201A1-compatible** |
| Issue | Standard smoke load | Standard smoke load | **+1–2 per soldier** |
| Unit cost | ~$15–25 | ~$15–25 | **$75–150 target** |
| Irritation | High (HCl) | Low | **Acceptable (non-lethal)** |
| Role | Visual screening, signaling | Practice screening | **UAS multispectral screen** |

---

## Document Map

### Core Documents

| # | Document | Description |
|---|----------|-------------|
| 01 | [Concept Overview](docs/01-concept-overview.md) | Purpose, problem statement, design philosophy |
| 02 | [Operational Requirements](docs/02-operational-requirements.md) | Mission, KPPs, MoE, secondary requirements |
| 03 | [Design Constraints](docs/03-design-constraints.md) | Form factor, safety, cost, logistics |
| 04 | [CONOPS / Use Cases](docs/04-conops-use-cases.md) | Five drone-manipulation scenarios |
| 05 | [Key Design Trades](docs/05-key-design-trades.md) | Density, duration, toxicity, cost trade-offs |
| 06 | [System Description](docs/06-system-description.md) | Components, functioning, combined employment |
| 07 | [Limitations and Risks](docs/07-limitations-and-risks.md) | Honest capability limits and risks |
| 08 | [Layered Defense Integration](docs/08-layered-defense-integration.md) | Detection, EW, signal smoke, kinetic layers |

### Engineering Annexes

| Annex | Document | Description |
|-------|----------|-------------|
| A | [Baseline Grenade Comparison](annexes/A-baseline-grenade-comparison.md) | TM 43-0001-29 data vs MS-V v2 |
| B | [KPP Targets (v2)](annexes/B-kpp-targets.md) | Performance parameters and MoE |
| C | [Trades Matrix (v2)](annexes/C-trades-matrix.md) | Fill options and recommended baseline |
| D | [Spectrum and Cloud Model (v2)](annexes/D-spectrum-and-cloud-model.md) | Bands, FPV/fiber-optic notes, timing |
| E | [References and Bibliography](annexes/E-references-bibliography.md) | Sources and revision history |

### Data

| File | Description |
|------|-------------|
| [data/baseline_grenades.json](data/baseline_grenades.json) | Machine-readable baseline specs and MS-V v2 targets |

---

## Key Design Decisions (v2)

| Decision | Selection | Rationale |
|----------|-----------|-----------|
| Design priority | **Density + duration** | 2+ min thick cloud; user requirement |
| Weight | **~850 g** | ~25% larger; enables fill mass for 120+ s burn |
| Build-up | **≤ 12–15 s** | Moderate priority; realistic with multispectral fill |
| Duration | **120+ s** | Matches/exceeds AN-M8; with added IR |
| Fill | Unified bispectral (Option A) | ECBC-validated; VIS + NIR + MWIR |
| Employment | **2–3 MS-V + visual smoke** | Required for FPV/fiber-optic MoE |
| Irritation | **Accepted (non-lethal)** | Trade for IR performance; document + minimize |
| Fuze | M201A1-compatible | Training and logistics commonality |
| Philosophy | Soldier-first, obscuration only | No detection, jamming, or kinetic |

---

## Layered Defense Context

MS-V is the **multispectral obscuration layer** — always paired with standard visual smoke:

```
Detection → EW (optional) → MS-V + Signal Smoke → Kinetic (MKFS)
```

| Layer | MS-V Relationship |
|-------|-------------------|
| Detection | Cues employment; MS-V does not detect |
| EW | Complementary — jams RF; MS-V defeats EO/IR |
| Visual smoke (AN-M8/M83) | **Required partner** — combined MoE vs FPV/fiber-optic |
| Kinetic (MKFS) | MS-V degrades sensors; kinetic defeats persisted threats |

Fiber-optic and FPV drones immune to EW are the **primary MoE target** for combined MS-V + visual smoke employment.

---

## Repository Structure

```
MS-V/
├── README.md
├── docs/          (01–08 core documents)
├── annexes/       (A–E engineering annexes)
└── data/          (baseline_grenades.json)
```

---

## Primary Sources

- [TM 43-0001-29 — Army Ammunition Data Sheets: Grenades](https://www.militarynewbie.com/wp-content/uploads/2013/11/TM-43-0001-29-Army-Ammunition-Data-Sheets-for-Grenades.pdf)
- [FM 3-50 Ch. 7 — Visual-Infrared Obscurants](https://www.globalsecurity.org/military/library/policy/army/fm/3-50/Ch7.htm)
- [ECBC Bispectral Obscurant Grenade (Army.mil, 2014)](https://www.army.mil/article/116366/ecbc_develops_the_u_s_armys_first_bispectral_obscurants_grenade)

Full bibliography: [Annex E](annexes/E-references-bibliography.md)
