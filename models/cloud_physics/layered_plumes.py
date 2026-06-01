"""Layered plumes — explicit per-band optical depth for MS-V + HC.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

import numpy as np


def ms_v_band_cl(
    aerosol_mass_g: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
    *,
    dilution: np.ndarray,
    generation_factor: np.ndarray,
) -> np.ndarray:
    """Peak centerline CL for MS-V tri-band fill."""
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.42, 0.42, 1.0)
    humidity_factor = 1.0 + (humidity_rh - 50.0) / 100.0 * 0.07
    denom = np.maximum(area_m2 * depth_m, 0.01)
    return (aerosol_mass_g / denom) * wind_factor * humidity_factor * dilution * generation_factor


def hc_band_cl_vis(
    hc_mass_g: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
    *,
    hc_width_factor: float = 1.35,
    dilution: np.ndarray,
) -> np.ndarray:
    """AN-M8/M83 visual smoke — VIS band only."""
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.40, 0.45, 1.0)
    humidity_factor = 1.0 + (humidity_rh - 50.0) / 100.0 * 0.09
    denom = np.maximum(area_m2 * depth_m * hc_width_factor, 0.01)
    return (hc_mass_g / denom) * wind_factor * humidity_factor * dilution


def layered_band_cls(
    cl_ms_v: np.ndarray,
    cl_hc_vis: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Per-band CL: MS-V fills tri-band; HC adds VIS only."""
    cl_vis = cl_ms_v + cl_hc_vis
    cl_nir = cl_ms_v
    cl_mwir = cl_ms_v
    return cl_vis, cl_nir, cl_mwir


def diurnal_contrast_factor(
    rng: np.random.Generator,
    n: int,
    temp_c: np.ndarray,
    spec: dict,
) -> np.ndarray:
    """Background thermal contrast surrogate (affects MWIR MoE margin)."""
    # Hot afternoon → lower contrast → easier to obscure thermally
    ref = float(spec.get("reference_c", 20.0))
    scale = float(spec.get("contrast_scale_per_c", 0.004))
    base = 1.0 - (temp_c - ref) * scale
    return np.clip(base * rng.uniform(0.95, 1.05, size=n), 0.85, 1.15)
