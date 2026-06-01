"""Operator / autopilot lock-break probability beyond transmittance threshold.

Literature-order surrogate — NOT VALIDATION.
"""

from __future__ import annotations

import numpy as np


def lock_break_probability(
    rng: np.random.Generator,
    t_vis: np.ndarray,
    t_nir: np.ndarray,
    t_mwir: np.ndarray,
    *,
    threshold: float,
    netd_floor: np.ndarray,
    contrast_scene: np.ndarray | None = None,
    require_all_bands: bool = True,
) -> np.ndarray:
    """
    Probabilistic lock-break: sharp logistic around effective contrast threshold.

    Returns boolean mask (True = lock broken / obscured).
    """
    eff = np.maximum(threshold, netd_floor)
    if contrast_scene is None:
        contrast_scene = np.ones_like(t_vis)

    margins = []
    for t in (t_vis, t_nir, t_mwir):
        p = 1.0 / (1.0 + np.exp(8.0 * (t / np.maximum(eff, 1e-6) - 1.0)))
        margins.append(p)

    stack = np.stack(margins, axis=1)
    if require_all_bands:
        p_combined = np.min(stack, axis=1)
    else:
        p_combined = np.max(stack, axis=1)

    return rng.uniform(0.0, 1.0, size=t_vis.shape[0]) < p_combined


def fiber_vs_rf_penalty(
    rng: np.random.Generator,
    n: int,
    spec: dict,
) -> np.ndarray:
    """Fiber-optic guided FPV — tighter coupling of VIS+MWIR (AND logic stricter)."""
    rf_frac = float(spec.get("rf_link_fraction", 0.35))
    is_rf = rng.uniform(0.0, 1.0, size=n) < rf_frac
    penalty = np.where(is_rf, float(spec.get("rf_relax_factor", 1.08)), 1.0)
    return penalty
