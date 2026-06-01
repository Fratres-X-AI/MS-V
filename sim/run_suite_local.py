#!/usr/bin/env python3
"""Run full local simulation suite (Phase 0/1).

Usage: python sim/run_suite_local.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402

OUT = ROOT / "analysis" / "results"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    params = load_params(ROOT)
    local_n = params.get("profiles", {}).get("local", {}).get("n_samples", 100_000)
    seed = params["monte_carlo"]["seed"]

    scenarios = [
        SimConfig(n_samples=local_n, seed=seed, n_grenades=1, label="single_grenade"),
        SimConfig(n_samples=local_n, seed=seed + 1, n_grenades=2, label="two_grenade_group"),
        SimConfig(n_samples=local_n, seed=seed + 2, n_grenades=3, label="three_grenade_group"),
    ]

    # Wind sensitivity: fixed 3-grenade at low vs high wind via param override
    suite: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "n_samples_per_scenario": local_n,
        "scenarios": {},
    }

    for cfg in scenarios:
        print(f"Running {cfg.label} ({cfg.n_samples:,} samples)...")
        result = run_vectorized(params, cfg)
        suite["scenarios"][cfg.label] = result
        path = OUT / f"{cfg.label}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"  -> {path}")
        checks = result["kpp_checks"]
        print(f"  KPP checks: {checks}")

    # Wind bins (3 grenade)
    print("Running wind sensitivity (3 grenade)...")
    wind_results = {}
    for wind_label, wmin, wmax in [("calm_0_5mph", 0, 5), ("moderate_5_10mph", 5, 10), ("high_10_15mph", 10, 15)]:
        p = json.loads(json.dumps(params))  # deep copy
        p["environment"]["wind_speed_mph"] = {"min": wmin, "max": wmax}
        cfg = SimConfig(n_samples=local_n // 2, seed=seed + 10, n_grenades=3, label=f"wind_{wind_label}")
        wind_results[wind_label] = run_vectorized(p, cfg)
    suite["wind_sensitivity_3_grenade"] = wind_results
    with (OUT / "wind_sensitivity.json").open("w", encoding="utf-8") as f:
        json.dump(wind_results, f, indent=2)

    with (OUT / "suite_summary.json").open("w", encoding="utf-8") as f:
        json.dump(suite, f, indent=2)

    print(f"\nSuite complete. Summary: {OUT / 'suite_summary.json'}")


if __name__ == "__main__":
    main()
