# MS-V Visuals

Concept art and reference imagery. Figures are **notional** until hardware exists.

> **Required caption (external use — exact text):**  
> *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

**Verification:** [`../analysis/LINKEDIN_VISUAL_VERIFICATION.md`](../analysis/LINKEDIN_VISUAL_VERIFICATION.md) · **Status:** PASS (2026-06-02) · **Pins:** [`tests/test_canonical_renders.py`](../tests/test_canonical_renders.py)

---

## Grenade — v2 KPP (authoritative trio)

User-approved **authoritative** set for briefings, LinkedIn, and prime diligence. SHA256-pinned in [`tests/test_canonical_renders.py`](../tests/test_canonical_renders.py).

| # | Asset | Role |
|---|-------|------|
| 1 | [`../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png`](../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png) | **Product hero** — v2 photoreal, M201 fuze, multispectral markings |
| 2 | [`../analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png`](../analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png) | **Scale comparison** — true-scale v2 vs M83 / AN-M8 + weights |
| 3 | [`../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png`](../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png) | **Cutaway** — interior fuze, starter, bispectral filler |

**Spec:** [`grenade/V2-KPP-SPEC.md`](grenade/V2-KPP-SPEC.md)  
**Gallery:** [`../analysis/figures/form_factor/renders/v2_kpp/index.html`](../analysis/figures/form_factor/renders/v2_kpp/index.html)  
**Index:** [`../analysis/figures/form_factor/CANONICAL_RENDERS.md`](../analysis/figures/form_factor/CANONICAL_RENDERS.md)

### GitHub raw URLs (download for slides / LinkedIn)

1. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png  
2. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png  
3. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png  

**LinkedIn carousel order:** hero → scale → cutaway

---

## Engineering support set

| Asset | Role |
|-------|------|
| [`../analysis/figures/form_factor/engineering/ms_v_exploded_assembly.png`](../analysis/figures/form_factor/engineering/ms_v_exploded_assembly.png) | Exploded assembly |
| [`../analysis/figures/form_factor/engineering/ms_v_cutaway_dimensioned.png`](../analysis/figures/form_factor/engineering/ms_v_cutaway_dimensioned.png) | Dimensioned cutaway |
| [`../analysis/figures/form_factor/engineering/ms_v_stencil_layout_guide.png`](../analysis/figures/form_factor/engineering/ms_v_stencil_layout_guide.png) | Marking field (draft — not AMCCOM-approved) |

---

## Deprecated / alternate tracks

| Path | Status |
|------|--------|
| `../analysis/figures/form_factor/renders/deprecated_v3_concepts/` | v3 existing-container track — **not** primary external set |
| `../analysis/figures/form_factor/renders/ms_v_product_*.png` | Early RADR-style matplotlib — superseded by authoritative trio |

Policy: [`../analysis/VISUAL_CONCEPT_ASSESSMENT.md`](../analysis/VISUAL_CONCEPT_ASSESSMENT.md)

---

## M&S figures (generated)

| Asset | Generator |
|-------|-----------|
| `../analysis/figures/mega_suite_duration_p10.png` | `python analysis/generate_figures.py` |
| `../analysis/figures/duration_sensitivity.png` | `python analysis/generate_figures.py` |

Provenance: [`../analysis/figures/FIGURE_PROVENANCE.md`](../analysis/figures/FIGURE_PROVENANCE.md)
