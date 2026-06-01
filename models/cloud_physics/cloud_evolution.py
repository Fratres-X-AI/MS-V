"""Cloud concentration-length, build-up, duration, and environmental modifiers.

STATUS: Sensitivity-model for Phase 1 — not empirical validation.
"""

from __future__ import annotations

import numpy as np

from models.cloud_physics.extinction import transmittance


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

    Wind increases dispersion (reduces peak CL). High humidity perturbs effective CL.
    """
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.45, 0.45, 1.0)
    # Hygroscopic: modest VIS boost / MWIR penalty — net small on CL magnitude
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


def effective_duration_s(
    raw_duration_s: np.ndarray,
    wind_mph: np.ndarray,
    rng: np.random.Generator,
    n: int,
    thickness_fraction: tuple[float, float] = (0.82, 0.98),
) -> np.ndarray:
    """
    Duration at 'good thickness' — fraction of raw burn when cloud maintains effective opacity.
    Wind shortens uniform phase.
    """
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.35, 0.50, 1.0)
    frac = rng.uniform(thickness_fraction[0], thickness_fraction[1], size=n)
    return raw_duration_s * wind_factor * frac


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
    t_mwir: np.ndarray,
    threshold: float,
    visual_smoke_factor: float,
) -> np.ndarray:
    """Both VIS (boosted by visual smoke partner) and MWIR below threshold."""
    # factor > 1 increases effective obscuration: T_combined = T_ms_v ** factor
    t_vis_eff = np.power(np.clip(t_vis, 1e-9, 1.0), visual_smoke_factor)
    return (t_vis_eff < threshold) & (t_mwir < threshold)


def lock_break_duration_estimate_s(
    effective_duration_s: np.ndarray,
    moe_mask: np.ndarray,
    build_up_s: np.ndarray,
    threshold_s: float = 60.0,
) -> np.ndarray:
    """Estimated seconds MoE held after build-up; zero if MoE not met."""
    available = np.maximum(effective_duration_s - build_up_s, 0.0)
    return np.where(moe_mask, available, 0.0)


def lock_break_moe_met(lock_break_s: np.ndarray, threshold_s: float = 60.0) -> np.ndarray:
    return lock_break_s >= threshold_s
