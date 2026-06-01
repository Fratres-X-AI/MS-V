"""Parametric MS-V triangle mesh for 3D rendering (ports + fuze shoulder)."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from models.system.envelope import derive_envelope, load_form_factor


@dataclass(frozen=True)
class TriangleMesh:
    vertices: np.ndarray
    faces: np.ndarray


def _cylinder_mesh(
    radius: float,
    z0: float,
    z1: float,
    segments: int = 48,
) -> TriangleMesh:
    angles = np.linspace(0, 2 * math.pi, segments, endpoint=False)
    xs = radius * np.cos(angles)
    ys = radius * np.sin(angles)

    bottom = np.column_stack([xs, ys, np.full(segments, z0)])
    top = np.column_stack([xs, ys, np.full(segments, z1)])
    center_bot = np.array([[0.0, 0.0, z0]])
    center_top = np.array([[0.0, 0.0, z1]])
    verts = np.vstack([bottom, top, center_bot, center_top])

    faces: list[tuple[int, int, int]] = []
    for i in range(segments):
        j = (i + 1) % segments
        b0, b1 = i, j
        t0, t1 = i + segments, j + segments
        faces.append((b0, b1, t1))
        faces.append((b0, t1, t0))
        cb = 2 * segments
        ct = 2 * segments + 1
        faces.append((cb, b1, b0))
        faces.append((ct, t0, t1))

    return TriangleMesh(vertices=verts, faces=np.array(faces, dtype=np.int32))


def _merge(meshes: list[TriangleMesh]) -> TriangleMesh:
    verts: list[np.ndarray] = []
    faces: list[np.ndarray] = []
    offset = 0
    for mesh in meshes:
        verts.append(mesh.vertices)
        faces.append(mesh.faces + offset)
        offset += len(mesh.vertices)
    return TriangleMesh(vertices=np.vstack(verts), faces=np.vstack(faces))


def _translate(mesh: TriangleMesh, dx: float, dy: float, dz: float) -> TriangleMesh:
    return TriangleMesh(
        vertices=mesh.vertices + np.array([dx, dy, dz]),
        faces=mesh.faces.copy(),
    )


def build_ms_v_mesh(*, segments: int = 64) -> TriangleMesh:
    spec = load_form_factor()
    env = derive_envelope(spec)
    fuze = spec["ms_v"]["fuze"]
    ports = spec["ms_v"]["ports"]

    r_body = env.outer_diameter_mm / 2.0
    r_fuze = fuze["outer_diameter_mm"] / 2.0
    z_top = env.outer_length_mm
    z_shoulder = fuze["stack_height_mm"]
    r_port = ports["port_diameter_mm"] / 2.0

    body = _cylinder_mesh(r_body, 0.0, z_top - z_shoulder, segments)
    fuze_mesh = _cylinder_mesh(r_fuze, z_top - z_shoulder, z_top, segments)

    port_meshes: list[TriangleMesh] = []
    port_z = (z_top - z_shoulder) * 0.85
    for deg in (0, 90, 180, 270):
        rad = math.radians(deg)
        cx = (r_body - 1.5) * math.cos(rad)
        cy = (r_body - 1.5) * math.sin(rad)
        port = _cylinder_mesh(r_port, port_z - 6, port_z + 6, max(16, segments // 4))
        port_meshes.append(_translate(port, cx, cy, 0.0))

    bottom = _cylinder_mesh(r_port, 4, 14, max(16, segments // 4))
    return _merge([body, fuze_mesh, *port_meshes, bottom])


def build_an_m8_mesh(*, segments: int = 64) -> TriangleMesh:
    import json
    from pathlib import Path

    from models.system.envelope import in_to_mm

    root = Path(__file__).resolve().parents[2]
    an_m8 = json.loads((root / "data" / "baseline_grenades.json").read_text(encoding="utf-8"))[
        "grenades"
    ]["AN-M8"]
    r = in_to_mm(an_m8["diameter_in"]) / 2.0
    h = in_to_mm(an_m8["length_in"])
    return _cylinder_mesh(r, 0.0, h, segments)


def translate_mesh(mesh: TriangleMesh, dx: float, dy: float, dz: float) -> TriangleMesh:
    return _translate(mesh, dx, dy, dz)


def face_normals(mesh: TriangleMesh) -> np.ndarray:
    normals = []
    for a, b, c in mesh.faces:
        v0, v1, v2 = mesh.vertices[a], mesh.vertices[b], mesh.vertices[c]
        n = np.cross(v1 - v0, v2 - v0)
        norm = np.linalg.norm(n)
        normals.append(n / norm if norm > 1e-12 else np.array([0.0, 0.0, 1.0]))
    return np.array(normals)
