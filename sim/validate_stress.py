#!/usr/bin/env python3
"""Stress validation — verify KPPs under adversarial sampling (no crutches).

Runs worst-case correlated draws: high wind, high temp, low fill, fast burn,
high humidity, low yield. All KPP checks should still be understood; this
confirms we are not passing only on mean cases.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402


def run_stress(params: dict, n: int = 100_000) -> None:
    """Override params to adversarial corners before standard engine run."""
    p = dict(params)
    p["environment"] = dict(params["environment"])
    p["environment"]["wind_speed_mph"] = {"min": 12, "max": 15}
    p["environment"]["temperature_c"] = {"min": 35, "max": 50}
    p["environment"]["humidity_rh_pct"] = {"min": 80, "max": 95}
    p["grenade"] = dict(params["grenade"])
    p["grenade"]["filler_mass_g"] = {"min": 624, "max": 640}
    p["grenade"]["burn_rate_g_s"] = {"min": 4.0, "max": 4.2}
    p["grenade"]["yield_factor"] = {"min": 0.22, "max": 0.30}

    cfg = SimConfig(n_samples=n, seed=999, n_grenades=3, label="stress_adversarial")
    r = run_vectorized(p, cfg)
    print("=== Adversarial stress (3 grenade, high wind/temp/humidity) ===")
    print("KPP checks:", r["kpp_checks"])
    print("Duration p10/p50:", r["kpp_03_duration_effective_s"]["p10"], r["kpp_03_duration_effective_s"]["p50"])
    print("MoE lock>=60s:", r["moe"]["lock_break_ge_60s_fraction"])
    print("Good thickness fraction:", r["physics_diagnostics"]["good_thickness_fraction"])
    return r


def main() -> None:
    params = load_params(ROOT)
    r = run_stress(params)
    failed = [k for k, v in r["kpp_checks"].items() if not v]
    if failed:
        print(f"\nAdversarial margin note — FAIL under stacked corners: {failed}")
        print("(Nominal 0-15 mph envelope passes; see analysis/kpp_gap_analysis.md)")
    else:
        print("\nAll KPP checks PASS under adversarial stress envelope.")


if __name__ == "__main__":
    main()
