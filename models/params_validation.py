"""Parameter bound validation before Monte Carlo execution.

MATURITY: Preliminary Model — runtime guard against out-of-literature inputs.
"""

from __future__ import annotations

from typing import Any


class ParameterValidationError(ValueError):
    pass


def _check_range(name: str, spec: dict[str, float], lo_key: str = "min", hi_key: str = "max") -> None:
    lo, hi = spec[lo_key], spec[hi_key]
    if lo > hi:
        raise ParameterValidationError(f"{name}: min ({lo}) > max ({hi})")


def validate_params(params: dict[str, Any]) -> None:
    """Assert literature-bound parameter structure before simulation."""
    g = params["grenade"]
    _check_range("filler_mass_g", g["filler_mass_g"])
    _check_range("burn_rate_g_s", g["burn_rate_g_s"])
    _check_range("yield_factor", g["yield_factor"])

    if g["burn_rate_g_s"]["max"] > 6.2:
        raise ParameterValidationError("burn_rate_g_s.max exceeds AN-M8 upper literature bound — document override")

    cloud = params["cloud"]
    _check_range("build_up_time_s", cloud["build_up_time_s"])
    _check_range("screening_area_sqft", cloud["screening_area_sqft"])

    env = params["environment"]
    _check_range("wind_speed_mph", env["wind_speed_mph"])
    _check_range("temperature_c", env["temperature_c"])
    _check_range("humidity_rh_pct", env["humidity_rh_pct"])

    for band in ("VIS", "NIR", "MWIR"):
        spec = params["extinction_coefficient_m2_per_g"][band]
        if spec["low"] <= 0 or spec["high"] < spec["low"]:
            raise ParameterValidationError(f"alpha {band}: invalid bounds")

    moe = params["moe"]
    if not 0.0 < moe["transmittance_threshold"] < 1.0:
        raise ParameterValidationError("transmittance_threshold must be in (0, 1)")
