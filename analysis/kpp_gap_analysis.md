# KPP Gap Analysis — Phase 1 M&S (v3/v4 + 140M Mega Suite + Sobol)

> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION  
> Model: `phase1_v3_cl_ramp` (campaign) / `phase1_v4_sensor` (current engine)  
> **Pass ≠ design confirmation.** See [`REMEDIATION_PLAN.md`](REMEDIATION_PLAN.md), [`tail_risk_analysis.md`](tail_risk_analysis.md), [`uncertainty_propagation.md`](uncertainty_propagation.md)

## Summary (140M mega suite — 38/38 jobs all-KPP-pass)

| KPP | Target | Nominal (3G baseline) | Worst-case evidence | Quantified margin | Status |
|-----|--------|-------------------------|---------------------|-------------------|--------|
| KPP-02 build-up p90 | ≤ 15 s | 12.6 s | all jobs | **+16.1% headroom** | **PASS** |
| KPP-03 duration p10 | ≥ 120 s | 160.0 s | burn_hi_4.4: 152.4 s | **+33.3%** (+27.0% tightest sweep) | **PASS** |
| KPP-04 area p10 | ≥ 30 sq ft | ~31 sq ft (1G) | single G baseline | **+3.4%** | **PASS** |
| KPP-06 tri-band | VIS+NIR+MWIR | T ≪ τ | all jobs | **Surrogate saturates** | **PASS*** |
| MOE-01 lock ≥ 60 s | Primary MoE | 100% | adversarial 100% | **Non-discriminative** | **PASS*** |

*KPP-06 and MOE-01 pass is **not binding** — see A-013 in [`rtm/assumption_register.md`](../rtm/assumption_register.md).

**Primary evidence jobs:** `baseline_10M_g3_n10000000` (seed 45), `sweep_burn_hi_4.4_g3_n2000000`, `baseline_10M_adversarial_g3_n10000000`

## Ranked sensitivity — Sobol (duration, 3 grenade)

| Rank | Parameter | ST | S1 | KPP | TRL 3 action |
|------|-----------|-----|-----|-----|--------------|
| 1 | `burn_rate_g_s` | 0.83 | 0.83 | KPP-03 | P0 burn cup |
| 2 | `temp_c` | 0.12 | 0.12 | KPP-03,09 | P0 chamber |
| 3 | `filler_mass_g` | 0.05 | 0.05 | KPP-03 | P0 burn cup |
| — | α bands | <0.001 | ~0 | KPP-06 | P0 spectrometry anyway |
| — | `build_up_time_s` | <0.001 on duration | — | KPP-02 | ST≈1.0 on build-up output |

Full report: [`SOBOL_SENSITIVITY_REPORT.md`](SOBOL_SENSITIVITY_REPORT.md) · Figures: [`figures/duration_sensitivity.png`](figures/duration_sensitivity.png)

## Ranked sensitivity — OAT mega sweeps (duration p10)

| Rank | Sweep | Job ID | Duration p10 | Δ vs nominal |
|------|-------|--------|--------------|--------------|
| 1 | Burn max 4.4 g/s | `sweep_burn_hi_4.4_g3_n2000000` | 152.4 s | −4.7% |
| 2 | Hot 35–50°C | `sweep_temp_hot_g3_n2000000` | 152.9 s | −4.4% |
| 3 | Adversarial stack | `baseline_10M_adversarial_g3_n10000000` | 143.6 s | −10.3% |
| — | Yield / α / VSF | all sweep jobs | ~160 s | no binding change |

## Gaps that remain (cannot close without lab/range)

| Gap | Why it matters | Blocked by |
|-----|----------------|------------|
| MoE surrogate saturation | 100% pass non-discriminative | UAS instrumented test |
| No MS-V α(λ) empirical | KPP-06 pass is literature-only | Spectrometry |
| Throw / deployment | Cloud centering unmodeled | HF range (850 g) |
| Combined plume spatial | Doctrine requires MS-V + smoke | Phase 1B geometry |
| Toxicity / irritation | KPP-11 qualitative | Safety panel |

## Honest external statement

> "Physics-informed sensitivity modeling (140M-sample mega suite + Saltelli Sobol) indicates the MS-V concept meets proposed duration and build-up KPPs under literature-bound parameters, with burn rate and temperature as dominant variance drivers. MoE and tri-band checks saturate in the current surrogate and **require empirical validation**. **Not validated experimentally.**"

## Regeneration

```bash
python -m sim.reproduce
python analysis/generate_verification_matrix.py
python sim/run_sobol.py --n-base 8192 --workers 31
python analysis/summarize_sobol.py
python analysis/generate_figures.py
```

Traceability: [`rtm/verification_matrix.md`](../rtm/verification_matrix.md)
