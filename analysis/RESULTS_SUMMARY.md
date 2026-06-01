# MS-V Simulation Results Summary

> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION

## single_grenade

- MoE fused EO/IR degraded: **100.0%**
- MoE lock >= 60s: **99.8%**
- Build-up p50: 10.1s (p90: 12.6s)
- Duration p50: 96.4s (p10: 74.6s)
- Area p50: 35.0 sq ft
- KPP checks: build_up_p90_le_15s: PASS | duration_p10_ge_120s: FAIL | area_p10_ge_30_sqft: PASS | moe_lock_break_p50_ge_60s: PASS

## three_grenade_group

- MoE fused EO/IR degraded: **100.0%**
- MoE lock >= 60s: **99.8%**
- Build-up p50: 10.1s (p90: 12.6s)
- Duration p50: 96.5s (p10: 74.6s)
- Area p50: 77.1 sq ft
- KPP checks: build_up_p90_le_15s: PASS | duration_p10_ge_120s: FAIL | area_p10_ge_30_sqft: PASS | moe_lock_break_p50_ge_60s: PASS

## two_grenade_group

- MoE fused EO/IR degraded: **100.0%**
- MoE lock >= 60s: **99.8%**
- Build-up p50: 10.1s (p90: 12.6s)
- Duration p50: 96.5s (p10: 74.6s)
- Area p50: 57.6 sq ft
- KPP checks: build_up_p90_le_15s: PASS | duration_p10_ge_120s: FAIL | area_p10_ge_30_sqft: PASS | moe_lock_break_p50_ge_60s: PASS

## Wind Sensitivity (3 grenade)

- **calm_0_5mph**: MoE lock>=60s 100.0%, duration p50 110s
- **moderate_5_10mph**: MoE lock>=60s 100.0%, duration p50 97s
- **high_10_15mph**: MoE lock>=60s 99.6%, duration p50 83s
