# Annex B — MS-V Key Performance Parameters (Proposed Targets, v2)

All values in this annex are **proposed design goals** for the MS-V concept (revision v2). They prioritize **density + duration** over ultra-fast build-up. Derived from baseline US smoke grenade specifications, ECBC bispectral obscurant research, and project source-of-truth requirements.

---

## KPP Summary Table

| ID | Parameter | Threshold | Objective | Baseline Reference | Rationale |
|----|-----------|-----------|-----------|-------------------|-----------|
| KPP-01 | Total weight | ~850 g | 850 g | AN-M8: 680 g; M83: 454 g | ~25% larger envelope for fill mass; issue quantity not authorized |
| KPP-02 | Cloud build-up to effective density | ≤ 15 s | ≤ 12 s | HC: ~10–20 s | Realistic with thicker/longer-burning fill; moderate priority |
| KPP-03 | Effective duration at good thickness | 120 s min | 130+ s | AN-M8: 105–150 s | User priority: 2+ minute dense screen |
| KPP-04 | Screening area (single grenade) | 30 sq ft | 40 sq ft | AN-M8: ~20–30 sq ft est. | Larger body + fill; used in 2–3 grenade groups |
| KPP-05 | Modeled group size | 2 grenades min | 3 grenades | — | Paired-cloud scenario only; not doctrine |
| KPP-06 | Spectral coverage | VIS + NIR + MWIR | Same | AN-M8: VIS only | Target common drone EO/IR sensors; not measured |
| KPP-07 | Fuze delay | 0.7–2.0 s | M201A1 standard | Inventory common | Training and logistics commonality |
| KPP-08 | Throw range | ≥ 20 m | ≥ 25 m | M18: ~35 m | Heavier grenade; realistic under stress |
| KPP-09 | Form factor | ~25% larger than AN-M8/M83 | ~7.1 × 3.1 in | 5.7 × 2.5 in baseline | Necessary for fill mass |
| KPP-10 | Operating temperature | −20°C to +50°C | Same | Military standard | Broad environmental coverage |
| KPP-11 | Wind tolerance | ≤ 15 mph | Same | FM 3-50 planning | Light to moderate crosswind for majority of burn |
| KPP-12 | Respiratory irritation | **Unverified — no target set** | No panel yet | M83: low; AN-M8: high | Do not claim non-lethal. See SOLDIER_SAFETY.md |
| KPP-13 | Unit cost at scale | ≤ $150 | $75–100 | Vehicle systems: $10k+ | Ambitious but achievable with proven bispectral tech |
| KPP-14 | Issue quantity | Planning target only | Same | — | Not authorized while KPP-12 is open |

---

## Measures of Effectiveness (MoE)

For a future paired-cloud test case using **groups of 2–3 MS-V grenades** in combination with **standard visual smoke** (AN-M8/M83), MS-V would need to:

1. Create measured multispectral obscuration against FPV and fiber-optic guided drone surrogate sensors
2. Avoid implying a casualty-movement, break-contact, or reposition procedure until MOE-02 closes
3. Demonstrate effective cloud thickness in measured wind, not only model duration

MoE remains unclosed until assessed against UAS surrogate sensors (visible camera + uncooled/cooled thermal) in instrumented tests.

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

**Definition:** Respiratory effect of the cloud at employment distance. Not measured.

**Acceptance:** None. No standoff, no mask drill, and no “brief exposure” is cleared. KPP-12 stays open until a toxicology panel on the actual fill says otherwise.

---

## Environmental Operating Envelope

| Condition | Effective Range | Degradation Notes |
|-----------|----------------|-------------------|
| Wind 0–5 mph | Not measured | Future range case |
| Wind 5–10 mph | Not measured | Do not write throw guidance |
| Wind 10–15 mph | Not measured | KPP-11 not closed |
| Wind > 15 mph | Not measured | No recommendation |
| Temperature −20 to +50°C | Model duration above threshold | Chamber still required |
| Humidity 20–95% | Not measured | Fill must be humidity-stable |
| Heavy rain | Not measured | Do not use a duration-reduction figure |
| Drop from 1.5 m | No functional degradation | Durability requirement |

---

## Test and Evaluation Framework

Based on ECBC bispectral obscurant grenade program metrics:

| Metric | Description | Application |
|--------|-------------|-------------|
| Mass extinction coefficient (α) | Extinction per unit mass (m²/g), wavelength-dependent | Fill down-select |
| Cloud geometry | Height, width, area vs. time | KPP-04 verification |
| Duration at effective thickness | Time above density threshold | KPP-03 verification |
| Paired-cloud test | 2–3 MS-V + AN-M8 vs. FPV/fiber-optic surrogate | Future MoE verification |
| Respiratory exposure assessment | Irritation characterization | KPP-12 safety gate |

Transmittance at fixed LOS remains a useful test metric. The current tri-band value is numerically saturated and not a measured cloud; no operational defeat claim takes precedence over that gap.

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
