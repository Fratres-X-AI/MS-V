# Canonical MS-V v2 Visuals

> **Required caption (exact):** *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

**Verification status:** PASS — see [`LINKEDIN_VISUAL_VERIFICATION.md`](../../LINKEDIN_VISUAL_VERIFICATION.md). SHA256-pinned in `tests/test_canonical_renders.py`.

These three figures are the approved repo set for briefings and external concept materials.
**SHA256-pinned** in `tests/test_canonical_renders.py` — do not overwrite via script regen without explicit approval.

| # | Figure | Path | Role |
|---|--------|------|------|
| 1 | Scale comparison | [`engineering/scale_comparison_v2_inventory.png`](engineering/scale_comparison_v2_inventory.png) | True-scale v2 vs M83 / AN-M8 + weights |
| 2 | Product hero | [`renders/v2_kpp/ms_v_v2_hero.png`](renders/v2_kpp/ms_v_v2_hero.png) | v2 photoreal with M201 fuze + multispectral markings |
| 3 | Cutaway | [`renders/v2_kpp/ms_v_v2_cutaway_photoreal.png`](renders/v2_kpp/ms_v_v2_cutaway_photoreal.png) | Interior — fuze, starter, bispectral filler |

### GitHub raw URLs (LinkedIn / slides)

1. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png
2. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png
3. https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png

Gallery: [`renders/v2_kpp/index.html`](renders/v2_kpp/index.html)

Supporting engineering set: `engineering/` (exploded, dimensioned cutaway, stencil guide).

**Regeneration:** `analysis/generate_form_factor_assets.py` writes Tier B plots under `analysis/figures/form_factor/` — it does **not** overwrite the three SHA256-pinned files above. `analysis/generate_engineering_drawings.py` may refresh `engineering/` only; do not run it against `scale_comparison_v2_inventory.png` or `renders/v2_kpp/*` without updating `tests/test_canonical_renders.py`.

Policy: [`analysis/VISUAL_CONCEPT_ASSESSMENT.md`](../../VISUAL_CONCEPT_ASSESSMENT.md)
