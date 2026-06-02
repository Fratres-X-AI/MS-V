# LinkedIn Campaign Brief — MS-V Veil

> **Read first:** [`docs/linkedin-posting-guide.md`](../docs/linkedin-posting-guide.md)  
> **Visual check:** [`analysis/LINKEDIN_VISUAL_VERIFICATION.md`](LINKEDIN_VISUAL_VERIFICATION.md)  
> **Mandatory disclaimer:** Literature-parameter **TRL 2 sensitivity study** — **NOT field validation.**

---

## Posting readiness (2026-06-02)

| Post type | Ready? |
|-----------|--------|
| **Option C** — problem only, no numbers | **Yes** (safest first post) |
| **Option B** — short M&S with surrogate caveats | **Yes** (recommended) |
| **Carousel** (3 canonical images + caption) | **Yes** |
| **Option A** — technical deep-dive | **Use with caution** — expert audience only |
| **Repo link in first post** | **Defer** — see posting guide Phase 2 |

Campaign numbers below are from pod runs `2026-06-01` @ 31 workers (`phase2_v1_full_physics` + v6 probabilistic sensor). **No new pod run required for posting.**

---

## MoE / lock-break — required framing (read before any post)

**Do not say "80% drone defeat" or "breaks lock" as fact.**

| What we measured | What it is NOT |
|------------------|----------------|
| Fraction of MC samples where a **planning surrogate** (fused EO/IR transmittance < τ) stays below threshold for ≥60 s | Measured UAS lock-break or Pk |
| ~**80%** under **nominal** literature stack in mega job `baseline_10M_g3` | Validated operational effectiveness |
| ~**55%** under **adversarial** stack (`adversarial_20M_g3`) | Worst-case field performance |

Traceability: assumption **A-013** · matrix note on `surrogate_saturated` · [`rtm/verification_matrix.md`](../rtm/verification_matrix.md)

**"Phase 2"** = **model tier** in code (microphysics pipeline), not program Phase II or field test.

---

## Headline metrics (conservative citations)

| Metric | Value | Safe framing |
|--------|-------|----------------|
| Mega-suite samples | 140M (38 jobs) | "Monte Carlo sensitivity campaign" |
| Model stack | phase2 microphysics + v6 probabilistic sensor path | "Literature-bound M&S" |
| Duration p10 (3× g3) | ~170 s | "Model p10 at bounded parameters" |
| vs 120 s KPP | +~42% margin in sim | "Headroom in sensitivity study" |
| MoE surrogate (nominal / stress) | ~80% / ~55% lock-met **fraction** | "Surrogate metric — not field MoE" |
| Sobol (MoE phase2) | burn_rate ST ≈ 0.82 | "Prioritizes TRL 3 burn cup" |

Pod detail (optional footnotes): Round 2 CONOPS 1M, MoE Sobol N=8192 · Round 3 tail-risk 50M stable — see `DEEP_DIVE_REPORT.md`.

---

## Canonical visuals

**Carousel order:** hero → scale → cutaway

| # | Raw GitHub URL |
|---|----------------|
| 1 | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png |
| 2 | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png |
| 3 | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png |

**Caption (every image):** *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

---

## Option C — safest first post (recommended week 1)

**No repo link. No performance percentages.**

Standard smoke hides you from the eye. It does not hide you from a thermal camera — and fiber-optic FPV does not care about your jammer.

We are developing **MS-V Veil**, a hand-thrown **multispectral obscurant concept** meant to pair with inventory visual smoke: same grenadier TTP, layered under detection → EW → obscuration → kinetic.

This is **early concept work (TRL 2)** — not a product, not field validation. We published a literature-bound Monte Carlo study and full requirements traceability for partners who care about honest sensitivity analysis.

If you work counter-UAS, obscurants, or squad force protection — happy to connect.

#defenseinnovation #counterUAS #simulation

---

## Option B — recommended (short + honest numbers)

**Repo link optional — add in Phase 2 per posting guide.**

Standard smoke is VIS-only. Thermal and fused EO/IR UAS still see you.

**MS-V Veil** is a squad-portable **multispectral obscurant concept** (~850 g design target) — hand-thrown, paired with AN-M8/M83 visual smoke, same basic TTP as inventory smoke.

We completed a **140-million-sample Monte Carlo sensitivity study** (literature-parameter bounds, **not field test**):

• Model duration margin (p10, 3-grenade employment) ~**2.8 min** vs 120 s requirement — **in sim only**  
• **Planning surrogate** for fused EO/IR "lock-met" shows spread (**~80%** nominal stack · **~55%** stress stack) — **not measured UAS defeat**  
• Global sensitivity: **burn rate** dominates — points TRL 3 bench to burn cup first  

Concept art and traceability are on GitHub under **evaluation license (CEL)** — not commercial/production rights.

Looking for fill-characterization and range partners for TRL 3 bench.

#defenseinnovation #counterUAS #modeling

*(Add when ready: Open evaluation: https://github.com/Fratres-X-AI/MS-V)*

---

## Option A — technical audience only (use with care)

**Not recommended as first public post.**

We published a **140M-sample literature-bound sensitivity study** for **MS-V Veil** — a hand-thrown multispectral obscurant **concept** (~850 g v2 KPP) intended to degrade fused FPV/thermal observation when employed with standard visual smoke.

**This is M&S, not validation.**

→ 38-scenario Monte Carlo campaign (`phase2` model tier + probabilistic EO/IR **surrogate**)  
→ Duration p10 ~**170 s** (3× employment) vs 120 s KPP — **inside modeled bounds only**  
→ Surrogate lock-met fractions **~80% / ~55%** (nominal vs adversarial stack) — **planning metric A-013, not range data**  
→ Sobol: **burn_rate** ST ≈ 0.83 on duration — guides bench priority  

Next gate: TRL 3 fill bench + UAS surrogate (see repo DOC-11). No claim of military ready or empirical fill performance.

Repo (CEL, evaluation only): https://github.com/Fratres-X-AI/MS-V  
#defense #modeling #counterUAS #simulation

---

## Still do NOT claim

- Field validation, TRL 4+, military ready, procurement authority  
- Empirical MS-V fill performance or measured α(λ)  
- "Drone defeat rate" from MoE percentages  
- Standalone employment without visual smoke  
- Toxicology (KPP-12) or unit cost (KPP-13)  

---

## Appendix — pod campaign log (not for LinkedIn copy)

<details>
<summary>Round 2–3 metrics (internal reference)</summary>

| Campaign | Scale | Notes |
|----------|-------|-------|
| Mega refresh | 140M | phase2/v6, 38/38 pass in model |
| CONOPS | 1M × 5 cases | CONOPS_REPORT |
| MoE Sobol phase2 | N=8192 | burn_rate ST=0.82 on MoE surrogate |
| burn_worst_50M | 50M | dur p10 161.8s stable |

```bash
export RUNPOD_CPU_COUNT=32
bash sim/run_linkedin_campaign.sh   # optional refresh only
```

</details>
