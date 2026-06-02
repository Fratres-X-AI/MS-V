# Annex F — Form Factor, Ergonomics & Digital Representation (Tier B/C)

> **MATURITY:** Parametric engineering estimate + concept visualization — **NOT VALIDATION**  
> **Machine-readable:** [`models/system/form_factor.yaml`](../models/system/form_factor.yaml) · [`data/baseline_grenades.json`](../data/baseline_grenades.json)

---

## 1. Envelope Summary (v2 KPP — primary)

| Parameter | MS-V v2 (KPP) | AN-M8 HC (baseline) | Δ |
|-----------|---------------|---------------------|---|
| Total mass | **850 g** | 680 g | +25% |
| Length × diameter | **7.1 × 3.1 in** (180 × 79 mm) | 5.7 × 2.5 in | ~25% larger |
| Spectrum | VIS + NIR + MWIR | VIS only | Multispectral |
| Fuze | M201A1-compatible | M201A1 | Common |

Alternate **v3 existing-container** track (680 g, AN-M8 shell) documented in `form_factor.yaml` for production-reuse study only.

---

## 2. Canonical Concept Visuals (approved repo set)

| Figure | Path |
|--------|------|
| Scale vs inventory | `analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png` |
| v2 product hero | `analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png` |
| Cutaway interior | `analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png` |

Index: [`analysis/figures/form_factor/CANONICAL_RENDERS.md`](../analysis/figures/form_factor/CANONICAL_RENDERS.md)

**Caption required:** *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

---

## 3. KPP-08 Throw Range

| Source | Range |
|--------|-------|
| Requirement (KPP-08) | **≥ 20 m** (objective 25 m) |
| Phase 2 deployment model (p50, 850 g) | **~21.5 m** |
| Tier B report (regenerated) | [`analysis/FORM_FACTOR_REPORT.md`](../analysis/FORM_FACTOR_REPORT.md) |
| System API | [`models/system/kinematics.py`](../models/system/kinematics.py) |

Range test required for TRL 3+ closure (A-012).

---

## 4. Carry Load & Pouch Fit (v2)

| Configuration | Mass |
|---------------|------|
| 2× MS-V per soldier | **1.70 kg** |
| Typical event (2 MS-V + 1 AN-M8) | **2.38 kg** |

Pouch fit at 7.1 × 3.1 in — **review required** (snug vs standard grenade pouch).

---

## 5. Engineering Assets

| Asset | Path |
|-------|------|
| Exploded assembly | `analysis/figures/form_factor/engineering/ms_v_exploded_assembly.png` |
| Dimensioned cutaway | `analysis/figures/form_factor/engineering/ms_v_cutaway_dimensioned.png` |
| Stencil layout (draft) | `analysis/figures/form_factor/engineering/ms_v_stencil_layout_guide.png` |
| OpenSCAD / STL | `models/system/openscad/` · `models/system/assets/` |

Regenerate: `python analysis/generate_engineering_drawings.py`

---

## 6. Open Items

- AMCCOM stencil / NSN / hazard marking review
- Throw trial at 850 g (KPP-08)
- Pouch NSN verification at v2 envelope

**Assumptions:** A-012 (throw), form-factor geometry in `rtm/assumption_register.md`

---

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION · Report: [FORM_FACTOR_REPORT.md](../analysis/FORM_FACTOR_REPORT.md)*
