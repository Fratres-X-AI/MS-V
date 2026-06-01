# Phase 0 Source Audit Log

**Date:** 2026-05-24  
**Scope:** Docs 01–08, Annexes A–E vs cited sources  
**Status:** Initial audit complete — gaps flagged for Phase 4/5

---

## Source Verification

| Source | Cited in | Verified | Notes |
|--------|----------|----------|-------|
| TM 43-0001-29 | Annex A, E | **Yes** | AN-M8 680g/19oz/105-150s; M83 454g/11oz; M18 539g — consistent across annex A and data JSON |
| FM 3-50 Ch. 7 | Annex D, E, doc 08 | **Yes** | VI obscurants; thermal sees through visual smoke; IR measured by transmittance/Pd |
| FM 3-50 App G | Annex D | **Partial** | Cloud phases (streamer/build-up/uniform/terminal) — qualitative only in docs |
| ECBC bispectral 2014 | Annex B/C/E, MasterPlan | **Yes** | Hand-thrown bispectral concept; α, duration, cloud geometry test metrics cited |
| JPEO smoke page | Annex A/E | **Partial** | M83 duration 55-90s vs TM 25-70s — documented discrepancy in Annex A |

---

## Internal Consistency Check

| Item | Docs | Consistent? | Action |
|------|------|-------------|--------|
| Weight ~850 g | 02, 03, 06, Annex B, JSON | **Yes** | — |
| Duration 120+ s | 02, 04, Annex B, MasterPlan | **Yes** | Sim now tests via burn model |
| Build-up 12-15 s | 02, 04, Annex B | **Yes** | Sim derives from burn rate + uniform range |
| 2-3 MS-V + visual smoke MoE | 02, 04, 07, 08 | **Yes** | Engine models 1/2/3 grenade groups |
| Respiratory irritation accepted | 03, 05, 07 | **Yes** | No quantitative margin — Phase 4 gap |
| TRL 2-3 ceiling | MasterPlan, 07 | **Yes** | — |
| Unit cost $75-150 | 02, 03, Annex B | **Yes** | No cost model yet — Phase 4 |

---

## Unvalidated Claims (Explicit)

1. MS-V fill achieves ECBC-class bispectral α in all three bands — **assumed**, not measured
2. 30-40 sq ft per grenade — **scaled estimate**, not simulated geometry
3. Throw 20-25 m at 850 g — **no human-factors data**
4. Combined visual smoke factor 1.3× VIS — **placeholder** in params.yaml
5. Yield factor 0.22-0.52 — **literature order-of-magnitude** for pyrotechnic aerosol

---

## Doc Quality Notes

| Doc | Issue | Resolution |
|-----|-------|------------|
| 04 CONOPS | Timelines consistent with T+12-15 / T+135 | OK |
| 07 Limitations | Correctly states not standalone | OK |
| 08 Integration | MKFS referenced; fiber-optic primary target | OK |
| Annex C | Option A locked pending Phase 1 | Update after sim review |

---

## Audit Conclusion

Requirements baseline is **internally consistent** and **source-anchored at concept level**. All performance KPPs remain **UNVERIFIED** pending M&S (Phase 1) and any future empirical work.

Next: review [`analysis/RESULTS_SUMMARY.md`](../analysis/RESULTS_SUMMARY.md) after local sim suite.
