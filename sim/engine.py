"""Vectorized Monte Carlo engine for MS-V Phase 1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from models.cloud_physics.burn_model import (
    aerosol_mass_g,
    raw_burn_duration_s,
    sample_burn_rate_g_s,
    sample_filler_mass_g,
    sample_yield_factor,
)
from models.cloud_physics.cloud_evolution import (
    build_up_time_s,
    cl_threshold_g_m2,
    time_to_spectral_threshold_s,
    duration_at_good_thickness_s,
    good_thickness_mask,
    lock_break_duration_estimate_s,
    lock_break_moe_met,
    moe_fused_eoir_mask,
    peak_concentration_length_g_m2,
    screening_area_m2,
    transmittance_bands,
)


@dataclass
class SimConfig:
    n_samples: int
    seed: int
    n_grenades: int
    label: str


def load_params(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[1]
    path = root / "models" / "cloud_physics" / "params.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _sample_alpha(rng: np.random.Generator, n: int, band: str, params: dict) -> np.ndarray:
    spec = params["extinction_coefficient_m2_per_g"][band]
    return rng.uniform(spec["low"], spec["high"], size=n)


def run_vectorized(params: dict, config: SimConfig) -> dict[str, Any]:
    rng = np.random.default_rng(config.seed)
    n = config.n_samples
    g = params["grenade"]
    cloud = params["cloud"]
    env = params["environment"]
    emp = params["employment"]
    moe = params["moe"]
    kpp = params.get("kpp", {})

    wind_mph = rng.uniform(env["wind_speed_mph"]["min"], env["wind_speed_mph"]["max"], size=n)
    temp_c = rng.uniform(env["temperature_c"]["min"], env["temperature_c"]["max"], size=n)
    humidity = rng.uniform(env["humidity_rh_pct"]["min"], env["humidity_rh_pct"]["max"], size=n)

    filler_mass = sample_filler_mass_g(rng, n, g["filler_mass_g"])
    burn_rate = sample_burn_rate_g_s(
        rng, n, g["burn_rate_g_s"], temp_c, env.get("temperature_burn_coupling")
    )
    yield_factor = sample_yield_factor(
        rng, n, g["yield_factor"], humidity, env.get("humidity_yield_penalty")
    )
    raw_duration = raw_burn_duration_s(filler_mass, burn_rate)

    area = screening_area_m2(
        rng, n,
        cloud["screening_area_sqft"]["min"],
        cloud["screening_area_sqft"]["max"],
        config.n_grenades,
    )
    depth_spec = cloud.get("cloud_depth_m", {"min": 2.0, "max": 4.0})
    depth = rng.uniform(depth_spec["min"], depth_spec["max"], size=n)

    aerosol = aerosol_mass_g(filler_mass, yield_factor, config.n_grenades, g.get("overlap_efficiency", 0.85))
    cl_peak = peak_concentration_length_g_m2(aerosol, area, depth, wind_mph, humidity)

    alpha_vis = _sample_alpha(rng, n, "VIS", params)
    alpha_nir = _sample_alpha(rng, n, "NIR", params)
    alpha_mwir = _sample_alpha(rng, n, "MWIR", params)

    cl_required = cl_threshold_g_m2(
        alpha_vis, alpha_nir, alpha_mwir,
        moe["transmittance_threshold"],
        emp["visual_smoke_factor"],
    )
    thickness_met = good_thickness_mask(cl_peak, cl_required)

    t_vis, t_nir, t_mwir = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_peak)
    moe_mask = moe_fused_eoir_mask(
        t_vis, t_nir, t_mwir, moe["transmittance_threshold"], emp["visual_smoke_factor"]
    )

    build_up = build_up_time_s(
        rng, n, burn_rate,
        cloud["build_up_time_s"]["min"],
        cloud["build_up_time_s"]["max"],
    )
    ramp_exp = cloud.get("cl_ramp_exponent", 1.0)
    time_at_threshold = time_to_spectral_threshold_s(build_up, cl_peak, cl_required, ramp_exp)
    duration = duration_at_good_thickness_s(raw_duration, time_at_threshold, thickness_met)
    lock_break = lock_break_duration_estimate_s(duration, moe_mask, moe["lock_break_duration_threshold_s"])
    moe_60s = lock_break_moe_met(lock_break, moe["lock_break_duration_threshold_s"])

    area_sqft = area / 0.092903

    def pct(x: np.ndarray, q: float) -> float:
        return float(np.percentile(x, q))

    bu_max = kpp.get("build_up_p90_max_s", 15.0)
    dur_min = kpp.get("duration_p10_min_s", 120.0)
    area_min = kpp.get("area_p10_min_sqft", 30.0)
    lock_min = kpp.get("lock_break_p50_min_s", 60.0)

    return {
        "label": config.label,
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": "phase1_v3_cl_ramp",
        "config": {
            "n_samples": n,
            "seed": config.seed,
            "n_grenades": config.n_grenades,
        },
        "environment_sampled": {
            "wind_mph_p50": pct(wind_mph, 50),
            "temp_c_p50": pct(temp_c, 50),
            "humidity_rh_p50": pct(humidity, 50),
        },
        "kpp_02_build_up_s": {"p10": pct(build_up, 10), "p50": pct(build_up, 50), "p90": pct(build_up, 90)},
        "kpp_03_duration_effective_s": {"p10": pct(duration, 10), "p50": pct(duration, 50), "p90": pct(duration, 90)},
        "kpp_04_screening_area_sqft": {"p10": pct(area_sqft, 10), "p50": pct(area_sqft, 50), "p90": pct(area_sqft, 90)},
        "transmittance": {
            "VIS_p50": pct(t_vis, 50),
            "NIR_p50": pct(t_nir, 50),
            "MWIR_p50": pct(t_mwir, 50),
            "fraction_below_threshold": float(np.mean(moe_mask)),
        },
        "physics_diagnostics": {
            "good_thickness_fraction": float(np.mean(thickness_met)),
            "filler_mass_g_p50": pct(filler_mass, 50),
            "burn_rate_g_s_p50": pct(burn_rate, 50),
            "cl_peak_p10": pct(cl_peak, 10),
            "cl_required_p90": pct(cl_required, 90),
            "time_to_threshold_p50_s": pct(time_at_threshold, 50),
            "build_up_p50_s": pct(build_up, 50),
        },
        "moe": {
            "fused_eoir_degraded_fraction": float(np.mean(moe_mask)),
            "lock_break_ge_60s_fraction": float(np.mean(moe_60s)),
            "lock_break_duration_s": {"p10": pct(lock_break, 10), "p50": pct(lock_break, 50), "p90": pct(lock_break, 90)},
        },
        "kpp_checks": {
            "build_up_p90_le_15s": pct(build_up, 90) <= bu_max,
            "duration_p10_ge_120s": pct(duration, 10) >= dur_min,
            "area_p10_ge_30_sqft": pct(area_sqft, 10) >= area_min,
            "moe_lock_break_p50_ge_60s": pct(lock_break, 50) >= lock_min,
        },
        "raw_burn_duration_s": {"p10": pct(raw_duration, 10), "p50": pct(raw_duration, 50), "p90": pct(raw_duration, 90)},
        "peak_cl_g_m2": {"p10": pct(cl_peak, 10), "p50": pct(cl_peak, 50), "p90": pct(cl_peak, 90)},
    }
