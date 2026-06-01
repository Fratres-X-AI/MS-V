"""FPV + thermal threat models with band integration and NETD noise (Phase 1B).

Wired to sim/engine.py when sim.sensor_model == v5_threat_hardened.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from models.sensors.degradation import load_sensor_params


def _load_band_alphas(params: dict[str, Any], band: str) -> tuple[float, float, float]:
    ext = params["extinction_coefficient_m2_per_g"][band]
    return ext["low"], ext["mid"], ext["high"]


def band_integrated_transmittance(
    alpha_low: np.ndarray,
    alpha_mid: np.ndarray,
    alpha_high: np.ndarray,
    weights: np.ndarray,
    cl: np.ndarray,
) -> np.ndarray:
    """Integrate T(λ)=exp(-α·CL) over surrogate band buckets."""
    w = weights / np.sum(weights)
    alphas = np.stack([alpha_low, alpha_mid, alpha_high], axis=1)
    t_bands = np.exp(-alphas * cl[:, None])
    return np.sum(t_bands * w, axis=1)


def sample_band_alphas(
    rng: np.random.Generator,
    n: int,
    cloud_params: dict[str, Any],
    band: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    spec = cloud_params["extinction_coefficient_m2_per_g"][band]
    lo, mid, hi = spec["low"], spec["mid"], spec["high"]
    spread = (hi - lo) * 0.15
    mid_a = rng.uniform(mid - spread, mid + spread, size=n)
    low_a = np.clip(mid_a - spread, lo, mid)
    high_a = np.clip(mid_a + spread, mid, hi)
    return low_a, mid_a, high_a


def netd_contrast_limit(
    rng: np.random.Generator,
    n: int,
    netd_mk: float,
    *,
    contrast_scale: float = 0.002,
) -> np.ndarray:
    """Minimum detectable contrast fraction from NETD surrogate (threat-side noise floor)."""
    base = netd_mk * contrast_scale
    return rng.uniform(base * 0.8, base * 1.2, size=n)


def moe_threat_lock_obscured(
    rng: np.random.Generator,
    cloud_params: dict[str, Any],
    sensor_params: dict[str, Any],
    *,
    cl_vis: np.ndarray,
    cl_nir: np.ndarray,
    cl_mwir: np.ndarray,
    visual_smoke_boost: np.ndarray | float = 1.0,
) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """
    Threat lock broken when band-integrated transmitted contrast falls below threshold + NETD.

    Returns (obscured_mask, diagnostics) where True = threat cannot maintain lock.
    Stricter than v4 scalar — partial plumes and NETD cause failures.
    """
    deg = sensor_params["degradation"]
    t_thresh = deg["transmittance_threshold"]
    uncooled = sensor_params["uncooled_thermal"]
    bands = sensor_params["bands"]

    n = cl_vis.shape[0]
    w_vis = np.array(bands["VIS"]["weights"], dtype=float)
    w_nir = np.array(bands["NIR"]["weights"], dtype=float)
    w_mwir = np.array(bands["MWIR"]["weights"], dtype=float)

    vis_lo, vis_mid, vis_hi = sample_band_alphas(rng, n, cloud_params, "VIS")
    nir_lo, nir_mid, nir_hi = sample_band_alphas(rng, n, cloud_params, "NIR")
    mw_lo, mw_mid, mw_hi = sample_band_alphas(rng, n, cloud_params, "MWIR")

    vsf = np.asarray(visual_smoke_boost)
    t_vis = band_integrated_transmittance(vis_lo, vis_mid, vis_hi, w_vis, cl_vis)
    t_vis_eff = np.power(np.clip(t_vis, 1e-12, 1.0), vsf)
    t_nir = band_integrated_transmittance(nir_lo, nir_mid, nir_hi, w_nir, cl_nir)
    t_mwir = band_integrated_transmittance(mw_lo, mw_mid, mw_hi, w_mwir, cl_mwir)

    netd_floor = netd_contrast_limit(rng, n, uncooled["netd_mk"])
    effective_thresh = np.maximum(t_thresh, netd_floor)

    vis_ok = t_vis_eff < effective_thresh
    nir_ok = t_nir < effective_thresh
    mwir_ok = t_mwir < effective_thresh

    if deg.get("require_all_bands", True):
        obscured = vis_ok & nir_ok & mwir_ok
    else:
        obscured = vis_ok | nir_ok | mwir_ok

    diag = {
        "t_vis_p50": float(np.median(t_vis_eff)),
        "t_nir_p50": float(np.median(t_nir)),
        "t_mwir_p50": float(np.median(t_mwir)),
        "netd_floor_p50": float(np.median(netd_floor)),
    }
    return obscured, diag


def load_v5_config(root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root or Path(__file__).resolve().parents[2]
    cloud_path = root / "models" / "cloud_physics" / "params.yaml"
    with cloud_path.open(encoding="utf-8") as f:
        import yaml as _yaml

        cloud = _yaml.safe_load(f)
    sensor = load_sensor_params(root)
    return cloud, sensor
