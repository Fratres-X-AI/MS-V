"""FPV visible + thermal sensor degradation models (Phase 1B scaffold).

Planned v4 sensor path — replaces scalar transmittance threshold with
band-integrated response curves. NOT YET wired to sim/engine.py.

See analysis/REMEDIATION_PLAN.md §1B-2.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from models.cloud_physics.extinction import transmittance


@dataclass
class SensorParams:
    """Placeholder — populate from models/sensors/params.yaml in 1B-2."""

    vis_wavelengths_um: tuple[float, ...] = (0.45, 0.55, 0.65)
    vis_weights: tuple[float, ...] = (0.3, 0.4, 0.3)
    mwir_wavelengths_um: tuple[float, ...] = (3.5, 4.5, 5.0)
    mwir_weights: tuple[float, ...] = (0.25, 0.5, 0.25)
    contrast_threshold: float = 0.15  # minimum usable contrast fraction
    netd_mk: float = 50.0  # uncooled surrogate


def band_integrated_transmittance(
    wavelengths_um: np.ndarray,
    weights: np.ndarray,
    alpha_by_band: np.ndarray,
    cl_g_m2: float,
) -> float:
    """Integrate T(λ) = exp(-α(λ)·CL) over surrogate band."""
    w = weights / np.sum(weights)
    t = np.exp(-alpha_by_band * cl_g_m2)
    return float(np.dot(w, t))


def fpv_visible_contrast_fraction(
    alpha_vis: float,
    cl_g_m2: float,
    visual_smoke_factor: float = 1.0,
) -> float:
    """Usable contrast fraction in FPV band (1 = clear, 0 = no contrast)."""
    t = transmittance(alpha_vis, cl_g_m2)
    t_eff = t ** max(visual_smoke_factor, 1.0)
    return max(0.0, 1.0 - t_eff)


def thermal_contrast_fraction(alpha_mwir: float, cl_g_m2: float) -> float:
    """Surrogate thermal contrast fraction from MWIR transmittance."""
    t = transmittance(alpha_mwir, cl_g_m2)
    return max(0.0, 1.0 - t)


def fused_degraded(
    alpha_vis: float,
    alpha_mwir: float,
    cl_g_m2: float,
    visual_smoke_factor: float = 1.0,
    contrast_threshold: float = 0.15,
) -> bool:
    """MoE: both FPV visible and thermal contrast below usable threshold."""
    vis_c = fpv_visible_contrast_fraction(alpha_vis, cl_g_m2, visual_smoke_factor)
    ir_c = thermal_contrast_fraction(alpha_mwir, cl_g_m2)
    return vis_c >= (1.0 - contrast_threshold) and ir_c >= (1.0 - contrast_threshold)
