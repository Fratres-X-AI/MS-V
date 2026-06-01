"""Tests for Tier B form-factor envelope and STL export."""

from __future__ import annotations

from pathlib import Path

import pytest
from models.system.envelope import (
    check_pouch_fit,
    derive_envelope,
    load_form_factor,
    loadout_mass_g,
)
from models.system.stl_export import export_ms_v_stl


def test_envelope_volume_budget_consistent() -> None:
    env = derive_envelope()
    assert 600 <= env.fill_volume_cm3 <= 750
    assert env.internal_chamber_cm3 >= env.fill_volume_cm3 * 0.85


def test_pouch_fit_parametric() -> None:
    spec = load_form_factor()
    env = derive_envelope(spec)
    fit = check_pouch_fit(env, spec["ms_v"]["mass_g"], spec["pouch"])
    assert fit.fits_mass
    assert fit.clearance_height_mm >= 0


def test_loadout_mass_two_ms_v() -> None:
    spec = load_form_factor()
    lo = loadout_mass_g(spec, n_ms_v=2, n_hc=1)
    assert lo["ms_v_kg"] == 1.7
    assert lo["total_kg"] == pytest.approx(2.38, rel=0.01)


def test_stl_export_writes_file(tmp_path: Path) -> None:
    p = export_ms_v_stl(tmp_path / "test.stl")
    assert p.exists()
    assert p.stat().st_size > 1000
