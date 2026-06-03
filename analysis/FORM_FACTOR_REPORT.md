# MS-V Form Factor Report (Tier B)

> **MATURITY:** Parametric digital representation — **NOT VALIDATION**
> No ergonomic range test · No issued-pouch verification
> **Variant:** `v2_kpp` — primary external envelope

## Envelope (volume budget)

| Parameter | Value |
|-----------|-------|
| Outer L × D | 180 × 79 mm (7.1" × 3.1") |
| Inner chamber | 660 cm³ |
| Fill volume (mid) | 676 cm³ @ 0.97 g/cm³ |
| Mass | 850 g |

## KPP-08 Throw

| Metric | Value |
|--------|-------|
| KPP band | 20–25 m |
| Design authority p50 | 21.5 m |
| MC stressed p10 / p50 / p90 | 20.0 / 21.5 / 23.5 m |
| Lateral dispersion p50 / p90 | 2.35 / 3.35 m |

Source: [`models/system/kinematics.py`](../models/system/kinematics.py) · [`human_factors.yaml`](../models/system/human_factors.yaml).
RTM: matrix KPP-08 · job `baseline_10M_g3_n10000000` (MC pass — **not** range validation).

## Human factors (notional inputs)

| Input | Value |
|-------|-------|
| Loadout 2× MS-V (est.) | 1.70 kg |
| Throw band (YAML) | 20.0–25.0 m |
| Load range penalty | −1.0 m |
| Stress lateral multiplier | ×1.25 |
| Posture mix (standing / kneel / prone) | 55% / 35% / 10% |

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
