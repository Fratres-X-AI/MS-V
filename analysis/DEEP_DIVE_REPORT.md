# Tail-Risk Deep Dive — High-N Confirmation

> **MATURITY:** Literature-parameter sensitivity — **NOT VALIDATION**
> **Physics:** phase2 · **Sensor:** v6_probabilistic_lock
> **Total samples:** 140,000,000 · **Elapsed:** 155.58s

## Results

| Job | N | Seed | Dur p10 | Dur p50 | MoE lock | Pass |
|-----|---|------|---------|---------|----------|------|
| `adversarial_20M_g3` | 20,000,000 | 999 | 152.3s | 156.7s | 55.1% | YES |
| `burn_worst_seed4099_10M_g3` | 10,000,000 | 4099 | 161.8s | 187.1s | 80.3% | YES |
| `burn_worst_seed137_10M_g3` | 10,000,000 | 137 | 161.8s | 187.1s | 80.3% | YES |
| `burn_worst_50M_g3` | 50,000,000 | 544 | 161.8s | 187.1s | 80.3% | YES |
| `baseline_confirm_50M_g3` | 50,000,000 | 45 | 169.9s | 197.6s | 80.1% | YES |

## Burn-worst seed stability

- **p10 spread across seeds:** 0.01 s (161.8–161.8 s)
- **50M canonical (seed 544):** 161.8 s p10

Tight spread → tail-risk estimate stable at high N.

## Adversarial vs nominal (50M baseline)

- **Nominal MoE:** 80.1% · **Adversarial MoE:** 55.1%
- **Nominal dur p10:** 169.9s · **Adversarial dur p10:** 152.3s

Auto-generated from `analysis/results/deep_dive/manifest.json`.
