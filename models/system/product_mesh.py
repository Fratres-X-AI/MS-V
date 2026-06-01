"""MS-V product-style mesh — smoke grenade body for RADR-like renders."""

from __future__ import annotations

import numpy as np
from models.system.envelope import derive_envelope, load_form_factor
from models.system.render_mesh import TriangleMesh, _cylinder_mesh, _merge


def _rotate_z_to_x(mesh: TriangleMesh) -> TriangleMesh:
    v = mesh.vertices
    rotated = np.column_stack([v[:, 2], v[:, 1], -v[:, 0]])
    return TriangleMesh(vertices=rotated, faces=mesh.faces.copy())


def _ring_groove(
    x_center: float,
    radius: float,
    groove_depth_mm: float = 1.2,
    width_mm: float = 3.0,
    segments: int = 64,
) -> TriangleMesh:
    r_outer = radius + 0.6
    r_inner = radius - groove_depth_mm
    outer = _cylinder_mesh(r_outer, x_center - width_mm / 2, x_center + width_mm / 2, segments)
    inner = _cylinder_mesh(r_inner, x_center - width_mm / 2 - 0.1, x_center + width_mm / 2 + 0.1, segments)
    return _merge([outer, inner])


def build_ms_v_product_mesh(*, segments: int = 72) -> TriangleMesh:
    """Horizontal body (X = long axis) with fuze shoulder + groove rings."""
    spec = load_form_factor()
    env = derive_envelope(spec)
    fuze = spec["ms_v"]["fuze"]

    r_body = env.outer_diameter_mm / 2.0
    r_fuze = fuze["outer_diameter_mm"] / 2.0
    length = env.outer_length_mm
    fuze_len = fuze["stack_height_mm"]
    body_len = length - fuze_len

    body = _cylinder_mesh(r_body, 0.0, body_len, segments)
    fuze_mesh = _cylinder_mesh(r_fuze, body_len, length, segments)
    groove_a = _ring_groove(body_len - 10, r_body, segments=segments)
    groove_b = _ring_groove(body_len - 18, r_body, segments=segments)
    end_cap = _cylinder_mesh(r_body * 0.98, -1.5, 0.0, segments)

    mesh = _merge([body, fuze_mesh, groove_a, groove_b, end_cap])
    return _rotate_z_to_x(mesh)


def mesh_bounds(mesh: TriangleMesh) -> tuple[float, float, float, float, float, float]:
    xs, ys, zs = mesh.vertices.T
    return float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max()), float(zs.min()), float(zs.max())
