# MS-V Veil — Pitch Deck Outline (8–10 Slides)

**Audience:** Squad/SOF stakeholders, pyrotechnic partners, **defense primes**, concept sponsors  
**Version:** 2.0.0 · Expand each slide to 1–2 minutes spoken

---

## Slide 1 — Title

- **MS-V Veil** — Multispectral Obscurant Grenade  
- Squad-layer **drone manipulation** — not another smoke grenade  
- TRL 2 · 140M-sample sensitivity study · v2 KPP (850 g)  
- Visual: [Hero](../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png) + [scale](../analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png)

---

## Slide 2 — The gap

- Standard smoke defeats **day optics** — **thermal sees through**  
- FPV and **fiber-optic** drones don't jam  
- Need: **squad-portable multispectral screen** without new launchers or TTP overhaul  

---

## Slide 3 — System overview

- Hand-thrown concept, **850 g** design target · fuze not tested  
- **VIS + NIR + MWIR** fill (concept, not synthesized)  
- **2–3 MS-V + visual smoke** is a modeled pairing, not a doctrine  
- Visual: [Cutaway](../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png)  

---

## Slide 4 — What the model shows (not a drill)

- Model duration p10 is ~170 s on the nominal case. That is a threshold, not cover time.
- Nothing here is cleared to throw, breathe, or move through. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).
- Toxicology (KPP-12) is unverified. Throw range (KPP-08) is not closed.
- Say "concept" and "model," not "fights" or "employs."

---

## Slide 5 — Layered defense

```
Detect → EW → MS-V + smoke → kinetic window
```

- MS-V fills the **obscuration gap** when EW is degraded or fiber-optic  
- Ref: [DOC-08](08-layered-defense-integration.md) · [CONOPS](04-conops-use-cases.md)  

---

## Slide 6 — M&S evidence (honest framing)

- **140M Monte Carlo** · 38 scenarios · phase2 microphysics + v6 probabilistic lock  
- Duration p10 **~170 s** (3 grenades, model only) · **+42%** vs 120 s threshold  
- MoE **80%** nominal · **55%** adversarial — planning surrogate (A-013), not a defeat rate  
- **Literature-parameter bounds — NOT field validation**  
- Ref: [MEGA_SUITE_REPORT](../analysis/MEGA_SUITE_REPORT.md) · [verification matrix](../rtm/verification_matrix.md)  

---

## Slide 7 — Sensitivity drives TRL 3 priority

- **Burn rate** dominates duration (Sobol ST ≈ 0.83)  
- **α_MWIR** second for MoE lock-break  
- CONOPS lock-met fractions vary by use case — honest spread  
- Ref: [SOBOL report](../analysis/SOBOL_SENSITIVITY_REPORT.md) · [fill test plan](../analysis/fill_physics_test_plan.md)  

---

## Slide 8 — Form factor & ergonomics

- v2 KPP: **7.1 × 3.1 in** — ~25% larger than AN-M8  
- MOLLE pouch fit studied · throw p10 of 20.0 m was floored. Do not brief it.  
- Ref: [Annex F](../annexes/F-form-factor-and-ergonomics.md) · [V2-KPP-SPEC](../visuals/grenade/V2-KPP-SPEC.md)  

---

## Slide 9 — Roadmap and open questions

- **TRL 3 bench:** burn cup, α(λ), throw range, UAS surrogate  
- **Open:** fill chemistry down-select (Annex C) · tox (KPP-12) · cost model (KPP-13)  
- Ref: [DOC-10](10-phase-1-prototype-gates.md) · [DOC-11](11-partner-validation-and-trl-gates.md)  

---

## Slide 10 — IP & prime partnership

- **Evaluation access:** CEL on repo (internal trade study, capture, diligence — not commercial use)  
- **Prime path:** [LICENSE-COMMERCIAL](../LICENSE-COMMERCIAL.md) — evaluation → development → production under **PCA**  
- **Background IP** (concept + M&S) · **Foreground IP** (fill, prototype) — defined up front  
- Guide: [Licensing & partnership](licensing-and-partnership.md)  
- CTA: [Partnership inquiry](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml)  

---

## Slide 11 — Ask / close

- Feedback on **squad-layer obscuration** vs. layered stack (DOC-08)  
- Partners for **fill characterization**, **body prototype**, **range validation** · **prime integrators welcome**  
- Repo: https://github.com/Fratres-X-AI/MS-V  
- **Not** fielded · **not** procurement-ready · **not** validation  

---

## Appendix slides (optional)

- Comparison table vs. AN-M8 / M83 / vehicle obscurants (Annex A)  
- Five CONOPS use cases + MoE windows ([CONOPS_REPORT](../analysis/CONOPS_REPORT.md))  
- Full KPP traceability matrix  
- Canonical concept trio ([visuals/README](../visuals/README.md), [VISUAL_VERIFICATION](../analysis/VISUAL_VERIFICATION.md))
