"""System-level kinematics facade — v2 envelope, throw, load effects.

Delegates physics to cloud_physics.deployment_kinematics; YAML authority in form_factor.yaml
and human_factors.yaml.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from models.cloud_physics.deployment_kinematics import resolve_deployment_state
from models.system.envelope import derive_envelope, load_form_factor, loadout_mass_g


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


def _params_with_stress_flag(params: dict[str, Any], stressed: bool) -> dict[str, Any]:
    """KPP-08 matrix uses stressed throw; nominal MC omits stress lateral multiplier."""
    p = copy.deepcopy(params)
    hf = p.setdefault("human_factors", {})
    stress = hf.setdefault("stress", {})
    if stressed:
        stress.setdefault("lateral_error_multiplier", 1.25)
    else:
        stress["lateral_error_multiplier"] = 1.0
    return p


def human_factors_summary(spec: dict | None = None) -> dict[str, Any]:
    """Design-authority human-factors inputs for reports (notional — NOT VALIDATION)."""
    spec = spec or load_form_factor("v2_kpp")
    hf_path = Path(__file__).resolve().parent / "human_factors.yaml"
    hf = yaml.safe_load(hf_path.read_text(encoding="utf-8"))
    return {
        "variant": spec.get("variant_key", "v2_kpp"),
        "mass_g": spec["ms_v"]["mass_g"],
        "throw_range_m": hf["throw_range_m"],
        "load_penalty": hf["load_penalty"],
        "posture": hf["posture"],
        "stress": hf["stress"],
        "loadout_2x_ms_v_kg": loadout_mass_g(spec, n_ms_v=2)["total_kg"],
        "rtm_job_kpp08": "baseline_10M_g3_n10000000",
        "matrix_ref": "rtm/verification_matrix.md#kpp--moe-summary",
    }


def throw_distribution(
    rng: np.random.Generator,
    n: int,
    *,
    stressed: bool = True,
    params: dict[str, Any] | None = None,
) -> dict[str, np.ndarray]:
    """Sample throw range and lateral offset for v2 employment (m)."""
    params = _params_with_stress_flag(params or _load_params(), stressed)
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
