# 11 — Partner Validation and TRL Gates

**Document ID:** MS-V / DOC-11  
**Version:** 1.0.0  
**Status:** Conceptual — **no partner test data in repo**; partner-ready plan

Traceability: [DOC-10](10-phase-1-prototype-gates.md) · [fill_physics_test_plan.md](../analysis/fill_physics_test_plan.md) · [trl_gate_external.md](../proposals/trl_gate_external.md) · [Licensing & partnership](licensing-and-partnership.md)

---

## What “validation” means here

MS-V does **not** claim bench or range validation until a partner records measured data. This document defines:

1. **What must be tested** (fill bench, throw range, UAS surrogate, environmental chamber)  
2. **Pass/fail metrics** aligned with KPPs and RTM  
3. **How results enter the repo** via [`data/partner_validation_results.template.json`](../data/partner_validation_results.template.json)

Repo M&S remains **literature-parameter sensitivity** until `status` moves from `pending` to `partial` or `complete`.

---

## Phase 2 validation gates (partner / lab / range)

Phase 1 ([DOC-10](10-phase-1-prototype-gates.md)) proves mechanical feasibility. Phase 2 proves **fill physics, throw, sensor degradation, and environmental performance**.

| Gate | ID | Proves | Does not prove |
|------|-----|--------|----------------|
| **Fill burn cup** | **2A** | Duration vs temperature/RH; burn rate for MC update | Full employment MoE |
| **Spectral extinction** | **2B** | α(λ) VIS/NIR/MWIR vs mass loading | Live UAS defeat |
| **Throw range** | **2C** | KPP-08 p10 ≥ 20 m under stress (n≥30) | Every soldier every load |
| **UAS surrogate** | **2D** | Fused EO/IR lock-break vs planning surrogate | Classified threat models |
| **Environmental chamber** | **2E** | KPP-10 confirmation −20/+50°C | Long-term storage |

### 2A — Fill burn cup

| Item | Detail |
|------|--------|
| **Entry** | Fill batch ID linked to Annex C down-select |
| **Procedure** | ASTM-style cup at 20/35/50°C, RH 30/70/90% per fill test plan T-01 |
| **Pass** | p10 duration ≥ **120 s** at nominal loading |
| **Fail** | Cannot meet KPP-03 at any bound without reformulation |
| **JSON block** | `fill_burn_cup` |

### 2B — Spectral extinction α(λ)

| Item | Detail |
|------|--------|
| **Entry** | Representative fill from 2A pass batch |
| **Procedure** | VIS/NIR/MWIR transmissometer vs mass loading (T-02) |
| **Pass** | Bands support MoE threshold at design cloud loading |
| **Fail** | MWIR band insufficient for fused lock-break concept |
| **JSON block** | `spectral_extinction` |

### 2C — Throw range under load

| Item | Detail |
|------|--------|
| **Entry** | Inert round at **850 g**; DOC-10 1D screening passed |
| **Procedure** | n≥30 throws under stress posture per `human_factors.yaml` |
| **Pass** | p10 ≥ **20 m**; objective 25 m documented |
| **Fail** | p10 < 18 m without envelope change |
| **JSON block** | `throw_range` |

### 2D — UAS surrogate lock-break

| Item | Detail |
|------|--------|
| **Entry** | Live or surrogate fill per range rules; fused VIS+MWIR sensor rig |
| **Procedure** | Nominal vs adversarial stacks; measure lock-break duration |
| **Pass** | MoE behavior **directionally consistent** with M&S (not exact % match required at TRL 3) |
| **Fail** | No measurable lock-break vs baseline smoke-only |
| **JSON block** | `uas_surrogate` |

### 2E — Environmental chamber

| Item | Detail |
|------|--------|
| **Entry** | Production-representative article |
| **Procedure** | −20°C and +50°C storage/func check per KPP-10 |
| **Pass** | No functional failure; duration within MC temp-bin expectations |
| **JSON block** | `environmental_chamber` |

---

## Instrumentation (recommended)

| Measurement | Purpose |
|-------------|---------|
| Load cell / gravimetric capture | 2A burn rate, yield |
| FTIR / transmissometer | 2B α(λ) |
| Laser range / surveyed grid | 2C throw distance |
| Fused EO/IR test rig | 2D lock-break |
| Environmental chamber log | 2E KPP-10 |

---

## Data handoff (repo)

1. Copy [`data/partner_validation_results.template.json`](../data/partner_validation_results.template.json) → `data/partner_validation_results.json` (do not commit classified partner data without approval).  
2. Set `status`: `pending` → `partial` → `complete`.  
3. Fill measured fields only — **no fabricated numbers**.  
4. Update [verification matrix](../rtm/verification_matrix.md) rows for KPP-12/13 when applicable.

---

## Collaboration opportunities

MS-V (concept + 140M M&S + RTM) pairs well with partners who have:

| Need from partner | MS-V brings |
|-------------------|-------------|
| **Pyrotechnic / fill lab** | Sobol-ranked test plan, literature bounds, Annex C trades |
| **Grenade body prototype shop** | v2 KPP envelope, STL, Phase 1 gates |
| **Range / UAS test** | CONOPS scenarios, MoE surrogate definition, honest limits |
| **Prime integrator** | Full RTM, SRD/TEMP drafts, IP framework |

**Inquiry:** [Partnership issue template](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml) · [Licensing & partnership](licensing-and-partnership.md)

---

## Honest limits

- This repo **cannot** substitute for bench or range data.  
- Until `partner_validation_results.json` is populated, all KPP pass rows remain **SENSITIVITY_PASS** or **UNVERIFIED** per RTM.  
- KPP-12 (toxicology) and KPP-13 (cost) require Phase 4 manufacturing/safety programs — not closed by M&S.

---

[← Phase 1 gates](10-phase-1-prototype-gates.md) · [Fill test plan](../analysis/fill_physics_test_plan.md) · [TRL gate](../proposals/trl_gate_external.md)
