# Contributing to MS-V Veil

Thank you for improving the MS-V concept.

## License

By contributing documentation, data, code, or visuals to this repository, you
agree that your contribution may be distributed under the
[Concept Evaluation License (CEL)](LICENSE) for public evaluation access.

If your employer or contract requires different terms, **do not contribute** until
you have written approval from Fratres-X-AI (see
[LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) for prime collaboration).

## What we welcome

- Corrections to notional specs with traceability to annexes, RTM, or YAML
- Link fixes, diagram clarity, and CONOPS wording
- Monte Carlo, CI, and reproducibility improvements
- References with citations (Annex E style)
- Partner validation data **only** via the schema in [`data/partner_validation_results.template.json`](data/partner_validation_results.template.json)

## What to avoid

- Export-controlled or classified technical data
- Proprietary third-party fill formulations without permission
- Changes that present M&S figures as field-tested or procurement-ready performance
- Overwriting **SHA256-pinned** canonical renders without explicit approval (see [`tests/test_canonical_renders.py`](tests/test_canonical_renders.py))

## Process

1. Fork and branch from `main`
2. Keep changes scoped to one topic per pull request
3. Run `python -m ruff check sim models analysis tests` and `pytest tests/ -q`
4. If touching RTM: update both `rtm/verification_matrix.md` and `rtm/requirements_traceability.csv`
5. Open a PR with a short summary and which annexes/docs you updated

## Prime or government contributors

If you are contributing on behalf of a defense prime or fill vendor under a PCA, coordinate with
your contracts lead and use the
[partnership inquiry template](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml)
so contribution IP can be aligned with your agreement.
