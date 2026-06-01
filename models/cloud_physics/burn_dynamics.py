"""Burn dynamics — multi-phase pyrotechnic burn and aerosol generation rate.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class BurnProfile:
    burn_rate_effective_g_s: np.ndarray
    raw_duration_s: np.ndarray
    ignition_delay_s: np.ndarray
    generation_rate_factor: np.ndarray
    tail_fraction: np.ndarray


def three_phase_burn_rate(
    burn_base: np.ndarray,
    *,
    ignition_boost: float = 1.35,
    tail_reduction: float = 0.72,
    ignition_frac: float = 0.08,
    tail_frac: float = 0.15,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Ignition / steady / tail phases → effective mean burn rate and tail fraction.
    """
    rate = burn_base * (1.0 - ignition_frac - tail_frac) + burn_base * (
        ignition_frac * ignition_boost + tail_frac * tail_reduction
    )
    tail_f = np.full_like(burn_base, tail_frac)
    return rate, tail_f


def aerosol_generation_rate_factor(
    burn_rate: np.ndarray,
    *,
    ramp_s: float = 3.0,
    peak_g_s: float = 4.0,
) -> np.ndarray:
    """Generation not instantaneous — ramp to peak in first few seconds."""
    return np.clip(burn_rate / peak_g_s, 0.65, 1.15) * (1.0 - 0.08 * np.exp(-burn_rate / ramp_s))


def post_burn_dilution_duration_factor(
    tail_fraction: np.ndarray,
    *,
    dissipate_s: float = 25.0,
    boost: float = 0.35,
) -> np.ndarray:
    """After fuel exhaustion, residual cloud provides partial screening."""
    return 1.0 + tail_fraction * boost


def resolve_burn_profile(
    filler_mass_g: np.ndarray,
    burn_base_g_s: np.ndarray,
    params: dict,
) -> BurnProfile:
    spec = params.get("phase2", {}).get("burn_dynamics", {})
    rate, tail = three_phase_burn_rate(
        burn_base_g_s,
        ignition_boost=float(spec.get("ignition_boost", 1.35)),
        tail_reduction=float(spec.get("tail_reduction", 0.72)),
        ignition_frac=float(spec.get("ignition_fraction", 0.08)),
        tail_frac=float(spec.get("tail_fraction", 0.15)),
    )
    gen = aerosol_generation_rate_factor(rate)
    raw = filler_mass_g / np.maximum(rate, 0.01)
    ign_delay = np.full_like(rate, float(spec.get("ignition_delay_s", 0.4)))
    return BurnProfile(
        burn_rate_effective_g_s=rate,
        raw_duration_s=raw,
        ignition_delay_s=ign_delay,
        generation_rate_factor=gen,
        tail_fraction=tail,
    )
