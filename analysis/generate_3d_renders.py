#!/usr/bin/env python3
"""Generate shaded 3D renders of MS-V (AN-M8-matched envelope) vs inventory baseline."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.system.envelope import derive_envelope, load_form_factor  # noqa: E402
from models.system.render_mesh import (  # noqa: E402
    build_an_m8_mesh,
    build_ms_v_mesh,
    face_normals,
    translate_mesh,
)

OUT = ROOT / "analysis" / "figures" / "form_factor" / "renders"


def _face_rgba(mesh, base_rgb: tuple[float, float, float], ls: LightSource, alpha: float = 1.0):
    normals = face_normals(mesh)
    intensity = np.clip(normals @ np.array(ls.direction), 0.35, 1.0)
    rgb = np.array(base_rgb) * intensity[:, np.newaxis]
    return np.column_stack([rgb, np.full(len(rgb), alpha)])


def _mesh_polys(mesh) -> list[np.ndarray]:
    return [mesh.vertices[tri] for tri in mesh.faces]


def _draw_mesh(ax, mesh, base_rgb, ls, alpha=1.0, edgecolor=(0.15, 0.15, 0.15, 0.25)):
    polys = _mesh_polys(mesh)
    colors = _face_rgba(mesh, base_rgb, ls, alpha)
    coll = Poly3DCollection(polys, facecolors=colors, edgecolors=edgecolor, linewidths=0.15)
    ax.add_collection3d(coll)
    xs, ys, zs = mesh.vertices.T
    ax.set_xlim(xs.min() - 10, xs.max() + 10)
    ax.set_ylim(ys.min() - 10, ys.max() + 10)
    ax.set_zlim(zs.min() - 5, zs.max() + 10)


def _style_axes(ax, title: str) -> None:
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.view_init(elev=22, azim=-58)
    ax.set_box_aspect([1, 1, 1.6])


def render_isometric_ms_v(out: Path) -> Path:
    spec = load_form_factor()
    env = derive_envelope(spec)
    mesh = build_ms_v_mesh()
    ls = LightSource(azdeg=225, altdeg=55)

    fig = plt.figure(figsize=(7, 9))
    ax = fig.add_subplot(111, projection="3d")
    _draw_mesh(ax, mesh, (0.22, 0.45, 0.72), ls)
    _style_axes(
        ax,
        f"MS-V — {spec['ms_v']['body']['length_in']}\" × {spec['ms_v']['body']['diameter_in']}\" "
        f"({env.outer_length_mm:.0f} × {env.outer_diameter_mm:.0f} mm)",
    )
    fig.text(
        0.5, 0.02,
        "Parametric render — AN-M8 matched envelope · NOT VALIDATION",
        ha="center", fontsize=8, style="italic",
    )
    fig.tight_layout()
    path = out / "ms_v_isometric.png"
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_comparison(out: Path) -> Path:
    spec = load_form_factor()
    ms_v = build_ms_v_mesh()
    an_m8 = build_an_m8_mesh()
    offset = ms_v.vertices[:, 0].max() + 25
    an_m8 = translate_mesh(an_m8, offset, 0.0, 0.0)

    ls = LightSource(azdeg=225, altdeg=55)
    fig = plt.figure(figsize=(11, 7))
    ax = fig.add_subplot(111, projection="3d")
    _draw_mesh(ax, ms_v, (0.22, 0.45, 0.72), ls)
    _draw_mesh(ax, an_m8, (0.55, 0.58, 0.62), ls)

    ax.text(
        ms_v.vertices[:, 0].mean(), ms_v.vertices[:, 1].max() + 8, ms_v.vertices[:, 2].max() + 6,
        "MS-V (proposed)", ha="center", fontsize=9, fontweight="bold", color="#2b6cb0",
    )
    ax.text(
        an_m8.vertices[:, 0].mean(), an_m8.vertices[:, 1].max() + 8, an_m8.vertices[:, 2].max() + 6,
        "AN-M8 HC (inventory)", ha="center", fontsize=9, fontweight="bold", color="#4a5568",
    )

    _style_axes(ax, "Same outer envelope — MS-V vs AN-M8 HC")
    fig.text(
        0.5, 0.02,
        f"Matched to {spec['envelope']['match_baseline']} outer dimensions (TM 43-0001-29)",
        ha="center", fontsize=8, style="italic",
    )
    fig.tight_layout()
    path = out / "ms_v_vs_an_m8_isometric.png"
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def render_ortho_views(out: Path) -> Path:
    mesh = build_ms_v_mesh()
    ls = LightSource(azdeg=225, altdeg=55)
    views = [
        ("Front", 0, 0),
        ("Side", 0, 90),
        ("Isometric", 22, -58),
    ]
    fig = plt.figure(figsize=(12, 4.5))
    for i, (name, elev, azim) in enumerate(views, 1):
        ax = fig.add_subplot(1, 3, i, projection="3d")
        _draw_mesh(ax, mesh, (0.22, 0.45, 0.72), ls)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(name, fontsize=10, fontweight="bold")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_box_aspect([1, 1, 1.6])
    spec = load_form_factor()
    fig.suptitle(
        f"MS-V orthographic views — {spec['ms_v']['body']['length_in']}\" × "
        f"{spec['ms_v']['body']['diameter_in']}\"",
        fontsize=11, fontweight="bold",
    )
    fig.tight_layout()
    path = out / "ms_v_ortho_views.png"
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        render_isometric_ms_v(OUT),
        render_comparison(OUT),
        render_ortho_views(OUT),
    ]
    for p in paths:
        print(f"Wrote {p}")


if __name__ == "__main__":
    main()
