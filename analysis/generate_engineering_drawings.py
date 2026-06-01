#!/usr/bin/env python3
"""Dimensioned engineering figures — addresses VISUAL_CONCEPT_ASSESSMENT gaps."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.system.envelope import derive_envelope, in_to_mm, load_form_factor  # noqa: E402

OUT = ROOT / "analysis" / "figures" / "form_factor" / "engineering"
BASE = json.loads((ROOT / "data" / "baseline_grenades.json").read_text(encoding="utf-8"))


def _dim_arrow(ax, x: float, y0: float, y1: float, label: str, xoff: float = 0) -> None:
    ax.annotate("", xy=(x + xoff, y1), xytext=(x + xoff, y0),
                arrowprops=dict(arrowstyle="<->", color="black", lw=1.0))
    ax.text(x + xoff + 3, (y0 + y1) / 2, label, va="center", fontsize=8, rotation=90)


def plot_scale_comparison_v2() -> Path:
    v2 = load_form_factor("v2_kpp")
    items = [
        ("M83 TA", BASE["grenades"]["M83"], "#a0aec0"),
        ("AN-M8 HC", BASE["grenades"]["AN-M8"], "#718096"),
        ("MS-V v2 (KPP)", {
            "length_in": v2["ms_v"]["body"]["length_in"],
            "diameter_in": v2["ms_v"]["body"]["diameter_in"],
            "weight_g": v2["ms_v"]["mass_g"],
        }, "#2b6cb0"),
    ]
    fig, ax = plt.subplots(figsize=(12, 6), facecolor="white")
    x = 0.0
    gap = 18.0
    max_h = 0.0
    for name, g, color in items:
        h = in_to_mm(g["length_in"])
        w = in_to_mm(g["diameter_in"])
        max_h = max(max_h, h)
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, 0), w, h, boxstyle="round,pad=0.4,rounding_size=1.5",
            facecolor=color, edgecolor="black", alpha=0.88, linewidth=1.2,
        ))
        ax.text(x + w / 2, h + 6, name, ha="center", fontweight="bold", fontsize=9)
        ax.text(
            x + w / 2, h / 2,
            f'{g["length_in"]}" × {g["diameter_in"]}"\n{g["weight_g"]} g',
            ha="center", va="center", fontsize=8,
            color="white" if color == "#2b6cb0" else "black",
        )
        _dim_arrow(ax, x + w + 4, 0, h, f'{g["length_in"]}"')
        x += w + gap

    ax.set_xlim(-5, x)
    ax.set_ylim(-10, max_h + 40)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("True-scale envelope comparison — MS-V v2 KPP vs inventory smoke", fontweight="bold")
    fig.text(0.5, 0.02, "Dimensioned parametric — NOT VALIDATION · Source: TM 43-0001-29 + Annex B KPP-01/09",
             ha="center", fontsize=8, style="italic")
    fig.tight_layout()
    p = OUT / "scale_comparison_v2_inventory.png"
    fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return p


def plot_envelope_tracks() -> Path:
    v2 = load_form_factor("v2_kpp")
    v3 = load_form_factor("v3_existing_container")
    tracks = [
        ("v2 KPP target\n850 g · VIS+NIR+MWIR", v2, "#2b6cb0"),
        ("v3 existing container\n680 g · filler-only Δ", v3, "#38a169"),
    ]
    fig, ax = plt.subplots(figsize=(11, 5.5), facecolor="white")
    x = 0.0
    for title, spec, color in tracks:
        body = spec["ms_v"]["body"]
        h = in_to_mm(body["length_in"])
        w = in_to_mm(body["diameter_in"])
        ax.add_patch(Rectangle((x, 0), w, h, facecolor=color, alpha=0.35, ec="black", lw=1.5))
        ax.text(x + w / 2, h / 2, title, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + w / 2, -8, f'{body["length_in"]}" × {body["diameter_in"]}"', ha="center", fontsize=8)
        x += w + 25

    an = BASE["grenades"]["AN-M8"]
    w = in_to_mm(an["diameter_in"])
    h = in_to_mm(an["length_in"])
    ax.add_patch(Rectangle((x, 0), w, h, facecolor="#718096", alpha=0.35, ec="black", lw=1.5, linestyle="--"))
    ax.text(x + w / 2, h / 2, "AN-M8\n(reference)", ha="center", va="center", fontsize=8)
    ax.set_xlim(-5, x + w + 10)
    ax.set_ylim(-20, in_to_mm(7.1) + 30)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Design tracks — do not conflate v2 KPP with v3 production reuse", fontweight="bold")
    fig.tight_layout()
    p = OUT / "envelope_tracks_v2_vs_v3.png"
    fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return p


def plot_exploded() -> Path:
    spec = load_form_factor("v2_kpp")
    env = derive_envelope(spec)
    fuze = spec["ms_v"]["fuze"]
    od = env.outer_diameter_mm
    fig, ax = plt.subplots(figsize=(12, 7), facecolor="white")
    ax.set_xlim(0, 420)
    ax.set_ylim(0, 220)
    ax.axis("off")
    ax.set_title("Exploded assembly — MS-V v2 (parametric)", fontweight="bold")

    parts = [
        (320, 150, od * 0.22, fuze["stack_height_mm"], "M201A1\nFUZE", "#cbd5e0"),
        (280, 130, od * 0.35, 12, "ADAPTER", "#a0aec0"),
        (180, 60, od, env.outer_length_mm - fuze["stack_height_mm"], "BODY\n(sheet steel)", "#b8c4b0"),
        (200, 80, env.inner_diameter_mm, env.inner_length_mm * 0.7, "BISPECTRAL\nFILLER", "#7b6b9a"),
        (140, 170, 8, 8, "TOP PORT\n(×4)", "#4a5568"),
        (140, 55, 8, 8, "BOTTOM\nPORT", "#4a5568"),
    ]
    for x, y, w, h, label, color in parts:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, ec="black", lw=1))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=7, fontweight="bold")

    ax.text(50, 180, "VIS + NIR + MWIR\nemission via ports", fontsize=9, color="#553c9a", fontweight="bold")
    ax.annotate("", xy=(300, 165), xytext=(250, 165), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.annotate("", xy=(240, 125), xytext=(270, 145), arrowprops=dict(arrowstyle="->", lw=1.2))
    fig.text(0.5, 0.02, "NOT VALIDATION — interfaces per M201A1 smoke grenade family", ha="center", fontsize=8, style="italic")
    fig.tight_layout()
    p = OUT / "ms_v_exploded_assembly.png"
    fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return p


def plot_cutaway_dimensioned() -> Path:
    spec = load_form_factor("v2_kpp")
    env = derive_envelope(spec)
    fuze_h = spec["ms_v"]["fuze"]["stack_height_mm"]
    wall = spec["ms_v"]["body"]["wall_thickness_mm"]
    od = env.outer_diameter_mm
    length = env.outer_length_mm
    id_ = env.inner_diameter_mm

    fig, axes = plt.subplots(1, 2, figsize=(12, 8), facecolor="white")
    ax_sec, ax_full = axes

    ax_sec.set_xlim(-od * 0.1, od * 1.15)
    ax_sec.set_ylim(-length * 0.05, length * 1.05)
    ax_sec.set_aspect("equal")
    ax_sec.axis("off")
    ax_sec.set_title("Section — v2 KPP envelope", fontweight="bold")

    ax_sec.add_patch(Rectangle((0, 0), od / 2, length, fill=False, ec="black", lw=2))
    ax_sec.add_patch(Rectangle((wall, fuze_h), id_ / 2, env.inner_length_mm, fc="#d8dee8", ec="#2b6cb0"))
    ax_sec.add_patch(Rectangle((wall + 1, fuze_h + 4), id_ / 2 - 2, env.inner_length_mm - 8,
                               fc="#7b6b9a", ec="#4a3f63"))
    ax_sec.add_patch(Rectangle((od * 0.12, length - fuze_h), od * 0.26, fuze_h, fc="#cbd5e0", ec="black"))
    _dim_arrow(ax_sec, od / 2 + 8, 0, length, f'{spec["ms_v"]["body"]["length_in"]}"')
    ax_sec.annotate("", xy=(od + 6, 0), xytext=(od + 6, od),
                    arrowprops=dict(arrowstyle="<->", lw=1))
    ax_sec.text(od + 10, od / 2, f'{spec["ms_v"]["body"]["diameter_in"]}"', va="center", fontsize=8)

    ax_full.set_xlim(-od * 0.4, od * 0.4)
    ax_full.set_ylim(-length * 0.05, length * 1.08)
    ax_full.set_aspect("equal")
    ax_full.axis("off")
    ax_full.set_title("Full view + spectrum", fontweight="bold")
    ax_full.add_patch(Rectangle((-od / 2, 0), od, length - fuze_h, fc="#b8c4b0", ec="black", lw=2))
    ax_full.add_patch(Wedge((0, length - 2), od * 0.18, 20, 160, fc="#a0aec0", ec="black"))
    for i, band in enumerate(["VIS", "NIR", "MWIR"]):
        ax_full.text(od / 2 + 12, length * (0.75 - i * 0.08), f"● {band}", fontsize=9, color="#553c9a")

    fig.text(0.5, 0.02, f'{env.internal_chamber_cm3:.0f} cm³ chamber · ~{env.fill_volume_cm3:.0f} cm³ fill target · NOT VALIDATION',
             ha="center", fontsize=8, style="italic")
    fig.tight_layout()
    p = OUT / "ms_v_cutaway_dimensioned.png"
    fig.savefig(p, dpi=220, bbox_inches="tight")
    plt.close(fig)
    return p


def plot_stencil_guide() -> Path:
    spec = load_form_factor("v2_kpp")
    body = spec["ms_v"]["body"]
    fig, ax = plt.subplots(figsize=(8, 10), facecolor="white")
    od = in_to_mm(body["diameter_in"])
    length = in_to_mm(body["length_in"])
    ax.add_patch(Rectangle((-od / 2, 0), od, length, fc="#b8c4b0", ec="black", lw=2))
    fields = [
        (0.78, "GRENADE, HAND: SMOKE, OBSCURANT", 7),
        (0.68, "MS-V VEIL", 11),
        (0.55, "MULTISPECTRAL (VIS/NIR/MWIR)", 7),
        (0.42, "1.3G  [HAZARD CLASS TBD]", 7),
        (0.30, "NSN XXXX-XX-XXX-XXXX [TBD]", 7),
        (0.18, "LOT XXXX", 8),
        (0.08, "MFG / CAGE [TBD]", 7),
    ]
    for yf, text, sz in fields:
        ax.text(0, length * yf, text, ha="center", fontsize=sz, fontfamily="DejaVu Sans Mono", fontweight="bold")
    ax.set_xlim(-od, od)
    ax.set_ylim(-length * 0.05, length * 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Stencil layout guide (DRAFT — requires AMCCOM / TM review)", fontweight="bold")
    fig.text(0.5, 0.02, "Do not use for production marking without ordnance packaging authority review",
             ha="center", fontsize=8, style="italic", color="#c53030")
    fig.tight_layout()
    p = OUT / "ms_v_stencil_layout_guide.png"
    fig.savefig(p, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return p


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        plot_scale_comparison_v2(),
        plot_envelope_tracks(),
        plot_exploded(),
        plot_cutaway_dimensioned(),
        plot_stencil_guide(),
    ]
    for p in paths:
        print(f"Wrote {p}")


if __name__ == "__main__":
    main()
