"""Phase 2 physics pipeline — composes microphysics, structure, atmosphere, spectral.

STATUS: Literature-parameter sensitivity — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from models.cloud_physics.aerosol_microphysics import resolve_aerosol_state
from models.cloud_physics.atmospheric_coupling import resolve_atmospheric_modifiers
from models.cloud_physics.burn_dynamics import resolve_burn_profile
from models.cloud_physics.burn_model import aerosol_mass_g
from models.cloud_physics.cloud_structure import resolve_cloud_structure
from models.cloud_physics.deployment_kinematics import resolve_deployment_state
from models.cloud_physics.geometry_settling import resolve_threat_geometry_cl
from models.cloud_physics.layered_plumes import (
    diurnal_contrast_factor,
    hc_band_cl_vis,
    layered_band_cls,
    ms_v_band_cl,
)
from models.cloud_physics.spectral_extinction import (
    effective_alphas_per_band,
    multiple_scatter_correction,
)


@dataclass
class Phase2PhysicsResult:
    cl_center_ms_v: np.ndarray
    cl_vis: np.ndarray
    cl_nir: np.ndarray
    cl_mwir: np.ndarray
    alpha_vis: np.ndarray
    alpha_nir: np.ndarray
    alpha_mwir: np.ndarray
    settling_velocity_m_s: np.ndarray
    raw_burn_duration_s: np.ndarray
    build_up_delay_s: np.ndarray
    duration_washout_factor: np.ndarray
    post_burn_duration_boost: np.ndarray
    diurnal_mwir_factor: np.ndarray
    deployment: object
    geom: object | None
    diagnostics: dict[str, float] = field(default_factory=dict)


def run_phase2_physics(
    rng: np.random.Generator,
    n: int,
    params: dict,
    *,
    filler_mass_g: np.ndarray,
    burn_rate_base: np.ndarray,
    yield_base: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    temp_c: np.ndarray,
    humidity_rh: np.ndarray,
    n_grenades: int,
    n_hc: int,
    apply_threat_geometry: bool = True,
) -> Phase2PhysicsResult:
    """Full Phase 2 physics stack → centerline and threat-band CL."""
    p1b = params.get("phase1b", {})
    g = params["grenade"]

    deployment = resolve_deployment_state(rng, n, params)
    burn = resolve_burn_profile(filler_mass_g, burn_rate_base, params)

    # First-pass CL for coagulation feedback
    aerosol_pre = aerosol_mass_g(
        filler_mass_g, yield_base, n_grenades, g.get("overlap_efficiency", 0.85),
    )
    cl_pre = ms_v_band_cl(
        aerosol_pre, area_m2 * deployment.area_scale, depth_m,
        wind_mph, humidity_rh,
        dilution=np.ones(n), generation_factor=np.ones(n),
    )

    aerosol = resolve_aerosol_state(
        rng, n, params, yield_base=yield_base, humidity_rh=humidity_rh, cl_peak=cl_pre,
    )
    aerosol_mass = aerosol_mass_g(
        filler_mass_g, aerosol.yield_factor, n_grenades, g.get("overlap_efficiency", 0.85),
    )

    structure = resolve_cloud_structure(
        rng, n, params,
        area_m2=area_m2 * deployment.area_scale,
        depth_m=depth_m + deployment.initial_height_m * 0.15,
        wind_mph=wind_mph, temp_c=temp_c,
        burn_rate_g_s=burn.burn_rate_effective_g_s,
        n_grenades=n_grenades,
        throw_offsets_m=np.abs(deployment.throw_offset_m),
    )
    atm = resolve_atmospheric_modifiers(rng, n, params, humidity_rh=humidity_rh, temp_c=temp_c, wind_mph=wind_mph)

    dilution = structure.dilution_factor * atm.stability_mixing_factor
    cl_center = ms_v_band_cl(
        aerosol_mass, structure.area_m2, structure.depth_m,
        wind_mph, humidity_rh,
        dilution=dilution, generation_factor=burn.generation_rate_factor,
    )

    hc_yield = rng.uniform(
        p1b.get("hc_yield_factor", {}).get("min", 0.28),
        p1b.get("hc_yield_factor", {}).get("max", 0.48),
        size=n,
    )
    hc_mass = np.full(n, p1b.get("hc_grenade_fill_g", 539.0) * n_hc) * hc_yield
    cl_hc = hc_band_cl_vis(
        hc_mass, structure.area_m2, structure.depth_m,
        wind_mph, humidity_rh,
        hc_width_factor=float(p1b.get("hc_plume_width_factor", 1.35)),
        dilution=dilution,
    )
    cl_vis_c, cl_nir_c, cl_mwir_c = layered_band_cls(cl_center, cl_hc)

    alphas = effective_alphas_per_band(
        rng, n, params, diameter_um=aerosol.diameter_um, alpha_scale=aerosol.alpha_scale,
    )
    alpha_vis = alphas["VIS"][1] * atm.extinction_humidity_factor
    alpha_nir = alphas["NIR"][1] * atm.extinction_humidity_factor
    alpha_mwir = alphas["MWIR"][1] * atm.extinction_humidity_factor

    ms_vis = multiple_scatter_correction(cl_vis_c, alpha_vis)
    ms_nir = multiple_scatter_correction(cl_nir_c, alpha_nir)
    ms_mwir = multiple_scatter_correction(cl_mwir_c, alpha_mwir)
    alpha_vis = alpha_vis * ms_vis
    alpha_nir = alpha_nir * ms_nir
    alpha_mwir = alpha_mwir * ms_mwir

    diurnal = diurnal_contrast_factor(
        rng, n, temp_c, params.get("phase2", {}).get("diurnal", {}),
    )

    geom = None
    cl_vis, cl_nir, cl_mwir = cl_vis_c, cl_nir_c, cl_mwir_c
    if apply_threat_geometry and p1b:
        p1b_geo = dict(p1b)
        p1b_geo.setdefault("throw_offset_m", {"min": 0.0, "max": 4.0})
        geom = resolve_threat_geometry_cl(
            rng, n, p1b_geo,
            cl_center_ms_v=cl_center,
            hc_aerosol_g=hc_mass,
            area_m2=structure.area_m2,
            depth_m=structure.depth_m,
            wind_mph=wind_mph,
            humidity_rh=humidity_rh,
            n_grenades=n_grenades,
        )
        cl_vis = geom.cl_vis_combined
        cl_nir = geom.cl_nir
        cl_mwir = geom.cl_mwir * diurnal

    post_boost = 1.0 + burn.tail_fraction * float(
        params.get("phase2", {}).get("burn_dynamics", {}).get("post_burn_dissipate_boost", 0.35),
    )

    def pct(x: np.ndarray, q: float) -> float:
        return float(np.percentile(x, q))

    humidity_alpha_chain = aerosol.alpha_scale * atm.extinction_humidity_factor
    diag = {
        "psd_diameter_um_p50": pct(aerosol.diameter_um, 50),
        "settling_velocity_p50_m_s": pct(aerosol.settling_velocity_m_s, 50),
        "hygroscopic_growth_p50": pct(aerosol.hygroscopic_growth, 50),
        "humidity_alpha_chain_p50": pct(humidity_alpha_chain, 50),
        "extinction_humidity_factor_p50": pct(atm.extinction_humidity_factor, 50),
        "coagulation_factor_p50": pct(aerosol.coagulation_factor, 50),
        "wind_shear_dilution_p50": pct(structure.dilution_factor, 50),
        "merge_factor_p50": pct(structure.merge_factor, 50),
        "buoyancy_rise_p50_m": pct(structure.buoyancy_rise_m, 50),
        "washout_active_fraction": float(np.mean(atm.precipitation_active)),
        "throw_range_p50_m": pct(deployment.throw_range_m, 50),
        "fuze_delay_p50_s": pct(deployment.fuze_delay_s, 50),
    }

    return Phase2PhysicsResult(
        cl_center_ms_v=cl_center,
        cl_vis=cl_vis,
        cl_nir=cl_nir,
        cl_mwir=cl_mwir,
        alpha_vis=alpha_vis,
        alpha_nir=alpha_nir,
        alpha_mwir=alpha_mwir,
        settling_velocity_m_s=aerosol.settling_velocity_m_s,
        raw_burn_duration_s=burn.raw_duration_s,
        build_up_delay_s=burn.ignition_delay_s + deployment.fuze_delay_s,
        duration_washout_factor=atm.duration_washout_factor,
        post_burn_duration_boost=post_boost,
        diurnal_mwir_factor=diurnal,
        deployment=deployment,
        geom=geom,
        diagnostics=diag,
    )
