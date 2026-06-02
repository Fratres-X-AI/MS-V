# MS-V Veil — Capture Brief (Primes & Sponsors)

**Version:** 1.1 · 2026-06-02  
**Maturity:** TRL 2 sensitivity study — **NOT field validation**  
**License:** Public repo under [CEL](../LICENSE); development/production under [PCA](../LICENSE-COMMERCIAL.md)  
**Full review path:** [External review ready](../docs/EXTERNAL_REVIEW_READY.md)

---

## Elevator pitch (30 seconds)

Inventory smoke defeats the eye, not the thermal channel. Squad forces lack a **portable multispectral screen** against FPV and fiber-optic UAS when EW and kinetic layers are thin. **MS-V Veil** is a hand-thrown obscurant **concept** (~850 g) meant to pair with standard visual smoke — same pin-pull TTP, layered under detection → EW → obscuration → kinetic. We completed a **140M-sample literature-bound Monte Carlo campaign** with full requirements traceability; we need **fill and range partners** for TRL 3.

---

## Problem

| Gap | Today | With MS-V (concept) |
|-----|-------|---------------------|
| Thermal sees through smoke | AN-M8 is VIS-only | Model-bound VIS+NIR+MWIR attenuation |
| Fiber-optic drones | EW irrelevant | Obscuration path |
| Squad portability | Vehicle obscurants too heavy | Hand-thrown, 2–3 + visual smoke |

---

## What we have (in repo)

| Asset | Location |
|-------|----------|
| Requirements + RTM | `rtm/verification_matrix.md`, CSV |
| 140M mega suite evidence | `analysis/MEGA_SUITE_REPORT.md` |
| Global sensitivity | `analysis/SOBOL_SENSITIVITY_REPORT.md` |
| CONOPS (5 cases) | `analysis/CONOPS_REPORT.md` |
| SRD / TEMP drafts | `proposals/srd/`, `proposals/temp/` |
| TRL 3–4 gate | `proposals/trl_gate_external.md`, `docs/11-partner-validation-and-trl-gates.md` |
| Form factor + STL | `annexes/F`, `models/system/form_factor.yaml` |
| Reproducibility | `python -m sim.reproduce`, CI green |

---

## What we do not have

- MS-V fill empirical data (burn cup, α(λ), tox)  
- Range UAS lock-break test  
- Prototype at 850 g  
- Cost model (KPP-13)  
- Production or export authorization  

---

## M&S headline (conservative framing)

| Metric | Value | Caveat |
|--------|-------|--------|
| Samples | 140M (38 jobs) | Literature bounds only |
| Duration p10 (3× g3) | ~170 s in model | +42% vs 120 s KPP in sim |
| MoE surrogate (nominal / adversarial) | ~80% / ~55% lock-met fraction | **Not** field defeat rate (A-013) |
| Top Sobol driver | burn_rate on duration | Prioritize burn cup in TRL 3 |

---

## Ask (typical teaming)

| Partner type | We need | We offer |
|--------------|---------|----------|
| **Pyrotechnic / fill** | Burn cup, α(λ), PSD, tox screening | Sobol-ranked test plan, literature bounds |
| **Prime integrator** | Prototype body, capture, Program | Full RTM, M&S, CONOPS, IP framework (PCA) |
| **Range / UAS lab** | Surrogate lock-break test | CONOPS scenarios, honest MoE definition |

**Inquiry:** https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml

---

## Compliance note

Repository is **unclassified notional** material. No ITAR/EAR data in public repo. Evaluation under **CEL** only until PCA executed.

---

## One-page + deck

- [MS-V one-pager](../docs/MS-V-one-pager.md)  
- [Pitch deck outline](../docs/pitch-deck-outline.md)  
- [Program narrative](narratives/MS-V-program-narrative.md)
