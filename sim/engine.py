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
    duration_at_good_thickness_s,
    good_thickness_mask,
    lock_break_duration_estimate_s,
    lock_break_moe_met,
    moe_fused_eoir_mask,
    peak_concentration_length_g_m2,
    screening_area_m2,
    time_to_spectral_threshold_s,
    transmittance_bands,
)
from models.cloud_physics.geometry_settling import (
    duration_until_cl_below_threshold,
    friendly_thermal_blinded,
    hc_smoke_aerosol_mass_g,
    resolve_threat_geometry_cl,
)
from models.cloud_physics.phase2_pipeline import run_phase2_physics
from models.sensors.degradation import moe_fused_degraded_mask, sensor_diagnostics
from models.sensors.fpv_thermal import (
    band_integrated_transmittance,
    load_sensor_params,
    moe_threat_lock_obscured,
    netd_contrast_limit,
    sample_band_alphas,
)
from models.sensors.lock_break import fiber_vs_rf_penalty, lock_break_probability
from sim.manifest_util import build_traceability


@dataclass
class SimConfig:
    n_samples: int
    seed: int
    n_grenades: int
    label: str
    n_hc_grenades: int = 1


def load_params(root: Path | None = None, *, profile: str | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[1]
    path = root / "models" / "cloud_physics" / "params.yaml"
    with path.open(encoding="utf-8") as f:
        params = yaml.safe_load(f)
    hf_path = root / "models" / "system" / "human_factors.yaml"
    if hf_path.exists():
        with hf_path.open(encoding="utf-8") as f:
            params["human_factors"] = yaml.safe_load(f)
    if profile == "reproduce" and "reproduce" in params:
        rep = params["reproduce"]
        params.setdefault("sim", {})
        params["sim"]["physics_tier"] = rep.get("physics_tier", "v4")
        params["sim"]["sensor_model"] = rep.get("sensor_model", "v4_band_integrated")
    from models.params_validation import validate_params

    validate_params(params)
    return params


def _sample_alpha(rng: np.random.Generator, n: int, band: str, params: dict) -> np.ndarray:
    spec = params["extinction_coefficient_m2_per_g"][band]
    return rng.uniform(spec["low"], spec["high"], size=n)


def _resolve_moe_mask(
    params: dict,
    rng: np.random.Generator,
    t_vis: np.ndarray,
    t_nir: np.ndarray,
    t_mwir: np.ndarray,
    alpha_vis: np.ndarray,
    alpha_nir: np.ndarray,
    alpha_mwir: np.ndarray,
    cl_vis: np.ndarray,
    cl_nir: np.ndarray,
    cl_mwir: np.ndarray,
    visual_smoke_factor: float | np.ndarray,
    threshold: float,
) -> tuple[np.ndarray, str, dict[str, float]]:
    sim_cfg = params.get("sim", {})
    model = sim_cfg.get("sensor_model", "v4_band_integrated")
    extra_diag: dict[str, float] = {}

    if model == "v6_probabilistic_lock":
        sensor_params = load_sensor_params()
        n = cl_vis.shape[0]
        deg = sensor_params["degradation"]
        bands = sensor_params["bands"]
        w_vis = np.array(bands["VIS"]["weights"], dtype=float)
        w_nir = np.array(bands["NIR"]["weights"], dtype=float)
        w_mwir = np.array(bands["MWIR"]["weights"], dtype=float)
        vis_lo, vis_mid, vis_hi = sample_band_alphas(rng, n, params, "VIS")
        nir_lo, nir_mid, nir_hi = sample_band_alphas(rng, n, params, "NIR")
        mw_lo, mw_mid, mw_hi = sample_band_alphas(rng, n, params, "MWIR")
        vsf = np.asarray(visual_smoke_factor)
        t_vis = band_integrated_transmittance(vis_lo, vis_mid, vis_hi, w_vis, cl_vis)
        t_vis = np.power(np.clip(t_vis, 1e-12, 1.0), vsf)
        t_nir = band_integrated_transmittance(nir_lo, nir_mid, nir_hi, w_nir, cl_nir)
        t_mwir = band_integrated_transmittance(mw_lo, mw_mid, mw_hi, w_mwir, cl_mwir)
        netd_floor = netd_contrast_limit(rng, n, sensor_params["uncooled_thermal"]["netd_mk"])
        rf_pen = fiber_vs_rf_penalty(rng, n, sensor_params.get("fiber_optic", {}))
        eff_thresh = np.maximum(threshold, netd_floor) / rf_pen
        mask = lock_break_probability(
            rng, t_vis, t_nir, t_mwir,
            threshold=threshold,
            netd_floor=eff_thresh,
            require_all_bands=deg.get("require_all_bands", True),
        )
        extra_diag = {
            "t_vis_p50": float(np.median(t_vis)),
            "t_nir_p50": float(np.median(t_nir)),
            "t_mwir_p50": float(np.median(t_mwir)),
            "netd_floor_p50": float(np.median(netd_floor)),
            "lock_prob_obscured_fraction": float(np.mean(mask)),
        }
        return mask, "phase2_v1_full_physics", extra_diag

    if model == "v5_threat_hardened":
        sensor_params = load_sensor_params()
        mask, diag = moe_threat_lock_obscured(
            rng, params, sensor_params,
            cl_vis=cl_vis, cl_nir=cl_nir, cl_mwir=cl_mwir,
            visual_smoke_boost=visual_smoke_factor,
        )
        extra_diag = diag
        return mask, "phase1_v6_threat_geometry", extra_diag

    if model == "v3_scalar":
        mask = moe_fused_eoir_mask(t_vis, t_nir, t_mwir, threshold, float(visual_smoke_factor))
        return mask, "phase1_v3_cl_ramp", extra_diag

    contrast = 1.0 - threshold
    mask = moe_fused_degraded_mask(
        alpha_vis, alpha_nir, alpha_mwir, cl_mwir,
        visual_smoke_factor=visual_smoke_factor,
        contrast_threshold=contrast,
    )
    return mask, "phase1_v4_sensor", extra_diag


def run_vectorized(params: dict, config: SimConfig) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[1]
    params_path = root / "models" / "cloud_physics" / "params.yaml"
    rng = np.random.default_rng(config.seed)
    n = config.n_samples
    g = params["grenade"]
    cloud = params["cloud"]
    env = params["environment"]
    emp = params["employment"]
    moe = params["moe"]
    kpp = params.get("kpp", {})
    sim_cfg = params.get("sim", {})
    p1b = params.get("phase1b", {})
    physics_tier = sim_cfg.get("physics_tier", "v4")
    n_hc = int(getattr(config, "n_hc_grenades", 1))

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
    cl_peak_raw = peak_concentration_length_g_m2(aerosol, area, depth, wind_mph, humidity)

    vsf = emp["visual_smoke_factor"]
    cl_vis = cl_peak_raw
    cl_nir = cl_peak_raw
    cl_mwir = cl_peak_raw
    coverage = np.ones(n)
    friendly_blind_frac = 0.0
    threat_diag: dict[str, float] = {}
    phase2_diag: dict[str, float] = {}
    duration_washout = np.ones(n)
    post_burn_boost = np.ones(n)
    p2_result = None

    if physics_tier == "phase2":
        p2_result = run_phase2_physics(
            rng, n, params,
            filler_mass_g=filler_mass,
            burn_rate_base=burn_rate,
            yield_base=yield_factor,
            area_m2=area,
            depth_m=depth,
            wind_mph=wind_mph,
            temp_c=temp_c,
            humidity_rh=humidity,
            n_grenades=config.n_grenades,
            n_hc=n_hc,
            apply_threat_geometry=True,
        )
        cl_peak_raw = p2_result.cl_center_ms_v
        cl_peak = cl_peak_raw
        cl_vis = p2_result.cl_vis
        cl_nir = p2_result.cl_nir
        cl_mwir = p2_result.cl_mwir
        alpha_vis = p2_result.alpha_vis
        alpha_nir = p2_result.alpha_nir
        alpha_mwir = p2_result.alpha_mwir
        raw_duration = p2_result.raw_burn_duration_s
        duration_washout = p2_result.duration_washout_factor
        post_burn_boost = p2_result.post_burn_duration_boost
        if p2_result.geom is not None:
            geom = p2_result.geom
            coverage = geom.los_cloud_fraction
            threat_diag = {
                "threat_distance_p50_m": float(np.median(geom.threat_distance_m)),
                "radial_fraction_p50": float(np.median(geom.radial_fraction_ms_v)),
                "los_cloud_fraction_p50": float(np.median(geom.los_cloud_fraction)),
                "edge_of_plume_fraction": float(np.mean(geom.edge_of_plume)),
                "in_plume_core_fraction": float(np.mean(geom.in_plume_core)),
                "cl_threat_p50": float(np.median(geom.cl_ms_v)),
                "cl_center_p50": float(np.median(cl_peak_raw)),
            }
        phase2_diag = p2_result.diagnostics
        vsf_arr = vsf * (1.0 + 0.15 * max(n_hc - 1, 0))
        vsf = vsf_arr
        friendly_blind_frac = float(np.mean(friendly_thermal_blinded(
            cl_peak_raw, p1b.get("friendly_thermal_max_cl_g_m2", 5.5),
        )))
    elif physics_tier == "phase1b" and p1b:
        hc_yield = rng.uniform(
            p1b.get("hc_yield_factor", {}).get("min", 0.28),
            p1b.get("hc_yield_factor", {}).get("max", 0.48),
            size=n,
        )
        hc_mass = hc_smoke_aerosol_mass_g(n_hc, p1b.get("hc_grenade_fill_g", 539.0), hc_yield)
        geom = resolve_threat_geometry_cl(
            rng, n, p1b,
            cl_center_ms_v=cl_peak_raw,
            hc_aerosol_g=hc_mass,
            area_m2=area,
            depth_m=depth,
            wind_mph=wind_mph,
            humidity_rh=humidity,
            n_grenades=config.n_grenades,
        )
        # MoE evaluated at threat LOS; KPP duration uses cloud-center physics
        cl_msv_threat = geom.cl_ms_v
        cl_vis = geom.cl_vis_combined
        cl_nir = geom.cl_nir
        cl_mwir = geom.cl_mwir
        coverage = geom.los_cloud_fraction
        cl_peak = cl_peak_raw
        vsf_arr = vsf * (1.0 + 0.15 * max(n_hc - 1, 0))
        vsf = vsf_arr
        friendly_blind_frac = float(np.mean(friendly_thermal_blinded(
            cl_peak_raw, p1b.get("friendly_thermal_max_cl_g_m2", 2.5),
        )))
        threat_diag = {
            "threat_distance_p50_m": float(np.median(geom.threat_distance_m)),
            "radial_fraction_p50": float(np.median(geom.radial_fraction_ms_v)),
            "los_cloud_fraction_p50": float(np.median(geom.los_cloud_fraction)),
            "edge_of_plume_fraction": float(np.mean(geom.edge_of_plume)),
            "in_plume_core_fraction": float(np.mean(geom.in_plume_core)),
            "cl_threat_p50": float(np.median(cl_msv_threat)),
            "cl_center_p50": float(np.median(cl_peak_raw)),
        }
    else:
        cl_peak = cl_peak_raw
        cl_msv_threat = cl_peak_raw
        cl_vis = cl_peak_raw
        cl_nir = cl_peak_raw
        cl_mwir = cl_peak_raw

    if physics_tier != "phase2":
        alpha_vis = _sample_alpha(rng, n, "VIS", params)
        alpha_nir = _sample_alpha(rng, n, "NIR", params)
        alpha_mwir = _sample_alpha(rng, n, "MWIR", params)

    cl_required = cl_threshold_g_m2(
        alpha_vis, alpha_nir, alpha_mwir,
        moe["transmittance_threshold"],
        emp["visual_smoke_factor"] if physics_tier not in ("phase1b", "phase2") else float(np.median(vsf) if hasattr(vsf, "__len__") else vsf),
    )
    thickness_met = good_thickness_mask(cl_peak, cl_required)

    t_vis, t_nir, t_mwir = transmittance_bands(alpha_vis, alpha_nir, alpha_mwir, cl_vis)
    moe_mask, model_version, sensor_extra = _resolve_moe_mask(
        params, rng, t_vis, t_nir, t_mwir,
        alpha_vis, alpha_nir, alpha_mwir,
        cl_vis, cl_nir, cl_mwir,
        vsf, moe["transmittance_threshold"],
    )

    build_up = build_up_time_s(
        rng, n, burn_rate,
        cloud["build_up_time_s"]["min"],
        cloud["build_up_time_s"]["max"],
    )
    build_up_kpp = build_up
    if physics_tier == "phase2" and p2_result is not None:
        build_up = build_up + p2_result.build_up_delay_s
        build_up_kpp = build_up - p2_result.build_up_delay_s
        mf = params.get("phase2", {}).get("model_form", {}).get("ramp_exponent", {})
        ramp_exp = rng.uniform(mf.get("min", 0.85), mf.get("max", 1.15), size=n)
        ramp_exp = float(np.median(ramp_exp))
    else:
        build_up_kpp = build_up
        ramp_exp = cloud.get("cl_ramp_exponent", 1.0)
    time_at_threshold = time_to_spectral_threshold_s(build_up, cl_peak, cl_required, ramp_exp)

    if physics_tier in ("phase1b", "phase2") and p1b:
        if physics_tier == "phase2" and p2_result is not None:
            settling = p2_result.settling_velocity_m_s
        else:
            settling = p1b.get("settling_velocity_m_s", params.get("particle", {}).get("settling_velocity_m_s", 0.02))
        duration = duration_until_cl_below_threshold(
            cl_peak, cl_required, build_up, raw_duration, time_at_threshold, thickness_met,
            settling_velocity_m_s=settling,
            depth_m=depth,
        )
        if physics_tier == "phase2" and p2_result is not None:
            duration = duration * duration_washout
            duration = duration * post_burn_boost
    else:
        duration = duration_at_good_thickness_s(raw_duration, time_at_threshold, thickness_met)

    lock_break = lock_break_duration_estimate_s(duration, moe_mask, moe["lock_break_duration_threshold_s"])
    moe_60s = lock_break_moe_met(lock_break, moe["lock_break_duration_threshold_s"])

    area_sqft = area / 0.092903
    throw_arr: np.ndarray | None = None
    fuze_arr: np.ndarray | None = None
    if physics_tier == "phase2" and p2_result is not None:
        throw_arr = p2_result.deployment.throw_range_m
        fuze_arr = p2_result.deployment.fuze_delay_s

    def pct(x: np.ndarray, q: float) -> float:
        return float(np.percentile(x, q))

    lock_frac = float(np.mean(moe_60s))
    degraded_frac = float(np.mean(moe_mask))
    surrogate_saturated = lock_frac >= 0.999 and degraded_frac >= 0.999
    sensor_extra["surrogate_saturated"] = surrogate_saturated
    sensor_extra["lock_break_ge_60s_fraction"] = lock_frac

    bu_max = kpp.get("build_up_p90_max_s", 15.0)
    dur_min = kpp.get("duration_p10_min_s", 120.0)
    area_min = kpp.get("area_p10_min_sqft", 30.0)
    lock_min = kpp.get("lock_break_p50_min_s", 60.0)

    trace = build_traceability(
        job_id=config.label,
        seed=config.seed,
        n_samples=n,
        n_grenades=config.n_grenades,
        model_version=model_version,
        params_path=params_path,
        assumption_ids=list(sim_cfg.get("assumption_ids", [])),
    )

    return {
        "label": config.label,
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "study_type": "literature_parameter_sensitivity",
        "model_version": model_version,
        "traceability": trace,
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
        "kpp_02_build_up_s": {"p10": pct(build_up_kpp, 10), "p50": pct(build_up_kpp, 50), "p90": pct(build_up_kpp, 90)},
        "kpp_03_duration_effective_s": {"p10": pct(duration, 10), "p50": pct(duration, 50), "p90": pct(duration, 90)},
        "kpp_04_screening_area_sqft": {"p10": pct(area_sqft, 10), "p50": pct(area_sqft, 50), "p90": pct(area_sqft, 90)},
        **(
            {
                "kpp_08_throw_range_m": {
                    "p10": pct(throw_arr, 10),
                    "p50": pct(throw_arr, 50),
                    "p90": pct(throw_arr, 90),
                },
                "kpp_07_fuze_delay_s": {
                    "p10": pct(fuze_arr, 10),
                    "p50": pct(fuze_arr, 50),
                    "p90": pct(fuze_arr, 90),
                },
            }
            if throw_arr is not None and fuze_arr is not None
            else {}
        ),
        "transmittance": {
            "VIS_p50": pct(t_vis, 50),
            "NIR_p50": pct(t_nir, 50),
            "MWIR_p50": pct(t_mwir, 50),
            "fraction_below_threshold": float(np.mean(moe_mask)),
        },
        "sensor_diagnostics": {
            **sensor_diagnostics(alpha_vis, alpha_nir, alpha_mwir, cl_peak, emp["visual_smoke_factor"]),
            **sensor_extra,
        },
        "physics_diagnostics": {
            "good_thickness_fraction": float(np.mean(thickness_met)),
            "filler_mass_g_p50": pct(filler_mass, 50),
            "burn_rate_g_s_p50": pct(burn_rate, 50),
            "cl_peak_p10": pct(cl_peak, 10),
            "cl_required_p90": pct(cl_required, 90),
            "time_to_threshold_p50_s": pct(time_at_threshold, 50),
            "build_up_p50_s": pct(build_up, 50),
            "physics_tier": physics_tier,
            "plume_coverage_p50": pct(coverage, 50),
            "friendly_blinded_fraction": friendly_blind_frac,
            **threat_diag,
            **{f"phase2_{k}": v for k, v in phase2_diag.items()},
        },
        "moe": {
            "fused_eoir_degraded_fraction": float(np.mean(moe_mask)),
            "lock_break_ge_60s_fraction": float(np.mean(moe_60s)),
            "lock_break_duration_s": {"p10": pct(lock_break, 10), "p50": pct(lock_break, 50), "p90": pct(lock_break, 90)},
        },
        "kpp_checks": {
            "build_up_p90_le_15s": pct(build_up_kpp, 90) <= bu_max,
            "duration_p10_ge_120s": pct(duration, 10) >= dur_min,
            "area_p10_ge_30_sqft": pct(area_sqft, 10) >= area_min,
            "moe_lock_break_p50_ge_60s": pct(lock_break, 50) >= lock_min,
            **(
                {"throw_p10_ge_20m": pct(throw_arr, 10) >= kpp.get("throw_p10_min_m", 20.0)}
                if throw_arr is not None
                else {}
            ),
            **(
                {
                    "fuze_delay_m201_band": (
                        float(np.min(fuze_arr)) >= 0.7 and float(np.max(fuze_arr)) <= 2.0
                    ),
                }
                if fuze_arr is not None
                else {}
            ),
        },
        "raw_burn_duration_s": {"p10": pct(raw_duration, 10), "p50": pct(raw_duration, 50), "p90": pct(raw_duration, 90)},
        "peak_cl_g_m2": {"p10": pct(cl_peak, 10), "p50": pct(cl_peak, 50), "p90": pct(cl_peak, 90)},
    }
