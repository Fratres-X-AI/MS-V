"""System-level kinematics facade — v2 envelope, throw, load effects.

Delegates physics to cloud_physics.deployment_kinematics; YAML authority in form_factor.yaml
and human_factors.yaml.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import yaml
from models.cloud_physics.deployment_kinematics import resolve_deployment_state
from models.system.envelope import derive_envelope, load_form_factor


def load_v2_envelope():
    """v2 KPP envelope (850 g, 7.1 x 3.1 in)."""
    return derive_envelope(load_form_factor("v2_kpp"))


def _load_params(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[2]
    path = root / "models" / "cloud_physics" / "params.yaml"
    with path.open(encoding="utf-8") as f:
        params = yaml.safe_load(f)
    hf_path = root / "models" / "system" / "human_factors.yaml"
    with hf_path.open(encoding="utf-8") as f:
        params["human_factors"] = yaml.safe_load(f)
    return params


def throw_distribution(
    rng: np.random.Generator,
    n: int,
    *,
    stressed: bool = True,
    params: dict[str, Any] | None = None,
) -> dict[str, np.ndarray]:
    """Sample throw range and lateral offset for v2 employment (m)."""
    params = params or _load_params()
    state = resolve_deployment_state(rng, n, params)
    return {
        "throw_range_m": state.throw_range_m,
        "throw_offset_m": state.throw_offset_m,
        "initial_height_m": state.initial_height_m,
    }


def impact_dispersion_summary(
    *,
    n: int = 10_000,
    seed: int = 44,
    stressed: bool = True,
) -> dict[str, float]:
    """Percentiles for form-factor / CONOPS reports."""
    rng = np.random.default_rng(seed)
    dist = throw_distribution(rng, n, stressed=stressed)
    t = dist["throw_range_m"]
    lat = np.abs(dist["throw_offset_m"])
    return {
        "throw_p10_m": float(np.percentile(t, 10)),
        "throw_p50_m": float(np.percentile(t, 50)),
        "throw_p90_m": float(np.percentile(t, 90)),
        "lateral_p50_m": float(np.percentile(lat, 50)),
        "lateral_p90_m": float(np.percentile(lat, 90)),
        "n_samples": float(n),
        "stressed": stressed,
    }
