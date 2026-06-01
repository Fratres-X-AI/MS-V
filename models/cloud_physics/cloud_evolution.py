"""Cloud concentration-length, build-up, duration, and environmental modifiers.

STATUS: Sensitivity-model for Phase 1 — not empirical validation.

Duration at good thickness is derived from Beer-Lambert threshold physics during
active burn — no arbitrary thickness fractions or duplicate wind penalties.
"""

from __future__ import annotations

import numpy as np


def screening_area_m2(
    rng: np.random.Generator,
    n: int,
    sqft_min: float,
    sqft_max: float,
    n_grenades: int,
) -> np.ndarray:
    """Effective ground screening area; sub-linear scale for multi-grenade overlap."""
    base = rng.uniform(sqft_min, sqft_max, size=n) * 0.092903
    scale = n_grenades ** 0.72 if n_grenades > 1 else 1.0
    return base * scale


def peak_concentration_length_g_m2(
    aerosol_mass_g: np.ndarray,
    area_m2: np.ndarray,
    cloud_depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
) -> np.ndarray:
    """
    Peak CL (g/m^2) along representative 50 m LOS path through cloud center.

    Wind increases dispersion (reduces peak CL). Humidity perturbs effective CL modestly.
    """
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.45, 0.45, 1.0)
    humidity_factor = 1.0 + (humidity_rh - 50.0) / 100.0 * 0.08
    cl = (aerosol_mass_g / np.maximum(area_m2 * cloud_depth_m, 0.01)) * wind_factor * humidity_factor
    return np.maximum(cl, 0.0)


def build_up_time_s(
    rng: np.random.Generator,
    n: int,
    burn_rate_g_s: np.ndarray,
    t_min: float = 8.0,
    t_max: float = 15.0,
) -> np.ndarray:
    """Higher burn rate tends to faster pressurization / streamer merge."""
    base = rng.uniform(t_min, t_max, size=n)
    rate_factor = np.clip((burn_rate_g_s / 10.0) ** 0.25, 0.88, 1.12)
    return base * rate_factor


def cl_threshold_g_m2(
    alpha_vis: np.ndarray,
    alpha_nir: np.ndarray,
    alpha_mwir: np.ndarray,
    transmittance_threshold: float,
    visual_smoke_factor: float,
) -> np.ndarray:
    """
    Minimum CL (g/m^2) required for fused VIS+NIR+MWIR obscuration at threshold.

    visual_smoke_factor > 1 increases effective VIS attenuation from partner smoke.
    """
    t_vis_eff = transmittance_threshold ** (1.0 / max(visual_smoke_factor, 1.0))
    cl_vis = -np.log(np.clip(t_vis_eff, 1e-12, 1.0)) / np.maximum(alpha_vis, 1e-9)
    cl_nir = -np.log(transmittance_threshold) / np.maximum(alpha_nir, 1e-9)
    cl_mwir = -np.log(transmittance_threshold) / np.maximum(alpha_mwir, 1e-9)
    return np.maximum(np.maximum(cl_vis, cl_nir), cl_mwir)


def transmittance_bands(
    alpha_vis: np.ndarray,
    alpha_nir: np.ndarray,
    alpha_mwir: np.ndarray,
    cl: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    t_vis = np.exp(-alpha_vis * cl)
    t_nir = np.exp(-alpha_nir * cl)
    t_mwir = np.exp(-alpha_mwir * cl)
    return t_vis, t_nir, t_mwir


def moe_fused_eoir_mask(
    t_vis: np.ndarray,
    t_nir: np.ndarray,
    t_mwir: np.ndarray,
    threshold: float,
    visual_smoke_factor: float,
) -> np.ndarray:
    """VIS (boosted by visual smoke partner), NIR, and MWIR all below threshold."""
    t_vis_eff = np.power(np.clip(t_vis, 1e-12, 1.0), visual_smoke_factor)
    return (t_vis_eff < threshold) & (t_nir < threshold) & (t_mwir < threshold)


def good_thickness_mask(cl_peak: np.ndarray, cl_required: np.ndarray) -> np.ndarray:
    """Cloud center maintains spectral screening thickness."""
    return cl_peak >= cl_required


def time_to_spectral_threshold_s(
    build_up_s: np.ndarray,
    cl_peak: np.ndarray,
    cl_required: np.ndarray,
    ramp_exponent: float = 1.0,
) -> np.ndarray:
    """
    Seconds until CL ramp reaches fused spectral threshold.

    Models CL(t) = CL_peak * (t / build_up)^exp for t <= build_up (linear by default).
    More rigorous than assuming zero obscuration until build_up clock expires.
    """
    ratio = np.clip(cl_required / np.maximum(cl_peak, 1e-12), 0.0, 1.0)
    exp = max(ramp_exponent, 0.1)
    return build_up_s * np.power(ratio, 1.0 / exp)


def duration_at_good_thickness_s(
    raw_burn_duration_s: np.ndarray,
    time_at_threshold_s: np.ndarray,
    thickness_met: np.ndarray,
) -> np.ndarray:
    """
    KPP-03: seconds at good thickness during active burn (uniform phase).

    Counts from first spectral threshold crossing until fuel exhaustion.
    """
    available = np.maximum(raw_burn_duration_s - time_at_threshold_s, 0.0)
    return np.where(thickness_met, available, 0.0)


def lock_break_duration_estimate_s(
    duration_good_s: np.ndarray,
    moe_mask: np.ndarray,
    threshold_s: float = 60.0,
) -> np.ndarray:
    """MoE lock-break window equals good-thickness duration when fused MoE is met."""
    return np.where(moe_mask, duration_good_s, 0.0)


def lock_break_moe_met(lock_break_s: np.ndarray, threshold_s: float = 60.0) -> np.ndarray:
    return lock_break_s >= threshold_s
