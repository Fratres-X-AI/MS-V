# MS-V Remediation Plan — Closing Phase 1 Gaps

**Status:** **Closed (in-repo)** — empirical gates E-1..E-5 remain external  
**Last updated:** 2026-06-02  
**Gap closure:** 2026-06-02 plan delivered (form factor v2, SRD/TEMP, phase2 sensors, CI guards, MasterPlan align). See [`MasterPlan.md`](../MasterPlan.md) delivered-vs-planned table.  
**Scope:** Address documented weaknesses in M&S maturity, interpretation risk, and path to TRL 3+  
**Principle:** Fix with rigor — never trade honesty for green checks.

---

## Problem Statement

The 140M-sample mega suite shows **all KPP checks pass** inside **literature-derived parameter bounds**. That result is **conditional sensitivity analysis**, not design validation. External reviewers correctly flag:

- No empirical fill/aerosol data for the unified bispectral ~850 g form factor
- Surrogate Beer-Lambert + scalar thresholds — not FPV/thermal sensor curves
- No cloud geometry, settling, or MS-V + visual smoke plume interaction model
- Human factors (throw, load, deployment) outside Monte Carlo scope
- Risk of over-interpreting pass rates as confirmation

This plan maps each gap to **work packages**, **deliverables**, **owners**, and **exit criteria** before Phase 3 CONOPS or external claims.

---

## Gap → Fix Matrix

| # | Weakness / Risk | Root cause | Work package | Deliverable | Phase |
|---|-----------------|------------|--------------|-------------|-------|
| W1 | No empirical aerosol physics | Internal TRL ceiling; no lab | **1B-1** Fill physics charter + external test plan | `analysis/fill_physics_test_plan.md` | 1B → external |
| W2 | No sensor transmittance curves | Surrogate only in `surrogate_sensors.py` | **1B-2** FPV + thermal sensor models | `models/sensors/fpv_thermal.py`, sensor MC jobs | 1B |
| W3 | No cloud geometry / settling / combined plumes | Phase 1 CL lumped model | **1B-3** Geometry + settling module | `models/cloud_physics/geometry_settling.py` | 1B |
| W4 | Form factor / throw / load unmodeled | Phase 2 not started | **2-1** Human-factors + deployment params | `models/system/human_factors.yaml`, throw model | 2 |
| R1 | Over-interpreting “all pass” | Labeling + interpretation | **GOV-1** Mandatory disclaimer block on all outputs | RTM + README + sim manifest | 0 |
| R2 | Wide unquantified input uncertainty | Assumption register sparse | **1B-4** Uncertainty register from mega suite | `rtm/uncertainty_register.md` | 1B |
| R3 | No TRL 3+ path without lab | Funding / access | **EXT-1** Funded prototype gate document | `proposals/trl_gate_external.md` | 5 |
| R4 | Repo bloat from raw JSON | Policy missing | **GOV-2** Results data policy + gitignore | `analysis/RESULTS_DATA_POLICY.md` | 0 |

---

## Work Packages (Detailed)

### Phase 1B — Complete M&S Before Phase 3 (4–6 weeks)

**Goal:** Reach honest **TRL 3 analytical proof** — “critical functions characterized with stated uncertainty,” not “design confirmed.”

#### 1B-1 — Fill & Aerosol Physics Charter (external gate)

| Task | Action |
|------|--------|
| Document required measurements | α(λ) VIS/NIR/MWIR, PSD, bulk density, burn rate vs T/RH, yield |
| Map to ECBC bispectral metrics | Annex B test framework alignment |
| Define down-select criteria | Pass/fail for fill candidates vs KPP-03/06 |
| Identify lab partners | ECBC, university combustion lab, or CSO performer |

**Deliverable:** `analysis/fill_physics_test_plan.md`  
**Exit:** Signed test plan ready for funded SOW — **cannot close internally**

#### 1B-2 — Sensor Degradation Models (FPV + Thermal)

Replace scalar threshold checks with band-limited sensor response:

| Component | Model |
|-----------|--------|
| FPV visible | CMOS response 400–700 nm × α(λ) integration; optional AGC saturation |
| Uncooled thermal | 8–14 µm band; NETD-degraded contrast vs transmittance |
| Cooled thermal | 3–5 µm MWIR path (primary MS-V band) |
| Fiber-optic link | Conservative: fused VIS+MWIR AND (not RF) |
| MoE threshold | Target contrast / SNR margin, not single τ = 0.15 |

**Tasks:**
1. Fix `surrogate_sensors.py` (broken `t_vis` reference) → deprecate in favor of new module
2. Implement `models/sensors/fpv_thermal.py` with configurable curves in `models/sensors/params.yaml`
3. Add `sim/run_sensor_jobs.py` — RunPod-targeted degradation sweeps
4. Wire optional sensor path in `sim/engine.py` (`model_version: phase1_v4_sensor`)

**Exit:** MoE fraction varies with yield/alpha sweeps (no longer saturated 100%); documented degradation curves in RTM

#### 1B-3 — Cloud Geometry, Settling, Combined Plumes

| Task | Model addition |
|------|----------------|
| Time-varying cloud height/width | Annex D phase timeline → parametric growth |
| Settling depletion | `particle.settling_velocity_m_s` → CL decay post-peak |
| Multi-grenade plume interaction | Overlap efficiency → spatial correlation (not just area scale) |
| Visual smoke partner | Separate HC plume superposition (VIS boost, not duration multiplier) |

**Deliverable:** `models/cloud_physics/geometry_settling.py`, updated `params.yaml`  
**Exit:** Duration and MoE respond to geometry stress cases; wind sensitivity on **geometry** not burn clock alone

#### 1B-4 — Quantitative Uncertainty Register

Populate from mega suite + literature:

| Parameter | Current bounds | Mega-suite sensitivity | Confidence |
|-----------|----------------|------------------------|------------|
| burn_rate_g_s max | 4.2 | **High** — 4.4 → 152 s p10 | LOW (no cal) |
| yield_factor | 0.22–0.52 | **Low** in current model (saturates) | LOW |
| α MWIR | 2–9 m²/g | **Low** until sensor v4 | MEDIUM (literature) |
| visual_smoke_factor | 1.3 ± sweep | **Low** on duration | LOW (UNVALIDATED) |
| temp coupling | ±0.2%/°C | **Medium** — hot bin −7 s p10 | LOW |

**Deliverables:** `rtm/uncertainty_register.md`, `analysis/tail_risk_analysis.md` (automated)  
**Exit:** Every KPP has ranked uncertainty driver + external measurement needed

#### 1B-5 — Tail-Risk & Margin Analysis (freeze artifact)

| Task | Output |
|------|--------|
| Run `analysis/analyze_tail_risk.py` on each mega campaign | `tail_risk_analysis.md` |
| Add p1 estimates (MC) where sample size allows | Extend engine to emit percentiles 1/5/10 |
| Document break points | Burn rate / temp / yield where KPP-03 fails |
| Adversarial + **beyond-envelope** cases | Cases outside params.yaml (explicit FAIL expected) |

**Exit:** `analysis/kpp_gap_analysis.md` references tail-risk ranks; no “all pass” without disclaimer

---

### Phase 2 — System & Human Factors (parallel, 2–4 weeks)

#### 2-1 — Form Factor, Throw, Load

| Task | Deliverable |
|------|-------------|
| Parametric geometry | Extend `models/system/geometry.md` → YAML |
| Throw range model | Mass 850 g, stress throw distribution (literature grenade HF) |
| Soldier load | 1–2 MS-V + standard smoke weight budget |
| Pouch / carry | Qualitative fit assessment vs ALICE/FLC |

**Deliverable:** `models/system/human_factors.yaml`, `analysis/human_factors_notes.md`  
**Exit:** KPP-08 throw range has M&S basis (still UNVALIDATED until range test)

#### 2-2 — Deployment Dynamics (Monte Carlo extension)

Optional Phase 2.5: employment error (throw scatter, wind misjudgment, late fuze) → CONOPS input distributions for Phase 3.

---

### Phase 3 — CONOPS Simulation (after 1B freeze)

**Prerequisite:** Phase 1B exit criteria met — sensor + geometry paths live, uncertainty register populated.

| Task | Deliverable |
|------|-------------|
| `sim/conops/kill_chain.py` | Timeline MC for 5 use cases (doc 04) |
| Sample from Phase 1B distributions | Build-up, duration, MoE per employment |
| Friendly-force degradation | Own thermal blinded window |
| MoE vs use case | CASEVAC, break contact, exfil metrics |

**Exit:** CONOPS doc updated with simulated windows + limitations section

---

### Governance & Repo Hygiene

#### GOV-1 — Interpretation Controls

- All JSON manifests: `"study_type": "literature_parameter_sensitivity"`
- README + executive brief: **“Pass = within assumed bounds, not field confirmation”**
- Proposals: mandatory uncertainty paragraph from `uncertainty_register.md`

#### GOV-2 — Results Data Policy

See [`analysis/RESULTS_DATA_POLICY.md`](RESULTS_DATA_POLICY.md).

**Immediate action:** gitignore raw per-job JSON above local profile; retain manifest + summary + reports in git; archive bulk to release assets or external storage.

---

### External Path — TRL 3+ (cannot close in Cursor)

| TRL | Requirement | MS-V action |
|-----|-------------|-------------|
| 3 | Analytical/experimental critical function proof | Phase 1B complete + **limited lab** (burn cup, α bench) |
| 4 | Component validation relevant environment | Range test: 2–3 grenade + smoke vs surrogate UAS |
| 5+ | Field relevance | Government partner / SBIR Phase II |

**Deliverable:** `proposals/trl_gate_external.md` — budget, facility, metrics, schedule

---

## Recommended Execution Order

```
Week 1–2:  GOV-2 repo policy | 1B-4 uncertainty register | 1B-5 tail-risk | fix sensor stub
Week 2–4:  1B-2 sensor models + sensor MC jobs
Week 3–5:  1B-3 geometry/settling/combined plume
Week 4–6:  2-1 human factors | 1B-1 fill test plan draft
Week 6:    PHASE 1B FREEZE REVIEW → go/no-go Phase 3
Week 7–10: Phase 3 CONOPS (if freeze approved)
Ongoing:   EXT-1 proposal package for funded lab/range
```

---

## Phase 1B Freeze Criteria (Go / No-Go Phase 3)

| Criterion | Required state |
|-----------|----------------|
| Sensor model v4 | FPV + uncooled + cooled paths; MoE not saturated at 100% |
| Geometry/settling | Coupled to duration or MoE in ≥1 stress scenario |
| Uncertainty register | All KPP inputs have bounds + sensitivity rank + cal need |
| Tail-risk doc | Published; tightest margin and break points documented |
| Disclaimer | On every artifact; external brief updated |
| Repo policy | Raw JSON policy enforced |
| RTM | KPP-02/03/04/MoE trace to v4 model refs |

**No-go:** Proceeding to Phase 3 on v3 CL-ramp alone — CONOPS would inherit false confidence.

---

## Immediate Actions (This Sprint)

- [x] `analysis/REMEDIATION_PLAN.md` (this document)
- [x] `analysis/analyze_tail_risk.py` → `analysis/tail_risk_analysis.md`
- [x] `rtm/uncertainty_register.md`
- [x] `analysis/RESULTS_DATA_POLICY.md`
- [x] `models/sensors/fpv_thermal.py` + `lock_break.py` + [`INTEGRATION.md`](../models/sensors/INTEGRATION.md)
- [x] Phase2 geometry / microphysics / deployment — [`phase2_pipeline.py`](../models/cloud_physics/phase2_pipeline.py)
- [x] `MasterPlan.md` aligned (phase2 campaign, v6 MoE framing)
- [x] Form factor v2 KPP — [`FORM_FACTOR_REPORT.md`](FORM_FACTOR_REPORT.md), [`models/system/kinematics.py`](../models/system/kinematics.py)
- [x] Proposals SRD/TEMP expanded; CI validate-only + golden manifest tests
- [ ] Empirical E-1..E-5 — **external partner only**

---

## Decision: Freeze vs Phase 3

| Option | When | Recommendation |
|--------|------|----------------|
| **A — Complete Phase 1B first** | Sensor + geometry + uncertainty done | **Recommended** — addresses all reviewer gaps analytically |
| **B — Phase 3 now on v3 distributions** | Need CONOPS narrative fast | Accept explicit “surrogate only” limitation; do not claim KPP confirmation |
| **C — External lab first** | Funding available | Parallel to 1B; empirical data feeds v5 model |

**Program recommendation:** **Option A** — 4–6 weeks internal, then Phase 3 with defensible MoE distributions.

---

## Traceability

| Document | Role |
|----------|------|
| [MasterPlan.md](../MasterPlan.md) | Program phases |
| [kpp_gap_analysis.md](kpp_gap_analysis.md) | Current KPP vs model |
| [tail_risk_analysis.md](tail_risk_analysis.md) | Parameter rankings |
| [MEGA_SUITE_REPORT.md](MEGA_SUITE_REPORT.md) | 140M campaign summary |
| [rtm/uncertainty_register.md](../rtm/uncertainty_register.md) | Quantified bounds |
| [rtm/assumption_register.md](../rtm/assumption_register.md) | Assumption status |
| [risk_register.md](risk_register.md) | R-07, R-08, R-09 mitigation |
