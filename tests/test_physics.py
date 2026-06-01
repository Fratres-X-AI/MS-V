"""Unit tests for MS-V core physics — regression against known cases."""

from __future__ import annotations

import math

import numpy as np
from models.cloud_physics.burn_model import raw_burn_duration_s
from models.cloud_physics.cloud_evolution import (
    cl_threshold_g_m2,
    duration_at_good_thickness_s,
    transmittance_bands,
)
from models.cloud_physics.extinction import transmittance
from sim.engine import SimConfig, load_params, run_vectorized


def test_beer_lambert_transmittance() -> None:
    t = transmittance(10.0, 0.1)
    assert abs(float(t) - math.exp(-1.0)) < 1e-9


def test_raw_burn_duration() -> None:
    mass = np.array([680.0])
    rate = np.array([4.0])
    dur = raw_burn_duration_s(mass, rate)
    assert abs(dur[0] - 170.0) < 1e-6


def test_cl_threshold_monotonic_in_alpha() -> None:
    alpha_lo = np.array([4.0, 3.0, 2.0])
    alpha_hi = np.array([12.0, 10.0, 9.0])
    cl_lo = cl_threshold_g_m2(alpha_lo, alpha_lo, alpha_lo, 0.15, 1.3)
    cl_hi = cl_threshold_g_m2(alpha_hi, alpha_hi, alpha_hi, 0.15, 1.3)
    assert float(cl_hi[0]) < float(cl_lo[0])


def test_duration_at_good_thickness() -> None:
    raw = np.array([160.0])
    t_thresh = np.array([10.0])
    met = np.array([True])
    d = duration_at_good_thickness_s(raw, t_thresh, met)
    assert abs(d[0] - 150.0) < 1e-6


def test_transmittance_bands() -> None:
    a = np.full(3, 8.0)
    cl = np.full(3, 0.05)
    t_vis, t_nir, t_mwir = transmittance_bands(a, a, a, cl)
    assert all(0.0 < t < 1.0 for t in (t_vis[0], t_nir[0], t_mwir[0]))


def test_baseline_mega_suite_duration_order_of_magnitude() -> None:
    """Regression: 3-grenade 100k run duration p10 in expected band (v4 centerline physics)."""
    params = load_params()
    params.setdefault("sim", {})
    params["sim"]["physics_tier"] = "v4"
    params["sim"]["sensor_model"] = "v4_band_integrated"
    cfg = SimConfig(n_samples=50_000, seed=45, n_grenades=3, label="regression_g3")
    result = run_vectorized(params, cfg)
    p10 = result["kpp_03_duration_effective_s"]["p10"]
    assert 120.0 <= p10 <= 200.0, f"duration p10={p10} outside literature envelope"
