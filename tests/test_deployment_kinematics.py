"""Deployment kinematics — KPP-07/08 human factors."""

from __future__ import annotations

import numpy as np
from models.cloud_physics.deployment_kinematics import resolve_deployment_state


def test_throw_p10_meets_kpp8_under_mc() -> None:
    rng = np.random.default_rng(4242)
    params = {
        "phase2": {"deployment": {"throw_range_m": {"min": 20, "max": 25}}},
        "human_factors": {
            "throw_range_m": {"min": 20, "max": 25},
            "load_penalty": {"range_reduction_m": 1.0, "lateral_error_multiplier": 1.12},
            "stress": {"lateral_error_multiplier": 1.25},
            "posture": {"standing_fraction": 0.55, "kneeling_fraction": 0.35},
        },
    }
    state = resolve_deployment_state(rng, 50_000, params)
    p10 = float(np.percentile(state.throw_range_m, 10))
    assert p10 >= 20.0, f"p10 throw {p10:.2f} m below KPP-8"
    assert np.min(state.fuze_delay_s) >= 0.7
    assert np.max(state.fuze_delay_s) <= 2.0
