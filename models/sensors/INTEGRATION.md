# Sensor stack integration (M&S)

> **NOT VALIDATION** — planning surrogates for lock-break and degradation only.

## Physics tiers vs sensor path

| Tier | Engine flag | Sensor functions | Notes |
|------|-------------|------------------|-------|
| v3 lumped | `physics_tier=v3` (legacy) | Band transmittance + threshold MoE | MoE often **saturated** — non-discriminative |
| phase1b | `physics_tier=phase1b` | `fpv_thermal` + geometry CL | Threat LOS geometry |
| **phase2** (production) | `physics_tier=phase2` | `run_phase2_physics` → `fpv_thermal` → **`lock_break`** / **`degradation`** | **Default** mega suite / CONOPS |
| v6 lock | `sensor_model=v6_probabilistic_lock` | `lock_break_probability` in [`lock_break.py`](lock_break.py) | ~80% / ~55% nominal/adversarial **surrogate lock-met** |

## Where wiring lives

| Entry | File | Calls |
|-------|------|-------|
| Vectorized MC | [`sim/engine.py`](../../sim/engine.py) | `_resolve_moe_mask` → phase2 pipeline + v6 lock |
| CONOPS use cases | [`sim/conops/kill_chain.py`](../../sim/conops/kill_chain.py) | Same stack per `UseCaseSpec` |
| Seeds / jobs | [`sim/config/seeds.yaml`](../../sim/config/seeds.yaml) | `physics_tier: phase2` on mega jobs |

## `surrogate_saturated` flag

Set in engine when `lock_met_fraction` and `degraded_fraction` both ≥ 99.9%. When true:

- Do **not** cite MoE pass rate as empirical lock-break.
- Tri-band “pass” rows in RTM are **non-discriminative** (A-013).

v6 campaign reports **spread** (~80% nominal / ~55% adversarial stacks) — discriminative relative to v3 saturation, still a **planning surrogate**.

## Module map

| Module | Role |
|--------|------|
| [`fpv_thermal.py`](fpv_thermal.py) | Band-integrated contrast / NETD floor |
| [`lock_break.py`](lock_break.py) | Probabilistic fused EO/IR lock-break duration |
| [`degradation.py`](degradation.py) | Friendly-force / squad thermal exposure |

## Assumptions

See **A-013**, **A-022**, **A-027** in [`rtm/assumption_register.md`](../../rtm/assumption_register.md).
