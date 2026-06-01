# Simulation

Phase 1 Monte Carlo and Phase 3 CONOPS simulation.

| Script | Purpose |
|--------|---------|
| [run_monte_carlo.py](run_monte_carlo.py) | Baseline KPP/MoE sensitivity study |
| `conops/` | Kill-chain and use-case sim (Phase 3) |

## Run

```bash
pip install -r requirements.txt
python sim/run_monte_carlo.py
```

Output: [`analysis/results/monte_carlo_baseline.json`](../analysis/results/monte_carlo_baseline.json)

**All outputs labeled sensitivity studies — not validation.**
