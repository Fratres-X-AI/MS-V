# Annex C — Design Trades Matrix (v2)

Decision matrix for MS-V design options. Scoring: 1 (poor) to 5 (excellent). **Recommended baseline** marked with ★. Priority direction reflects v2 source of truth: **density + duration first**.

---

## Priority Direction Summary

| Priority | Direction | Rationale |
|----------|-----------|-----------|
| Density + Duration | **High** | User requirement: 2+ min thick cloud |
| Build-up Speed | **Moderate** | 12–15 s acceptable; realistic compromise |
| Multispectral Performance | **High** | Core capability vs drones |
| Toxicity / Irritation | **Acceptable** | Non-lethal threshold; document + minimize |
| Size / Weight | **~850 g** | Necessary for performance |
| Cost | **$75–150 target** | Ambitious but worth aiming for |
| Simplicity | **High** | Soldier-first philosophy |

---

## Fill Material Options

### Option A: Unified Bispectral Composition ★ RECOMMENDED BASELINE

| Criterion | Score | Notes |
|-----------|-------|-------|
| Spectral coverage (VIS–MWIR) | 5 | ECBC-validated approach |
| Duration at density (120+ s) | 4 | Tunable via fill mass in 850 g body |
| Build-up (12–15 s) | 4 | Achievable with optimized burn rate |
| Manufacturing complexity | 3 | Single fill; moderate formulation |
| Unit cost | 3 | $100–150 estimated |
| Simplicity | 4 | Single composition; proven path |
| **Total** | **23/30** | |

### Option B: Dual-Composition Fill

| Criterion | Score | Notes |
|-----------|-------|-------|
| Spectral coverage | 5 | Optimized per band |
| Duration at density | 4 | Possible with larger body |
| Build-up | 3 | Two ignition sequences may desync |
| Manufacturing complexity | 2 | Partitioned body or dual fill |
| Unit cost | 2 | $120–180 estimated |
| Simplicity | 2 | Increased failure modes |
| **Total** | **18/30** | |

### Option C: IR Additive in Pyrotechnic Base

| Criterion | Score | Notes |
|-----------|-------|-------|
| Spectral coverage (VIS–MWIR) | 3 | Additive may limit MWIR performance |
| Duration at density | 5 | TA-class base burns long |
| Build-up | 4 | Standard pyrotechnic |
| Manufacturing complexity | 4 | Simple additive mixing |
| Unit cost | 5 | $75–120 estimated |
| Simplicity | 5 | Lowest complexity |
| **Total** | **26/30** | |

**Decision:** Option A baseline for multispectral performance; Option C fallback if cost or MWIR KPP not met at acceptable irritation levels.

---

## Performance Trade Matrix

### Density + Duration vs. Build-Up Speed

| Design Point | Build-Up | Duration | Density | Score | Notes |
|-------------|----------|----------|---------|-------|-------|
| Ultra-fast | ≤ 8 s | 60–90 s | High initial | 2 | v1 approach; rejected — insufficient duration |
| **v2 baseline ★** | **12–15 s** | **120+ s** | **High sustained** | **5** | **850 g enables both** |
| Extended slow | ≤ 20 s | 150+ s | Moderate | 3 | AN-M8-like; loses build-up advantage |

### Size/Weight vs. Performance

| Design Point | Weight | Filler | Duration | Carry (2×) | Score |
|-------------|--------|--------|----------|------------|-------|
| M83-class | 454 g | 11 oz | 60–90 s | 908 g | 2 |
| AN-M8-class | 680 g | 19 oz | 105–150 s VIS only | 1.36 kg | 3 |
| **MS-V v2 ★** | **850 g** | **22–24 oz** | **120+ s multispectral** | **1.7 kg** | **4** |
| Oversized | 1000 g | 28 oz | 150+ s | 2.0 kg | 2 |

850 g is the accepted compromise: heavier than standard smoke but within soldier load limits for 1–2 grenades.

---

## Combined Decision Matrix

| Trade Space | Selection | Value | Trade Accepted |
|-------------|-----------|-------|----------------|
| Fill material | Option A (unified bispectral) | VIS–MWIR + 120+ s | Cost; moderate irritation |
| Fill fallback | Option C (IR additive) | Cost reduction | May sacrifice MWIR depth |
| Build-up vs. duration | v2 baseline | 12–15 s / 120+ s | Not sub-8 s instant opacity |
| Weight vs. filler | 850 g / 22–24 oz | 2+ min dense burn | Heavier throw; pouch load |
| Multispectral vs. toxicity | Accept irritation | Document + PPE | Worse than M83 TA |
| Employment | 2–3 MS-V + visual smoke | FPV/fiber-optic MoE | Not standalone |
| Simplicity | M201A1 + burning type | No new launchers | Larger body only change |

---

## Recommended Baseline Design Point ★ (v2)

| Parameter | Value |
|-----------|-------|
| Fill | Option A — unified bispectral composition |
| Weight | ~850 g |
| Filler | 22–24 oz |
| Build-up | ≤ 12–15 s to effective density |
| Duration | 120+ s at good thickness |
| Spectrum | VIS + NIR + MWIR |
| Form factor | ~7.1 × 3.1 in (~25% larger than AN-M8/M83) |
| Fuze | M201A1-compatible |
| Employment | 2–3 MS-V + standard visual smoke per event |
| Irritation | Acceptable non-lethal; safety data required |
| Cost target | $75–150 |

---

## Sensitivity Analysis

| If... | Mitigation |
|-------|------------|
| Build-up exceeds 15 s | Optimize port design; accept up to 18 s if duration KPP met |
| Duration below 120 s | Increase fill mass within 850 g envelope; optimize burn rate |
| MWIR KPP not met (Option A) | Hybrid A+C; or Option B for Block II |
| Irritation exceeds acceptable threshold | Reformulate; add employment standoff guidance |
| Cost exceeds $150 | Switch to Option C; increase production volume |
| 850 g too heavy for issue doctrine | Reduce to 1 per soldier; increase platoon pool |

See [05 — Key Design Trades](../docs/05-key-design-trades.md) for narrative analysis.
