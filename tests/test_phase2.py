"""Tests for Phase 2 full physics stack."""

from __future__ import annotations

import numpy as np
from models.cloud_physics.aerosol_microphysics import (
    stokes_settling_velocity_m_s,
)
from models.cloud_physics.phase2_pipeline import run_phase2_physics
from models.cloud_physics.spectral_extinction import multiple_scatter_correction
from models.sensors.lock_break import lock_break_probability
from sim.conops.kill_chain import UseCaseSpec, run_use_case
from sim.engine import SimConfig, load_params, run_vectorized


def test_psd_settling_increases_with_diameter() -> None:
    d = np.array([0.5, 5.0])
    v = stokes_settling_velocity_m_s(d)
    assert float(v[1]) > float(v[0])


def test_phase2_pipeline_runs() -> None:
    params = load_params()
    rng = np.random.default_rng(0)
    n = 500
    r = run_phase2_physics(
        rng, n, params,
        filler_mass_g=np.full(n, 650.0),
        burn_rate_base=np.full(n, 3.5),
        yield_base=np.full(n, 0.35),
        area_m2=np.full(n, 30.0),
        depth_m=np.full(n, 3.0),
        wind_mph=np.full(n, 5.0),
        temp_c=np.full(n, 20.0),
        humidity_rh=np.full(n, 60.0),
        n_grenades=2,
        n_hc=1,
    )
    assert r.cl_center_ms_v.shape == (n,)
    assert float(np.median(r.cl_vis)) > 0.0
    assert r.geom is not None


def test_multiple_scatter_reduces_effective_alpha() -> None:
    cl = np.array([15.0])
    alpha = np.array([8.0])
    corr = multiple_scatter_correction(cl, alpha)
    assert float(corr[0]) < 1.0


def test_engine_phase2_vectorized() -> None:
    params = load_params()
    out = run_vectorized(params, SimConfig(5000, 42, 3, "phase2_test", n_hc_grenades=1))
    assert out["physics_diagnostics"]["physics_tier"] == "phase2"
    assert "phase2_psd_diameter_um_p50" in out["physics_diagnostics"]


def test_conops_phase2_discriminates() -> None:
    params = load_params()
    spec = UseCaseSpec("test", "Test", 2, 1, 15.0, 120.0, 60.0, 45.0, "test")
    r = run_use_case(params, spec, n_samples=15_000, seed=7)
    assert r["physics_tier"] == "phase2"
    assert 0.05 < r["moe"]["obscured_fraction"] < 0.99
    assert r["moe"]["lock_met_fraction"] < 0.95


def test_lock_break_probability_varies() -> None:
    rng = np.random.default_rng(1)
    n = 2000
    t_low = np.full(n, 0.05)
    t_high = np.full(n, 0.9)
    netd = np.full(n, 0.1)
    m_low = lock_break_probability(rng, t_low, t_low, t_low, threshold=0.15, netd_floor=netd)
    m_high = lock_break_probability(rng, t_high, t_high, t_high, threshold=0.15, netd_floor=netd)
    assert float(np.mean(m_low)) > float(np.mean(m_high))
