# MS-V Veil — One-Page Concept Summary

**Multispectral Obscurant Grenade · v2 KPP · TRL 2**  
**Version 2.0.0** · M&S-supported — not procurement authority

---

## Problem

Squad and SOF face **FPV, fiber-optic, and thermal UAS** that see through standard **VIS-only** smoke (AN-M8/M83). EW does not defeat fiber. Kinetic is last resort. There is no **squad-portable multispectral screen** in inventory.

## Solution

**MS-V Veil** — hand-thrown, pin-pull, **~850 g** obscurant grenade generating **VIS + NIR + MWIR** cloud. Employed as **2–3 MS-V + visual smoke** to break fused EO/IR lock and enable movement under the layered defense stack.

## How it works (employment)

1. Threat cue → grenadier throws **2–3 MS-V + 1–2 AN-M8/M83**
2. Build-up **~12–15 s** · dense screen **120+ s** (design target)
3. Squad moves, CASEVAC, or breaks contact under combined obscuration
4. EW / kinetic layers engage if threat persists

**Always pair with visual smoke** — required for FPV and fiber-optic MoE.

## Locked specs (summary)

| Item | Value |
|------|--------|
| Form factor (v2 KPP) | **850 g**, **7.1 × 3.1 in** |
| Spectrum | **VIS + NIR + MWIR** |
| Duration (KPP) | **≥ 120 s** dense (p10 MC) |
| Employment | **2–3 grenades** + visual smoke |
| Throw (KPP-08) | **≥ 20 m** (objective 25 m) |
| Fuze | **M201A1-compatible** |
| Cost target | **$75–150** at scale (not modeled) |

## M&S evidence (140M samples — literature bounds)

| Metric | Result | Caveat |
|--------|--------|--------|
| Mega suite | **38/38 pass** | phase2 + v6 probabilistic lock |
| Duration p10 (3× g3) | **~170 s** | +42% vs 120 s KPP |
| MoE lock-break ≥60 s | **80%** nominal · **55%** adversarial | Not field validation |
| Top Sobol driver | **burn_rate** ST≈0.83 | Guides TRL 3 burn cup |

## Repo & partnership

https://github.com/Fratres-X-AI/MS-V

**Open concept:** MIT · **Prime / Program:** [LICENSE-COMMERCIAL](../LICENSE-COMMERCIAL.md) · [Partnership guide](licensing-and-partnership.md)

**Deep dives:** [Annex F](../annexes/F-form-factor-and-ergonomics.md) · [CONOPS](../docs/04-conops-use-cases.md) · [Verification matrix](../rtm/verification_matrix.md) · [Pitch deck outline](pitch-deck-outline.md)

**Traceability:** TRL 2 sensitivity study complete — **not** procurement-ready · **not** field validation.
