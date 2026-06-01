# Sensor Models

## Current (Phase 1 — v3 engine)

| File | Status |
|------|--------|
| [surrogate_sensors.py](surrogate_sensors.py) | Legacy scalar threshold — **deprecated after 1B-2** |
| Engine MoE | Inline tri-band Beer-Lambert in `cloud_evolution.py` |

## Planned (Phase 1B — v4)

| File | Purpose |
|------|---------|
| [fpv_thermal.py](fpv_thermal.py) | Band-integrated FPV + uncooled/cooled thermal contrast |
| `params.yaml` | Sensor curves, NETD, contrast thresholds |
| `sim/run_sensor_jobs.py` | Targeted degradation Monte Carlo |

## Requirements (from remediation plan)

1. MoE must **vary** with yield/α sweeps (not saturate at 100%)
2. Separate uncooled (8–14 µm) and cooled (3–5 µm) paths
3. Traceability to ECBC surrogate UAS test metrics
4. Explicit “surrogate, not threat system” labeling

See [analysis/REMEDIATION_PLAN.md](../../analysis/REMEDIATION_PLAN.md) §1B-2.
