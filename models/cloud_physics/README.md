# Cloud Physics Model

Phase 1 — wavelength-dependent extinction and cloud evolution.

## Files

| File | Purpose |
|------|---------|
| [params.yaml](params.yaml) | MS-V literature-bound parameters (burn, fill, α) |
| [burn_model.py](burn_model.py) | Fill mass, sustained burn rate, aerosol yield |
| [extinction.py](extinction.py) | Beer-Lambert transmittance vs band |
| [cloud_evolution.py](cloud_evolution.py) | CL, build-up, CL-threshold duration, tri-band MoE |

## Model version: `phase1_v3_cl_ramp`

- **Duration (KPP-03):** seconds from first CL threshold crossing (linear ramp during build-up) until fuel exhaustion.
- **Burn rate:** MS-V density-optimized **2.9–4.2 g/s** on **624–680 g** fill.
- **MoE:** fused VIS (with visual smoke factor) + NIR + MWIR transmittance below τ = 0.15.
- **Temperature:** symmetric burn-rate coupling ±0.2%/°C from 20°C reference.

## Bands

- VIS: 0.4–0.7 µm
- NIR: 0.7–1.4 µm
- MWIR: 3–5 µm

## Validation scripts

- `python sim/run_suite_local.py` — 100k nominal envelope
- `python sim/validate_stress.py` — adversarial corner margins

## Status

Literature-parameter sensitivity study — **not empirical validation**.
