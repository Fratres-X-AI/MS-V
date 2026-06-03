"""Tests for models/system/kinematics facade."""

from __future__ import annotations

import numpy as np
from models.system.envelope import load_form_factor
from models.system.kinematics import (
    human_factors_summary,
    impact_dispersion_summary,
    load_v2_envelope,
    throw_distribution,
)


def test_load_v2_envelope_matches_yaml() -> None:
    env = load_v2_envelope()
    spec = load_form_factor("v2_kpp")
    assert spec["ms_v"]["mass_g"] == 850
    assert env.outer_length_mm == 7.1 * 25.4
    assert env.outer_diameter_mm == 3.1 * 25.4


def test_human_factors_summary_v2_mass() -> None:
    hf = human_factors_summary()
    assert hf["mass_g"] == 850
    assert hf["throw_range_m"]["min"] == 20.0


def test_throw_distribution_stressed_p10_meets_kpp() -> None:
    rng = np.random.default_rng(123)
    dist = throw_distribution(rng, 5000, stressed=True)
    p10 = float(np.percentile(dist["throw_range_m"], 10))
    assert p10 >= 20.0


def test_impact_dispersion_summary_keys() -> None:
    stats = impact_dispersion_summary(n=2000, seed=1)
    assert stats["throw_p10_m"] >= 18.0
    assert stats["throw_p50_m"] <= 26.0
    assert stats["stressed"] is True
