# Annex B — MS-V Key Performance Parameters (Proposed Targets, v2)

All values in this annex are **proposed design goals** for the MS-V concept (revision v2). They prioritize **density + duration** over ultra-fast build-up. Derived from baseline US smoke grenade specifications, ECBC bispectral obscurant research, and project source-of-truth requirements.

---

## KPP Summary Table

| ID | Parameter | Threshold | Objective | Baseline Reference | Rationale |
|----|-----------|-----------|-----------|-------------------|-----------|
| KPP-01 | Total weight | ~850 g | 850 g | AN-M8: 680 g; M83: 454 g | ~25% larger envelope for fill mass; soldier-portable at 1–2 per soldier |
| KPP-02 | Cloud build-up to effective density | ≤ 15 s | ≤ 12 s | HC: ~10–20 s | Realistic with thicker/longer-burning fill; moderate priority |
| KPP-03 | Effective duration at good thickness | 120 s min | 130+ s | AN-M8: 105–150 s | User priority: 2+ minute dense screen |
| KPP-04 | Screening area (single grenade) | 30 sq ft | 40 sq ft | AN-M8: ~20–30 sq ft est. | Larger body + fill; used in 2–3 grenade groups |
| KPP-05 | Employment group size | 2 grenades min | 3 grenades | — | MoE requires combined MS-V + visual smoke in groups |
| KPP-06 | Spectral coverage | VIS + NIR + MWIR | Same | AN-M8: VIS only | Defeat common drone EO/IR sensors |
| KPP-07 | Fuze delay | 0.7–2.0 s | M201A1 standard | Inventory common | Training and logistics commonality |
| KPP-08 | Throw range | ≥ 20 m | ≥ 25 m | M18: ~35 m | Heavier grenade; realistic under stress |
| KPP-09 | Form factor | ~25% larger than AN-M8/M83 | ~7.1 × 3.1 in | 5.7 × 2.5 in baseline | Necessary for fill mass |
| KPP-10 | Operating temperature | −20°C to +50°C | Same | Military standard | Broad environmental coverage |
| KPP-11 | Wind tolerance | ≤ 15 mph | Same | FM 3-50 planning | Light to moderate crosswind for majority of burn |
| KPP-12 | Respiratory irritation | Acceptable (non-lethal) | Documented + minimized | M83: low; AN-M8: high | Stronger IR fill likely more irritating than TA |
| KPP-13 | Unit cost at scale | ≤ $150 | $75–100 | Vehicle systems: $10k+ | Ambitious but achievable with proven bispectral tech |
| KPP-14 | Issue quantity | 1–2 per soldier | Same | — | In addition to standard signal smoke |

---

## Measures of Effectiveness (MoE)

When employed in **groups of 2–3 MS-V grenades** in combination with **standard visual smoke** (AN-M8/M83), MS-V must:

1. Create sufficient multispectral obscuration to **defeat or significantly degrade** observation from FPV and fiber-optic guided drones
2. Provide adequate screening during the critical window for casualty movement, break contact, or reposition under observation
3. Maintain effective cloud thickness for the **majority of the 120+ second burn** in light to moderate crosswind (≤ 15 mph)

MoE is assessed against UAS surrogate sensors (visible camera + uncooled/cooled thermal) in operational demonstration tests, not against RF-linked or autonomous navigation-only threats.

---

## Detailed KPP Definitions

### KPP-02: Cloud Build-Up Time

**Definition:** Elapsed time from first visible emission until the cloud reaches effective density across target spectral bands (VIS, NIR, MWIR) within the grenade's screening area.

**Acceptance:** ≤ 15 s threshold; ≤ 12 s objective at 3 m height, ≤ 10 mph wind, 20°C, 50% RH.

**Note:** Build-up speed is a **moderate** design priority. Density and duration take precedence.

### KPP-03: Effective Duration

**Definition:** Duration during which cloud maintains effective screening thickness (qualitative density assessment + spectral attenuation) at cloud center.

**Acceptance:** 120 s minimum; 130+ s objective. "Good thickness" means visually opaque at 10 m and measurably attenuating in NIR/MWIR bands.

### KPP-04: Screening Area

**Definition:** Horizontal area at 2 m AGL where effective screening is achieved per single grenade.

**Acceptance:** 30 sq ft threshold; 40 sq ft objective. Groups of 2–3 grenades create overlapping coverage for squad-level MoE.

### KPP-12: Respiratory Irritation

**Definition:** Acceptable non-lethal respiratory effects from obscurant cloud at standard employment standoff (≥ 5 m from ignition point).

**Acceptance:** Irritation acceptable with standard protective measures (mask when entering dense cloud; brief exposure tolerable in open terrain). Full safety characterization and employment guidelines required before fielding. Must remain below acute toxicity thresholds for non-lethal employment.

---

## Environmental Operating Envelope

| Condition | Effective Range | Degradation Notes |
|-----------|----------------|-------------------|
| Wind 0–5 mph | Full KPP performance | Optimal |
| Wind 5–10 mph | Full to slightly reduced coverage | Throw upwind of protected position |
| Wind 10–15 mph | Reduced coverage; cloud elongates | Effective for majority of burn if thrown correctly |
| Wind > 15 mph | Not recommended | Rapid dissipation |
| Temperature −20 to +50°C | Full performance | Standard operating range |
| Humidity 20–95% | Full performance | Fill must be humidity-stable |
| Heavy rain | Duration reduced 30–50% | Degraded; not primary employment condition |
| Drop from 1.5 m | No functional degradation | Durability requirement |

---

## Test and Evaluation Framework

Based on ECBC bispectral obscurant grenade program metrics:

| Metric | Description | Application |
|--------|-------------|-------------|
| Mass extinction coefficient (α) | Extinction per unit mass (m²/g), wavelength-dependent | Fill down-select |
| Cloud geometry | Height, width, area vs. time | KPP-04 verification |
| Duration at effective thickness | Time above density threshold | KPP-03 verification |
| Combined employment test | 2–3 MS-V + AN-M8 vs. FPV/fiber-optic surrogate | MoE verification |
| Respiratory exposure assessment | Irritation characterization | KPP-12 safety gate |

Transmittance at fixed LOS remains a useful test metric but is not a hard gating KPP in v2 — operational MoE (drone observation defeat in combined employment) takes precedence.

---

## Traceability to Baseline

| MS-V KPP | vs. AN-M8 | vs. M83 | Design Trade |
|----------|-----------|---------|--------------|
| KPP-01 (850 g) | +25% weight | +87% weight | Enables KPP-03 duration + density |
| KPP-03 (120+ s) | Comparable | Exceeds | Requires larger fill mass |
| KPP-02 (12–15 s) | Similar | Similar | Accepts slower build-up for multispectral fill |
| KPP-06 (spectrum) | Exceeds (IR added) | Exceeds | Core capability |
| KPP-12 (irritation) | Better than HC | Worse than TA | Accepted for performance |

See [Annex C — Trades Matrix](C-trades-matrix.md) for design option analysis.

---

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION · Primary envelope: v2 KPP (850 g, 7.1 × 3.1 in)*
