# Changelog

## v2.1.1 — Remove platform-specific outreach docs (2026-06-03)

- Removed posting guide, campaign brief, and dedicated outreach tests/scripts.
- Renamed visual verification to [`analysis/VISUAL_VERIFICATION.md`](analysis/VISUAL_VERIFICATION.md).
- Pod refresh script: `sim/run_evidence_refresh.sh` → `analysis/results/evidence_refresh.json`.

## v2.1.0 — Gap closure & quality gates (2026-06-02)

- **External review pack:** [`docs/EXTERNAL_REVIEW_READY.md`](docs/EXTERNAL_REVIEW_READY.md), expanded SRD/TEMP, v2 `FORM_FACTOR_REPORT`, [`models/system/kinematics.py`](models/system/kinematics.py).
- **Quality:** `make check`, `tests/test_repo_invariants.py`, CI split (fast `quality` job + `simulation`).
- **Physics/docs:** phase2 PSD settling per sample, sensor [`INTEGRATION.md`](models/sensors/INTEGRATION.md), MasterPlan + docs 00–08 footers, A-013 v6 framing.
- **Agent guide:** [`AGENTS.md`](AGENTS.md).

## v2.0.2 — Public outreach pack (2026-06-02) — superseded

- Outreach docs later removed in v2.1.1; use **capture brief** + **visual verification** only.

## v2.0.1 — CEL license (2026-06-01)

- Replaced MIT with **Concept Evaluation License (CEL)** — evaluation-only public access; commercial/production under PCA.
- Updated LICENSE, LICENSE-COMMERCIAL, CONTRIBUTING, partnership docs, and inquiry template.

## v2.0.0 — Partner handoff pack (RADR-parity) (2026-06-01)

- **Prime / creator handoff:** [LICENSE](LICENSE) (CEL) + [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md), [CONTRIBUTING.md](CONTRIBUTING.md), [partnership issue template](.github/ISSUE_TEMPLATE/partnership_inquiry.yml).
- **Partner docs:** [Licensing & partnership](docs/licensing-and-partnership.md), [MS-V one-pager](docs/MS-V-one-pager.md), [Pitch deck outline](docs/pitch-deck-outline.md), [DOC-10 prototype gates](docs/10-phase-1-prototype-gates.md), [DOC-11 partner validation](docs/11-partner-validation-and-trl-gates.md).
- **Visuals catalog:** [visuals/README.md](visuals/README.md), [V2-KPP-SPEC](visuals/grenade/V2-KPP-SPEC.md); README gallery with authoritative concept trio.
- **Partner data schema:** [`data/partner_validation_results.template.json`](data/partner_validation_results.template.json) (`status: pending` — no fabricated test data).
- **Canonical render pins:** SHA256 lock in `tests/test_canonical_renders.py`.

## v1.9.0 — Pod campaign closure (2026-06-01)

- Pod rounds 2–3: MoE Sobol phase2 (N=8192), CONOPS 1M, tail-risk deep dives (50M burn-worst stable).
- Full RTM: KPP-01–14, MOE-01/02, LIM-01–03; `REPRODUCE.md`; phase2/v6 mega suite.
- KPP-08 throw model; deep dive reports.

## v1.8.0 — v2 canonical renders & form factor (2026-05)

- User-approved v2 KPP concept trio (850 g, 7.1 × 3.1 in); engineering figure set; dual v2/v3 tracks in `form_factor.yaml`.
