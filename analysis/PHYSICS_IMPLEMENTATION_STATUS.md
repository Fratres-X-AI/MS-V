# MS-V Cloud & Sensor Physics — Implementation Status

> **Maturity:** Phase 2 Monte Carlo sensitivity model (`phase2_v1_full_physics`)  
> **Disclaimer:** LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION

## Tier Summary

| Tier | ID | Scope |
|------|-----|-------|
| v4 | `phase1_v4_sensor` | Lumped CL, band-integrated MoE (140M campaign locked) |
| phase1b | `phase1_v6_threat_geometry` | Geometry, settling, HC plumes, edge-of-plume LOS |
| **phase2** | **`phase2_v1_full_physics`** | **Full stack below + v6 probabilistic lock-break** |

Default engine: `physics_tier: phase2` · `sensor_model: v6_probabilistic_lock`

---

## Implemented (Phase 2)

| Gap area | Module | Status |
|----------|--------|--------|
| **1. Aerosol microphysics** | `aerosol_microphysics.py` | PSD log-normal, Stokes settling, coagulation yield, hygroscopic growth |
| **2. Cloud geometry** | `cloud_structure.py` | Gaussian vertical profile, wind shear, multi-grenade merge, buoyancy rise |
| **3. Atmospheric coupling** | `atmospheric_coupling.py` | Humidity extinction boost, precip washout tail, stability mixing |
| **4. Spectral extinction** | `spectral_extinction.py` | Band-internal α, Mie diameter scaling, multiple-scatter correction |
| **5. Sensor degradation** | `fpv_thermal.py`, `lock_break.py` | Band integration, NETD, **probabilistic lock-break**, fiber vs RF |
| **6. Deployment kinematics** | `deployment_kinematics.py`, `human_factors.yaml` | Throw range/dispersion, fuze delay, posture height |
| **7. Time-dependent burn** | `burn_dynamics.py` | Ignition/steady/tail phases, generation ramp, post-burn dissipate |
| **8. Layered plumes** | `layered_plumes.py`, `phase2_pipeline.py` | Per-band MS-V + HC optical depth, diurnal MWIR contrast |
| **9. Threat geometry** | `geometry_settling.py` | Edge-of-plume radial, orbit, wind advection (Phase 1B retained) |
| **10. Model-form uncertainty** | `params.yaml` phase2.model_form | Ramp exponent sampling |
| **Orchestrator** | `phase2_pipeline.py` | Composes all layers → engine + CONOPS |

---

## Still Simplified / External

| Item | Notes |
|------|-------|
| Empirical MS-V α(λ), PSD cal | Requires lab — `fill_physics_test_plan` gate |
| Full Mie scattering code | Diameter-scaled α surrogate only |
| CFD plume / LES | Parametric Gaussian + shear scalars |
| Classified threat sensor curves | v6 logistic lock-break is planning surrogate |
| Toxicity / KPP-11 | Not in MC scope |
| Sobol on phase2 | `sobol_model.py` still v4 (campaign continuity) |
| 140M mega suite | Locked v4 via `load_mega_params()` |

---

## Run

```bash
bash one_pass.sh 31 8192          # full pipeline
python sim/run_conops.py          # five use cases
pytest tests/ -q                  # unit + integration
python -m sim.reproduce           # v4 golden gate
```

---

## Key Parameters

See `models/cloud_physics/params.yaml` → `phase2:` and `phase1b:`  
Assumptions **A-023–A-027** in `rtm/assumption_register.md`
