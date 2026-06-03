# Agent / contributor guide — MS-V

## Quality bar

Everything in-repo we control should pass **`make check`** (lint, tests, validate-only, invariants, mypy).

## Non-negotiables

1. **v2 KPP authority:** 850 g, 7.1 × 3.1 in — not v3 680 g envelope for MS-V claims.
2. **MoE:** Planning surrogate (A-013); never field defeat rate. Cite ~80%/55% only with caveat.
3. **License:** CEL — never describe as MIT.
4. **Canonical renders:** Do not overwrite SHA256-pinned PNGs without updating `tests/test_canonical_renders.py`.
5. **RTM:** KPP/MoE claims need `rtm/verification_matrix.md` job ID.
6. **Labels:** M&S outputs = literature-parameter sensitivity — **NOT VALIDATION**.
7. **No platform/social collateral** in this repo — partner and RTM artifacts only.

## Key paths

| Area | Path |
|------|------|
| Reviewer onboarding | `docs/EXTERNAL_REVIEW_READY.md` |
| Engine | `sim/engine.py` (`physics_tier=phase2`) |
| Sensors | `models/sensors/INTEGRATION.md` |
| Form factor | `models/system/form_factor.yaml`, `kinematics.py` |
| Partner pack | `proposals/capture-brief.md` |

## Before PR

```bash
make check
```

Heavy (CI only / optional): `make ci` — reproduce + mega `--quick` + Sobol.
