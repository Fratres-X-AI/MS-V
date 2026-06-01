# System Requirements Document (SRD) — MS-V Veil

> **Status:** Draft for DIU/OTA/SBIR submission package  
> **Maturity:** TRL 2 literature-parameter sensitivity study — **NOT field validation**  
> **Evidence:** [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) · [`analysis/MEGA_SUITE_REPORT.md`](../analysis/MEGA_SUITE_REPORT.md)

## 1. Purpose

Define operational requirements for the MS-V multispectral obscurant grenade and map each requirement to M&S evidence or planned TRL 3/4 verification.

## 2. Scope

In scope: squad-layer obscuration against FPV and thermal UAS when combined with standard visual smoke.  
Out of scope: RF defeat, standalone employment without visual smoke, vehicle-mounted systems.

## 3. Key Performance Parameters

| ID | Requirement | M&S Status | Verification Path |
|----|-------------|------------|-------------------|
| KPP-02 | Build-up ≤ 15 s (p90) | **Sensitivity pass** — +16.1% headroom | High-speed video, chamber |
| KPP-03 | Duration ≥ 120 s at good thickness (p10) | **Sensitivity pass** — +33.3% nominal; +27% worst burn sweep | Burn cup vs T/RH |
| KPP-04 | Screening 30–40 sq ft | **Sensitivity pass** — single grenade p10 +3.4% | Lidar / geometry |
| KPP-06 | VIS + NIR + MWIR attenuation | **Surrogate saturated** — non-discriminative | Spectrometer α(λ) |
| KPP-09 | −20 to +50 °C operation | **Sensitivity pass** — hot bin tightest | Environmental chamber |
| KPP-10 | ≤ 15 mph wind | **Sensitivity pass** — not duration-bound v3 | Range plume |
| KPP-01,07,08,11,12 | Mass, fuze, throw, tox, cost | **Not in MC** | Phase 2 prototype / Phase 4 |

## 4. Measures of Effectiveness

| ID | Requirement | M&S Status | Verification Path |
|----|-------------|------------|-------------------|
| MOE-01 | Fused EO/IR lock-break ≥ 60 s | **Surrogate saturated** (100% all jobs) | UAS surrogate range test |

## 5. Known Limitations (mandatory disclosure)

1. No MS-V fill empirical data — all aerosol parameters from open literature.
2. MoE and tri-band KPP checks saturate in current Beer-Lambert surrogate (assumption A-013).
3. Combined plume spatial interaction not modeled (Phase 1B).
4. Sim pass ≠ design confirmation.

## 6. Traceability

Full matrix: [`rtm/requirements_traceability.csv`](../rtm/requirements_traceability.csv)  
Assumptions: [`rtm/assumption_register.md`](../rtm/assumption_register.md)  
Seeds: [`sim/config/seeds.yaml`](../sim/config/seeds.yaml)
