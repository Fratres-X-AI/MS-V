# LinkedIn Visual Verification — v2 KPP Canonical Trio

**Date:** 2026-06-02  
**Verifier:** Repository automation + design authority cross-check  
**Status:** **PASS** for external posting (with required caption)

---

## Design authority (machine-readable)

Source: [`models/system/form_factor.yaml`](../models/system/form_factor.yaml) → `variants.v2_kpp`

| Parameter | Required (v2 KPP) | Visual intent |
|-----------|-------------------|---------------|
| Mass | **850 g** | Heavier than AN-M8 (680 g); callout on scale image |
| Length × diameter | **7.1 × 3.1 in** (180 × 79 mm) | ~25% larger than AN-M8 (5.7 × 2.5 in) |
| Fuze | M201A1-compatible | Pull ring + spoon on hero and cutaway |
| Spectrum | VIS + NIR + MWIR | Multispectral band / marking on hero |
| Primary variant | `v2_kpp` | **Not** v3_existing_container (680 g shell) |

---

## Asset checklist

| # | File | SHA256 pinned | Role | v2 alignment |
|---|------|---------------|------|--------------|
| 1 | `renders/v2_kpp/ms_v_v2_hero.png` | Yes (`test_canonical_renders.py`) | Product hero | PASS — v2 markings, M201 fuze, larger envelope |
| 2 | `engineering/scale_comparison_v2_inventory.png` | Yes | True-scale vs M83/AN-M8 | PASS — MS-V visibly larger; weight labels |
| 3 | `renders/v2_kpp/ms_v_v2_cutaway_photoreal.png` | Yes | Interior concept | PASS — bispectral filler, fuze stack at v2 scale |

**Do not use for LinkedIn:** `renders/deprecated_v3_concepts/*`, early `ms_v_product_*.png` (AN-M8 envelope / RADR-style camo).

---

## Required caption (all three images)

```
Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in per Annex B). Not validation.
```

---

## Carousel order (approved)

1. Hero → 2. Scale comparison → 3. Cutaway

Rationale: Hook → credibility (size vs inventory) → interior story.

---

## Known limitations (honest)

| Item | Note |
|------|------|
| Photoreal render | AI/concept art — **not** AMCCOM marking approval |
| Interior fill color | Illustrative — not measured formulation |
| Throw posture | Not depicted — see KPP-08 MC model only |
| Scale image | Qualitative true-scale; not metrology drawing |

---

## Re-verification trigger

Re-run this checklist if any canonical PNG is replaced:

```bash
pytest tests/test_canonical_renders.py -q
```

Update SHA256 pins in `tests/test_canonical_renders.py` only after explicit approval.

---

[Index: CANONICAL_RENDERS.md](figures/form_factor/CANONICAL_RENDERS.md) · [Spec: V2-KPP-SPEC.md](../visuals/grenade/V2-KPP-SPEC.md)
