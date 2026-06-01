"""CONOPS kill-chain Monte Carlo — five use cases from docs/04.

Couples Phase 1B physics + hardened MoE to operational time windows.
"""

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
    good_thickness_mask,
    peak_concentration_length_g_m2,
    screening_area_m2,
    time_to_spectral_threshold_s,
    transmittance_bands,
)
from models.cloud_physics.geometry_settling import (
    cl_at_time,
    duration_until_cl_below_threshold,
    friendly_thermal_blinded,
    hc_smoke_aerosol_mass_g,
    radial_cl_fraction,
    resolve_threat_geometry_cl,
    screening_radius_m,
)
from models.cloud_physics.phase2_pipeline import run_phase2_physics
from sim.engine import _resolve_moe_mask, _sample_alpha, load_params


@dataclass(frozen=True)
class UseCaseSpec:
    id: str
    name: str
    n_ms_v: int
    n_hc: int
    window_start_s: float
    window_end_s: float
    min_lock_s: float
    movement_required_s: float
    doc_ref: str


USE_CASES: tuple[UseCaseSpec, ...] = (
    UseCaseSpec(
        "casualty_recovery", "Casualty Recovery", 2, 1, 15.0, 120.0, 60.0, 45.0, "docs/04 UC1"
    ),
    UseCaseSpec(
        "break_contact", "Break Contact / Exfil", 3, 2, 15.0, 120.0, 60.0, 90.0, "docs/04 UC2"
    ),
    UseCaseSpec(
        "mask_infil", "Mask Infil / Approach", 2, 1, 15.0, 90.0, 45.0, 60.0, "docs/04 UC3"
    ),
    UseCaseSpec(
        "bounding_overwatch", "Bounding Overwatch", 2, 1, 15.0, 60.0, 30.0, 30.0, "docs/04 UC4"
    ),
    UseCaseSpec(
        "hasty_defense", "Hasty Defense", 2, 2, 12.0, 120.0, 60.0, 0.0, "docs/04 UC5"
    ),
)


def load_use_cases_config(root: Path | None = None) -> list[UseCaseSpec]:
    root = root or Path(__file__).resolve().parents[2]
    path = root / "sim" / "conops" / "use_cases.yaml"
    if not path.exists():
        return list(USE_CASES)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return [
        UseCaseSpec(
            u["id"], u["name"], u["n_ms_v"], u["n_hc"],
            u["window_start_s"], u["window_end_s"], u["min_lock_s"],
            u.get("movement_required_s", 0.0), u.get("doc_ref", "docs/04"),
        )
        for u in data["use_cases"]
    ]


def _evaluate_window_lock(
    obscured: np.ndarray,
    build_up: np.ndarray,
    duration: np.ndarray,
    window_start: float,
    window_end: float,
    min_lock: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Lock-break in CONOPS window: obscured through window with build-up before window_start.

    effective_lock = min(duration, window_end - max(window_start, build_up))
    """
    screen_ready = build_up <= window_start + 3.0  # allow 3s slack past doctrine T+15
    window_dur = np.maximum(window_end - np.maximum(window_start, build_up), 0.0)
    effective = np.minimum(duration, window_dur)
    lock_met = obscured & screen_ready & (effective >= min_lock)
    return lock_met, effective


def run_use_case(
    params: dict[str, Any],
    spec: UseCaseSpec,
    *,
    n_samples: int,
    seed: int,
) -> dict[str, Any]:
    """Monte Carlo one CONOPS use case with Phase 1B/2 physics."""
    rng = np.random.default_rng(seed)
    n = n_samples
    p1b = params.get("phase1b", {})
    sim_cfg = params.get("sim", {})
    physics_tier = sim_cfg.get("physics_tier", "phase1b")
    g = params["grenade"]
    cloud = params["cloud"]
    env = params["environment"]
    emp = params["employment"]
    moe_cfg = params["moe"]

    wind = rng.uniform(env["wind_speed_mph"]["min"], env["wind_speed_mph"]["max"], size=n)
    temp = rng.uniform(env["temperature_c"]["min"], env["temperature_c"]["max"], size=n)
    humidity = rng.uniform(env["humidity_rh_pct"]["min"], env["humidity_rh_pct"]["max"], size=n)

    filler = sample_filler_mass_g(rng, n, g["filler_mass_g"])
    burn_rate = sample_burn_rate_g_s(rng, n, g["burn_rate_g_s"], temp, env.get("temperature_burn_coupling"))
    yield_f = sample_yield_factor(rng, n, g["yield_factor"], humidity, env.get("humidity_yield_penalty"))
    raw_dur = raw_burn_duration_s(filler, burn_rate)

    area = screening_area_m2(
        rng, n, cloud["screening_area_sqft"]["min"], cloud["screening_area_sqft"]["max"], spec.n_ms_v,
    )
    depth_spec = cloud.get("cloud_depth_m", {"min": 2.0, "max": 4.0})
    depth = rng.uniform(depth_spec["min"], depth_spec["max"], size=n)
    build_up = build_up_time_s(rng, n, burn_rate, cloud["build_up_time_s"]["min"], cloud["build_up_time_s"]["max"])
    phase2_diag: dict[str, float] = {}
    p2_result = None

    if physics_tier == "phase2":
        p2_result = run_phase2_physics(
            rng, n, params,
            filler_mass_g=filler, burn_rate_base=burn_rate, yield_base=yield_f,
            area_m2=area, depth_m=depth, wind_mph=wind, temp_c=temp, humidity_rh=humidity,
            n_grenades=spec.n_ms_v, n_hc=spec.n_hc, apply_threat_geometry=True,
        )
        cl_center = p2_result.cl_center_ms_v
        cl_msv_threat = p2_result.geom.cl_ms_v if p2_result.geom else cl_center
        cl_vis = p2_result.cl_vis
        cl_nir = p2_result.cl_nir
        cl_mwir = p2_result.cl_mwir
        geom = p2_result.geom
        coverage = geom.los_cloud_fraction if geom else np.ones(n)
        alpha_vis, alpha_nir, alpha_mwir = p2_result.alpha_vis, p2_result.alpha_nir, p2_result.alpha_mwir
        raw_dur = p2_result.raw_burn_duration_s
        build_up = build_up + p2_result.build_up_delay_s
        settling = float(np.median(p2_result.settling_velocity_m_s))
        phase2_diag = p2_result.diagnostics
        model_version = "phase2_v1_full_physics"
    else:
        aerosol = aerosol_mass_g(filler, yield_f, spec.n_ms_v, g.get("overlap_efficiency", 0.85))
        cl_center = peak_concentration_length_g_m2(aerosol, area, depth, wind, humidity)
        hc_yield = rng.uniform(
            p1b.get("hc_yield_factor", {}).get("min", 0.28),
            p1b.get("hc_yield_factor", {}).get("max", 0.48),
            size=n,
        )
        hc_mass = hc_smoke_aerosol_mass_g(spec.n_hc, p1b.get("hc_grenade_fill_g", 539.0), hc_yield)
        geom = resolve_threat_geometry_cl(
            rng, n, p1b,
            cl_center_ms_v=cl_center,
            hc_aerosol_g=hc_mass,
            area_m2=area,
            depth_m=depth,
            wind_mph=wind,
            humidity_rh=humidity,
            n_grenades=spec.n_ms_v,
        )
        cl_msv_threat = geom.cl_ms_v
        cl_vis = geom.cl_vis_combined
        cl_nir = cl_msv_threat
        cl_mwir = cl_msv_threat
        coverage = geom.los_cloud_fraction
        alpha_vis = _sample_alpha(rng, n, "VIS", params)
        alpha_nir = _sample_alpha(rng, n, "NIR", params)
        alpha_mwir = _sample_alpha(rng, n, "MWIR", params)
        settling = p1b.get("settling_velocity_m_s", params.get("particle", {}).get("settling_velocity_m_s", 0.02))
        model_version = "phase1_v6_threat_geometry"

    cl_req = cl_threshold_g_m2(
        alpha_vis, alpha_nir, alpha_mwir, moe_cfg["transmittance_threshold"], emp.get("visual_smoke_factor", 1.0),
    )
    thickness_center = good_thickness_mask(cl_center, cl_req)
    thickness_threat = good_thickness_mask(cl_msv_threat, cl_req)
    ramp_exp = cloud.get("cl_ramp_exponent", 1.0)
    t_thresh = time_to_spectral_threshold_s(build_up, cl_center, cl_req, ramp_exp)

    duration = duration_until_cl_below_threshold(
        cl_center, cl_req, build_up, raw_dur, t_thresh, thickness_center,
        settling_velocity_m_s=settling, depth_m=depth,
    )
    if p2_result is not None:
        duration = duration * p2_result.duration_washout_factor * p2_result.post_burn_duration_boost

    vsf = emp.get("visual_smoke_factor", 1.3) * (1.0 + 0.15 * np.maximum(spec.n_hc - 1, 0))
    t_eval = (spec.window_start_s + spec.window_end_s) / 2.0
    cl_time_scale = cl_at_time(
        np.ones(n), t_eval, build_up,
        settling_velocity_m_s=settling, depth_m=depth, ramp_exponent=ramp_exp,
    )
    cl_vis_eval = cl_vis * cl_time_scale
    cl_nir_eval = (cl_nir if physics_tier == "phase2" else cl_msv_threat) * cl_time_scale
    cl_mwir_eval = (cl_mwir if physics_tier == "phase2" else cl_msv_threat) * cl_time_scale

    t_vis, _, _ = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_vis_eval)
    _, t_nir, _ = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_nir_eval)
    _, _, t_mwir = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_mwir_eval)
    obscured, model_version, sensor_diag = _resolve_moe_mask(
        params, rng, t_vis, t_nir, t_mwir,
        alpha_vis, alpha_nir, alpha_mwir,
        cl_vis_eval, cl_nir_eval, cl_mwir_eval,
        vsf, moe_cfg["transmittance_threshold"],
    )

    spread = float(p1b.get("plume_spread_factor", 3.0))
    radius_geo = screening_radius_m(area) * (1.0 + 0.08 * max(spec.n_ms_v - 1, 0)) * spread
    squad_orbit = rng.uniform(
        p1b.get("squad_radial_fraction", {}).get("min", 0.35),
        p1b.get("squad_radial_fraction", {}).get("max", 0.85),
        size=n,
    )
    edge_exp = float(p1b.get("plume_edge_exponent", 1.4))
    cl_squad = cl_center * radial_cl_fraction(
        squad_orbit * radius_geo, radius_geo, edge_exp,
    )
    friendly_blind = friendly_thermal_blinded(
        cl_squad, p1b.get("friendly_thermal_max_cl_g_m2", 5.5),
    )
    friendly_ok = ~friendly_blind | (spec.movement_required_s <= 0)

    lock_met, effective_lock = _evaluate_window_lock(
        obscured & thickness_threat & friendly_ok,
        build_up, duration,
        spec.window_start_s, spec.window_end_s, spec.min_lock_s,
    )

    t_mid = (spec.window_start_s + spec.window_end_s) / 2.0
    cl_mid = cl_at_time(cl_center, t_mid, build_up, settling_velocity_m_s=settling, depth_m=depth, ramp_exponent=ramp_exp)
    cl_threat_mid = cl_msv_threat * (cl_mid / np.maximum(cl_center, 1e-9))

    def pct(x: np.ndarray, q: float) -> float:
        return float(np.percentile(x, q))

    return {
        "use_case_id": spec.id,
        "use_case_name": spec.name,
        "doc_ref": spec.doc_ref,
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": model_version,
        "physics_tier": physics_tier,
        "config": {"n_samples": n, "seed": seed, "n_ms_v": spec.n_ms_v, "n_hc": spec.n_hc},
        "window_s": [spec.window_start_s, spec.window_end_s],
        "moe": {
            "lock_met_fraction": float(np.mean(lock_met)),
            "obscured_fraction": float(np.mean(obscured)),
            "friendly_blinded_fraction": float(np.mean(friendly_blind)),
            "coverage_p50": pct(coverage, 50),
            "threat_distance_p50_m": pct(geom.threat_distance_m, 50),
            "radial_fraction_p50": pct(geom.radial_fraction_ms_v, 50),
            "edge_of_plume_fraction": float(np.mean(geom.edge_of_plume)),
            "in_plume_core_fraction": float(np.mean(geom.in_plume_core)),
            "effective_lock_p10": pct(effective_lock, 10),
            "effective_lock_p50": pct(effective_lock, 50),
            "build_up_p90": pct(build_up, 90),
        },
        "kpp_in_window": {
            "build_up_before_window": pct(build_up, 90) <= spec.window_start_s + 3.0,
            "lock_met_majority": float(np.mean(lock_met)) >= 0.5,
        },
        "sensor_diagnostics": sensor_diag,
        "physics_diagnostics": {
            "cl_center_p50": pct(cl_center, 50),
            "cl_threat_p50": pct(cl_msv_threat, 50),
            "cl_threat_mid_window_p50": pct(cl_threat_mid, 50),
            "cl_mid_window_p50": pct(cl_mid, 50),
            "duration_p10": pct(duration, 10),
            **{f"phase2_{k}": v for k, v in phase2_diag.items()},
        },
    }


def run_all_use_cases(
    params: dict[str, Any] | None = None,
    *,
    n_samples: int = 100_000,
    seed: int = 4242,
) -> dict[str, Any]:
    params = params or load_params()
    cases = load_use_cases_config()
    results = []
    for i, spec in enumerate(cases):
        results.append(run_use_case(params, spec, n_samples=n_samples, seed=seed + i))
    tier = params.get("sim", {}).get("physics_tier", "phase1b")
    mv = "phase2_v1_full_physics" if tier == "phase2" else "phase1_v6_threat_geometry"
    return {
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": mv,
        "n_samples_per_case": n_samples,
        "use_cases": results,
    }
