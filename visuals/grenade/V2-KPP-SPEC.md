# MS-V v2 KPP — Grenade Visual & Envelope Spec (Locked for Phase 0)

**Status:** Design authority · **NOT VALIDATION**  
**Machine-readable:** [`models/system/form_factor.yaml`](../../models/system/form_factor.yaml) · [`data/baseline_grenades.json`](../../data/baseline_grenades.json)

---

## Role

Primary external visual and envelope set for MS-V Veil partner handoff. Matches **v2 KPP** track (850 g bispectral fill envelope), not the alternate v3 existing-container reuse study.

---

## Locked envelope

| Parameter | MS-V v2 (KPP) | AN-M8 HC (baseline) |
|-----------|---------------|---------------------|
| Total mass | **850 g** | 680 g |
| Length × diameter | **7.1 × 3.1 in** (180 × 79 mm) | 5.7 × 2.5 in |
| Spectrum | VIS + NIR + MWIR | VIS only |
| Fuze | M201A1-compatible | M201A1 |
| Markings | MS-V / OBSCURANT / VEIL + multispectral band | SMOKE / HC |

---

## Authoritative art (do not regenerate without approval)

| View | File | Orientation |
|------|------|-------------|
| Hero | `analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png` | Vertical, fuze up, pull ring visible |
| Scale | `analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png` | Side-by-side with M83 + AN-M8 + weight callouts |
| Cutaway | `analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png` | Half-section: fuze, adapter, starter, bispectral filler |

Interior labels (cutaway): fuze M201A1, adapter, starter mixture, MS-V bispectral filler, steel body wall.

---

## CAD / parametric assets

| Asset | Path |
|-------|------|
| YAML envelope | `models/system/form_factor.yaml` → `variants.v2_kpp` |
| STL body | `models/system/assets/ms_v_body.stl` |
| OpenSCAD | `models/system/openscad/ms-v_body.scad` |

Regenerate Tier B diagrams: `python analysis/generate_engineering_drawings.py`  
**Warning:** `scale_comparison_v2_inventory.png` is SHA256-pinned — do not overwrite via script without explicit approval.

---

## Throw & ergonomics (linked)

| Source | KPP-08 |
|--------|--------|
| Requirement | ≥ 20 m (objective 25 m) |
| MC model p50 | ~21.5 m @ 850 g |
| Human factors | `models/system/human_factors.yaml` |

Full gate: [DOC-11 § 2C](../../docs/11-partner-validation-and-trl-gates.md)

---

## External use checklist

- [ ] Caption: *Concept visualization only — not validation*  
- [ ] Do not crop out size context on scale comparison slide  
- [ ] Do not imply AMCCOM-approved markings  
- [ ] Pair performance claims with RTM status (SENSITIVITY_PASS vs UNVERIFIED)

---

[← Visuals index](../README.md) · [Annex F](../../annexes/F-form-factor-and-ergonomics.md)
