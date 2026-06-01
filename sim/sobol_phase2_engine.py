"""Phase2 engine-backed Sobol for MoE — discriminative under v6 sensor."""

from __future__ import annotations

import copy
from typing import Any

import numpy as np

MOE_SOBOL_NAMES: list[str] = [
    "burn_rate_g_s",
    "filler_mass_g",
    "temp_c",
    "humidity_rh",
    "alpha_vis",
    "alpha_mwir",
]


def build_moe_sobol_problem(params: dict[str, Any]) -> dict[str, Any]:
    g = params["grenade"]
    env = params["environment"]
    ext = params["extinction_coefficient_m2_per_g"]
    bounds = [
        [g["burn_rate_g_s"]["min"], g["burn_rate_g_s"]["max"]],
        [g["filler_mass_g"]["min"], g["filler_mass_g"]["max"]],
        [env["temperature_c"]["min"], env["temperature_c"]["max"]],
        [env["humidity_rh_pct"]["min"], env["humidity_rh_pct"]["max"]],
        [ext["VIS"]["low"], ext["VIS"]["high"]],
        [ext["MWIR"]["low"], ext["MWIR"]["high"]],
    ]
    return {"num_vars": len(MOE_SOBOL_NAMES), "names": MOE_SOBOL_NAMES, "bounds": bounds}


def _pin_params(params: dict[str, Any], row: np.ndarray) -> dict[str, Any]:
    p = copy.deepcopy(params)
    p.setdefault("sim", {})
    p["sim"]["physics_tier"] = "phase2"
    p["sim"]["sensor_model"] = "v6_probabilistic_lock"
    br, fm, tc, rh, av, am = row
    p["grenade"]["burn_rate_g_s"] = {"min": float(br), "max": float(br)}
    p["grenade"]["filler_mass_g"] = {"min": float(fm), "max": float(fm)}
    p["environment"]["temperature_c"] = {"min": float(tc), "max": float(tc)}
    p["environment"]["humidity_rh_pct"] = {"min": float(rh), "max": float(rh)}
    for band, val in (("VIS", av), ("MWIR", am)):
        p["extinction_coefficient_m2_per_g"][band] = {
            **p["extinction_coefficient_m2_per_g"][band],
            "low": float(val),
            "high": float(val),
        }
    return p
