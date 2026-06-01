#!/usr/bin/env python3
"""MS-V Phase 1 Monte Carlo skeleton.

Literature-parameter sensitivity study — NOT empirical validation.
Run from repo root: python sim/run_monte_carlo.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from models.sensors.surrogate_sensors import fused_eoir_degraded  # noqa: E402


def load_params() -> dict:
    path = ROOT / "models" / "cloud_physics" / "params.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def sample_extinction(rng: np.random.Generator, band: str, params: dict) -> float:
    spec = params["extinction_coefficient_m2_per_g"][band]
    return rng.uniform(spec["low"], spec["high"])


def sample_concentration_length(rng: np.random.Generator, params: dict) -> float:
    """Placeholder CL (g/m^2) from screening area and notional fill yield."""
    area_sqft = rng.uniform(
        params["cloud"]["screening_area_sqft"]["min"],
        params["cloud"]["screening_area_sqft"]["max"],
    )
    area_m2 = area_sqft * 0.092903
    # Notional aerosol mass per m^2 path — UNVALIDATED
    yield_g_m2 = rng.uniform(5.0, 25.0)
    return area_m2 * yield_g_m2


def run_monte_carlo(params: dict) -> dict:
    mc = params["monte_carlo"]
    rng = np.random.default_rng(mc["seed"])
    n = mc["n_samples"]
    threshold = params["moe"]["transmittance_threshold"]
    smoke_factor = params["employment"]["visual_smoke_factor"]

    moe_hits = 0
    build_ups = []
    durations = []

    for _ in range(n):
        alpha_vis = sample_extinction(rng, "VIS", params)
        alpha_mwir = sample_extinction(rng, "MWIR", params)
        cl = sample_concentration_length(rng, params)

        if fused_eoir_degraded(alpha_vis, alpha_mwir, cl, smoke_factor, threshold):
            moe_hits += 1

        build_ups.append(
            rng.uniform(
                params["cloud"]["build_up_time_s"]["min"],
                params["cloud"]["build_up_time_s"]["max"],
            )
        )
        durations.append(
            rng.uniform(
                params["cloud"]["duration_effective_s"]["min"],
                params["cloud"]["duration_effective_s"]["max"],
            )
        )

    return {
        "label": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "n_samples": n,
        "moe_fused_eoir_degraded_fraction": moe_hits / n,
        "build_up_time_s": {
            "p10": float(np.percentile(build_ups, 10)),
            "p50": float(np.percentile(build_ups, 50)),
            "p90": float(np.percentile(build_ups, 90)),
        },
        "duration_effective_s": {
            "p10": float(np.percentile(durations, 10)),
            "p50": float(np.percentile(durations, 50)),
            "p90": float(np.percentile(durations, 90)),
        },
        "kpp_checks": {
            "build_up_p90_le_15s": float(np.percentile(build_ups, 90)) <= 15,
            "duration_p10_ge_120s": float(np.percentile(durations, 10)) >= 120,
        },
    }


def main() -> None:
    params = load_params()
    results = run_monte_carlo(params)

    out_dir = ROOT / "analysis" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "monte_carlo_baseline.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
