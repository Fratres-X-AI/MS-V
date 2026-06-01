# MS-V Veil — Multispectral Obscurant Grenade

Hand-thrown. Pin-pull. Squad-layer **drone manipulation** — not another smoke grenade.

MS-V generates a dense **visual + infrared** cloud to break UAS observation when detection, EW, and kinetic layers are degraded, jammed, or saturated. Carried **in addition to** standard signal smoke. Employed as **2–3 MS-V + visual smoke** against FPV and fiber-optic guided drones.

> **Conceptual design — TRL 2.** Literature-parameter sensitivity study complete (140M samples). **NOT validation.**  
> **Master plan:** [**MasterPlan.md**](MasterPlan.md) · **One-pager:** [Executive Brief](docs/00-executive-brief.md)

**Repository:** https://github.com/Fratres-X-AI/MS-V

---

## Program Status

| | |
|--|--|
| **Maturity** | TRL 2 — Sensitivity Study Complete (38 jobs, 140M samples) |
| **Evidence** | [`analysis/MEGA_SUITE_REPORT.md`](analysis/MEGA_SUITE_REPORT.md) · [`rtm/verification_matrix.md`](rtm/verification_matrix.md) |
| **Reproduce** | `bash one_pass.sh` or `make one-pass` (RunPod/local) |

## Quick Start

```bash
pip install -r requirements-lock.txt
python -m sim.reproduce              # golden checksum gate
python sim/run_suite_local.py        # 100k local suite
python sim/run_mega_suite.py --quick # CI-scale mega smoke test
python analysis/generate_verification_matrix.py
```

Full campaign: see [RUNPOD.md](RUNPOD.md) · Seeds: [`sim/config/seeds.yaml`](sim/config/seeds.yaml)

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
| [**MasterPlan.md**](MasterPlan.md) | Phased plan, TRL 3 path, governance |
| [**RUNPOD.md**](RUNPOD.md) | Scale-up + one-step `run_all.sh` |
| [**rtm/verification_matrix.md**](rtm/verification_matrix.md) | KPP/MoE ↔ 38 job IDs with margins |
| [**rtm/assumption_register.md**](rtm/assumption_register.md) | Literature bounds + OAT sensitivity |
| [docs/](docs/) | Concept docs 00–08 |
| [annexes/](annexes/) | Engineering annexes A–F (incl. form factor) |
| [models/](models/) | Cloud physics, sensors, validation |
| [sim/](sim/) | Monte Carlo runners, seed manifest |
| [**analysis/CONOPS_REPORT.md**](analysis/CONOPS_REPORT.md) | Five use cases — Phase 1B windows + hardened MoE |
| [**analysis/FORM_FACTOR_REPORT.md**](analysis/FORM_FACTOR_REPORT.md) | Tier B parametric envelope, pouch fit, STL |
| [**annexes/F-form-factor-and-ergonomics.md**](annexes/F-form-factor-and-ergonomics.md) | One-page form-factor annex |
| [proposals/](proposals/) | SRD, TEMP outline |

---

## Reviewer Audit Trail (2-minute lookup)

| Step | Artifact | Command |
|------|----------|---------|
| 1 | Requirement → job → margin | `rtm/verification_matrix.md` |
| 2 | Assumption → Sobol rank → TRL 3 test | `rtm/assumption_register.md` |
| 3 | Global sensitivity (Saltelli) | `analysis/SOBOL_SENSITIVITY_REPORT.md` |
| 4 | Reproduce statistics | `make reproduce` or `python -m sim.reproduce` |
| 5 | Known MoE gap | A-013 in assumption register |

**Dominant finding:** Sobol ST ≈ 0.83 on `burn_rate_g_s` for KPP-03 duration — TRL 3 must prioritize burn cup testing.

---

## Layered Defense

```
Detect → EW → MS-V + smoke → kinetic window
```

See [CONOPS](docs/04-conops-use-cases.md) · [Limitations](docs/07-limitations-and-risks.md)
