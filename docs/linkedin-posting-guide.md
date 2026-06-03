# LinkedIn Posting Guide — MS-V Veil

**Version:** 1.0 · 2026-06-02  
**Audience:** Anyone posting on behalf of the program  
**Status:** Required reading before any public LinkedIn post

---

## Verdict (2026-06-02)

| Post type | Ready? | Notes |
|-----------|--------|-------|
| **Images only** (3 canonical + caption) | **Yes** | Use Option B copy from [`LINKEDIN_CAMPAIGN_BRIEF.md`](../analysis/LINKEDIN_CAMPAIGN_BRIEF.md) |
| **Short concept post** (problem + TRL 2, no numbers) | **Yes** | Option C in brief |
| **Post with repo link** | **Conditional** | Only after using conservative copy + CEL notice |
| **Technical deep-dive** (Option A) | **No** | DMs / invited reviewers only — too easy to over-claim MoE |

Visual verification: [`analysis/LINKEDIN_VISUAL_VERIFICATION.md`](../analysis/LINKEDIN_VISUAL_VERIFICATION.md)

---

## Mandatory language (every post)

Include **at least one** of these in the first three lines or image caption:

- *Concept / TRL 2 — not field validation*
- *Literature-parameter M&S — not empirical MS-V performance*
- *Planning surrogate — not measured UAS defeat*

Add on **every image**:

> *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

---

## Safe to say

| Claim | Framing |
|-------|---------|
| 140M-sample sensitivity campaign | "Monte Carlo **sensitivity study**" |
| 38 scenario jobs all pass **in model** | "Under literature bounds in M&S" |
| Duration p10 ~170 s (3 grenades) | "Model p10 at bounded parameters" |
| MoE 80% / 55% | "**Surrogate** lock-met fraction in sim — not field lock-break rate" |
| Sobol burn_rate ST ≈ 0.83 | "Guides **which bench tests to run first**" |
| v2 form factor 850 g | "Design target / concept envelope" |
| Open repo for evaluation | "Under **CEL** — evaluation only, not commercial use" |

---

## Do NOT say

| Forbidden | Why |
|-----------|-----|
| "Validated," "proven," "confirmed in testing" | No fill or range data |
| "Breaks drone lock" as fact | Surrogate MoE only (A-013) |
| "Military ready," "fielded," "procurement ready" | TRL 2 ceiling |
| "80% defeat rate" / "kills FPV" | Misreads MoE metric |
| "Phase 2 proves…" | Phase2 is a **model tier**, not test phase |
| Omit visual smoke pairing | Doctrine requires AN-M8/M83 + MS-V |
| Link repo without CEL mention | Legal/optics |

---

## Posting sequence (recommended)

### Phase 1 — No repo link (week 1)

1. Post **Option C** or **Option B** from [`LINKEDIN_CAMPAIGN_BRIEF.md`](../analysis/LINKEDIN_CAMPAIGN_BRIEF.md)  
2. Attach carousel: hero → scale → cutaway (raw URLs in brief)  
3. Hashtags: `#defenseinnovation` `#simulation` — avoid `#militaryready`

### Phase 2 — Soft repo link (after Phase 1, no negative feedback)

Add one line:

> Open evaluation concept (CEL): https://github.com/Fratres-X-AI/MS-V — partnership inquiries welcome.

### Phase 3 — Partner funnel

Direct serious DMs to [partnership inquiry](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml).

---

## Optics and compliance (self-check)

- [ ] No classified or export-controlled detail in post or comments  
- [ ] No specific unit, operation, or classified program names  
- [ ] Framed as **obscuration concept**, not weapon effectiveness claim  
- [ ] Visual smoke **always** mentioned as paired employment  
- [ ] MoE numbers labeled **surrogate / M&S** if cited at all  

---

## If a reviewer pushes back

| Pushback | Response |
|----------|----------|
| "Where's the test data?" | "TRL 2 sensitivity study; bench plan in repo DOC-11 / fill_physics_test_plan." |
| "80% seems high" | "Surrogate threshold in MC — v6 spread shows 55% under adversarial stack; not UAS test." |
| "Why public?" | "CEL evaluation repo for capture and fill-vendor partners — not production release." |

---

## Related artifacts

| Doc | Purpose |
|-----|---------|
| [`analysis/LINKEDIN_CAMPAIGN_BRIEF.md`](../analysis/LINKEDIN_CAMPAIGN_BRIEF.md) | Approved copy blocks |
| [`analysis/LINKEDIN_VISUAL_VERIFICATION.md`](../analysis/LINKEDIN_VISUAL_VERIFICATION.md) | Visual vs v2 KPP checklist |
| [`docs/MS-V-one-pager.md`](MS-V-one-pager.md) | PDF-style summary for DMs |
| [`docs/licensing-and-partnership.md`](licensing-and-partnership.md) | CEL + PCA path |
| [`proposals/capture-brief.md`](../proposals/capture-brief.md) | For primes reviewing repo |

---

*Not legal advice. Not authorization to field any system.*
