# Human Factors — KPP-08 Throw Ballistics

> **MATURITY:** Literature-order bounds — **NOT VALIDATION**  
> **Traceability:** KPP-08 · [`models/system/human_factors.yaml`](../models/system/human_factors.yaml) · [`models/cloud_physics/deployment_kinematics.py`](../models/cloud_physics/deployment_kinematics.py)

## Model

850 g MS-V throw range is sampled uniformly **18–25 m** (Annex B target ≥20 m under stress). The phase2 deployment model applies:

| Factor | Source | Effect |
|--------|--------|--------|
| Combat load | `load_penalty.range_reduction_m` (−1.5 m) | Reduces mean throw |
| Load dispersion | `load_penalty.lateral_error_multiplier` (×1.12) | Wider lateral error |
| Stress (under fire) | `stress.lateral_error_multiplier` (×1.25) | Wider dispersion |
| Posture mix | standing 55% / kneeling 35% / prone 10% | Initial release height |

Fuze delay **0.7–2.0 s** (M201A1 band) is sampled independently — closes **KPP-07** in MC.

## KPP-08 pass rule

Mega-suite job `baseline_10M_g3_n10000000`: **p10(throw_range_m) ≥ 20 m** (`kpp_checks.throw_p10_ge_20m`).

Evidence: [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) · job JSON `kpp_08_throw_range_m`.

## TRL 3 closure

| Test | Metric | Closes |
|------|--------|--------|
| Loaded throw range (n≥30) | p10 ≥ 20 m | KPP-08 empirical |
| Lateral dispersion vs range | Compare to MC fraction | `lateral_error_fraction` |
| Posture-stratified throws | Height offset | posture fractions in YAML |

## References

- Annex B KPP-08 (≥20 m stressed, ≥25 m objective)
- Annex F form factor (850 g v2_kpp)
- FM 3-50 smoke planning (wind — separate KPP-11)
