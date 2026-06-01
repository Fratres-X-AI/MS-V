"""Deployment kinematics — throw dispersion, fuze timing, posture effects.

Literature-order surrogates — NOT VALIDATION.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class DeploymentState:
    throw_offset_m: np.ndarray
    throw_range_m: np.ndarray
    fuze_delay_s: np.ndarray
    initial_height_m: np.ndarray
    area_scale: np.ndarray


def throw_range_m(
    rng: np.random.Generator,
    n: int,
    spec: dict,
) -> np.ndarray:
    """850 g grenade throw range under stress (m)."""
    return rng.uniform(spec.get("min", 18.0), spec.get("max", 25.0), size=n)


def throw_lateral_dispersion_m(
    rng: np.random.Generator,
    n: int,
    throw_range_m: np.ndarray,
    spec: dict,
) -> np.ndarray:
    """Lateral error scales with range and posture."""
    frac = float(spec.get("lateral_error_fraction", 0.12))
    sign = rng.choice(np.array([-1.0, 1.0]), size=n)
    return sign * throw_range_m * frac * rng.uniform(0.3, 1.0, size=n)


def fuze_delay_s(
    rng: np.random.Generator,
    n: int,
    spec: dict,
) -> np.ndarray:
    """M201A1 fuze function timing variability."""
    return rng.uniform(spec.get("min", 0.7), spec.get("max", 2.0), size=n)


def posture_height_offset_m(
    rng: np.random.Generator,
    n: int,
    spec: dict,
) -> np.ndarray:
    """Prone vs standing throw affects initial cloud height."""
    return rng.uniform(spec.get("min", 0.3), spec.get("max", 1.4), size=n)


def resolve_deployment_state(
    rng: np.random.Generator,
    n: int,
    params: dict,
) -> DeploymentState:
    dep = params.get("phase2", {}).get("deployment", {})
    hf = params.get("human_factors", {})
    throw_spec = {**dep.get("throw_range_m", {}), **hf.get("throw_range_m", {})}
    load = hf.get("load_penalty", {})
    stress = hf.get("stress", {})
    posture_spec = hf.get("posture", {})

    t_range = throw_range_m(rng, n, throw_spec)
    t_range = np.maximum(t_range - float(load.get("range_reduction_m", 0.0)), throw_spec.get("min", 20.0))

    lat_spec = dep.get("lateral_dispersion", {})
    lat_frac = float(lat_spec.get("lateral_error_fraction", 0.12))
    lat_frac *= float(load.get("lateral_error_multiplier", 1.0))
    lat_frac *= float(stress.get("lateral_error_multiplier", 1.0))
    sign = rng.choice(np.array([-1.0, 1.0]), size=n)
    lat = sign * t_range * lat_frac * rng.uniform(0.3, 1.0, size=n)

    fuze = fuze_delay_s(rng, n, dep.get("fuze_delay_s", {"min": 0.7, "max": 2.0}))

    stand = float(posture_spec.get("standing_fraction", 0.55))
    kneel = float(posture_spec.get("kneeling_fraction", 0.35))
    prone = max(0.0, 1.0 - stand - kneel)
    posture_idx = rng.choice(3, size=n, p=[stand, kneel, prone])
    height_base = dep.get("posture_height_m", {"min": 0.3, "max": 1.4})
    h_min, h_max = float(height_base.get("min", 0.3)), float(height_base.get("max", 1.4))
    height = np.empty(n)
    height[posture_idx == 0] = rng.uniform(0.9 * h_max, h_max, size=int(np.sum(posture_idx == 0)))
    height[posture_idx == 1] = rng.uniform(0.55 * h_max, 0.85 * h_max, size=int(np.sum(posture_idx == 1)))
    height[posture_idx == 2] = rng.uniform(h_min, 0.45 * h_max, size=int(np.sum(posture_idx == 2)))

    area_scale = 1.0 + 0.008 * (t_range - 20.0)
    return DeploymentState(
        throw_offset_m=lat,
        throw_range_m=t_range,
        fuze_delay_s=fuze,
        initial_height_m=height,
        area_scale=np.clip(area_scale, 0.92, 1.12),
    )
