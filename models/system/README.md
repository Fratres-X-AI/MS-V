# models/system — Form Factor, Ergonomics & Kinematics

Parametric **v2 KPP** envelope (**850 g**, **7.1 × 3.1 in**). **NOT VALIDATION** — design authority and literature-order MC only.

## Module map

| Module | Role | RTM |
|--------|------|-----|
| [`form_factor.yaml`](form_factor.yaml) | Authoritative `v2_kpp` / `v3_existing_container` tracks | KPP-01, KPP-09 |
| [`envelope.py`](envelope.py) | Volume budget, pouch fit, loadout mass | KPP-09, Annex F |
| [`human_factors.yaml`](human_factors.yaml) | Throw band, load, posture, stress | KPP-08, A-012 |
| [`kinematics.py`](kinematics.py) | Throw MC facade + report summaries | KPP-08 → matrix job |
| [`geometry.md`](geometry.md) | Human-readable notes | — |
| [`stl_export.py`](stl_export.py) | Tier B STL | DOC-10 |
| [`openscad/`](openscad/) | Parametric body | — |

## Kinematics API

```python
from models.system.kinematics import load_v2_envelope, throw_distribution, impact_dispersion_summary

env = load_v2_envelope()  # 850 g, 7.1 x 3.1 in
stats = impact_dispersion_summary(n=10_000, stressed=True)  # KPP-08 MC percentiles
```

| Function | Output |
|----------|--------|
| `load_v2_envelope()` | `Envelope` dataclass from `v2_kpp` |
| `throw_distribution(rng, n, stressed=True)` | `throw_range_m`, `throw_offset_m`, `initial_height_m` |
| `impact_dispersion_summary()` | p10/p50/p90 throw + lateral — feeds [`FORM_FACTOR_REPORT.md`](../../analysis/FORM_FACTOR_REPORT.md) |
| `human_factors_summary()` | YAML + loadout snapshot for reports |

Physics implementation: [`models/cloud_physics/deployment_kinematics.py`](../cloud_physics/deployment_kinematics.py) (phase2 path in [`sim/engine.py`](../../sim/engine.py)).

## Regeneration

```bash
python analysis/generate_form_factor_assets.py
```

Does **not** overwrite SHA256-pinned canonical renders — see [`analysis/figures/form_factor/CANONICAL_RENDERS.md`](../../analysis/figures/form_factor/CANONICAL_RENDERS.md).

## External caption (required on visuals)

*Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*
