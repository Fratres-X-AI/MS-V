"""Atmospheric coupling — humidity extinction, washout, stability.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class AtmosphericModifiers:
    extinction_humidity_factor: np.ndarray
    duration_washout_factor: np.ndarray
    stability_mixing_factor: np.ndarray
    precipitation_active: np.ndarray


def humidity_extinction_factor(
    humidity_rh: np.ndarray,
    *,
    ref_rh: float = 50.0,
    alpha_boost_per_rh: float = 0.0018,
) -> np.ndarray:
    """Hygroscopic particles — higher RH increases effective extinction."""
    return 1.0 + np.maximum(humidity_rh - ref_rh, 0.0) * alpha_boost_per_rh


def precipitation_washout_factor(
    rng: np.random.Generator,
    n: int,
    humidity_rh: np.ndarray,
    spec: dict,
) -> tuple[np.ndarray, np.ndarray]:
    """High RH tail represents light precip / washout shortening duration."""
    rh_thresh = float(spec.get("washout_rh_threshold", 88.0))
    prob = float(spec.get("washout_probability_at_max_rh", 0.12))
    active = (humidity_rh >= rh_thresh) & (rng.uniform(0.0, 1.0, size=n) < prob)
    factor = np.where(active, float(spec.get("duration_factor_when_active", 0.72)), 1.0)
    return factor, active


def stability_mixing_factor(
    rng: np.random.Generator,
    n: int,
    temp_c: np.ndarray,
    wind_mph: np.ndarray,
    spec: dict,
) -> np.ndarray:
    """Pasquill-lite: unstable (hot + light wind) dilutes faster."""
    unstable = (temp_c > 25.0) & (wind_mph < 6.0)
    stable = (temp_c < 5.0) & (wind_mph < 4.0)
    base = np.ones(n)
    base = np.where(unstable, float(spec.get("unstable_dilution", 0.88)), base)
    base = np.where(stable, float(spec.get("stable_trapping", 1.06)), base)
    jitter = rng.uniform(0.97, 1.03, size=n)
    return base * jitter


def resolve_atmospheric_modifiers(
    rng: np.random.Generator,
    n: int,
    params: dict,
    *,
    humidity_rh: np.ndarray,
    temp_c: np.ndarray,
    wind_mph: np.ndarray,
) -> AtmosphericModifiers:
    atm = params.get("phase2", {}).get("atmosphere", {})
    ext = humidity_extinction_factor(
        humidity_rh,
        ref_rh=float(atm.get("extinction_ref_rh", 50.0)),
        alpha_boost_per_rh=float(atm.get("extinction_boost_per_rh", 0.0018)),
    )
    wash, precip = precipitation_washout_factor(rng, n, humidity_rh, atm.get("washout", {}))
    stab = stability_mixing_factor(rng, n, temp_c, wind_mph, atm.get("stability", {}))
    return AtmosphericModifiers(
        extinction_humidity_factor=ext,
        duration_washout_factor=wash,
        stability_mixing_factor=stab,
        precipitation_active=precip,
    )
