"""MS-V form-factor envelope — volume budget, pouch fit, load mass.

STATUS: Engineering estimate — NOT VALIDATION.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class EnvelopeDimensions:
    outer_length_mm: float
    outer_diameter_mm: float
    inner_length_mm: float
    inner_diameter_mm: float
    fill_volume_cm3: float
    internal_chamber_cm3: float
    fill_density_g_cm3: float


@dataclass(frozen=True)
class PouchFitResult:
    fits_width: bool
    fits_depth: bool
    fits_height: bool
    fits_mass: bool
    fits_all: bool
    clearance_width_mm: float
    clearance_depth_mm: float
    clearance_height_mm: float
    notes: str


def load_form_factor(root: Path | None = None) -> dict[str, Any]:
    root = root or Path(__file__).resolve().parents[2]
    path = root / "models" / "system" / "form_factor.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def in_to_mm(inches: float) -> float:
    return inches * 25.4


def derive_envelope(spec: dict[str, Any] | None = None) -> EnvelopeDimensions:
    """Volume-budget derivation tying fill mass to cylindrical envelope."""
    spec = spec or load_form_factor()
    body = spec["ms_v"]["body"]
    fuze = spec["ms_v"]["fuze"]
    filler = spec["ms_v"]["filler_mass_g"]
    dens = spec["ms_v"]["filler_density_g_cm3"]

    fill_g = (filler["min"] + filler["max"]) / 2.0
    rho = (dens["min"] + dens["max"]) / 2.0
    fill_vol_cm3 = fill_g / rho

    outer_l = in_to_mm(body["length_in"])
    outer_d = in_to_mm(body["diameter_in"])
    wall = body["wall_thickness_mm"]

    inner_d = outer_d - 2.0 * wall
    fuze_stack = fuze["stack_height_mm"]
    inner_l = outer_l - fuze_stack - wall

    r_cm = inner_d / 20.0
    h_cm = inner_l / 10.0
    chamber_cm3 = math.pi * r_cm * r_cm * h_cm

    return EnvelopeDimensions(
        outer_length_mm=outer_l,
        outer_diameter_mm=outer_d,
        inner_length_mm=inner_l,
        inner_diameter_mm=inner_d,
        fill_volume_cm3=fill_vol_cm3,
        internal_chamber_cm3=chamber_cm3,
        fill_density_g_cm3=rho,
    )


def check_pouch_fit(
    env: EnvelopeDimensions,
    mass_g: float,
    pouch: dict[str, Any],
) -> PouchFitResult:
    """Check cylindrical MS-V against rectangular pouch inner envelope."""
    w = pouch["inner_width_mm"]
    d = pouch["inner_depth_mm"]
    h = pouch["inner_height_mm"]
    max_m = pouch["max_recommended_mass_g"]

    od = env.outer_diameter_mm
    ol = env.outer_length_mm

    # Grenade stored vertically (length along pouch height) — typical MOLLE layout
    fits_h = ol <= h
    fits_w = od <= w
    fits_d = od <= d
    fits_m = mass_g <= max_m

    return PouchFitResult(
        fits_width=fits_w,
        fits_depth=fits_d,
        fits_height=fits_h,
        fits_mass=fits_m,
        fits_all=fits_w and fits_d and fits_h and fits_m,
        clearance_width_mm=w - od,
        clearance_depth_mm=d - od,
        clearance_height_mm=h - ol,
        notes=pouch.get("note", ""),
    )


def loadout_mass_g(spec: dict[str, Any], n_ms_v: int, n_hc: int = 0) -> dict[str, float]:
    lo = spec["loadout"]
    ms = lo["ms_v_mass_g"] * n_ms_v
    hc = lo["an_m8_mass_g"] * n_hc
    return {
        "ms_v_kg": ms / 1000.0,
        "visual_smoke_kg": hc / 1000.0,
        "total_kg": (ms + hc) / 1000.0,
    }
