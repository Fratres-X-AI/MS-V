# System Requirements Document (SRD) — MS-V Veil

> **Status:** Draft for DIU/OTA/SBIR submission package  
> **Maturity:** TRL 2–3 literature-parameter sensitivity study — **NOT field validation**  
> **Evidence:** [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) · [`analysis/MEGA_SUITE_REPORT.md`](../analysis/MEGA_SUITE_REPORT.md)

## 1. Purpose

Define operational requirements for the MS-V multispectral obscurant grenade and map each requirement to M&S evidence or planned TRL 3/4 verification.

## 2. Scope

In scope: squad-layer obscuration against FPV and thermal UAS when combined with standard visual smoke.  
Out of scope: RF defeat, standalone employment without visual smoke, vehicle-mounted systems.

## 3. Requirements traceability summary

| ID | Type | M&S status | Matrix row | Empirical gate |
|----|------|------------|------------|----------------|
| KPP-01 | Mass ~850 g | DESIGN_AUTHORITY | KPP-01 | E-3 |
| KPP-02 | Build-up ≤ 15 s p90 | SENSITIVITY_PASS | KPP-02 | 2A / chamber |
| KPP-03 | Duration ≥ 120 s p10 | SENSITIVITY_PASS | KPP-03 | E-1 / 2A |
| KPP-04 | Screening 30–40 sq ft | SENSITIVITY_PASS | KPP-04 | 2A / lidar |
| KPP-05 | Group 2–3 grenades | SENSITIVITY_PASS | KPP-05 | doctrine |
| KPP-06 | VIS+NIR+MWIR | SENSITIVITY_PASS* | KPP-06 | E-1 / 2B |
| KPP-07 | Fuze 0.7–2.0 s | SENSITIVITY_PASS | KPP-07 | P2 fuze test |
| KPP-08 | Throw ≥ 20 m p10 | SENSITIVITY_PASS | KPP-08 | E-2 / 2C |
| KPP-09 | 7.1×3.1 in envelope | DESIGN_AUTHORITY | KPP-09 | E-3 |
| KPP-10 | −20 to +50 °C | SENSITIVITY_PASS | KPP-10 | E-5 / 2E |
| KPP-11 | ≤ 15 mph wind | SENSITIVITY_PASS | KPP-11 | range |
| KPP-12 | Respiratory acceptable | UNVERIFIED | KPP-12 | E-1 tox |
| KPP-13 | Cost $75–150 | PLANNED | KPP-13 | Phase 4 |
| KPP-14 | 1–2 per soldier | Doctrine | KPP-14 | logistics |
| MOE-01 | Lock-break ≥ 60 s | SENSITIVITY_PASS* | MOE-01 | E-4 / 2D |
| MOE-02 | CASEVAC window | SENSITIVITY_PASS | MOE-02 | CONOPS MC |

\*Check `surrogate_saturated` on job JSON; tri-band/MoE non-discriminative when true (A-013).

Full matrix: [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) · CSV: [`rtm/requirements_traceability.csv`](../rtm/requirements_traceability.csv)

### 3.1 Primary M&S job mapping (140M campaign)

Authoritative observed values and margins: **matrix only**. Table below is navigation — not a second source of truth.

| Req | Primary job ID | Seed | Matrix pass | Saturation caveat |
|-----|----------------|------|-------------|-------------------|
| KPP-02 | `baseline_10M_g3_n10000000` | 45 | YES | — |
| KPP-03 | `baseline_10M_g3_n10000000` | 45 | YES | Duration not fill-validated |
| KPP-04 | `baseline_10M_g1_n10000000` | 43 | YES | Single-grenade geometry |
| KPP-05 | `baseline_10M_g2_*`; `baseline_10M_g3_*` | 44; 45 | YES | Doctrine |
| KPP-06 | `baseline_10M_g3_n10000000` | 45 | YES* | Check `surrogate_saturated` in job JSON |
| KPP-07 | `baseline_10M_g3_n10000000` | 45 | YES | Fuze model, not lot test |
| KPP-08 | `baseline_10M_g3_n10000000` | 45 | YES | MC throw — gate **2C** required |
| KPP-10 | `sweep_temp_hot_g3_n2000000` (tightest) | 735 | YES | Chamber confirmation E-5 |
| KPP-11 | `baseline_10M_wind_high_g3_n10000000` | 208 | YES | Wind not duration-binding in campaign |
| MOE-01 | `baseline_10M_g3_n10000000` | 45 | YES* | **A-013:** ~80% lock-met fraction — not field MoE |
| MOE-01 stress | `baseline_10M_adversarial_g3_n10000000` | 999 | YES* | Adversarial ~55% lock-met — still surrogate |
| MOE-02 | CONOPS (`sim/run_conops.py`) | — | YES | Scenario MC — [`CONOPS_REPORT`](../analysis/CONOPS_REPORT.md) |
| KPP-01, KPP-09 | `N/A (design authority)` | — | YES | `models/system/form_factor.yaml` `v2_kpp` |
| KPP-12, KPP-13 | `N/A` | — | **NO** / PLANNED | External only |

\*When `surrogate_saturated=true`, treat MoE/tri-band row as **non-discriminative** per matrix header and A-013.

## 4. Key Performance Parameters

| ID | Requirement | M&S Status | Verification Path |
|----|-------------|------------|-------------------|
| KPP-01 | Mass ~850 g | **Design authority** — form_factor.yaml | Prototype weigh-off |
| KPP-02 | Build-up ≤ 15 s (p90) | **Sensitivity pass** — mega suite phase2 | High-speed video, chamber |
| KPP-03 | Duration ≥ 120 s (p10) | **Sensitivity pass** — burn/temp sweeps | Burn cup vs T/RH |
| KPP-04 | Screening 30–40 sq ft | **Sensitivity pass** — single grenade p10 | Lidar / geometry |
| KPP-05 | Group 2–3 grenades | **Sensitivity pass** — g2/g3 jobs + CONOPS | Doctrine / range |
| KPP-06 | VIS + NIR + MWIR | **Check surrogate_saturated flag** | Spectrometer α(λ) |
| KPP-07 | Fuze M201A1 0.7–2.0 s | **MC pass** — deployment_kinematics | Fuze lot test |
| KPP-08 | Throw ≥ 20 m (p10 stressed) | **MC pass** — human_factors | Loaded throw range |
| KPP-09 | Form factor 7.1×3.1 in | **Design authority** — Annex F | Engineering drawing |
| KPP-10 | −20 to +50 °C | **Sensitivity pass** — sweep_temp_* | Environmental chamber |
| KPP-11 | ≤ 15 mph wind | **Sensitivity pass** — wind baselines | Range plume |
| KPP-12 | Respiratory acceptable | **UNVERIFIED** | Toxicology panel |
| KPP-13 | Cost $75–150 | **PLANNED** | Manufacturing study |
| KPP-14 | 1–2 per soldier | **Doctrine** — Annex B | Logistics |

## 5. Measures of Effectiveness

| ID | Requirement | M&S Status | Verification Path |
|----|-------------|------------|-------------------|
| MOE-01 | Fused EO/IR lock-break ≥ 60 s | **v6 probabilistic** — see saturation flag | UAS surrogate range test |
| MOE-02 | CASEVAC T+15–135 s window | **CONOPS MC** | [`analysis/CONOPS_REPORT.md`](../analysis/CONOPS_REPORT.md) |

## 6. Known Limitations (mandatory disclosure)

### 6.1 What this SRD is not

- **Not** a validated system specification, ICD, or type-classified munition data package.
- **Not** evidence of field performance, procurement readiness, or safety certification.
- **Not** a substitute for [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) — that file is the quantitative authority for M&S pass/fail rows.

### 6.2 Technical limitations (traceable)

| Limitation | RTM / doc | External claim |
|------------|-----------|----------------|
| No MS-V fill empirical α(λ), burn rate, PSD, or tox | A-001..A-010; matrix KPP-12 **NO** | None beyond “planned test” |
| Literature-parameter MC only | Matrix header; LIM-03 | “Model-supported under stated assumptions” |
| `surrogate_saturated=true` → MoE/tri-band non-discriminative | A-013; matrix note | **Never** cite pass % as defeat rate |
| v6 lock-met ~80% / ~55% = **planning surrogate** only | MOE-01 row; A-013, A-027 | Directional planning only — requires gate **2D** |
| Form factor 850 g / 7.1×3.1 in = **design authority**, not weighed prototype | KPP-01, KPP-09; `form_factor.yaml` | “Concept envelope” — gate E-3 |
| Throw KPP-08 = MC + human_factors model, not range data | KPP-08 job; E-2 | “Model-bound” until gate **2C** |
| Requires visual smoke (not standalone) | LIM-01 | Doctrine only |
| No RF defeat | LIM-02 | Obscuration path only |

### 6.3 Forbidden language (external communications, briefings, capture)

Do **not** use: validated, proven, field-tested, military-ready, defeats drones, 100% MoE, MIT open source, Phase 2 **validated** physics.

Do use: literature-parameter sensitivity study, concept visualization, planning surrogate, CEL evaluation access, v2 KPP design authority.

### 6.4 Sim pass ≠ design confirmation

A **YES** in [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) means the requirement was met inside **stated literature bounds** for the cited job ID — not that the hardware will perform so in theater.

## 7. Traceability (artifacts)

Full matrix: [`rtm/requirements_traceability.csv`](../rtm/requirements_traceability.csv)  
Assumptions: [`rtm/assumption_register.md`](../rtm/assumption_register.md)  
Seeds: [`sim/config/seeds.yaml`](../sim/config/seeds.yaml)  
TRL gate: [`proposals/trl_gate_external.md`](../trl_gate_external.md)  
Reproduce: [`REPRODUCE.md`](../REPRODUCE.md)

## 8. Verification status legend

Statuses in this document match [`rtm/verification_matrix.md`](../rtm/verification_matrix.md):

| Status | Meaning | External claim allowed |
|--------|---------|------------------------|
| **DESIGN_AUTHORITY** | Fixed by `form_factor.yaml` / engineering envelope — not Monte Carlo | Mass, dimensions, fuze interface |
| **SENSITIVITY_PASS** | Requirement met in ≥90% of literature-bound MC runs (phase2/v6 campaign) | “Model-supported under stated assumptions” |
| **UNVERIFIED** | No empirical MS-V data; literature or placeholder only | None beyond “planned test” |
| **PLANNED** | Test defined in TEMP / TRL gate; not executed | Schedule only |

When `surrogate_saturated=true` on a run, tri-band / MoE rows are **non-discriminative** (A-013) — do not cite pass rate as field lock-break.

## 9. M&S evidence summary

| Campaign | Scale | Physics tier | Sensor stack | Primary artifacts |
|----------|-------|--------------|--------------|-------------------|
| Mega suite v6 | **140M** MC draws (committed manifest) | **phase2** — PSD, settling, humidity growth, multi-grenade structure | `fpv_thermal`, `lock_break`, `degradation` in [`sim/engine.py`](../sim/engine.py) | [`analysis/MEGA_SUITE_REPORT.md`](../analysis/MEGA_SUITE_REPORT.md), [`analysis/results/mega_suite/manifest.json`](../analysis/results/mega_suite/manifest.json) |
| CONOPS kill chain | Scenario MC | Same phase2 path via [`sim/conops/kill_chain.py`](../sim/conops/kill_chain.py) | Fused EO/IR surrogate | [`analysis/CONOPS_REPORT.md`](../analysis/CONOPS_REPORT.md) |
| Sobol | Global sensitivity | Literature-bound parameters | N/A | [`analysis/SOBOL_SENSITIVITY_REPORT.md`](../analysis/SOBOL_SENSITIVITY_REPORT.md) |
| Form factor | Throw MC (KPP-08) | [`models/system/kinematics.py`](../models/system/kinematics.py) | N/A | [`analysis/FORM_FACTOR_REPORT.md`](../analysis/FORM_FACTOR_REPORT.md) |

**MoE framing (conservative):** v6 probabilistic lock reports ~**80%** nominal / ~**55%** adversarial **surrogate lock-met fraction** — planning surrogate only, not UAS defeat rate. See assumption **A-013** in [`rtm/assumption_register.md`](../rtm/assumption_register.md).

**Reproduce:** `python -m sim.reproduce` (golden profile v4) · [`REPRODUCE.md`](../REPRODUCE.md)

## 10. Empirical gaps matrix

Maps external TRL gates E-1..E-5 ([`trl_gate_external.md`](../trl_gate_external.md)) to open evidence:

| Gap ID | Closes KPP/MOE | Current M&S | Required empirical | Partner gate |
|--------|----------------|-------------|-------------------|--------------|
| **E-1** | KPP-03, KPP-06, KPP-12 | Burn/yield/α(λ) sensitivity only | Fill bench: burn cup, spectrometry, tox panel | **2A**, **2B** ([DOC-11](../docs/11-partner-validation-and-trl-gates.md)) |
| **E-2** | KPP-08 | MC throw p10 ≥ 20 m (stressed) | n≥30 loaded throw range | **2C** |
| **E-3** | KPP-01, KPP-09 | Design authority envelope | Prototype weigh-off, drawing release | DOC-10 mechanical |
| **E-4** | MOE-01 | v6 surrogate lock-break | UAS FPV + thermal instrumented range | **2D** |
| **E-5** | KPP-10 | Temp sweep sensitivity | Environmental chamber −20/+50 °C | **2E** |

Until E-1..E-5 close, MS-V remains **TRL 2–3 analytical** — not TRL 4 component validation.

## 11. Intellectual property and licensing

| Tier | Document | Use |
|------|----------|-----|
| Concept evaluation | [`LICENSE`](../LICENSE) — **CEL** (not MIT) | Repo review, government concept evaluation |
| Commercial / PCA | [`LICENSE-COMMERCIAL.md`](../LICENSE-COMMERCIAL.md) | Manufacturing, fielding, integration — contact Fratres-X-AI |

Do **not** describe the repository as “open source MIT.” Partner diligence: [`docs/licensing-and-partnership.md`](../docs/licensing-and-partnership.md).

## 12. External engagement

| Audience | Document |
|----------|----------|
| Capture / primes | [`capture-brief.md`](../capture-brief.md) |
| Repo reviewers | [`partner-evaluation-faq.md`](../partner-evaluation-faq.md) |
| External review | [`EXTERNAL_REVIEW_READY.md`](../docs/EXTERNAL_REVIEW_READY.md) |
