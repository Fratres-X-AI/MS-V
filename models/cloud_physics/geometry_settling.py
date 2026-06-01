"""Phase 1B — cloud geometry, settling, combined MS-V + HC plumes, threat LOS.

Edge-of-plume threat geometry: radial CL falloff + partial LOS + wind advection.
STATUS: Literature-parameter sensitivity — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ThreatGeometryResult:
    """CL and diagnostics at threat sensor LOS (not cloud center)."""

    cl_ms_v: np.ndarray
    cl_hc_vis: np.ndarray
    cl_vis_combined: np.ndarray
    cl_nir: np.ndarray
    cl_mwir: np.ndarray
    throw_offset_m: np.ndarray
    threat_standoff_m: np.ndarray
    plume_center_offset_m: np.ndarray
    threat_distance_m: np.ndarray
    radial_fraction_ms_v: np.ndarray
    radial_fraction_hc: np.ndarray
    los_cloud_fraction: np.ndarray
    edge_of_plume: np.ndarray
    in_plume_core: np.ndarray


def sample_throw_offset_m(
    rng: np.random.Generator,
    n: int,
    offset_spec: dict[str, float],
    *,
    signed: bool = True,
) -> np.ndarray:
    """Grenade aim error — lateral offset magnitude of plume center from corridor (m)."""
    mag = rng.uniform(offset_spec["min"], offset_spec["max"], size=n)
    if not signed:
        return mag
    sign = rng.choice(np.array([-1.0, 1.0]), size=n)
    return mag * sign


def sample_threat_orbit_fraction(
    rng: np.random.Generator,
    n: int,
    orbit_spec: dict[str, float],
) -> np.ndarray:
    """
    Threat LOS pierce point as fraction of plume radius (0 = axis, 1 = edge, >1 = outside).

    UAS tracks along the employment corridor; orbit samples where the LOS cuts the plume cross-section.
    """
    return rng.uniform(orbit_spec["min"], orbit_spec["max"], size=n)


def wind_plume_shift_m(wind_mph: np.ndarray, max_shift_m: float) -> np.ndarray:
    """Downwind displacement of plume center from aim point."""
    return (wind_mph / 15.0) * max_shift_m


def screening_radius_m(area_m2: np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(area_m2, 0.01) / np.pi)


def radial_cl_fraction(
    threat_distance_m: np.ndarray,
    plume_radius_m: np.ndarray,
    edge_exponent: float,
) -> np.ndarray:
    """Gaussian radial CL falloff from plume center (1 at core, →0 at edge and beyond)."""
    r_norm = threat_distance_m / np.maximum(plume_radius_m, 0.5)
    return np.exp(-edge_exponent * r_norm * r_norm)


def los_cloud_fraction(
    threat_distance_m: np.ndarray,
    plume_radius_m: np.ndarray,
) -> np.ndarray:
    """
    Partial horizontal LOS through circular plume cross-section (chord fraction).

    At core = 1; at edge = partial; outside = 0 (clear sightline).
    """
    r = threat_distance_m
    r_cap = np.maximum(plume_radius_m, 0.5)
    outside = r >= r_cap
    x = np.clip(r / r_cap, 0.0, 0.999)
    chord = np.sqrt(np.clip(1.0 - x * x, 0.0, 1.0))
    return np.where(outside, 0.0, chord)


def plume_coverage_fraction(
    throw_offset_m: np.ndarray,
    screening_radius_m: np.ndarray,
    wind_mph: np.ndarray,
    n_grenades: int,
    *,
    wind_penalty: float = 0.45,
) -> np.ndarray:
    """Legacy scalar coverage — prefer resolve_threat_geometry_cl for Phase 1B."""
    radius = np.maximum(screening_radius_m, 0.5)
    base = np.clip(1.0 - throw_offset_m / (radius * 2.5), 0.15, 1.0)
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * wind_penalty, 0.35, 1.0)
    multi = 1.0 + 0.12 * max(n_grenades - 1, 0)
    return np.clip(base * wind_factor * multi, 0.08, 1.0)


def hc_smoke_aerosol_mass_g(
    n_hc_grenades: int,
    hc_fill_g: float,
    yield_factor: np.ndarray,
) -> np.ndarray:
    return np.full_like(yield_factor, hc_fill_g * n_hc_grenades) * yield_factor


def plume_cl_at_center(
    ms_v_cl_peak: np.ndarray,
    hc_aerosol_g: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Peak CL at cloud center (before threat radial geometry)."""
    wind_factor = np.clip(1.0 - (wind_mph / 15.0) * 0.45, 0.45, 1.0)
    humidity_factor = 1.0 + (humidity_rh - 50.0) / 100.0 * 0.08
    denom = np.maximum(area_m2 * depth_m, 0.01)
    cl_hc_vis = (hc_aerosol_g / denom) * wind_factor * humidity_factor
    return ms_v_cl_peak, cl_hc_vis


def combined_plume_cl(
    ms_v_cl_peak: np.ndarray,
    hc_aerosol_g: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
    hc_alpha_vis: np.ndarray,
    coverage: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Legacy combined CL with scalar coverage (v5.0). Use resolve_threat_geometry_cl in v6."""
    _ = hc_alpha_vis
    cl_hc = plume_cl_at_center(ms_v_cl_peak, hc_aerosol_g, area_m2, depth_m, wind_mph, humidity_rh)[1]
    cl_ms_v = ms_v_cl_peak * coverage
    cl_combined_vis = cl_ms_v + cl_hc
    return cl_ms_v, cl_hc, cl_combined_vis


def resolve_threat_geometry_cl(
    rng: np.random.Generator,
    n: int,
    p1b: dict,
    *,
    cl_center_ms_v: np.ndarray,
    hc_aerosol_g: np.ndarray,
    area_m2: np.ndarray,
    depth_m: np.ndarray,
    wind_mph: np.ndarray,
    humidity_rh: np.ndarray,
    n_grenades: int,
) -> ThreatGeometryResult:
    """
    Edge-of-plume threat geometry: CL at UAS LOS with radial falloff + partial LOS + wind shift.

    Threat at plume edge or outside sees reduced CL → MoE can fail (binds obscured metric).
    """
    radius = screening_radius_m(area_m2)
    multi_scale = 1.0 + 0.08 * max(n_grenades - 1, 0)
    radius_eff = radius * multi_scale
    spread = float(p1b.get("plume_spread_factor", 3.0))
    radius_geo = radius_eff * spread

    throw_off = sample_throw_offset_m(
        rng, n, p1b.get("throw_offset_m", {"min": 0.0, "max": 8.0}), signed=True,
    )
    orbit_frac = sample_threat_orbit_fraction(
        rng, n, p1b.get("threat_orbit_fraction", {"min": 0.0, "max": 1.05}),
    )
    wind_shift = wind_plume_shift_m(wind_mph, float(p1b.get("wind_plume_shift_max_m", 12.0)))
    plume_center = throw_off + wind_shift
    orbit_m = orbit_frac * radius_eff
    # Corridor-axis UAS LOS vs mis-aimed / wind-shifted plume center + cross-section pierce point
    threat_dist = np.sqrt(plume_center * plume_center + orbit_m * orbit_m)

    edge_exp = float(p1b.get("plume_edge_exponent", 2.2))
    hc_width = float(p1b.get("hc_plume_width_factor", 1.35))
    hc_edge_exp = float(p1b.get("hc_plume_edge_exponent", 1.6))

    ms_v_center, hc_center = plume_cl_at_center(
        cl_center_ms_v, hc_aerosol_g, area_m2, depth_m, wind_mph, humidity_rh,
    )

    rad_ms_v = radial_cl_fraction(threat_dist, radius_geo, edge_exp)
    rad_hc = radial_cl_fraction(threat_dist, radius_geo * hc_width, hc_edge_exp)
    los = los_cloud_fraction(threat_dist, radius_geo)
    # Radial profile sets concentration at pierce point; partial LOS scales grazing paths only
    outside = threat_dist >= radius_geo
    path_weight = np.where(outside, np.maximum(los, 0.08), 1.0)

    cl_ms_v = ms_v_center * rad_ms_v * path_weight
    cl_hc = hc_center * rad_hc * path_weight
    cl_vis = cl_ms_v + cl_hc

    r_norm = threat_dist / np.maximum(radius_geo, 0.5)
    edge = r_norm >= float(p1b.get("edge_radius_fraction", 0.75))
    in_core = r_norm <= float(p1b.get("core_radius_fraction", 0.35))

    return ThreatGeometryResult(
        cl_ms_v=cl_ms_v,
        cl_hc_vis=cl_hc,
        cl_vis_combined=cl_vis,
        cl_nir=cl_ms_v,
        cl_mwir=cl_ms_v,
        throw_offset_m=throw_off,
        threat_standoff_m=orbit_m,
        plume_center_offset_m=plume_center,
        threat_distance_m=threat_dist,
        radial_fraction_ms_v=rad_ms_v,
        radial_fraction_hc=rad_hc,
        los_cloud_fraction=los,
        edge_of_plume=edge,
        in_plume_core=in_core,
    )


def cl_at_time(
    cl_peak: np.ndarray,
    time_s: np.ndarray | float,
    build_up_s: np.ndarray,
    *,
    settling_velocity_m_s: float,
    depth_m: np.ndarray,
    ramp_exponent: float = 1.0,
) -> np.ndarray:
    t = np.asarray(time_s)
    if t.ndim == 0:
        t = np.full_like(cl_peak, float(t))
    exp = max(ramp_exponent, 0.1)
    during_ramp = t <= build_up_s
    ramp = cl_peak * np.power(np.clip(t / np.maximum(build_up_s, 0.1), 0.0, 1.0), exp)
    after = np.maximum(t - build_up_s, 0.0)
    decay = np.exp(-settling_velocity_m_s * after / np.maximum(depth_m, 0.1))
    uniform = cl_peak * decay
    return np.where(during_ramp, ramp, uniform)


def duration_until_cl_below_threshold(
    cl_peak: np.ndarray,
    cl_required: np.ndarray,
    build_up_s: np.ndarray,
    raw_burn_s: np.ndarray,
    time_at_threshold_s: np.ndarray,
    thickness_met: np.ndarray,
    *,
    settling_velocity_m_s: float,
    depth_m: np.ndarray,
) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        t_cross = build_up_s + (depth_m / max(settling_velocity_m_s, 1e-6)) * np.log(
            np.maximum(cl_peak / np.maximum(cl_required, 1e-12), 1.0)
        )
    t_end = np.minimum(raw_burn_s, t_cross)
    dur = np.maximum(t_end - time_at_threshold_s, 0.0)
    return np.where(thickness_met, dur, 0.0)


def friendly_thermal_blinded(
    cl_mwir: np.ndarray,
    cl_threshold_friendly: float,
) -> np.ndarray:
    return cl_mwir >= cl_threshold_friendly
