"""Tests for RADR-style product render outputs."""

from __future__ import annotations

from pathlib import Path

from models.system.product_mesh import build_ms_v_product_mesh, mesh_bounds


def test_product_mesh_horizontal_extent() -> None:
    mesh = build_ms_v_product_mesh(segments=24)
    xmin, xmax, ymin, ymax, zmin, zmax = mesh_bounds(mesh)
    assert xmax - xmin > ymax - ymin
    assert len(mesh.faces) > 50


def test_product_renders_write_files(tmp_path: Path, monkeypatch) -> None:
    import analysis.generate_product_renders as gpr

    monkeypatch.setattr(gpr, "OUT", tmp_path)
    gpr.main()
    assert (tmp_path / "ms_v_product_sheet.png").exists()
    assert (tmp_path / "ms_v_product_hero.png").stat().st_size > 5000
