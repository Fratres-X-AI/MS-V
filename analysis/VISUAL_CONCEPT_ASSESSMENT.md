# Visual Concept Assessment — MS-V Grenade Render

> **Maturity:** Conceptual product visualization / briefing-style mockup when applied to AI-generated or photographic-style renders. **Not** a technical illustration, engineering drawing, or manufacturing reference unless explicitly labeled and cross-checked against dimensioned figures in `analysis/figures/form_factor/engineering/`.

---

## Assessment Summary (Reviewer Findings)

### Strengths
- Clean cylindrical form with M201A1-style fuze and pull ring — reads as inventory smoke grenade class
- Professional presentation lighting suitable for early briefings **when captioned correctly**

### Gaps Identified
| Gap | Status |
|-----|--------|
| Form factor mismatch vs v2 KPP (~850 g, 7.1 × 3.1 in) | **Fixed** — v2 photoreal set in `renders/v2_kpp/` aligned to engineering scale figure |
| Markings not per U.S. ammunition stenciling conventions | **Partial** — draft stencil on v2 concepts + layout guide; AMCCOM review still required |
| No multispectral / size delta indication | **Fixed** — purple band + VIS/NIR/MWIR stencil + scale-vs-AN-M8 render |
| No scale, dimension, material, or interface callouts | **Fixed** — engineering drawing set under `engineering/` |
| Concept renders could imply false maturity | **Fixed** — usage policy + mandatory caption |

---

## Two Envelope Tracks (Do Not Conflate)

| Track | Mass | L × D | Use |
|-------|------|-------|-----|
| **v2_kpp** (primary) | 850 g | 7.1 × 3.1 in | Annex B, MasterPlan, KPP-01/09, simulation baselines |
| **v3_existing_container** | 680 g | 5.7 × 2.5 in | Production/sourcing reuse study — AN-M8/M18 shell + M201A1 fuze, filler-only delta |

Inventory-style concept renders in `deprecated_v3_concepts/` illustrate **v3** only. **v2 KPP** external materials use `v2_kpp/` + engineering figures.

---

## Recommended Use Policy

### Acceptable
- Internal discussion, early slides, Product Hunt-style teasers
- **Required caption:** *Concept visualization only — not to scale with v2 KPP envelope unless labeled v3 production-reuse variant*

### Not acceptable alone
- Proposal technical volumes, manufacturing RFQs, pouch qualification, throw-range claims
- Replace with: `engineering/scale_comparison_v2_inventory.png`, `ms_v_exploded_assembly.png`, `ms_v_cutaway_dimensioned.png`

---

## Engineering Figure Set

Regenerate: `python analysis/generate_engineering_drawings.py`

| Figure | Purpose |
|--------|---------|
| `scale_comparison_v2_inventory.png` | True-scale v2 vs AN-M8 vs M83 + weights |
| `envelope_tracks_v2_vs_v3.png` | Both design tracks side-by-side |
| `ms_v_exploded_assembly.png` | Fuze, adapter, ports, chamber, fill |
| `ms_v_cutaway_dimensioned.png` | Half-section with dimension callouts |
| `ms_v_stencil_layout_guide.png` | Marking field placement (draft — not AMCCOM-approved) |

---

## Open Items
- AMCCOM stencil font, color, hazard class (1.3G), NSN block, lot format — requires ordnance packaging review
- IR/low-observable finish — not represented in current figures
- Throw trial at 850 g — KPP-08, A-012

**Assumptions:** form-factor geometry; A-012 throw
