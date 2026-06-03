# External Review Ready — MS-V Veil

> **Purpose:** Single onboarding path for primes, sponsors, and technical reviewers.  
> **Maturity:** TRL 2–3 **literature-parameter M&S** — not field validation.  
> **License:** [CEL](../LICENSE) evaluation only · [PCA](../LICENSE-COMMERCIAL.md) for production.

---

## 60-second orientation

MS-V is a **hand-thrown multispectral obscurant grenade concept** (~**850 g**, **7.1 × 3.1 in**) meant to pair with standard visual smoke against fused EO/IR UAS. The repo delivers a **140M-sample phase2/v6 Monte Carlo campaign**, full RTM, CONOPS, form-factor authority, and partner test plans — **without claiming empirical fill or range validation**.

---

## Recommended read order (45–90 min)

| Step | Document | Why |
|------|----------|-----|
| 1 | [Capture brief](../proposals/capture-brief.md) | Problem, ask, what we have / don't |
| 2 | [Partner evaluation FAQ](../proposals/partner-evaluation-faq.md) | CEL, MoE surrogate, reproduce |
| 3 | [SRD](../proposals/srd/MS-V-SRD.md) | KPP/MoE + traceability legend + E-1..E-5 gaps |
| 4 | [Verification matrix](../rtm/verification_matrix.md) | 38 jobs, margins, saturation flags |
| 5 | [TEMP outline](../proposals/temp/MS-V-TEMP-outline.md) | TRL 3 test cards (gates 2A–2E) |
| 6 | [Annex F](../annexes/F-form-factor-and-ergonomics.md) + [FORM_FACTOR_REPORT](../analysis/FORM_FACTOR_REPORT.md) | v2 KPP envelope |
| 7 | [MEGA_SUITE_REPORT](../analysis/MEGA_SUITE_REPORT.md) | Campaign summary |
| 8 | [Limitations](../docs/07-limitations-and-risks.md) | Forbidden claims |

**External visuals:** [Visual verification](../analysis/VISUAL_VERIFICATION.md) — mandatory caption on all concept art.

---

## Reproduce (5 min, laptop-safe)

```bash
pip install -r requirements-lock.txt
python -m sim.reproduce --validate-only   # fast checksum gate
pytest tests/ -q                          # full unit + invariant suite
```

Full golden reproduce (heavier): `python -m sim.reproduce` · See [REPRODUCE.md](../REPRODUCE.md).

---

## What passes automated quality gates

| Gate | Command |
|------|---------|
| Lint | `ruff check sim models analysis tests` |
| Tests | `pytest tests/ -q` (includes SHA256 canonical renders) |
| Invariants | `pytest tests/test_repo_invariants.py -q` |
| Types (phased) | `mypy` |
| CI | [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) |

---

## Honest claim boundaries

| You may say | You may not say |
|-------------|-----------------|
| Model-supported under literature bounds | Field validated / military ready |
| 38/38 KPP pass in M&S (with matrix caveats) | MoE % = defeat rate |
| v2 KPP design authority (850 g, 7.1×3.1 in) | MIT open source (repo is **CEL**) |
| v6 lock-met ~80% / ~55% **planning surrogate (A-013)** | Unqualified performance percentages |

---

## Open empirical gaps (partner-only)

| Gate | Closes |
|------|--------|
| E-1 / 2A–2B | Fill burn, α(λ), tox |
| E-2 / 2C | Throw range n≥30 |
| E-3 | Prototype mass/drawing |
| E-4 / 2D | UAS surrogate lock-break |
| E-5 / 2E | Environmental chamber |

Details: [trl_gate_external.md](../proposals/trl_gate_external.md) · [DOC-11](11-partner-validation-and-trl-gates.md).

---

## Contact

[Partnership inquiry](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml) · [Licensing & partnership](licensing-and-partnership.md)

---

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION*
