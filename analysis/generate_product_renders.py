#!/usr/bin/env python3
"""RADR-style product renders — studio camo grenade, side + pull-ring top view."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.system.envelope import derive_envelope, load_form_factor  # noqa: E402
from models.system.product_mesh import build_ms_v_product_mesh, mesh_bounds  # noqa: E402

OUT = ROOT / "analysis" / "figures" / "form_factor" / "renders"
STUDIO_BG = "#8f8f8f"

CAMO_PALETTE = np.array([
    [0.28, 0.31, 0.22],
    [0.34, 0.36, 0.25],
    [0.42, 0.40, 0.28],
    [0.24, 0.26, 0.20],
    [0.48, 0.45, 0.32],
    [0.31, 0.33, 0.27],
])


def _digital_camo_rgb(centroids: np.ndarray, light: np.ndarray) -> np.ndarray:
    x, y, z = centroids.T
    u = np.mod(np.floor(x / 7.0) + np.floor(z * 0.35), 6).astype(int)
    v = np.mod(np.floor(y / 5.0) + np.floor(x * 0.08), 6).astype(int)
    idx = (u + 2 * v) % len(CAMO_PALETTE)
    base = CAMO_PALETTE[idx]
    intensity = np.clip(centroids @ light, 0.55, 1.0)[:, np.newaxis]
    return np.clip(base * intensity, 0, 1)


def _face_centroids(mesh) -> np.ndarray:
    return np.array([mesh.vertices[tri].mean(axis=0) for tri in mesh.faces])


def _draw_product_mesh(ax, mesh, light_vec: np.ndarray) -> None:
    polys = [mesh.vertices[tri] for tri in mesh.faces]
    colors = _digital_camo_rgb(_face_centroids(mesh), light_vec)
    coll = Poly3DCollection(polys, facecolors=colors, edgecolors=(0, 0, 0, 0), linewidths=0)
    ax.add_collection3d(coll)
    xmin, xmax, ymin, ymax, zmin, zmax = mesh_bounds(mesh)
    pad = 8
    ax.set_xlim(xmin - pad, xmax + pad)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_zlim(zmin - pad, zmax + pad)


def _draw_shadow_ellipse(ax, mesh, *, alpha: float = 0.22) -> None:
    xmin, xmax, ymin, ymax, zmin, _zmax = mesh_bounds(mesh)
    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2
    rx = (xmax - xmin) * 0.42
    ry = (ymax - ymin) * 0.55
    z = zmin - 2
    theta = np.linspace(0, 2 * np.pi, 80)
    xs = cx + rx * np.cos(theta)
    ys = cy + ry * np.sin(theta)
    zs = np.full_like(xs, z)
    ax.plot(xs, ys, zs, color=(0.15, 0.15, 0.15, alpha), linewidth=8, solid_capstyle="round")


def _stencil_text(ax, x: float, y: float, z: float, text: str, *, size: int = 14) -> None:
    ax.text(
        x, y, z, text,
        color="#c5c9bc",
        fontsize=size,
        fontfamily="DejaVu Sans Mono",
        fontweight="bold",
        ha="center",
        va="center",
        zorder=10,
    )


def render_side_profile(ax, mesh, env, spec) -> None:
    light = np.array([-0.55, -0.25, 0.80])
    light /= np.linalg.norm(light)
    _draw_shadow_ellipse(ax, mesh)
    _draw_product_mesh(ax, mesh, light)
    xmin, xmax, ymin, ymax, zmin, zmax = mesh_bounds(mesh)
    cx = (xmin + xmax) / 2
    _stencil_text(ax, cx, ymax + 2.5, (zmin + zmax) / 2 + 4, "MS-V VEIL")
    ax.view_init(elev=12, azim=-88)
    ax.set_axis_off()
    ax.set_box_aspect([2.4, 0.8, 0.8])
    ax.set_title(
        f"{spec['ms_v']['body']['length_in']}\" × {spec['ms_v']['body']['diameter_in']}\" · "
        f"AN-M8 envelope",
        fontsize=9, color="#ececec", pad=0,
    )


def render_pull_top(ax, spec) -> None:
    env = derive_envelope(spec)
    r_outer = env.outer_diameter_mm / 2.0
    r_cap = spec["ms_v"]["fuze"]["outer_diameter_mm"] / 2.0

    ax.set_facecolor(STUDIO_BG)
    ax.set_aspect("equal")
    ax.axis("off")

    # Outer body rim
    ax.add_patch(patches.Circle((0, 0), r_outer, facecolor="#4f5446", edgecolor="#2f3128", lw=1.2))
    ax.add_patch(patches.Circle((0, 0), r_outer - 2.5, facecolor="#5a5f52", edgecolor="#3a3d34", lw=0.8))
    ax.add_patch(patches.Circle((0, 0), r_cap + 1.5, facecolor="#666a5e", edgecolor="#3f4238", lw=0.8))
    ax.add_patch(patches.Circle((0, 0), r_cap, facecolor="#575b50", edgecolor="#33352f", lw=0.6))

    # Red pull ring (M201-style)
    ring_w = r_cap * 0.22
    ring_h = r_cap * 1.35
    round_r = ring_w * 0.35
    pull = patches.FancyBboxPatch(
        (-ring_w / 2, -ring_h * 0.15),
        ring_w, ring_h * 0.95,
        boxstyle=f"round,pad=0.02,rounding_size={round_r}",
        facecolor="#d62828",
        edgecolor="#8b1a1a",
        linewidth=1.0,
        zorder=5,
    )
    ax.add_patch(pull)
    handle = patches.FancyBboxPatch(
        (-ring_w * 0.75, ring_h * 0.55),
        ring_w * 1.5, ring_w * 1.15,
        boxstyle=f"round,pad=0.02,rounding_size={ring_w * 0.4}",
        facecolor="#d62828",
        edgecolor="#8b1a1a",
        linewidth=1.0,
        zorder=5,
    )
    ax.add_patch(handle)

    ax.text(0, -r_cap * 0.42, "PULL", ha="center", va="center",
            color="#c5c9bc", fontsize=11, fontfamily="DejaVu Sans Mono", fontweight="bold")
    ax.set_xlim(-r_outer * 1.25, r_outer * 1.25)
    ax.set_ylim(-r_outer * 1.25, r_outer * 1.25)


def render_product_sheet(out: Path) -> Path:
    spec = load_form_factor()
    env = derive_envelope(spec)
    mesh = build_ms_v_product_mesh()

    fig = plt.figure(figsize=(12, 5.5), facecolor=STUDIO_BG)
    ax_side = fig.add_subplot(121, projection="3d", facecolor=STUDIO_BG)
    ax_top = fig.add_subplot(122, facecolor=STUDIO_BG)

    render_side_profile(ax_side, mesh, env, spec)
    render_pull_top(ax_top, spec)

    fig.text(
        0.5, 0.03,
        "Concept render — parametric · NOT VALIDATION · M201A1-compatible fuze",
        ha="center", color="#e8e8e8", fontsize=8, style="italic",
    )
    fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.08, wspace=0.06)

    path = out / "ms_v_product_sheet.png"
    fig.savefig(path, dpi=240, facecolor=STUDIO_BG, bbox_inches="tight")
    plt.close(fig)
    return path


def render_product_hero(out: Path) -> Path:
    spec = load_form_factor()
    env = derive_envelope(spec)
    mesh = build_ms_v_product_mesh()

    fig = plt.figure(figsize=(11, 4.8), facecolor=STUDIO_BG)
    ax = fig.add_subplot(111, projection="3d", facecolor=STUDIO_BG)
    render_side_profile(ax, mesh, env, spec)
    ax.view_init(elev=8, azim=-92)
    fig.text(
        0.5, 0.04,
        "MS-V Veil — multispectral squad obscurant · same form factor as AN-M8 HC",
        ha="center", color="#ececec", fontsize=9,
    )
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0.06)

    path = out / "ms_v_product_hero.png"
    fig.savefig(path, dpi=260, facecolor=STUDIO_BG, bbox_inches="tight")
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [render_product_sheet(OUT), render_product_hero(OUT)]
    for p in paths:
        print(f"Wrote {p}")


if __name__ == "__main__":
    main()
