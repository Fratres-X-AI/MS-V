# System Requirements Document (SRD) — MS-V Veil

> **Status:** Draft for DIU/OTA/SBIR submission package  
> **Maturity:** TRL 2–3 literature-parameter sensitivity study — **NOT field validation**  
> **Evidence:** [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) · [`analysis/MEGA_SUITE_REPORT.md`](../analysis/MEGA_SUITE_REPORT.md)

## 1. Purpose

Define operational requirements for the MS-V multispectral obscurant grenade and map each requirement to M&S evidence or planned TRL 3/4 verification.

## 2. Scope

In scope: squad-layer obscuration against FPV and thermal UAS when combined with standard visual smoke.  
Out of scope: RF defeat, standalone employment without visual smoke, vehicle-mounted systems.

## 3. Key Performance Parameters

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

## 4. Measures of Effectiveness

| ID | Requirement | M&S Status | Verification Path |
|----|-------------|------------|-------------------|
| MOE-01 | Fused EO/IR lock-break ≥ 60 s | **v6 probabilistic** — see saturation flag | UAS surrogate range test |
| MOE-02 | CASEVAC T+15–135 s window | **CONOPS MC** | [`analysis/CONOPS_REPORT.md`](../analysis/CONOPS_REPORT.md) |

## 5. Known Limitations (mandatory disclosure)

1. No MS-V fill empirical data — all aerosol parameters from open literature.
2. When `surrogate_saturated=true`, MoE/tri-band pass is non-discriminative (A-013).
3. Phase2 models combined plume interaction, PSD, humidity growth, and deployment kinematics — still literature-bound.
4. Sim pass ≠ design confirmation.

## 6. Traceability

Full matrix: [`rtm/requirements_traceability.csv`](../rtm/requirements_traceability.csv)  
Assumptions: [`rtm/assumption_register.md`](../rtm/assumption_register.md)  
Seeds: [`sim/config/seeds.yaml`](../sim/config/seeds.yaml)  
TRL gate: [`proposals/trl_gate_external.md`](../trl_gate_external.md)  
Reproduce: [`REPRODUCE.md`](../REPRODUCE.md)
