"""Burn and aerosol yield model for MS-V obscurant grenade.

Links filler mass to burn duration and aerosol production.
STATUS: Literature-order-of-magnitude — UNVALIDATED against MS-V fill.
"""

from __future__ import annotations

import numpy as np


def sample_burn_rate_g_s(rng: np.random.Generator, n: int, low: float = 3.8, high: float = 6.2) -> np.ndarray:
    """Mass consumption rate (g/s). AN-M8: ~539g in 105-150s => ~3.6-5.1 g/s. MS-V slower burn for density."""
    return rng.uniform(low, high, size=n)


def raw_burn_duration_s(filler_mass_g: float, burn_rate_g_s: np.ndarray) -> np.ndarray:
    return filler_mass_g / burn_rate_g_s


def aerosol_mass_g(
    filler_mass_g: float,
    burn_rate_g_s: np.ndarray,
    yield_factor: np.ndarray,
    n_grenades: int = 1,
    overlap_efficiency: float = 0.85,
) -> np.ndarray:
    """Total aerosol mass available; multi-grenade with overlap penalty."""
    total_fill = filler_mass_g * n_grenades * overlap_efficiency
    return total_fill * yield_factor


def sample_yield_factor(rng: np.random.Generator, n: int, low: float = 0.22, high: float = 0.52) -> np.ndarray:
    """Fraction of fill converted to airborne obscurant aerosol."""
    return rng.uniform(low, high, size=n)
