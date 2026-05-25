# 02 — Operational Requirements

## Primary Mission

Serve as a squad-level, rapidly deployable multispectral obscurant tool to **manipulate and disrupt UAS/drone observation and targeting** during close contact, casualty recovery, and small unit maneuvers.

MS-V is not a general-purpose smoke grenade. It is a specialized drone-manipulation tool employed in combination with standard visual smoke.

---

## Key Performance Parameters (KPPs)

Proposed design targets (v2). Full definitions in [Annex B](../annexes/B-kpp-targets.md).

| Parameter | Revised Target | Rationale / Notes |
|-----------|---------------|-------------------|
| Weight | ~850 g (~25% larger than AN-M8/M83) | Allows more fill mass for longer, denser burn while staying soldier-portable |
| Cloud build-up time | ≤ 12–15 s to effective density | Relaxed from ultra-fast targets; realistic with thicker/longer-burning fill |
| Effective screening area | 30–40 sq ft per grenade (in 2–3 grenade groups) | Increased due to larger size and fill mass |
| Effective duration | **120+ seconds (2+ minutes)** at good thickness | User priority: longer burn while maintaining density |
| Spectrum coverage | Visual + NIR + MWIR | Disrupt common drone EO/IR sensors |
| Deployment method | Hand-thrown, pin-pull | Simple, intuitive under stress |
| Fuze | M201A1 compatible | Logistics and training commonality |
| Issue quantity | 1–2 per soldier (in addition to standard smoke) | Complementary capability |
| Operating temperature | −20°C to +50°C | Broad environmental coverage |
| Wind tolerance | Light to moderate (≤ 15 mph) | Realistic infantry conditions |
| Throw range | ≥ 20 m (≥ 25 m objective) | Heavier grenade; average soldier under stress |
| Unit cost | $75–150 (goal, not hard requirement) | Ambitious at multispectral performance level |

---

## Secondary Requirements

- Must remain **reliable after rough handling**, drops from 1.5 m onto hard surfaces, and exposure to moisture/rain.
- **Respiratory irritation is acceptable (non-lethal)** but must be documented and minimized where possible. Full safety characterization required.
- Cloud should remain effective in **light crosswinds (≤ 15 mph)** for the majority of burn time.
- Safe for training use with **standard protective measures** (mask in dense cloud; brief open-air exposure tolerable).
- When used in combination with standard visual smoke (AN-M8/M83), MS-V must enable effective obscuration against **FPV and fiber-optic guided drones** that rely on both visual and thermal observation.

---

## Measures of Effectiveness (MoE)

When employed in **groups of 2–3 MS-V grenades** in combination with **standard signal smoke**, MS-V must:

1. Create sufficient multispectral obscuration to **defeat or significantly degrade** observation from FPV and fiber-optic guided drones
2. Provide adequate screening during the critical window needed to conduct **casualty movement**, **break contact**, or **reposition under observation**
3. Maintain effective cloud thickness for the **majority of the 120+ second burn** in light to moderate crosswind

MoE is the primary acceptance standard — not single-grenade performance in isolation.

---

## Multispectral Performance

| Sensor Class | Band | Requirement |
|--------------|------|-------------|
| Visible UAS camera / FPV | VIS (0.4–0.7 µm) | Effective degradation in combined employment |
| Low-light / NVG | NIR (0.7–1.4 µm) | Effective degradation |
| Cooled / uncooled thermal | MWIR (3–5 µm) | Effective degradation |
| Fused EO/IR (FPV, fiber-optic) | VIS + IR | **Primary MoE target** with visual smoke supplement |

---

## Environmental Conditions

| Condition | Requirement |
|-----------|-------------|
| Temperature | −20°C to +50°C — full performance |
| Wind | 0–15 mph — effective for majority of burn; throw upwind |
| Wind > 15 mph | Not recommended |
| Humidity | 20–95% RH — fill must be humidity-stable |
| Rain | Degraded; duration reduced 30–50% in heavy rain |
| Durability | Functional after 1.5 m drop; moisture exposure without significant degradation |

---

## Verification

Per [Annex B](../annexes/B-kpp-targets.md) test framework:

1. Aerosol chamber fill screening (α across VIS/NIR/MWIR)
2. Static field test — single grenade duration and screening area
3. **Combined employment test** — 2–3 MS-V + AN-M8 vs. FPV/fiber-optic surrogate (MoE gate)
4. Environmental matrix (wind, temperature, humidity)
5. Respiratory exposure / safety characterization (KPP-12 gate)
