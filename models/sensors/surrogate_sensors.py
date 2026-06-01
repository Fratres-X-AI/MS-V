"""Surrogate sensor models for Phase 1 MoE studies.

Representative FPV visible and thermal channels — not specific threat systems.
"""

from __future__ import annotations

from models.cloud_physics.extinction import effective_obscuration


def fpv_visible_degraded(
    alpha_vis: float,
    cl_g_m2: float,
    visual_smoke_factor: float = 1.0,
    threshold: float = 0.15,
) -> bool:
    """FPV visible channel degraded if combined VIS obscuration effective."""
    t_vis_eff = min(t_vis ** visual_smoke_factor, 1.0)
    return t_vis_eff < threshold


def thermal_degraded(
    alpha_mwir: float,
    cl_g_m2: float,
    threshold: float = 0.15,
) -> bool:
    """Uncooled/cooled thermal degraded if MWIR obscuration effective."""
    return effective_obscuration(alpha_mwir, cl_g_m2, threshold)


def fused_eoir_degraded(
    alpha_vis: float,
    alpha_mwir: float,
    cl_g_m2: float,
    visual_smoke_factor: float = 1.0,
    threshold: float = 0.15,
) -> bool:
    """FPV/fiber-optic MoE: both visible and thermal channels degraded."""
    vis_ok = fpv_visible_degraded(alpha_vis, cl_g_m2, visual_smoke_factor, threshold)
    ir_ok = thermal_degraded(alpha_mwir, cl_g_m2, threshold)
    return vis_ok and ir_ok
