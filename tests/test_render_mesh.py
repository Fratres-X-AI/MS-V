"""Tests for 3D render mesh generation."""

from __future__ import annotations

import pytest
from models.system.envelope import derive_envelope, load_form_factor
from models.system.render_mesh import build_an_m8_mesh, build_ms_v_mesh, translate_mesh


def test_ms_v_mesh_has_vertices_and_faces() -> None:
    mesh = build_ms_v_mesh(segments=24)
    assert len(mesh.vertices) > 100
    assert len(mesh.faces) > 100


def test_ms_v_matches_an_m8_outer_envelope() -> None:
    spec = load_form_factor("v3_existing_container")
    env = derive_envelope(spec)
    mesh = build_an_m8_mesh(segments=24)
    assert mesh.vertices[:, 2].max() == pytest.approx(env.outer_length_mm, rel=1e-4)


def test_translate_mesh_offsets() -> None:
    mesh = build_an_m8_mesh(segments=16)
    cx = mesh.vertices[:, 0].mean()
    moved = translate_mesh(mesh, 50.0, 0.0, 0.0)
    assert moved.vertices[:, 0].mean() == pytest.approx(cx + 50.0, rel=1e-4)
