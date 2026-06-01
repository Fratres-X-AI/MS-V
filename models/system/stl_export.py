"""Export parametric MS-V body as binary STL (cylinder + fuze shoulder)."""

from __future__ import annotations

import json
import math
import struct
from pathlib import Path

import numpy as np
from models.system.envelope import derive_envelope, in_to_mm, load_form_factor


def _cylinder_mesh(
    radius: float,
    z0: float,
    z1: float,
    segments: int = 48,
) -> tuple[np.ndarray, np.ndarray]:
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

    return verts, np.array(faces, dtype=np.int32)


def _write_binary_stl(path: Path, vertices: np.ndarray, faces: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tris = []
    for a, b, c in faces:
        v0, v1, v2 = vertices[a], vertices[b], vertices[c]
        n = np.cross(v1 - v0, v2 - v0)
        norm = np.linalg.norm(n)
        n = n / norm if norm > 1e-12 else np.array([0.0, 0.0, 1.0])
        tris.append((n, v0, v1, v2))

    with path.open("wb") as f:
        header = (b"MS-V parametric body - NOT VALIDATION").ljust(80, b" ")[:80]
        f.write(header)
        f.write(struct.pack("<I", len(tris)))
        for n, v0, v1, v2 in tris:
            f.write(struct.pack("<3f", *n.astype(np.float32)))
            f.write(struct.pack("<3f", *v0.astype(np.float32)))
            f.write(struct.pack("<3f", *v1.astype(np.float32)))
            f.write(struct.pack("<3f", *v2.astype(np.float32)))
            f.write(struct.pack("<H", 0))


def export_ms_v_stl(out_path: Path, *, segments: int = 64) -> Path:
    spec = load_form_factor()
    env = derive_envelope(spec)
    fuze = spec["ms_v"]["fuze"]

    r_body = env.outer_diameter_mm / 2.0
    r_fuze = fuze["outer_diameter_mm"] / 2.0
    z_top = env.outer_length_mm
    z_shoulder = fuze["stack_height_mm"]

    v1, f1 = _cylinder_mesh(r_body, 0.0, z_top - z_shoulder, segments)
    v2, f2 = _cylinder_mesh(r_fuze, z_top - z_shoulder, z_top, segments)
    offset = len(v1)
    _write_binary_stl(out_path, np.vstack([v1, v2]), np.vstack([f1, f2 + offset]))
    return out_path


def export_comparison_stl(out_dir: Path) -> dict[str, Path]:
    spec = load_form_factor()
    body = spec["ms_v"]["body"]
    an_m8 = json.loads(
        (Path(__file__).resolve().parents[2] / "data" / "baseline_grenades.json").read_text(
            encoding="utf-8",
        ),
    )["grenades"]["AN-M8"]
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    def _one(name: str, length_in: float, dia_in: float, x_offset: float) -> None:
        r = in_to_mm(dia_in) / 2.0
        z1 = in_to_mm(length_in)
        v, f = _cylinder_mesh(r, 0.0, z1)
        v = v + np.array([x_offset, 0.0, 0.0])
        p = out_dir / f"{name}.stl"
        _write_binary_stl(p, v, f)
        paths[name] = p

    _one("ms_v_body", body["length_in"], body["diameter_in"], 0.0)
    _one("an_m8_reference", an_m8["length_in"], an_m8["diameter_in"], 100.0)
    return paths
