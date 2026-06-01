"""Tests for Phase 1B geometry and hardened MoE."""

from __future__ import annotations

import numpy as np
from models.cloud_physics.geometry_settling import (
    cl_at_time,
    plume_coverage_fraction,
    resolve_threat_geometry_cl,
)
from models.sensors.fpv_thermal import load_sensor_params, moe_threat_lock_obscured
from sim.engine import load_params


def test_coverage_decreases_with_throw_offset() -> None:
    offset = np.array([0.0, 8.0])
    radius = np.array([3.0, 3.0])
    wind = np.array([0.0, 0.0])
    cov = plume_coverage_fraction(offset, radius, wind, n_grenades=2)
    assert cov[0] > cov[1]


def test_cl_decays_with_settling() -> None:
    peak = np.array([1.0])
    build = np.array([10.0])
    cl_early = cl_at_time(peak, 20.0, build, settling_velocity_m_s=0.02, depth_m=np.array([3.0]))
    cl_late = cl_at_time(peak, 120.0, build, settling_velocity_m_s=0.02, depth_m=np.array([3.0]))
    assert float(cl_late[0]) < float(cl_early[0])


def test_v5_moe_not_saturated() -> None:
    """Hardened MoE must fail on low CL samples."""
    params = load_params()
    sensor = load_sensor_params()
    rng = np.random.default_rng(99)
    n = 5000
    low_cl = rng.uniform(0.01, 0.15, size=n)
    mask, _ = moe_threat_lock_obscured(
        rng, params, sensor,
        cl_vis=low_cl, cl_nir=low_cl, cl_mwir=low_cl,
        visual_smoke_boost=1.0,
    )
    frac = float(np.mean(mask))
    assert frac < 0.95, f"MoE still saturated at {frac}"


def test_edge_threat_reduces_cl_vs_core() -> None:
    """Threat at plume edge must see lower CL than core."""
    rng = np.random.default_rng(1)
    n = 500
    p1b = {
        "throw_offset_m": {"min": 2.0, "max": 2.0},
        "threat_orbit_fraction": {"min": 0.95, "max": 0.95},
        "wind_plume_shift_max_m": 4.0,
        "plume_edge_exponent": 2.2,
        "hc_plume_width_factor": 1.35,
        "hc_plume_edge_exponent": 1.6,
        "hc_yield_factor": {"min": 0.35, "max": 0.35},
        "hc_grenade_fill_g": 539.0,
        "edge_radius_fraction": 0.75,
        "core_radius_fraction": 0.35,
    }
    cl_center = np.full(n, 2.0)
    hc = np.full(n, 100.0)
    area = np.full(n, 30.0)
    depth = np.full(n, 3.0)
    wind = np.zeros(n)
    hum = np.full(n, 50.0)

    edge_geom = resolve_threat_geometry_cl(
        rng, n, p1b, cl_center_ms_v=cl_center, hc_aerosol_g=hc,
        area_m2=area, depth_m=depth, wind_mph=wind, humidity_rh=hum, n_grenades=2,
    )
    p1b_core = dict(p1b)
    p1b_core["threat_orbit_fraction"] = {"min": 0.1, "max": 0.1}
    p1b_core["throw_offset_m"] = {"min": 0.0, "max": 0.0}
    core_geom = resolve_threat_geometry_cl(
        np.random.default_rng(2), n, p1b_core, cl_center_ms_v=cl_center, hc_aerosol_g=hc,
        area_m2=area, depth_m=depth, wind_mph=wind, humidity_rh=hum, n_grenades=2,
    )
    assert float(np.median(edge_geom.cl_ms_v)) < float(np.median(core_geom.cl_ms_v))


def test_obscured_binds_with_threat_geometry() -> None:
    """v6: edge geometry + v5 sensor — obscured discriminates (not saturated, not collapsed)."""
    from sim.conops.kill_chain import UseCaseSpec, run_use_case

    params = load_params()
    params.setdefault("sim", {})
    params["sim"]["physics_tier"] = "phase1b"
    params["sim"]["sensor_model"] = "v5_threat_hardened"
    spec = UseCaseSpec("test", "Test", 2, 1, 15.0, 120.0, 60.0, 45.0, "test")
    r = run_use_case(params, spec, n_samples=20_000, seed=99)
    obs = r["moe"]["obscured_fraction"]
    assert 0.15 < obs < 0.98, f"obscured out of discriminating band: {obs}"
    assert r["moe"]["edge_of_plume_fraction"] > 0.1
    assert r["moe"]["in_plume_core_fraction"] > 0.05
