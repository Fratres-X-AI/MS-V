"""Burn and aerosol yield model for MS-V obscurant grenade.

Links filler mass to burn duration and aerosol production.
STATUS: Literature-order-of-magnitude — UNVALIDATED against MS-V fill.

MS-V uses density-optimized sustained burn — NOT AN-M8 HC rate envelope.
All bounds live in params.yaml with traceability to filler mass / duration design.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def sample_filler_mass_g(rng: np.random.Generator, n: int, spec: dict[str, float]) -> np.ndarray:
    return rng.uniform(spec["min"], spec["max"], size=n)


def sample_burn_rate_g_s(
    rng: np.random.Generator,
    n: int,
    spec: dict[str, float],
    temp_c: np.ndarray | None = None,
    temp_spec: dict[str, float] | None = None,
) -> np.ndarray:
    """Mass consumption rate (g/s). MS-V formulation targets slow sustained burn."""
    rate = rng.uniform(spec["min"], spec["max"], size=n)
    if temp_c is not None and temp_spec is not None:
        ref = temp_spec.get("reference_c", 20.0)
        coeff = temp_spec.get("rate_increase_per_c", 0.002)
        rate *= 1.0 + (temp_c - ref) * coeff
        rate = np.maximum(rate, spec["min"] * 0.5)
    return rate


def raw_burn_duration_s(filler_mass_g: np.ndarray, burn_rate_g_s: np.ndarray) -> np.ndarray:
    return filler_mass_g / np.maximum(burn_rate_g_s, 1e-6)


def aerosol_mass_g(
    filler_mass_g: np.ndarray,
    yield_factor: np.ndarray,
    n_grenades: int = 1,
    overlap_efficiency: float = 0.85,
) -> np.ndarray:
    """Total aerosol mass available; multi-grenade with overlap penalty."""
    total_fill = filler_mass_g * n_grenades * overlap_efficiency
    return total_fill * yield_factor


def sample_yield_factor(
    rng: np.random.Generator,
    n: int,
    spec: dict[str, float],
    humidity_rh: np.ndarray | None = None,
    humidity_penalty: dict[str, float] | None = None,
) -> np.ndarray:
    """Fraction of fill converted to airborne obscurant aerosol."""
    y = rng.uniform(spec["min"], spec["max"], size=n)
    if humidity_rh is not None and humidity_penalty is not None:
        # High humidity can agglomerate particles — modest yield reduction (pessimistic).
        rh_ref = humidity_penalty.get("reference_rh_pct", 50.0)
        coeff = humidity_penalty.get("loss_per_rh_pct", 0.0015)
        y *= 1.0 - np.maximum(humidity_rh - rh_ref, 0.0) * coeff
        y = np.clip(y, spec["min"] * 0.5, spec["max"])
    return y


def load_burn_spec(params: dict[str, Any]) -> dict[str, Any]:
    g = params["grenade"]
    return {
        "filler": g["filler_mass_g"],
        "burn_rate": g["burn_rate_g_s"],
        "yield_factor": g["yield_factor"],
        "overlap_efficiency": g.get("overlap_efficiency", 0.85),
        "temp": params.get("environment", {}).get("temperature_burn_coupling", {}),
        "humidity_yield": params.get("environment", {}).get("humidity_yield_penalty", {}),
    }
