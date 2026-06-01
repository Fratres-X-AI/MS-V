# MS-V Form Factor Report (Tier B)

> **MATURITY:** Parametric digital representation — **NOT VALIDATION**
> No ergonomic range test · No issued-pouch verification

## Envelope (volume budget)

| Parameter | Value |
|-----------|-------|
| Outer L × D | 180 × 79 mm (7.1" × 3.1") |
| Inner chamber | 660 cm³ |
| Fill volume (mid) | 676 cm³ @ 0.97 g/cm³ |
| Mass | 850 g |

## KPP-08 Throw

| Spec | Sim p50 |
|------|---------|
| 20–25 m | 21.5 m (phase2 deployment model) |

## Pouch fit (typical MOLLE grenade pouch)

| Check | Pass | Clearance |
|-------|------|-----------|
| Width | ✓ | 11 mm |
| Depth | ✓ | 16 mm |
| Height | ✓ | 5 mm |
| Mass | ✓ | ≤ 900 g |

**Overall:** PASS (estimate)

## Assets

- `analysis/figures/form_factor/scale_comparison.png`
- `analysis/figures/form_factor/cutaway_schematic.png`
- `analysis/figures/form_factor/employment_diagram.png`
- `analysis/figures/form_factor/load_layout.png`
- `analysis/figures/form_factor/pouch_fit.png`
- STL `ms_v_assembly`: `models/system/assets/ms_v_assembly.stl`
- STL `ms_v_body`: `models/system/assets/ms_v_body.stl`
- STL `an_m8_reference`: `models/system/assets/an_m8_reference.stl`

OpenSCAD source: `models/system/openscad/ms-v_body.scad`

Annex: [`annexes/F-form-factor-and-ergonomics.md`](../annexes/F-form-factor-and-ergonomics.md)
