# Annex F — Form Factor, Ergonomics & Digital Representation (Tier B)

> **MATURITY:** Parametric engineering estimate — **NOT VALIDATION**  
> **Machine-readable:** [`models/system/form_factor.yaml`](../models/system/form_factor.yaml) · [`data/baseline_grenades.json`](../data/baseline_grenades.json)

---

## 1. Envelope Summary

| Parameter | MS-V (proposed v2) | AN-M8 HC (baseline) | Δ |
|-----------|-------------------|---------------------|---|
| Total mass | **850 g** | 680 g | +25% |
| Length × diameter | **7.1 × 3.1 in** (180 × 79 mm) | 5.7 × 2.5 in | ~25% larger |
| Filler | 22–24 oz bispectral | 19 oz HC | — |
| Fuze | M201A1-compatible | M201A1 | Common |

Volume budget (mid-case): **~650 g fill** @ **~0.97 g/cm³** → **~670 cm³** fill volume; internal steel chamber **~660 cm³** at 2 mm wall — consistent with stated envelope.

---

## 2. KPP-08 Throw Range

| Source | Range |
|--------|-------|
| Requirement (KPP-08) | **≥ 20 m** (objective 25 m) |
| M18 reference (TM 43-0001-29) | ~35 m (lighter, 539 g) |
| Phase 2 deployment model (p50) | **~21.5 m** under stress bounds |

Heavier MS-V trades throw distance for fill mass and duration. Range test required for TRL 3+ closure (A-012).

---

## 3. Carry Load & Pouch Fit

| Configuration | Mass |
|---------------|------|
| 2× MS-V per soldier | **1.70 kg** |
| Typical event (2 MS-V + 1 AN-M8) | **2.38 kg** smoke stack |

**Pouch fit (typical MOLLE grenade pouch, vertical stow):** 79 mm diameter × 180 mm length against 90 × 95 × 185 mm inner envelope — **passes parametric check with ~5 mm clearance** (estimate only; verify against issued NSN).

---

## 4. Digital Assets (Tier B)

| Asset | Path |
|-------|------|
| Scale comparison figure | `analysis/figures/form_factor/scale_comparison.png` |
| Cutaway schematic | `analysis/figures/form_factor/cutaway_schematic.png` |
| Employment diagram | `analysis/figures/form_factor/employment_diagram.png` |
| Load layout | `analysis/figures/form_factor/load_layout.png` |
| Pouch fit | `analysis/figures/form_factor/pouch_fit.png` |
| STL assembly | `models/system/assets/ms_v_assembly.stl` |
| AN-M8 reference STL | `models/system/assets/an_m8_reference.stl` |
| OpenSCAD parametric | `models/system/openscad/ms-v_body.scad` |

Regenerate: `python analysis/generate_form_factor_assets.py`

Full report: [`analysis/FORM_FACTOR_REPORT.md`](../analysis/FORM_FACTOR_REPORT.md)

---

## 5. Cloud Employment (Plan View)

Typical 2 MS-V + 1 HC volley: overlapping screening envelopes (~30–40 sq ft per grenade, ~3.2× spread factor in sim) between threat UAS LOS and friendly squad. See employment diagram in figures folder.

---

## 6. Open Items (External)

- Ergonomic throw trial with 850 g form factor (KPP-08)
- Issued pouch NSN dimensional verification
- CAD release for manufacturing (Phase 5+)

**Assumptions:** A-012 (throw), form-factor geometry in `rtm/assumption_register.md`
