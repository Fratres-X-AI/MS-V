"""Spectral extinction — band-internal α, Mie surrogate, multiple scatter.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

import numpy as np


def sample_band_internal_alpha(
    rng: np.random.Generator,
    n: int,
    band: str,
    params: dict,
    *,
    diameter_um: np.ndarray | None = None,
    alpha_scale: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Three-point α within band + Mie diameter scaling."""
    spec = params["extinction_coefficient_m2_per_g"][band]
    lo, mid, hi = spec["low"], spec["mid"], spec["high"]
    spread = (hi - lo) * 0.12
    mid_a = rng.uniform(mid - spread, mid + spread, size=n)

    if diameter_um is not None:
        d_ref = float(params.get("phase2", {}).get("spectral", {}).get("mie_d_ref_um", 2.0))
        mie = np.sqrt(np.clip(diameter_um / d_ref, 0.3, 4.0))
        mid_a = mid_a * mie

    if alpha_scale is not None:
        mid_a = mid_a * alpha_scale

    low_a = np.clip(mid_a - spread, lo, mid)
    high_a = np.clip(mid_a + spread, mid, hi)
    return low_a, mid_a, high_a


def multiple_scatter_correction(
    cl: np.ndarray,
    alpha: np.ndarray,
    *,
    onset_cl: float = 8.0,
    max_boost: float = 0.18,
) -> np.ndarray:
    """Dense cloud forward scatter reduces effective obscuration (α eff decrease)."""
    optical_depth = alpha * cl
    boost = np.clip((optical_depth - onset_cl) / onset_cl, 0.0, 1.0) * max_boost
    return np.clip(1.0 - boost, 0.82, 1.0)


def band_optical_depth(
    alpha: np.ndarray,
    cl: np.ndarray,
    ms_correction: np.ndarray,
) -> np.ndarray:
    return alpha * cl * ms_correction


def effective_alphas_per_band(
    rng: np.random.Generator,
    n: int,
    params: dict,
    *,
    diameter_um: np.ndarray,
    alpha_scale: np.ndarray,
) -> dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    out = {}
    for band in ("VIS", "NIR", "MWIR"):
        out[band] = sample_band_internal_alpha(
            rng, n, band, params, diameter_um=diameter_um, alpha_scale=alpha_scale,
        )
    return out
