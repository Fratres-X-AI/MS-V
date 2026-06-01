"""Aerosol microphysics — PSD, settling, coagulation, hygroscopic growth.

Literature-order surrogates for Monte Carlo sensitivity — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class AerosolState:
    diameter_um: np.ndarray
    settling_velocity_m_s: np.ndarray
    yield_factor: np.ndarray
    alpha_scale: np.ndarray
    coagulation_factor: np.ndarray
    hygroscopic_growth: np.ndarray


def sample_psd_diameter_um(
    rng: np.random.Generator,
    n: int,
    spec: dict[str, float],
) -> np.ndarray:
    """Log-normal PSD sample (effective volume diameter)."""
    d_min = spec.get("min", 0.5)
    d_max = spec.get("max", 5.0)
    d_mid = (d_min + d_max) / 2.0
    sigma = float(spec.get("log_sigma", 0.45))
    log_d = rng.normal(np.log(d_mid), sigma, size=n)
    return np.clip(np.exp(log_d), d_min, d_max)


def stokes_settling_velocity_m_s(
    diameter_um: np.ndarray,
    *,
    density_kg_m3: float = 1500.0,
    air_viscosity: float = 1.8e-5,
) -> np.ndarray:
    """Stokes settling for spherical particles (order-of-magnitude)."""
    d_m = diameter_um * 1e-6
    rho_p = density_kg_m3
    rho_a = 1.2
    g = 9.81
    mu = air_viscosity
    return (rho_p - rho_a) * g * d_m * d_m / (18.0 * mu)


def coagulation_yield_factor(
    yield_base: np.ndarray,
    humidity_rh: np.ndarray,
    cl_peak: np.ndarray,
    *,
    ref_rh: float = 50.0,
    coag_rate: float = 0.0012,
) -> np.ndarray:
    """High concentration + humidity reduces effective aerosol yield."""
    rh_excess = np.maximum(humidity_rh - ref_rh, 0.0)
    conc_factor = np.clip(cl_peak / 10.0, 0.5, 3.0)
    loss = coag_rate * rh_excess * conc_factor
    return np.clip(yield_base * (1.0 - loss), yield_base * 0.55, yield_base)


def hygroscopic_growth_factor(
    humidity_rh: np.ndarray,
    diameter_um: np.ndarray,
    *,
    ref_rh: float = 50.0,
    growth_per_rh: float = 0.003,
) -> np.ndarray:
    """Water uptake increases effective diameter (Köhler-lite surrogate)."""
    rh_excess = np.maximum(humidity_rh - ref_rh, 0.0)
    growth = 1.0 + growth_per_rh * rh_excess
    return np.clip(growth, 1.0, 1.35)


def resolve_aerosol_state(
    rng: np.random.Generator,
    n: int,
    params: dict,
    *,
    yield_base: np.ndarray,
    humidity_rh: np.ndarray,
    cl_peak: np.ndarray,
) -> AerosolState:
    """Full aerosol microphysics state for one MC batch."""
    p2 = params.get("phase2", {})
    micro = p2.get("microphysics", {})
    particle = params.get("particle", {})

    d_spec = particle.get("diameter_um", {"min": 0.5, "max": 5.0})
    d_spec = {**d_spec, **micro.get("psd", {})}
    diameter = sample_psd_diameter_um(rng, n, d_spec)
    growth = hygroscopic_growth_factor(
        humidity_rh, diameter,
        ref_rh=micro.get("hygroscopic_ref_rh", 50.0),
        growth_per_rh=micro.get("hygroscopic_growth_per_rh", 0.003),
    )
    d_eff = diameter * growth
    settling = stokes_settling_velocity_m_s(
        d_eff,
        density_kg_m3=float(micro.get("particle_density_kg_m3", 1500.0)),
    )
    settling = np.clip(settling, 0.005, 0.15)

    coag = coagulation_yield_factor(
        yield_base, humidity_rh, cl_peak,
        ref_rh=micro.get("coagulation_ref_rh", 50.0),
        coag_rate=float(micro.get("coagulation_rate", 0.0012)),
    )
    alpha_scale = np.clip(1.0 / np.sqrt(growth), 0.75, 1.1)

    return AerosolState(
        diameter_um=d_eff,
        settling_velocity_m_s=settling,
        yield_factor=coag,
        alpha_scale=alpha_scale,
        coagulation_factor=coag / np.maximum(yield_base, 1e-9),
        hygroscopic_growth=growth,
    )
