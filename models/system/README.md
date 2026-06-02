# models/system — Form Factor & Ergonomics

Parametric **v2 KPP** envelope and deployment inputs. **NOT validation.**

| Module | Role |
|--------|------|
| [`form_factor.yaml`](form_factor.yaml) | Authoritative v2_kpp / v3 tracks |
| [`envelope.py`](envelope.py) | Volume budget, pouch fit, loadout mass |
| [`human_factors.yaml`](human_factors.yaml) | Throw range, load, posture fractions |
| [`kinematics.py`](kinematics.py) | Facade: throw dispersion summaries for reports |
| [`geometry.md`](geometry.md) | Human-readable envelope notes |
| [`stl_export.py`](stl_export.py) | Tier B STL export |
| [`openscad/`](openscad/) | Parametric body source |

## What lives elsewhere

| Concern | Location |
|---------|------|
| Throw dispersion in MC | [`models/cloud_physics/deployment_kinematics.py`](../cloud_physics/deployment_kinematics.py) |
| Phase 2 cloud physics | [`models/cloud_physics/phase2_pipeline.py`](../cloud_physics/phase2_pipeline.py) |
| EO/IR surrogate | [`models/sensors/`](../sensors/) |

## Primary variant

**v2_kpp:** 850 g, 7.1 × 3.1 in — see [`annexes/F-form-factor-and-ergonomics.md`](../../annexes/F-form-factor-and-ergonomics.md) · [`analysis/FORM_FACTOR_REPORT.md`](../../analysis/FORM_FACTOR_REPORT.md).

Regenerate Tier B assets: `python analysis/generate_form_factor_assets.py` (does not overwrite SHA256-pinned canonical renders).
