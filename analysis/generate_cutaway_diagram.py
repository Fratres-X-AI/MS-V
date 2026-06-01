#!/usr/bin/env python3
"""TM-style MS-V half-section cutaway (2D engineering diagram)."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.system.envelope import derive_envelope, load_form_factor  # noqa: E402

OUT = ROOT / "analysis" / "figures" / "form_factor" / "renders" / "ms_v_cutaway_half.png"


def _label(ax, x: float, y: float, text: str, tx: float, ty: float) -> None:
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(tx, ty),
        fontsize=9,
        fontweight="bold",
        ha="left",
        arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.0),
    )


def main() -> None:
    spec = load_form_factor()
    env = derive_envelope(spec)
    fuze_h = spec["ms_v"]["fuze"]["stack_height_mm"]
    wall = spec["ms_v"]["body"]["wall_thickness_mm"]

    # Scale: mm -> plot units (inches for title consistency)
    od = env.outer_diameter_mm
    length = env.outer_length_mm
    id_ = env.inner_diameter_mm
    inner_len = env.inner_length_mm

    fig, axes = plt.subplots(1, 2, figsize=(11, 8), facecolor="white")
    ax_sec, ax_full = axes

    # --- Section view (left) ---
    ax_sec.set_xlim(-od * 0.15, od * 1.05)
    ax_sec.set_ylim(-length * 0.08, length * 1.08)
    ax_sec.set_aspect("equal")
    ax_sec.axis("off")
    ax_sec.set_title("Sectional view — existing AN-M8 body", fontsize=11, fontweight="bold")

    # Outer wall (half section)
    ax_sec.add_patch(Rectangle((0, 0), od / 2, length, fill=False, ec="black", lw=2))
    ax_sec.add_patch(Rectangle((wall, fuze_h), id_ / 2, inner_len, fc="#d8dee8", ec="#2b6cb0", lw=1.2))
    # Filler
    ax_sec.add_patch(Rectangle((wall + 1, fuze_h + 4), id_ / 2 - 2, inner_len - 8, fc="#7b6b9a", ec="#4a3f63", lw=0.8))
    # Starter layer
    ax_sec.add_patch(Rectangle((wall + 1, fuze_h + inner_len - 18), id_ / 2 - 2, 12, fc="#e07a5f", ec="#9c4221", lw=0.8))
    # Fuze stack
    ax_sec.add_patch(Rectangle((od * 0.12, length - fuze_h), od * 0.26, fuze_h, fc="#cbd5e0", ec="black", lw=1))
    ax_sec.add_patch(Wedge((od * 0.25, length - fuze_h * 0.35), od * 0.12, 200, 340, fc="#a0aec0", ec="black", lw=0.8))
    # Bottom port
    ax_sec.add_patch(Rectangle((od * 0.08, 2), od * 0.06, 8, fc="#4a5568", ec="black"))
    # Top ports (section)
    for z in (length - fuze_h - 20, length - fuze_h - 35):
        ax_sec.add_patch(Rectangle((id_ / 2 - 2, z), 6, 5, fc="#4a5568", ec="black"))

    _label(ax_sec, od * 0.25, length - fuze_h * 0.5, "FUZE M201A1", od * 0.55, length - fuze_h * 0.2)
    _label(ax_sec, wall + id_ / 4, length - fuze_h - 8, "ADAPTER", od * 0.55, length - fuze_h - 15)
    _label(ax_sec, wall + id_ / 4, fuze_h + inner_len - 10, "STARTER\nMIXTURE", od * 0.55, fuze_h + inner_len - 5)
    _label(ax_sec, wall + id_ / 4, fuze_h + inner_len * 0.45, "MS-V BISPECTRAL\nFILLER", od * 0.55, fuze_h + inner_len * 0.55)
    _label(ax_sec, od / 2 - 1, length * 0.5, "STEEL\nBODY", od * 0.55, length * 0.65)
    _label(ax_sec, od * 0.11, 6, "BOTTOM\nPORT", od * 0.55, length * 0.08)

    ax_sec.plot([od / 2, od / 2], [0, length], "k--", lw=0.8, alpha=0.5)
    ax_sec.text(od / 2 + 2, length * 0.5, "CUT\nPLANE", fontsize=7, color="#555")

    # --- Full view (right) ---
    ax_full.set_xlim(-od * 0.35, od * 0.35)
    ax_full.set_ylim(-length * 0.05, length * 1.12)
    ax_full.set_aspect("equal")
    ax_full.axis("off")
    ax_full.set_title("Full view — MS-V in existing container", fontsize=11, fontweight="bold")

    body = mpatches.FancyBboxPatch(
        (-od / 2, 0), od, length - fuze_h,
        boxstyle="round,pad=0,rounding_size=2",
        facecolor="#b8c4b0", edgecolor="black", linewidth=2,
    )
    ax_full.add_patch(body)
    ax_full.add_patch(Rectangle((-spec["ms_v"]["fuze"]["outer_diameter_mm"] / 2, length - fuze_h),
                                spec["ms_v"]["fuze"]["outer_diameter_mm"], fuze_h,
                                fc="#cbd5e0", ec="black", lw=1.2))
    # Spoon
    spoon_x = [-od / 2 - 2, -od / 2 - 8, -od / 2 - 6, -od / 2 - 1]
    spoon_y = [length - fuze_h * 0.2, length - fuze_h * 0.55, length - fuze_h * 0.85, length - fuze_h * 0.75]
    ax_full.fill(spoon_x, spoon_y, color="#2d3748", ec="black", lw=0.8)
    ax_full.add_patch(Wedge((0, length - 2), od * 0.18, 20, 160, fc="#a0aec0", ec="black", lw=0.8))

    lines = ["MS-V", "OBSCURANT", "VEIL", "LOT MS-001"]
    for i, line in enumerate(lines):
        ax_full.text(0, length * (0.42 - i * 0.08), line, ha="center", va="center",
                     fontsize=10 if i < 3 else 8, fontweight="bold", fontfamily="DejaVu Sans Mono")

    ax_full.annotate("", xy=(od / 2 + 8, length - fuze_h), xytext=(od / 2 + 8, 0),
                     arrowprops=dict(arrowstyle="<->", color="black", lw=1.2))
    ax_full.text(od / 2 + 12, length / 2, f'{spec["ms_v"]["body"]["length_in"]}"', va="center", fontsize=9)

    fig.text(
        0.5, 0.02,
        "Engineering cutaway — existing AN-M8/M18 body + M201A1 fuze · MS-V delta is filler · NOT VALIDATION",
        ha="center", fontsize=8, style="italic", color="#555",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
