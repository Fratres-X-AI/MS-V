# 05 — Key Design Trades

Developing MS-V requires balancing competing factors. The following are the primary trade-offs driving design decisions (v2).

---

## Trade 1: Cloud Density vs. Burn Duration

**Goal:** Thick, effective obscuration for 2+ minutes.

**Reality:** Longer burn times often come at the cost of initial density. Fast-burning fills create thick clouds quickly but do not last. Slower-burning fills last longer but may not reach peak density as fast.

**Decision:** Prioritize **density + duration together**. The ~850 g target size supports larger fill mass and a burn rate optimized for **sustained thickness** rather than maximum initial speed. Accept 12–15 s build-up to achieve both.

---

## Trade 2: Build-up Speed vs. Multispectral Performance

**Challenge:** Achieving ≤ 12–15 s effective build-up while maintaining strong NIR + MWIR blocking is difficult. High-performing multispectral fills (red phosphorus, metal powders, metal-organic compounds) have different ignition and aerosolization characteristics than pure visual smokes.

**Decision:** Accept **12–15 s build-up** (moderate priority) to get reliable multispectral performance and 120+ s duration. Do not sacrifice IR attenuation or burn length for sub-8 s opacity.

---

## Trade 3: Multispectral Effectiveness vs. Toxicity / Respiratory Impact

**Reality:** Stronger IR/thermal obscuration generally requires more aggressive chemistry. These materials increase respiratory irritation compared to basic TA visual smoke (M83).

**Decision:** MS-V will likely be **more irritating than M83**. This is **accepted as long as it remains non-lethal**. Full safety characterization and clear employment guidelines are required. Minimize irritation where possible without sacrificing core multispectral performance.

---

## Trade 4: Size / Weight vs. Performance

**Trade:** ~850 g (~25% bigger than standard smoke) provides room for fill material supporting density + duration. Larger/heavier grenades are less comfortable in quantity and slightly harder to throw accurately under stress.

**Decision:** **850 g is an acceptable compromise** to achieve 2+ minute dense multispectral burn. Issue 1–2 per soldier; not a replacement for entire smoke basic load.

---

## Trade 5: Cost vs. Performance

**Reality:** High-performance multispectral fills drive cost above basic smoke grenades ($15–25). Target $75–150 is ambitious.

**Decision:** Aim for $75–150 with Option A (unified bispectral) fill at moderate production volumes. Option C (IR additive) fallback if cost exceeds target. Optimize fill for **cost-effective performance** rather than maximum theoretical multispectral defeat.

---

## Trade 6: Simplicity / Reliability vs. Capability

**Principle:** Adding complexity (special fuzes, exotic fills, complex manufacturing) increases failure risk and training burden.

**Decision:** Keep it **soldier-proof**. M201A1 fuze, burning-type architecture, proven or near-proven bispectral technology. Prefer ECBC-validated approaches over bleeding-edge chemistry. No new launchers or arming procedures.

---

## Priority Direction Summary

| Priority | Direction | Rationale |
|----------|-----------|-----------|
| Density + Duration | **High** | User requirement: 2+ min thick cloud |
| Build-up Speed | **Moderate** | 12–15 s acceptable |
| Multispectral Performance | **High** | Core capability vs drones |
| Toxicity / Irritation | **Acceptable** | Non-lethal threshold; document + minimize |
| Size / Weight | **~850 g** | Necessary for performance |
| Cost | **$75–150 target** | Ambitious but worth aiming for |
| Simplicity | **High** | Soldier-first philosophy |

---

## Recommended Design Point (v2)

| Parameter | Selection |
|-----------|-----------|
| Weight | ~850 g |
| Filler | 22–24 oz unified bispectral (Option A) |
| Build-up | ≤ 12–15 s |
| Duration | 120+ s at good thickness |
| Spectrum | VIS + NIR + MWIR |
| Employment | 2–3 MS-V + visual smoke per event |
| Irritation | Acceptable non-lethal |
| Fuze | M201A1-compatible |

See [Annex C — Trades Matrix](../annexes/C-trades-matrix.md) for scored option analysis.

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

