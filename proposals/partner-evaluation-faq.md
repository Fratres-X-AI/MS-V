# Partner Evaluation FAQ — MS-V Veil

**For primes, fill vendors, and labs reviewing the public repo**

> **Onboarding:** [External review ready](../docs/EXTERNAL_REVIEW_READY.md) · **Capture:** [capture-brief.md](capture-brief.md)

---

## Can we use this repo commercially?

**No**, under the public [Concept Evaluation License (CEL)](../LICENSE). Internal trade study and capture are allowed. Commercial use, production, and fielding require a signed [Prime Collaboration Agreement](../LICENSE-COMMERCIAL.md).

---

## Is the 140M campaign validation?

**No.** It is a **literature-parameter sensitivity study** (TRL 2). All KPP rows marked SENSITIVITY_PASS mean "passes inside modeled bounds," not "passes test."

---

## What does "80% MoE" mean?

It is the fraction of Monte Carlo samples where a **planning surrogate** (fused EO/IR transmittance below τ = 0.15) stays "lock-met" for ≥60 s under **nominal** employment. It is **not** a measured UAS kill or defeat rate. Under an **adversarial** parameter stack the same surrogate reports **~55%**. See assumption **A-013** in [`rtm/assumption_register.md`](../rtm/assumption_register.md).

---

## Why did MoE used to show 100%?

Earlier model tiers saturated the surrogate (non-discriminative). Current **phase2 + v6 probabilistic** stack shows spread (55–80% in campaign jobs). Rows with `surrogate_saturated=true` in job JSON must not be cited as discriminative.

---

## What is "phase2"?

A **physics model tier** in code (`phase2_v1_full_physics`) — aerosol microphysics, humidity, plume merge — **not** "Phase II" program maturity or field test.

---

## Which form factor is authoritative?

**v2 KPP:** 850 g, 7.1 × 3.1 in. The v3_existing_container track (680 g, AN-M8 shell) is a **sourcing alternate**, not the primary external visual set.

---

## What do we need to sign?

| Tier | Document |
|------|----------|
| Read repo | CEL (click-through by use) |
| Prototype / test / production | PCA from [LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md) |

Start: [Partnership inquiry](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml)

---

## How do we reproduce the numbers?

```bash
pip install -r requirements-lock.txt
python -m sim.reproduce
```

See [REPRODUCE.md](../REPRODUCE.md) for v4 golden vs phase2 campaign profiles.

---

## Where do partner test results go?

Copy [`data/partner_validation_results.template.json`](../data/partner_validation_results.template.json) → `partner_validation_results.json` (do not fabricate data). Gates: [DOC-11](../docs/11-partner-validation-and-trl-gates.md).

---

## Public communications

Use [`capture-brief.md`](capture-brief.md) and [`docs/07-limitations-and-risks.md`](../docs/07-limitations-and-risks.md). **Do not** represent M&S as field performance. MoE percentages require **A-013** surrogate disclosure.
