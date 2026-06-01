# KPP Gap Analysis — Local M&S (100k samples)

> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION  
> Generated after Phase 1 local suite. See [`RESULTS_SUMMARY.md`](RESULTS_SUMMARY.md).

## Summary

| KPP | Target | Sim Result (3 grenade) | Status |
|-----|--------|------------------------|--------|
| Build-up p90 | ≤ 15 s | ~16.4 s | **MARGINAL FAIL** — tune port/burn coupling or accept 16 s |
| Duration p10 | ≥ 120 s | ~74.6 s | **FAIL** — at HC-calibrated burn rates, 650 g fill yields ~75–110 s effective |
| Duration p50 | ≥ 120 s (goal) | ~96.5 s | **BELOW TARGET** |
| Screening area p10 | ≥ 30 sq ft | ~68 sq ft (3 grenade) | **PASS** |
| MoE lock ≥ 60 s | Primary MoE | **99.8%** | **PASS** |

## Interpretation

### Duration vs 120+ s design goal

At burn rates consistent with **AN-M8 HC** (~3.8–6.2 g/s for ~650 g fill), raw burn is ~105–170 s. After wind and thickness fractions, **effective duration p50 ~96 s** — close but below the 120 s KPP.

**Options (design trades, not sim fixes):**
1. Increase filler mass further (weight > 850 g)
2. Slow burn rate formulation (density-optimized fill)
3. Revise KPP-03 to **≥ 90 s p50 / ≥ 60 s p10** aligned with MoE (lock break ≥ 60 s)
4. Define "120+ s" as **combined employment** rescreen window (2 volleys) not single grenade

### MoE passes while duration KPP fails

Operational MoE is **lock break ≥ 60 s** with fused EO/IR degradation — sim shows **~99.8%** success at 3-grenade + visual smoke pairing. This supports CONOPS even if absolute 120 s single-grenade duration is optimistic.

### Wind sensitivity

| Wind | Duration p50 (3 grenade) | MoE lock ≥ 60 s |
|------|--------------------------|-----------------|
| 0–5 mph | ~110 s | 100% |
| 5–10 mph | ~97 s | 100% |
| 10–15 mph | ~83 s | 99.6% |

Wind is a **first-order driver** — doc 07 limits validated.

## RunPod Next Steps

1. 2M+ samples for stable CIs on marginal KPPs
2. Sweep burn rate vs yield factor jointly
3. Sensitivity on α extinction bands (ECBC literature bounds)
4. Document uncertainty intervals in proposal narrative

## Honest External Statement

> "Physics-informed sensitivity modeling suggests the v2 concept meets the primary operational MoE (60+ second fused EO/IR lock break in 2–3 grenade employment) under literature-bound parameters, while the 120-second single-grenade duration target is marginal and may require fill or KPP refinement. **Not validated experimentally.**"
