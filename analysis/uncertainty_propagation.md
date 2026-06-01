# Uncertainty Propagation — MS-V Phase 1

> **MATURITY:** Literature-parameter sensitivity — **NOT VALIDATION**  
> **Evidence:** 140M mega suite + Saltelli Sobol (`analysis/SOBOL_SENSITIVITY_REPORT.md`)

## 1. Uncertainty sources

| Layer | Type | Representation | Artifact |
|-------|------|----------------|----------|
| Fill / burn | Epistemic | Uniform 624–680 g, 2.9–4.2 g/s | A-002, params.yaml |
| Environment | Aleatory | Uniform wind/temp/RH | A-007, A-015, A-016 |
| Extinction α(λ) | Epistemic | Band uniform low–high | A-001, A-006 |
| Cloud geometry | Epistemic | Area, depth uniform | A-004, A-018 |
| MoE surrogate | Model form | τ=0.15, VSF=1.3 | A-013 (**saturation risk**) |

## 2. Propagation path (KPP-03 duration)

```
filler_mass, burn_rate, temp → raw_burn_duration
build_up, CL ramp, α, geometry → time_to_threshold
raw_burn − t_threshold (if good thickness) → duration_s
```

**Dominant variance driver (Sobol ST):** `burn_rate_g_s` ≈ 0.83  
**Second:** `temp_c` ≈ 0.12 (via burn coupling)  
**Third:** `filler_mass_g` ≈ 0.05

## 3. KPP uncertainty bands (3-grenade baseline, 10M samples)

| Statistic | Build-up (s) | Duration (s) | Margin to threshold |
|-----------|--------------|--------------|---------------------|
| p10 | — | 160.0 | +33.3% vs 120 s |
| p50 | — | ~170 | — |
| p90 build-up | 12.6 | — | +16.1% headroom vs 15 s |

**Tail risk (adversarial):** duration p10 = 143.6 s (+19.7% margin) — job `baseline_10M_adversarial_g3_n10000000`

**Tightest OAT sweep:** `sweep_burn_hi_4.4_g3` duration p10 = 152.4 s (+27.0% margin)

## 4. MoE uncertainty (honest)

- Binary MoE surrogate: **zero variance** in Sobol at current τ — all evaluations pass
- **Cannot propagate MoE uncertainty** until instrumented UAS surrogate (TRL 3)
- CL_peak variance driven by yield (ST≈0.47), depth (ST≈0.33), wind (ST≈0.22)

## 5. What would invalidate current claims

1. Measured burn rate > 4.4 g/s at nominal fill → duration p10 may approach 120 s bound
2. Measured α(λ) below literature low band → good-thickness fraction drops
3. Combined plume geometry reduces effective CL → MoE may fail in reality despite surrogate pass
4. Throw/deployment error moves cloud off target — unmodeled (KPP-08)

## 6. Regeneration

```bash
python -m sim.reproduce
python sim/run_sobol.py --n-base 8192 --workers 31
python analysis/summarize_sobol.py
python analysis/generate_figures.py
```

See `rtm/verification_matrix.md` for requirement-level mapping.
