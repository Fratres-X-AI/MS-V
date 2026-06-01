"""Deterministic MS-V physics batch for global sensitivity (Sobol / Saltelli).

Each row is one parameter vector → scalar outputs (duration, build-up, MoE).
Couplings match sim/engine.py (temp→burn, humidity→yield, burn→build-up).
"""

from __future__ import annotations

from typing import Any

import numpy as np
from models.cloud_physics.burn_model import aerosol_mass_g, raw_burn_duration_s
from models.cloud_physics.cloud_evolution import (
    cl_threshold_g_m2,
    duration_at_good_thickness_s,
    good_thickness_mask,
    lock_break_duration_estimate_s,
    lock_break_moe_met,
    peak_concentration_length_g_m2,
    time_to_spectral_threshold_s,
    transmittance_bands,
)
from models.sensors.degradation import moe_fused_degraded_mask

SOBOL_NAMES: list[str] = [
    "wind_mph",
    "temp_c",
    "humidity_rh",
    "filler_mass_g",
    "burn_rate_g_s",
    "yield_factor",
    "screening_area_sqft",
    "cloud_depth_m",
    "alpha_vis",
    "alpha_nir",
    "alpha_mwir",
    "build_up_time_s",
]


def build_sobol_problem(params: dict[str, Any]) -> dict[str, Any]:
    """SALib problem dict from params.yaml literature bounds."""
    g = params["grenade"]
    cloud = params["cloud"]
    env = params["environment"]
    ext = params["extinction_coefficient_m2_per_g"]
    depth = cloud.get("cloud_depth_m", {"min": 2.0, "max": 4.0})

    bounds = [
        [env["wind_speed_mph"]["min"], env["wind_speed_mph"]["max"]],
        [env["temperature_c"]["min"], env["temperature_c"]["max"]],
        [env["humidity_rh_pct"]["min"], env["humidity_rh_pct"]["max"]],
        [g["filler_mass_g"]["min"], g["filler_mass_g"]["max"]],
        [g["burn_rate_g_s"]["min"], g["burn_rate_g_s"]["max"]],
        [g["yield_factor"]["min"], g["yield_factor"]["max"]],
        [cloud["screening_area_sqft"]["min"], cloud["screening_area_sqft"]["max"]],
        [depth["min"], depth["max"]],
        [ext["VIS"]["low"], ext["VIS"]["high"]],
        [ext["NIR"]["low"], ext["NIR"]["high"]],
        [ext["MWIR"]["low"], ext["MWIR"]["high"]],
        [cloud["build_up_time_s"]["min"], cloud["build_up_time_s"]["max"]],
    ]
    return {
        "num_vars": len(SOBOL_NAMES),
        "names": SOBOL_NAMES,
        "bounds": bounds,
    }


def _apply_couplings(
    params: dict[str, Any],
    temp_c: np.ndarray,
    humidity: np.ndarray,
    burn_base: np.ndarray,
    yield_base: np.ndarray,
    build_up_base: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    env = params["environment"]
    g = params["grenade"]
    temp_spec = env.get("temperature_burn_coupling", {})
    hum_spec = env.get("humidity_yield_penalty", {})

    ref = temp_spec.get("reference_c", 20.0)
    coeff = temp_spec.get("rate_increase_per_c", 0.002)
    burn = burn_base * (1.0 + (temp_c - ref) * coeff)
    burn = np.maximum(burn, g["burn_rate_g_s"]["min"] * 0.5)

    rh_ref = hum_spec.get("reference_rh_pct", 50.0)
    hum_coeff = hum_spec.get("loss_per_rh_pct", 0.0015)
    yf = yield_base * (1.0 - np.maximum(humidity - rh_ref, 0.0) * hum_coeff)
    yf = np.clip(yf, g["yield_factor"]["min"] * 0.5, g["yield_factor"]["max"])

    rate_factor = np.clip((burn / 10.0) ** 0.25, 0.88, 1.12)
    build_up = build_up_base * rate_factor
    return burn, yf, build_up


def evaluate_physics_batch(
    params: dict[str, Any],
    X: np.ndarray,
    *,
    n_grenades: int = 3,
) -> dict[str, np.ndarray]:
    """Vectorized deterministic physics for Saltelli sample matrix X (n, 12)."""
    wind = X[:, 0]
    temp = X[:, 1]
    humidity = X[:, 2]
    filler = X[:, 3]
    burn_base = X[:, 4]
    yield_base = X[:, 5]
    area_sqft = X[:, 6]
    depth = X[:, 7]
    alpha_vis = X[:, 8]
    alpha_nir = X[:, 9]
    alpha_mwir = X[:, 10]
    build_up_base = X[:, 11]

    burn, yf, build_up = _apply_couplings(params, temp, humidity, burn_base, yield_base, build_up_base)
    raw_dur = raw_burn_duration_s(filler, burn)

    scale = n_grenades ** 0.72 if n_grenades > 1 else 1.0
    area_m2 = area_sqft * 0.092903 * scale

    cloud = params["cloud"]
    emp = params["employment"]
    moe = params["moe"]
    g = params["grenade"]
    overlap = g.get("overlap_efficiency", 0.85)
    ramp_exp = cloud.get("cl_ramp_exponent", 1.0)
    threshold = moe["transmittance_threshold"]
    vsf = emp["visual_smoke_factor"]

    aerosol = aerosol_mass_g(filler, yf, n_grenades, overlap)
    cl_peak = peak_concentration_length_g_m2(aerosol, area_m2, depth, wind, humidity)
    cl_req = cl_threshold_g_m2(alpha_vis, alpha_nir, alpha_mwir, threshold, vsf)
    thickness = good_thickness_mask(cl_peak, cl_req)

    t_vis, t_nir, t_mwir = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_peak)
    contrast = 1.0 - threshold
    moe_mask = moe_fused_degraded_mask(
        alpha_vis, alpha_nir, alpha_mwir, cl_peak,
        visual_smoke_factor=vsf,
        contrast_threshold=contrast,
    )

    t_thresh = time_to_spectral_threshold_s(build_up, cl_peak, cl_req, ramp_exp)
    duration = duration_at_good_thickness_s(raw_dur, t_thresh, thickness)
    lock_break = lock_break_duration_estimate_s(duration, moe_mask, moe["lock_break_duration_threshold_s"])
    moe_met = lock_break_moe_met(lock_break, moe["lock_break_duration_threshold_s"]).astype(np.float64)

    return {
        "duration_s": duration,
        "build_up_s": build_up,
        "lock_break_s": lock_break,
        "moe_met": moe_met,
        "cl_peak": cl_peak,
        "raw_burn_s": raw_dur,
        "t_vis": t_vis,
        "t_nir": t_nir,
        "t_mwir": t_mwir,
    }


def outputs_to_Y(outputs: dict[str, np.ndarray], output_name: str) -> np.ndarray:
    return np.asarray(outputs[output_name], dtype=np.float64)
