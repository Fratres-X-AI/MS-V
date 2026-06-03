# Canonical Visual Verification — v2 KPP Trio

**Date:** 2026-06-02  
**Status:** **PASS** for external briefings (with required caption)

---

## Design authority

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
| 1 | `renders/v2_kpp/ms_v_v2_hero.png` | Yes | Product hero | PASS |
| 2 | `engineering/scale_comparison_v2_inventory.png` | Yes | True-scale vs M83/AN-M8 | PASS |
| 3 | `renders/v2_kpp/ms_v_v2_cutaway_photoreal.png` | Yes | Interior concept | PASS |

**Do not use externally:** `renders/deprecated_v3_concepts/*`, early `ms_v_product_*.png`.

---

## Required caption (all three images)

```
Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.
```

---

## Recommended display order

1. Hero → 2. Scale comparison → 3. Cutaway

---

## Re-verification

```bash
pytest tests/test_canonical_renders.py tests/test_visual_standards.py -q
```

[Index: CANONICAL_RENDERS.md](figures/form_factor/CANONICAL_RENDERS.md) · [Spec: V2-KPP-SPEC.md](../visuals/grenade/V2-KPP-SPEC.md)
