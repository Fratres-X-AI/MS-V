# MS-V Veil — Multispectral Obscurant Grenade

Hand-thrown. Pin-pull. Squad-layer **drone manipulation** — not another smoke grenade.

MS-V generates a dense **visual + infrared** cloud to break UAS observation when detection, EW, and kinetic layers are degraded, jammed, or saturated. Carried **in addition to** standard signal smoke. Employed as **2–3 MS-V + visual smoke** against FPV and fiber-optic guided drones.

> **Conceptual design — TRL 2.** Proposed targets, not fielded requirements.  
> **Master plan:** [**MasterPlan.md**](MasterPlan.md) · **One-pager:** [Executive Brief](docs/00-executive-brief.md)

**Repository:** https://github.com/Fratres-X-AI/MS-V

---

## Program Status

| | |
|--|--|
| **Maturity** | TRL 2 + local M&S (100k samples) |
| **Today** | RunPod scale — see [RUNPOD.md](RUNPOD.md) |

## Quick Start

```bash
pip install -r requirements.txt
python sim/run_suite_local.py      # 100k local suite
python analysis/summarize_results.py
```

Results: [`analysis/RESULTS_SUMMARY.md`](analysis/RESULTS_SUMMARY.md) · Gap analysis: [`analysis/kpp_gap_analysis.md`](analysis/kpp_gap_analysis.md)

## Why MS-V

1. **Inventory smoke is visual-only** — thermal imagers see through AN-M8 HC.
2. **Vehicle obscurants don't fit the squad** — M56/M58 and ROSY aren't dismounted.
3. **Fiber-optic drones don't jam** — MS-V adds the IR channel standard smoke lacks.

---

## At a Glance

| | AN-M8 | **MS-V Veil** |
|--|-------|---------------|
| Weight | 680 g | **~850 g** |
| Burn | 105–150 s | **120+ s** (dense) |
| Spectrum | VIS | **VIS + NIR + MWIR** |
| Employment | As needed | **2–3 + visual smoke** |

---

## Repository Map

| Path | Purpose |
|------|---------|
| [**MasterPlan.md**](MasterPlan.md) | Phased plan, TRL honesty, local completion status |
| [**RUNPOD.md**](RUNPOD.md) | Scale-up instructions when pod is rented |
| [docs/](docs/) | Concept docs 00–08 |
| [annexes/](annexes/) | Engineering annexes A–E |
| [rtm/](rtm/) | Requirements traceability, decisions, assumptions |
| [models/](models/) | Cloud physics, sensors, system params |
| [sim/](sim/) | Monte Carlo runners |
| [analysis/](analysis/) | Results, risk, cost (Phase 4) |
| [proposals/](proposals/) | SRD, TEMP, SBIR/CSO (Phase 5) |
| [data/](data/baseline_grenades.json) | Baseline specs JSON |

---

## Quick Start (Phase 1)

```bash
pip install -r requirements.txt
python sim/run_monte_carlo.py
```

Output: `analysis/results/monte_carlo_baseline.json` (literature-parameter sensitivity — not validation).

---

## Layered Defense

```
Detect → EW → MS-V + Signal Smoke → Kinetic
```

---

## Sources

[TM 43-0001-29](https://www.militarynewbie.com/wp-content/uploads/2013/11/TM-43-0001-29-Army-Ammunition-Data-Sheets-for-Grenades.pdf) · [FM 3-50 Ch. 7](https://www.globalsecurity.org/military/library/policy/army/fm/3-50/Ch7.htm) · [ECBC bispectral grenade (2014)](https://www.army.mil/article/116366/ecbc_develops_the_u_s_armys_first_bispectral_obscurants_grenade)

