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

- Hand-thrown **850 g** grenade · **M201A1-compatible** fuze  
- **VIS + NIR + MWIR** bispectral fill (concept)  
- **2–3 MS-V + visual smoke** employment doctrine  
- Visual: [Cutaway](../analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png)  

---

## Slide 4 — How the squad fights (sequence)

1. Threat cue → grenadier throws MS-V + AN-M8/M83  
2. **~12–15 s** build-up → **2+ min** dense screen (design targets)  
3. Squad moves / CASEVAC / breaks contact under layered stack  
4. EW + kinetic if threat persists  

- Emphasize **complementary** to inventory smoke — not standalone  

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
- Duration p10 **~170 s** (3 grenades) · **+42%** headroom on 120 s KPP  
- MoE **80%** nominal · **55%** adversarial — **discriminative, not saturated**  
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
- MOLLE pouch fit studied · throw model p10 ≥ 20 m stressed  
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
