# Quantitative Uncertainty Register

Derived from mega suite (140M samples), literature bounds in `params.yaml`, and remediation plan gap analysis.  
**Confidence:** LOW = no MS-V cal data; MED = literature/order-of-magnitude; HIGH = requirement-locked.

| Parameter | Unit / range | Source | Mega-suite sensitivity | Binds KPP | Cal required | Confidence |
|-----------|--------------|--------|------------------------|-----------|--------------|------------|
| filler_mass_g | 624–680 | baseline_grenades.json | Low (duration) | KPP-03 | Load cell / QC | LOW |
| burn_rate_g_s | 2.9–4.2 | Design trade 1 | **HIGH** — 4.4→152s p10 | KPP-03 | Burn cup @ T/RH | LOW |
| yield_factor | 0.22–0.52 | Literature aerosol | **None** in v3 (CL saturates) | MoE, KPP-04 | Gravimetric capture | LOW |
| α VIS | 4–12 m²/g | ECBC / HC ref | Low until sensor v4 | MoE | Spectrometer + CL | MED |
| α NIR | 3–10 m²/g | ECBC bispectral | Low until sensor v4 | MoE | Spectrometer + CL | MED |
| α MWIR | 2–9 m²/g | ECBC bispectral | **Critical unknown** | KPP-06, MoE | FTIR / transmissometer | LOW |
| visual_smoke_factor | 1.0–1.6 sweep | UNVALIDATED | Low on duration | MoE VIS | Combined plume test | LOW |
| wind_speed_mph | 0–15 | FM 3-50 / req | Low on duration (v3) | KPP-11, geometry TBD | Range | MED |
| temperature_c | −20–50 | Military std | **MED** — hot −7s p10 | KPP-03, KPP-10 | Burn cup | LOW |
| humidity_rh_pct | 20–95 | Envelope | Low in v3 | Yield/agglomeration | Chamber test | LOW |
| cloud_depth_m | 2–4 | Order-of-magnitude | Medium (CL magnitude) | KPP-04 | Lidar / photography | LOW |
| settling_velocity_m_s | 0.02 | UNVALIDATED | Not modeled in v3 duration | KPP-03 tail | Stokes + cal | LOW |
| overlap_efficiency | 0.85 | Assumed | Medium (multi-grenade area) | MoE | Range geometry | LOW |
| transmittance_threshold τ | 0.15 | Planning surrogate | **Replaced in 1B-2** | MoE | Sensor SNR curves | LOW |
| throw_range_m | 20–25 | KPP-08 | Not in MC | KPP-08 | HF range test | LOW |
| body mass_g | 850 | KPP-01 | Not in MC | Load, throw | Prototype weigh | MED |

## Sensitivity ranking (duration p10)

1. **Burn rate upper bound** — dominant; must hold formulation ≤4.2 g/s
2. **Hot temperature** — secondary
3. **Adversarial stack** — modeled worst case still ~144 s p10
4. **Yield / α / visual smoke** — do not bind in v3 (model limitation, not physical proof)

## External measurements required (TRL 3 gate)

| Priority | Measurement | Closes uncertainty on |
|----------|-------------|------------------------|
| P0 | Bulk burn rate vs temperature @ RH | KPP-03, A-002 |
| P0 | α(λ) for candidate fill VIS/NIR/MWIR | KPP-06, A-001, A-005 |
| P0 | Particle size distribution + yield | MoE, A-004 |
| P1 | Combined MS-V + AN-M8 plume transmittance | A-009, visual_smoke_factor |
| P1 | Throw distance CDF (850 g, stressed thrower) | A-012, KPP-08 |
| P2 | Respiratory irritation panel | A-010, KPP-12 |

## Model version mapping

| Model | Uncertainty treatment |
|-------|----------------------|
| v3_cl_ramp (current) | Uniform sampling in bounds; tail-risk report |
| v4_sensor (planned) | Yield/α bind MoE; sensor curves replace τ |
| v5_geometry (planned) | Settling + plume interaction; wind binds duration |

Update after each model revision and mega suite campaign.
