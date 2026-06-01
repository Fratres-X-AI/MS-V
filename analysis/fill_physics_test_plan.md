# Fill Physics Test Plan — TRL 3 Closure

> **MATURITY:** Planned verification — **NOT YET EXECUTED**  
> **Traceability:** KPP-03, KPP-06, KPP-12 · [`rtm/assumption_register.md`](../rtm/assumption_register.md)

## Objective

Close literature-parameter assumptions (A-001–A-005, A-002 burn rate) with bench tests on MS-V fill formulations — not claimed by current M&S.

## Test matrix

| ID | Test | KPP / Assumption | Method | Pass criterion |
|----|------|------------------|--------|----------------|
| T-01 | Burn cup duration | KPP-03, A-002 | ASTM-style cup, 20/35/50°C, RH 30/70/90% | p10 duration ≥ 120 s at nominal fill |
| T-02 | α(λ) spectrometry | KPP-06, A-001, A-005 | VIS/NIR/MWIR transmissometer vs mass loading | Bands below MoE threshold at design CL |
| T-03 | Cloud geometry | KPP-04, A-004 | Lidar / stereo over single grenade | p10 area ≥ 30 sq ft |
| T-04 | PSD / settling | Phase2 aerosol | Cascade impactor | D50 within literature bound in params.yaml |
| T-05 | Irritation panel | KPP-12 | Controlled exposure screening | Non-lethal, documented vs AN-M8/TA |

## Configuration control

- Fill batch ID → link to `sim/config/seeds.yaml` job reruns after parameter update
- Results → `analysis/results/trl3/` (future) with checksum manifest

## Relationship to M&S

140M mega suite (`phase2_v1_full_physics`) bounds **sensitivity** only. This plan defines **validation** artifacts required before TRL 4 claims.
