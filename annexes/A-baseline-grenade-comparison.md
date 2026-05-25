# Annex A — Baseline US Smoke Grenade Comparison

This annex provides tabulated data for current US military hand-thrown smoke grenades sourced from [TM 43-0001-29](https://www.militarynewbie.com/wp-content/uploads/2013/11/TM-43-0001-29-Army-Ammunition-Data-Sheets-for-Grenades.pdf), with MS-V proposed targets (v2) for side-by-side comparison.

Machine-readable data is available in [`data/baseline_grenades.json`](../data/baseline_grenades.json).

---

## Summary Comparison

| Parameter | AN-M8 HC | M18 | M83 TA | M15 WP | **MS-V (proposed v2)** |
|-----------|----------|-----|--------|--------|------------------------|
| Type | Burning | Burning | Burning | Bursting | Burning |
| Total weight | 24 oz (680 g) | 19 oz (539 g) | 16 oz (454 g) | 31 oz (879 g) | **~850 g (~30 oz)** |
| Filler weight | 19 oz HC | 11.5 oz colored | 11 oz TA | 15 oz WP | **22–24 oz bispectral** |
| Length × diameter | 5.7 × 2.5 in | 5.75 × 2.5 in | 5.7 × 2.5 in | 4.5 × 2-3/8 in | **~7.1 × 3.1 in (~25% larger)** |
| Fuze | M201A1 | M201A1 | M201A1 | M206A1/A2 | **M201A1-compatible** |
| Fuze delay | 0.7–2 s | 0.7–2 s | 0.7–2 s | 4–5 s | **0.7–2 s** |
| Smoke duration | 105–150 s | 50–90 s | 25–70 s* | ~60 s | **120+ s** |
| Build-up to effective density | ~10–20 s | ~10–15 s | ~10–15 s | Burst (instant) | **≤ 12–15 s** |
| Spectral coverage | VIS only | VIS only | VIS only | VIS only | **VIS + NIR + MWIR** |
| Screening area | ~20–30 sq ft | ~15–25 sq ft | ~15–25 sq ft | Limited | **30–40 sq ft (2–3 grenade groups)** |
| Primary role | Screening, signaling | Signaling | Practice screening | Incendiary, limited screen | **UAS multispectral screen** |
| IR defeat | No | No | No | No | **Yes (design goal)** |
| Toxicity | High (HCl) | Moderate | Low | High (WP) | **Acceptable irritation (non-lethal)** |
| Fire hazard | Yes | Yes | Yes | Yes | **Reduced vs HC/WP** |

\* JPEO lists M83 duration as 55–90 seconds; TM 43-0001-29 lists 25–70 seconds average burn-time.

---

## AN-M8 HC Smoke Grenade

**Designation:** Grenade, Hand: Smoke, HC, AN-M8  
**NSN:** 1330-00-219-8511

### Tabulated Data (TM 43-0001-29)

| Item | Value |
|------|-------|
| Weight (with fuze) | 24 oz (680 g) |
| Length × diameter | 5.7 × 2.5 in |
| Filler | 19 oz HC (Type C) |
| Duration | 105–150 seconds |
| Fuze | M201A1, 0.7–2 s delay |

### MS-V Gap

No infrared attenuation; thermal imagers see through HC smoke. MS-V targets comparable or longer duration with added multispectral performance.

---

## M83 TA Practice Smoke Grenade

**Designation:** Grenade, Hand: Smoke, TA, Practice, M83  
**NSN:** 1330-01-380-0284

### Tabulated Data (TM 43-0001-29)

| Item | Value |
|------|-------|
| Weight (with fuze) | 16 oz (454 g) |
| Length × diameter | 5.7 × 2.5 in |
| Filler | 11 oz terephthalic acid |
| Duration | 25–70 s (TM); 55–90 s (JPEO) |

### MS-V Reference

M83 is the lightest standard smoke grenade — MS-V at ~850 g is roughly 25% larger in linear dimensions to accommodate additional fill mass for 2+ minute dense multispectral burn.

---

## Common Architecture (Burning-Type Smoke Grenades)

All burning-type inventory smoke grenades (AN-M8, M18, M83) share M201A1 fuze, sheet-metal cylinder body, 4 top + 1 bottom emission ports, and 1.3G hazard classification. MS-V adopts this proven architecture at a larger form factor.

---

## MS-V Differentiation Summary

| Capability | Best Baseline | MS-V Improvement |
|------------|---------------|------------------|
| Visual screening density | AN-M8 (105–150 s) | Comparable duration (120+ s) with added IR |
| IR/thermal defeat | None in inventory | Primary design driver |
| Cloud build-up | HC ~10–20 s | Target ≤ 12–15 s (density + duration priority) |
| Fill mass | AN-M8 (19 oz) | 22–24 oz bispectral in ~850 g body |
| Combined employment | AN-M8 visual only | MS-V + signal smoke for FPV/fiber-optic drones |
| Safety / toxicity | M83 TA (lowest) | Acceptable non-lethal irritation; document + minimize |

See [Annex B — KPP Targets](B-kpp-targets.md) for proposed MS-V performance thresholds.
