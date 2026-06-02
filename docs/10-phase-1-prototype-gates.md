# 10 — Phase 1 Prototype Gates

**Document ID:** MS-V / DOC-10  
**Version:** 1.0.0  
**Status:** Conceptual — **no physical prototype data in repo**; partner-ready plan

Traceability: [Annex F](../annexes/F-form-factor-and-ergonomics.md) · [form_factor.yaml](../models/system/form_factor.yaml) · [DOC-11](11-partner-validation-and-trl-gates.md)

---

## What Phase 1 proves

Phase 1 proves **mechanical and ergonomic feasibility** of the v2 KPP envelope — not cloud performance or MoE. A partner or machine shop can execute these gates before fill chemistry is finalized.

| Gate | ID | Proves | Does not prove |
|------|-----|--------|----------------|
| **Body prototype** | **1A** | v2 envelope (850 g, 7.1 × 3.1 in) manufacturable; M201 fuze interface | Fill burn or α(λ) |
| **Mass & balance** | **1B** | Weighed mass within KPP-01 band; CG within throw model assumptions | Field throw distance |
| **Fuze continuity** | **1C** | M201A1-compatible seating; safe transport mock-up | Live pyrotechnic function |
| **Throw ergonomics** | **1D** | n≥10 throws under load/posture per human_factors.yaml | Statistical KPP-08 closure |

---

## 1A — Body prototype

| Item | Detail |
|------|--------|
| **Entry** | Approved v2 KPP envelope from Annex F + STL |
| **Procedure** | Machine or print body shell; fit fuze adapter; verify ports and chamber volume |
| **Pass** | External dims within **±2 mm** of v2 KPP; fuze seats without interference |
| **Fail** | Cannot achieve mass target without wall thickness violation |
| **Artifacts** | Dimensional report, photos, STL revision ID |
| **JSON block** | `body_prototype` in partner validation file |

---

## 1B — Mass & balance

| Item | Detail |
|------|--------|
| **Entry** | 1A complete or equivalent CAD release |
| **Procedure** | Weigh empty body + fuze mock; compare to 850 g budget with fill placeholder |
| **Pass** | Projected loaded mass **820–880 g** with nominal fill allowance |
| **Fail** | >900 g without design change authority |
| **JSON block** | `mass_balance` |

---

## 1C — Fuze interface

| Item | Detail |
|------|--------|
| **Entry** | Inventory M201A1 or approved surrogate |
| **Procedure** | Seat fuze; verify lever/spoon clearance; document pin-pull path |
| **Pass** | No interference with v2 body; matches inventory TTP |
| **Fail** | Requires non-standard fuze modification |
| **JSON block** | `fuze_interface` |

---

## 1D — Throw ergonomics (screening)

| Item | Detail |
|------|--------|
| **Entry** | Inert training body at target mass |
| **Procedure** | n≥10 throws per posture in `human_factors.yaml`; measure distance |
| **Pass** | p50 ≥ 20 m under nominal posture; no unsafe handling observed |
| **Fail** | Systematic <18 m at design mass |
| **Note** | Full KPP-08 closure requires n≥30 under stress — see DOC-11 gate **2C** |
| **JSON block** | `throw_screening` |

---

## Artifacts in repo today

| Asset | Location |
|-------|----------|
| Parametric envelope | `models/system/form_factor.yaml` |
| STL export | `models/system/assets/ms_v_body.stl` |
| OpenSCAD source | `models/system/openscad/ms-v_body.scad` |
| Engineering drawings | `analysis/figures/form_factor/engineering/` |
| Canonical concept art | [visuals/README.md](../visuals/README.md) |

---

[← System description](06-system-description.md) · [Partner validation →](11-partner-validation-and-trl-gates.md)
