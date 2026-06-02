# Defense Projects HQ — MS-V Master Plan

**Program:** MS-V Veil (Multispectral Obscurant Grenade)  
**Repository:** https://github.com/Fratres-X-AI/MS-V  
**Current maturity:** TRL 2 — **Sensitivity study complete** (140M samples, full RTM, partner handoff pack v2.0)  
**Realistic ceiling (internal):** TRL 2–3 — literature-parameter M&S + path to analytical TRL 3 after partner bench/range  
**Last updated:** 2026-06-02

---

## Status Summary

Phase 0 complete. **Phase 1 v3 + phase2/v6 campaign complete** (140M mega suite — KPP pass inside literature bounds only). Phase 1B sensor, geometry, and CONOPS items **delivered via phase2 pipeline** (not a separate active sprint). Partner handoff pack v2.0: proposals, CEL licensing, LinkedIn readiness, v2 KPP form factor.

**Critical:** Sim pass ≠ design confirmation. Gap closure tracked in [`analysis/REMEDIATION_PLAN.md`](analysis/REMEDIATION_PLAN.md) (many items **closed** in-repo; empirical E-1..E-5 remain external).

### What We Can Reach (Cursor + RunPod Python/GPU + GitHub)

- Complete, traceable, physics-informed conceptual design
- Monte Carlo simulation package
- Credible whitepaper, CSO/OTA proposal, or SBIR narrative for **externally funded** prototype work

### What We Cannot Reach Internally

| Cannot do | Why |
|-----------|-----|
| TRL 4+ (breadboard validation in relevant environment) | No lab, range, or hardware |
| Fabricate hardware | No manufacturing capability |
| Live obscurant or sensor testing | No range time |
| Toxicological qualification | No lab access |
| MIL-STD safety certification | No qualification path |
| "Military ready" claims | No empirical backing |

**Any claim beyond a high-quality conceptual + M&S package is false.**

---

## Critical Gaps (Cannot Close Internally)

1. Fill chemistry and aerosol physics (particle size, extinction vs wavelength, burn rate)
2. Empirical validation of cloud density, duration, spectral attenuation
3. Quantitative respiratory irritation / toxicity margins
4. Structural integrity, fuze function, throw accuracy for 7.1 × 3.1 in / ~850 g form factor
5. Access to classified/restricted DoD obscurant program data and threat sensor models
6. Safety certification or environmental qualification path

---

## Phased Plan

### Phase 0 — Audit & Requirements Baseline (1–2 weeks)

**Goal:** Clean, auditable requirements baseline.

| Task | Output |
|------|--------|
| Cross-check docs 01–08 and annexes A–E against cited sources | Audit log |
| Build Requirements Traceability Matrix (RTM) | [`rtm/`](rtm/) |
| Extract Decision Log / Open Trades register | [`rtm/decision_log.md`](rtm/decision_log.md) |

**Gap/Risk:** Unquantified assumptions; potential internal inconsistencies; no independent technical review.

**Maturity after:** Auditable requirements baseline.

---

### Phase 1 — v3 + phase2/v6 COMPLETE

**Goal:** Quantitative KPP sensitivity **within stated uncertainty** — not field validation.

| Task | Output | Status |
|------|--------|--------|
| Cloud physics v3 CL-ramp | [`models/cloud_physics/`](models/cloud_physics/) | Done |
| Mega suite 140M samples (phase2 + v6) | [`analysis/MEGA_SUITE_REPORT.md`](analysis/MEGA_SUITE_REPORT.md) | Done |
| Tail-risk + uncertainty | [`analysis/tail_risk_analysis.md`](analysis/tail_risk_analysis.md), [`rtm/uncertainty_register.md`](rtm/uncertainty_register.md) | Done |
| Sensor stack (FPV + v6 lock-break) | [`models/sensors/`](models/sensors/) · [`INTEGRATION.md`](models/sensors/INTEGRATION.md) | **Done (phase2 path)** |
| Geometry / settling / combined plumes | [`geometry_settling.py`](models/cloud_physics/geometry_settling.py), [`phase2_pipeline.py`](models/cloud_physics/phase2_pipeline.py) | **Done (phase2)** |
| CONOPS kill chain | [`sim/conops/kill_chain.py`](sim/conops/kill_chain.py) | Done |
| Remediation plan | [`analysis/REMEDIATION_PLAN.md`](analysis/REMEDIATION_PLAN.md) | Closed for in-repo items |

**Gap/Risk:** v3-tier MoE could saturate ~100%; **v6 probabilistic lock** reports ~80%/55% nominal/adversarial surrogate lock-met — still **not** field validation (A-013). No empirical fill data.

**Maturity:** Analytical TRL 2–3 characterization; empirical TRL 4 requires partner gates E-1..E-5.

### Delivered vs planned (artifact truth table)

| Artifact | Path | Status |
|----------|------|--------|
| 140M mega manifest | `analysis/results/mega_suite/manifest.json` | **Done** |
| Verification matrix | `rtm/verification_matrix.md` | **Done** |
| Form factor v2 KPP report | `analysis/FORM_FACTOR_REPORT.md` | **Done** (regenerated) |
| SRD / TEMP (expanded) | `proposals/srd/`, `proposals/temp/` | **Done** (review-ready) |
| Partner pack | `proposals/capture-brief.md`, `docs/licensing-and-partnership.md` | **Done** |
| MasterPlan (this file) | `MasterPlan.md` | **Done** (aligned 2026-06-02) |
| Empirical validation JSON | `data/partner_validation_results.json` | **Planned** (template only) |
| Cost model / safety folder | `analysis/cost_model/`, `analysis/safety/` | **Planned** (Phase 4) |
| TRL 4 range data | External partner | **Planned** |

---

### Phase 2 — System Architecture & Digital Representation (2–4 weeks, parallel after Phase 0)

**Goal:** Traceable system architecture with quantified interfaces.

| Task | Output |
|------|--------|
| Component breakdown: body, fill chamber, ports, M201A1 interface | [`models/system/`](models/system/) |
| Parametric geometry for cloud + human-factors models | Geometry params |
| Logistics: carry weight, pouch fit, throw range, training burden | Human-factors notes |

**Gap/Risk:** No structural/ergonomic validation; 25% larger form factor effects unquantified.

---

### Phase 3 — Layered Defense & CONOPS Simulation (3–4 weeks, after Phase 1 core)

**Goal:** Validated CONOPS with measurable effectiveness claims and clear limitations.

| Task | Output |
|------|--------|
| Kill-chain model: detect → EW → MS-V + smoke → kinetic window | [`sim/conops/`](sim/conops/) |
| Quantitative simulation of five use cases ([doc 04](docs/04-conops-use-cases.md)) | MoE distributions |
| Friendly-force degradation (own thermal blinded) | Integration model |

**Gap/Risk:** Surrogate sensor/pilot models only; no real FPV/fiber-optic threat data.

---

### Phase 4 — Risk, Cost, Safety & Producibility (2–3 weeks)

**Goal:** Complete risk register and producibility assessment.

| Task | Output |
|------|--------|
| Expand risk register (likelihood/impact/mitigation) | [`analysis/risk_register.md`](analysis/risk_register.md) |
| Unit cost model vs $75–150 target | [`analysis/cost_model/`](analysis/cost_model/) |
| Fill chemistry from open literature + supply chain | [`analysis/fill_candidates.md`](analysis/fill_candidates.md) |
| Paper toxicity assessment plan + SDS outline | [`analysis/safety/`](analysis/safety/) |
| Manufacturing feasibility (sheet metal, fill loading, fuze compat) | [`analysis/producibility.md`](analysis/producibility.md) |

**Gap/Risk:** No quantitative safety margin; cost target aggressive; no actual safety testing path.

---

### Phase 5 — Artifact Generation & External Engagement (2–4 weeks, ongoing)

**Goal:** Submission-ready conceptual design package with simulation evidence.

| Deliverable | Location |
|-------------|----------|
| System Requirements Document (SRD) | [`proposals/srd/`](proposals/srd/) |
| Verification matrix | [`rtm/verification_matrix.md`](rtm/verification_matrix.md) |
| TEMP outline | [`proposals/temp/`](proposals/temp/) |
| CONOPS (updated with sim evidence) | [`docs/04-conops-use-cases.md`](docs/04-conops-use-cases.md) |
| Assumption register | [`rtm/assumption_register.md`](rtm/assumption_register.md) |
| DIU CSO / OTA / SBIR narrative | [`proposals/`](proposals/) |

**Positioning:** Model-supported concept for **funded prototype development** — not a ready system.

---

## Repository Structure (Target)

```
MS-V/
├── MasterPlan.md              ← this file
├── README.md
├── docs/                      ← concept docs 00–08
├── annexes/                   ← A–E
├── data/                      ← baseline_grenades.json
├── rtm/                       ← traceability, decisions, assumptions
├── models/
│   ├── cloud_physics/         ← extinction, dispersion, settling
│   ├── sensors/               ← FPV, thermal surrogate models
│   └── system/                ← geometry, logistics params
├── sim/                       ← Monte Carlo runners, CONOPS sim
├── analysis/                  ← results, risk, cost, safety
└── proposals/                 ← SRD, TEMP, SBIR/CSO drafts
```

---

## Today's Work Session — Immediate Actions

### Completed locally (2026-05-24)

- [x] Phase 0 audit log — [`rtm/audit_log.md`](rtm/audit_log.md)
- [x] RTM expanded — [`rtm/requirements_traceability.csv`](rtm/requirements_traceability.csv)
- [x] Physics-based cloud model — [`models/cloud_physics/`](models/cloud_physics/)
- [x] Vectorized Monte Carlo engine — [`sim/engine.py`](sim/engine.py)
- [x] Local suite (100k × 4 scenarios) — [`sim/run_suite_local.py`](sim/run_suite_local.py)
- [x] Results summary + charts — [`analysis/RESULTS_SUMMARY.md`](analysis/RESULTS_SUMMARY.md)
- [x] KPP gap analysis — [`analysis/kpp_gap_analysis.md`](analysis/kpp_gap_analysis.md)
- [x] Risk register seed — [`analysis/risk_register.md`](analysis/risk_register.md)
- [x] RunPod handoff — [`RUNPOD.md`](RUNPOD.md)

### RunPod (when rented)

```bash
pip install -r requirements.txt
python sim/run_runpod.py --samples 2000000
python analysis/summarize_results.py
```

See [`RUNPOD.md`](RUNPOD.md).

---

## TRL Roadmap (Honest)

| TRL | Description | MS-V status |
|-----|-------------|-------------|
| 1 | Basic principles observed | **Complete** (literature + concept) |
| 2 | Technology concept formulated | **Current** (140M sensitivity study complete) |
| 3 | Analytical/experimental critical function proof | **Target** — path defined below |
| 4 | Component validation in lab environment | **Requires external funding + lab** |
| 5+ | Relevant environment / fielded | **Out of scope internally** |

---

## Path to Validation (TRL 3 Test Plan)

Sensitivity data from the 140M mega suite **dictates** physical test priority — not marketing claims.

### High-risk variables (OAT ranking)

| Rank | Variable | Simulation signal | TRL 3 action |
|------|----------|-------------------|--------------|
| 1 | Burn rate upper bound | `sweep_burn_hi_4.4` — duration p10 +27.0% margin (tightest binding) | Burn cup gravimetric across 2.9–4.4 g/s |
| 2 | Hot temperature (35–50 °C) | `sweep_temp_hot` — −7 s vs nominal at p10 | Chamber burn tests at temperature extremes |
| 3 | Adversarial stack | `baseline_10M_adversarial` — +19.7% margin at p10 | Combined worst-case T/RH/wind/burn |
| — | Humidity > 75% RH | Low OAT on duration; yield penalty modeled | Chamber RH sweeps (P1) |
| — | α(λ) sweeps | **Non-binding** in surrogate — **does not reduce spectrometry priority** | P0 spectrometer still required (A-013) |

### Explicit non-claims

- v3-era **~100% MoE pass** is **surrogate saturation**; v6 reports **spread** (~80%/55%) — still not lock-break confirmation.
- KPP-06 tri-band pass is **non-discriminative** until α(λ) is measured on MS-V fill.
- Sim pass inside literature bounds ≠ design confirmation.

### Artifacts for reviewers

| Artifact | Location |
|----------|----------|
| Verification matrix (38 jobs, quantified margins) | [`rtm/verification_matrix.md`](rtm/verification_matrix.md) |
| Assumption register (OAT ranks, KPP impact) | [`rtm/assumption_register.md`](rtm/assumption_register.md) |
| Seed manifest | [`sim/config/seeds.yaml`](sim/config/seeds.yaml) |
| One-step reproduce | [`run_all.sh`](run_all.sh) · `make reproduce` |
| TEMP outline | [`proposals/temp/MS-V-TEMP-outline.md`](proposals/temp/MS-V-TEMP-outline.md) |
| SRD draft | [`proposals/srd/MS-V-SRD.md`](proposals/srd/MS-V-SRD.md) |

---

## Key Document Index

| Doc | Purpose |
|-----|---------|
| [Executive Brief](docs/00-executive-brief.md) | External one-pager |
| [Concept](docs/01-concept-overview.md) | Problem and philosophy |
| [Requirements](docs/02-operational-requirements.md) | KPPs and MoE |
| [Limitations](docs/07-limitations-and-risks.md) | What we won't claim |
| [Annex B — KPPs](annexes/B-kpp-targets.md) | Verification targets |
| [Annex D — Spectrum](annexes/D-spectrum-and-cloud-model.md) | Bands and cloud phases |

---

## Governance

- **No "military ready" language** in any external artifact without TRL 4+ evidence
- **All sim outputs** labeled: literature-parameter sensitivity study, not validation
- **MoE claims** require combined MS-V + visual smoke in model and doctrine
- **Version control** all params, assumptions, and results under `/rtm/` and `/analysis/`

---

## Claim → Evidence Cross-Reference

| External claim | Evidence artifact | Job / method |
|----------------|-------------------|--------------|
| Duration ≥ 120 s (p10) | `rtm/verification_matrix.md` | `baseline_10M_g3_n10000000` |
| Burn rate drives duration variance | `analysis/SOBOL_SENSITIVITY_REPORT.md` | Sobol ST(burn)≈0.83 |
| 38/38 jobs KPP-pass (literature bounds) | `analysis/MEGA_SUITE_REPORT.md` | 140M mega suite |
| Adversarial tail margin +19.7% | `analysis/tail_risk_analysis.md` | `baseline_10M_adversarial_g3` |
| MoE v6 lock-met spread | `rtm/assumption_register.md` A-013 | **Planning surrogate — not validation** |
| Reproducible baseline stats | `python -m sim.reproduce` | `analysis/reproduce_golden.json` |
| TRL 3 test priority | `proposals/temp/MS-V-TEMP-outline.md` | Sobol + OAT ranked |
| Requirements mapping | `rtm/requirements_traceability.csv` | per-row job provenance |

**RunPod 140M campaign spec:** 32 vCPU pod (213.173.107.24) · 31 workers · ~9 s wall time.  
**Current pod (Sobol refresh):** 256 vCPU · 2 TiB RAM · `91.199.227.82:40566` · see `RUNPOD.md`.
