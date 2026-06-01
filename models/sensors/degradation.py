"""Sensor degradation models — FPV visible + NIR + MWIR/LWIR thermal surrogates.

MATURITY: Preliminary Model (v4 band-integrated)
NOT validation against specific UAS systems.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import yaml


def load_sensor_params(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[2]
    path = root / "models" / "sensors" / "params.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _band_transmittance(alpha: np.ndarray, cl: np.ndarray) -> np.ndarray:
    return np.exp(-np.maximum(alpha, 0.0) * np.maximum(cl, 0.0))


def visible_contrast_fraction(
    alpha_vis: np.ndarray,
    cl: np.ndarray,
    visual_smoke_factor: float | np.ndarray,
) -> np.ndarray:
    """Usable visible contrast fraction after combined MS-V + visual smoke (1 = clear)."""
    t = _band_transmittance(alpha_vis, cl)
    vsf = np.asarray(visual_smoke_factor)
    t_eff = np.power(np.clip(t, 1e-12, 1.0), vsf)
    return np.clip(1.0 - t_eff, 0.0, 1.0)


def spectral_contrast_fraction(alpha: np.ndarray, cl: np.ndarray) -> np.ndarray:
    """Contrast fraction for NIR or MWIR/LWIR band (1 = clear)."""
    t = _band_transmittance(alpha, cl)
    return np.clip(1.0 - t, 0.0, 1.0)


def moe_fused_degraded_mask(
    alpha_vis: np.ndarray,
    alpha_nir: np.ndarray,
    alpha_mwir: np.ndarray,
    cl: np.ndarray,
    *,
    visual_smoke_factor: float | np.ndarray = 1.3,
    contrast_threshold: float = 0.15,
) -> np.ndarray:
    """
    MoE: FPV/fiber-optic surrogate — VIS (boosted) + NIR + MWIR all obscured.

    Degraded when usable contrast >= contrast_threshold in all required bands.
    Equivalent to T < (1 - contrast_threshold) per band with VIS boost applied.
    """
    vis_c = visible_contrast_fraction(alpha_vis, cl, visual_smoke_factor)
    nir_c = spectral_contrast_fraction(alpha_nir, cl)
    mwir_c = spectral_contrast_fraction(alpha_mwir, cl)
    return (vis_c >= contrast_threshold) & (nir_c >= contrast_threshold) & (mwir_c >= contrast_threshold)


def uncooled_thermal_degraded(
    alpha_lwir: np.ndarray,
    cl: np.ndarray,
    contrast_threshold: float = 0.15,
) -> np.ndarray:
    """Uncooled LWIR path degraded when contrast above threshold."""
    c = spectral_contrast_fraction(alpha_lwir, cl)
    return c >= contrast_threshold


def cooled_thermal_degraded(
    alpha_mwir: np.ndarray,
    cl: np.ndarray,
    contrast_threshold: float = 0.15,
) -> np.ndarray:
    """Cooled MWIR path degraded when contrast above threshold."""
    c = spectral_contrast_fraction(alpha_mwir, cl)
    return c >= contrast_threshold


def sensor_diagnostics(
    alpha_vis: np.ndarray,
    alpha_nir: np.ndarray,
    alpha_mwir: np.ndarray,
    cl: np.ndarray,
    visual_smoke_factor: float | np.ndarray,
) -> dict[str, float]:
    """Median diagnostics for manifests."""
    vis_c = visible_contrast_fraction(alpha_vis, cl, visual_smoke_factor)
    nir_c = spectral_contrast_fraction(alpha_nir, cl)
    mwir_c = spectral_contrast_fraction(alpha_mwir, cl)
    return {
        "vis_contrast_p50": float(np.median(vis_c)),
        "nir_contrast_p50": float(np.median(nir_c)),
        "mwir_contrast_p50": float(np.median(mwir_c)),
    }
