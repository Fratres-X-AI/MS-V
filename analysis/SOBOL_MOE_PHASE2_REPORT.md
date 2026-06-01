# MoE Sobol Report — Phase2 + v6 Probabilistic Lock

> **MATURITY:** Literature-parameter sensitivity — **NOT VALIDATION**
> **Engine:** Saltelli + Sobol (SALib) on phase2_v1_full_physics + v6_probabilistic_lock
> **Saltelli N=8,192** · **MC per row=5,000** · evaluations=114,688 · workers=31

## MOE-01 lock-break fraction — ranked by ST

- Y mean=0.800 p10=0.790 p50=0.800 p90=0.811

| Rank | Parameter | S1 | ST |
|------|-----------|-----|-----|
| 1 | `burn_rate_g_s` | 0.2780 | 0.7748 |
| 2 | `alpha_mwir` | 0.0885 | 0.6164 |
| 3 | `humidity_rh` | 0.0769 | 0.5826 |
| 4 | `temp_c` | 0.0535 | 0.5728 |
| 5 | `filler_mass_g` | 0.0151 | 0.5214 |
| 6 | `alpha_vis` | -0.0007 | 0.5108 |

Unlike v4 lumped Sobol, this campaign uses **full phase2 physics + v6 probabilistic lock-break**.

Auto-generated from `analysis/results/sobol_moe_phase2/sobol_moe_phase2_results.json`.
