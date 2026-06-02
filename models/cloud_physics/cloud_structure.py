"""Cloud spatial structure — vertical profile, shear, merge, buoyancy.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class CloudStructure:
    area_m2: np.ndarray
    depth_m: np.ndarray
    height_m: np.ndarray
    dilution_factor: np.ndarray
    merge_factor: np.ndarray
    buoyancy_rise_m: np.ndarray


def gaussian_vertical_depth_m(
    rng: np.random.Generator,
    n: int,
    base_depth: np.ndarray,
    *,
    sigma_factor: float = 0.35,
) -> np.ndarray:
    """Effective LOS depth through Gaussian vertical profile (not uniform slab)."""
    _sigma = base_depth * sigma_factor  # noqa: F841 — reserved for profile extension
    return base_depth * (1.0 + 0.12 * rng.uniform(-1.0, 1.0, size=n))


def wind_shear_dilution(
    wind_mph: np.ndarray,
    *,
    ref_mph: float = 15.0,
    shear_coeff: float = 0.38,
) -> np.ndarray:
    """Wind shear stretches cloud — reduces peak CL."""
    return np.clip(1.0 - (wind_mph / ref_mph) * shear_coeff, 0.45, 1.0)


def multi_grenade_merge_factor(
    n_grenades: int,
    throw_offsets_m: np.ndarray,
    *,
    merge_radius_m: float = 4.0,
) -> np.ndarray:
    """Spatial merge efficiency from throw dispersion (not scalar overlap only)."""
    if n_grenades <= 1:
        return np.ones_like(throw_offsets_m)
    spread = np.abs(throw_offsets_m)
    # Tighter throws → stronger overlap during CL build-up (P2)
    proximity = np.clip(1.0 - spread / merge_radius_m, 0.35, 1.0)
    overlap = np.clip(
        1.0 - spread / (merge_radius_m * max(n_grenades - 1, 1)),
        0.5,
        1.0,
    )
    n_bonus = 1.0 + 0.10 * max(n_grenades - 1, 0) * proximity
    return overlap * n_bonus


def buoyancy_rise_m(
    burn_rate_g_s: np.ndarray,
    temp_c: np.ndarray,
    *,
    rise_per_g_s: float = 0.35,
    temp_boost: float = 0.004,
) -> np.ndarray:
    """Heat-driven cloud rise (MWIR LOS geometry surrogate)."""
    ref = 20.0
    return burn_rate_g_s * rise_per_g_s * (1.0 + (temp_c - ref) * temp_boost)


def resolve_cloud_structure(
    rng: np.random.Generator,
    n: int,
    params: dict,
    *,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    temp_c: np.ndarray,
    burn_rate_g_s: np.ndarray,
    n_grenades: int,
    throw_offsets_m: np.ndarray,
) -> CloudStructure:
    """Combined cloud structure modifiers."""
    p2 = params.get("phase2", {}).get("cloud_structure", {})
    depth_eff = gaussian_vertical_depth_m(
        rng, n, depth_m, sigma_factor=float(p2.get("vertical_sigma_factor", 0.35)),
    )
    dilution = wind_shear_dilution(
        wind_mph,
        ref_mph=float(p2.get("wind_shear_ref_mph", 15.0)),
        shear_coeff=float(p2.get("wind_shear_coeff", 0.38)),
    )
    merge = multi_grenade_merge_factor(
        n_grenades, throw_offsets_m,
        merge_radius_m=float(p2.get("merge_radius_m", 4.0)),
    )
    rise = buoyancy_rise_m(
        burn_rate_g_s, temp_c,
        rise_per_g_s=float(p2.get("buoyancy_rise_per_g_s", 0.35)),
    )
    area_eff = area_m2 * merge
    height = depth_eff + rise
    return CloudStructure(
        area_m2=area_eff,
        depth_m=depth_eff,
        height_m=height,
        dilution_factor=dilution,
        merge_factor=merge,
        buoyancy_rise_m=rise,
    )
