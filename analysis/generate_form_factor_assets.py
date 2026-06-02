#!/usr/bin/env python3
"""Generate Tier B form-factor assets: figures, STL, pouch-fit report."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from models.system.envelope import (  # noqa: E402
    check_pouch_fit,
    derive_envelope,
    in_to_mm,
    load_form_factor,
    loadout_mass_g,
)
from models.system.kinematics import impact_dispersion_summary  # noqa: E402
from models.system.stl_export import export_comparison_stl, export_ms_v_stl  # noqa: E402

FIG = ROOT / "analysis" / "figures" / "form_factor"
STL = ROOT / "models" / "system" / "assets"
REPORT = ROOT / "analysis" / "FORM_FACTOR_REPORT.md"


def _load_baselines() -> dict:
    return json.loads((ROOT / "data" / "baseline_grenades.json").read_text(encoding="utf-8"))


def _load_plume_spread() -> float:
    params_path = ROOT / "models" / "cloud_physics" / "params.yaml"
    with params_path.open(encoding="utf-8") as f:
        params = yaml.safe_load(f)
    return float(params.get("phase1b", {}).get("plume_spread_factor", 3.2))


def plot_scale_comparison(out: Path, spec: dict) -> Path:
    data = _load_baselines()
    ms_v = {
        "length_in": spec["ms_v"]["body"]["length_in"],
        "diameter_in": spec["ms_v"]["body"]["diameter_in"],
        "weight_g": spec["ms_v"]["mass_g"],
    }
    grenades = [
        ("AN-M8 HC", data["grenades"]["AN-M8"], "#718096"),
        ("M83 TA", data["grenades"]["M83"], "#a0aec0"),
        ("MS-V v2 KPP", ms_v, "#2b6cb0"),
    ]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = 0.0
    gap = 15.0
    max_h = 0.0
    for name, g, color in grenades:
        h = in_to_mm(g["length_in"])
        w = in_to_mm(g["diameter_in"])
        max_h = max(max_h, h)
        rect = mpatches.FancyBboxPatch(
            (x, 0), w, h,
            boxstyle="round,pad=0.5,rounding_size=2",
            facecolor=color, edgecolor="black", linewidth=1.2, alpha=0.85,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, h + 4, name, ha="center", va="bottom", fontsize=9, fontweight="bold")
        ax.text(
            x + w / 2, h / 2,
            f"{g['length_in']}\" × {g['diameter_in']}\"\n{g['weight_g']} g",
            ha="center", va="center", fontsize=8, color="white" if color == "#2b6cb0" else "black",
        )
        x += w + gap
    ax.set_xlim(-5, x + 5)
    ax.set_ylim(-5, max_h + 35)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Form factor scale comparison (v2 KPP vs inventory)")
    fig.text(
        0.5, 0.02,
        "Engineering estimate — NOT VALIDATION · MS-V v2 KPP 850 g / 7.1×3.1 in",
        ha="center", fontsize=8, style="italic",
    )
    fig.tight_layout()
    path = out / "scale_comparison.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_cutaway(out: Path, spec: dict, env) -> Path:
    fig, ax = plt.subplots(figsize=(8, 6))
    wall = spec["ms_v"]["body"]["wall_thickness_mm"]
    od = env.outer_diameter_mm
    ol = env.outer_length_mm
    id_ = env.inner_diameter_mm
    fuze_h = spec["ms_v"]["fuze"]["stack_height_mm"]

    # outer shell
    ax.add_patch(plt.Rectangle((0, 0), od, ol, fill=False, edgecolor="black", linewidth=2))
    ax.add_patch(plt.Rectangle((wall, fuze_h), id_, ol - fuze_h - wall,
                               facecolor="#bee3f8", edgecolor="#2b6cb0", linewidth=1))
    ax.add_patch(plt.Rectangle((od / 2 - spec["ms_v"]["fuze"]["outer_diameter_mm"] / 2, ol - fuze_h),
                               spec["ms_v"]["fuze"]["outer_diameter_mm"], fuze_h,
                               facecolor="#cbd5e0", edgecolor="black", linewidth=1))
    for i, label in enumerate(["Port 1", "Port 2", "Port 3", "Port 4"]):
        px = od * (0.25 + 0.15 * (i % 2))
        py = ol - fuze_h - 25 - i * 8
        ax.plot([px, px], [py, py + 6], "k-", lw=2)
        ax.text(px + 3, py + 3, label, fontsize=7)
    ax.plot([od / 2, od / 2], [5, 15], "k-", lw=2)
    ax.text(od / 2 + 3, 8, "Bottom port", fontsize=7)
    ax.text(od + 8, ol / 2, f"Fill chamber\n~{env.internal_chamber_cm3:.0f} cm³",
            va="center", fontsize=9)
    ax.set_xlim(-5, od + 60)
    ax.set_ylim(-5, ol + 15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("MS-V notional cutaway (parametric)")
    fig.tight_layout()
    path = out / "cutaway_schematic.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_employment(out: Path, spec: dict) -> Path:
    ce = spec["cloud_employment"]
    area_sqft = (ce["screening_area_sqft"]["min"] + ce["screening_area_sqft"]["max"]) / 2.0
    area_m2 = area_sqft * 0.092903
    radius = math.sqrt(area_m2 / math.pi)
    spread = _load_plume_spread()
    radius_geo = radius * spread

    fig, ax = plt.subplots(figsize=(9, 7))
    squad = (0.0, 0.0)
    throws = [( -3.0, 8.0), (0.0, 10.0), (3.0, 8.0)][: ce["typical_n_ms_v"]]

    for i, (tx, ty) in enumerate(throws):
        circle = plt.Circle((tx, ty), radius_geo, facecolor="#4299e1", alpha=0.25, edgecolor="#2b6cb0")
        ax.add_patch(circle)
        ax.plot(tx, ty, "s", color="#2b6cb0", markersize=8)
        ax.text(tx, ty - radius_geo - 1.5, f"MS-V {i + 1}", ha="center", fontsize=8)

    ax.plot(*squad, "g^", markersize=12, label="Friendly squad")
    ax.annotate("", xy=(0, 35), xytext=(0, 5), arrowprops=dict(arrowstyle="-|>", color="red", lw=2))
    ax.text(2, 22, "Threat UAS LOS", color="red", fontsize=9)
    ax.annotate("", xy=(25, 15), xytext=(5, 12),
                arrowprops=dict(arrowstyle="-|>", color="gray", lw=1.5))
    ax.text(18, 18, "Wind", color="gray", fontsize=9)

    ax.set_xlim(-radius_geo * 2, radius_geo * 2.5)
    ax.set_ylim(-radius_geo * 1.2, 40)
    ax.set_aspect("equal")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Meters (notional plan view)")
    ax.set_title(f"Cloud employment — {ce['typical_n_ms_v']} MS-V + {ce['typical_n_hc']} HC · r≈{radius_geo:.0f} m envelope")
    fig.tight_layout()
    path = out / "employment_diagram.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_load_layout(out: Path, spec: dict) -> Path:
    lo = loadout_mass_g(spec, n_ms_v=2, n_hc=1)
    fig, ax = plt.subplots(figsize=(8, 4))
    items = [
        ("2× MS-V", lo["ms_v_kg"], "#2b6cb0"),
        ("1× AN-M8", lo["visual_smoke_kg"], "#718096"),
    ]
    x = 0.1
    for label, kg, color in items:
        w = 0.15 + kg * 0.25
        ax.barh(0.5, w, height=0.35, left=x, color=color, edgecolor="black")
        ax.text(x + w / 2, 0.5, f"{label}\n{kg:.2f} kg", ha="center", va="center", color="white", fontsize=9)
        x += w + 0.08
    ax.set_xlim(0, 1.2)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(f"Typical event load — total {lo['total_kg']:.2f} kg (notional kit slice)")
    fig.tight_layout()
    path = out / "load_layout.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_pouch_fit(out: Path, env, pouch_fit) -> Path:
    fig, ax = plt.subplots(figsize=(6, 7))
    pw, pouch_depth, ph = 90, 95, 185
    ax.add_patch(plt.Rectangle((0, 0), pw, ph, fill=False, edgecolor="black", linewidth=2, linestyle="--"))
    ax.text(pw / 2, ph + 5, f"Pouch inner envelope ({pouch_depth} mm deep)", ha="center", fontsize=9)
    od, ol = env.outer_diameter_mm, env.outer_length_mm
    ox = (pw - od) / 2
    color = "#48bb78" if pouch_fit.fits_all else "#f56565"
    ax.add_patch(plt.Rectangle((ox, 5), od, ol, facecolor=color, alpha=0.5, edgecolor="black"))
    ax.text(pw / 2, ol / 2 + 5, f"MS-V\n{od:.0f}×{ol:.0f} mm", ha="center", va="center", fontsize=9)
    status = "FITS (estimate)" if pouch_fit.fits_all else "TIGHT / REVIEW"
    ax.text(pw / 2, -15, status, ha="center", fontsize=10, fontweight="bold", color=color)
    ax.set_xlim(-15, pw + 15)
    ax.set_ylim(-25, ph + 20)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Pouch fit check (vertical stow)")
    fig.tight_layout()
    path = out / "pouch_fit.png"
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def write_report(
    spec: dict,
    env,
    pouch_fit,
    paths: list[Path],
    stl_paths: dict,
    throw_stats: dict[str, float],
) -> None:
    throw = spec["throw"]
    variant = spec.get("variant_key", "v2_kpp")
    lines = [
        "# MS-V Form Factor Report (Tier B)",
        "",
        "> **MATURITY:** Parametric digital representation — **NOT VALIDATION**",
        "> No ergonomic range test · No issued-pouch verification",
        f"> **Variant:** `{variant}` — primary external envelope",
        "",
        "## Envelope (volume budget)",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
        f"| Outer L × D | {env.outer_length_mm:.0f} × {env.outer_diameter_mm:.0f} mm ({spec['ms_v']['body']['length_in']}\" × {spec['ms_v']['body']['diameter_in']}\") |",
        f"| Inner chamber | {env.internal_chamber_cm3:.0f} cm³ |",
        f"| Fill volume (mid) | {env.fill_volume_cm3:.0f} cm³ @ {env.fill_density_g_cm3:.2f} g/cm³ |",
        f"| Mass | {spec['ms_v']['mass_g']} g |",
        "",
        "## KPP-08 Throw",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| KPP band | {throw['range_m']['min']}–{throw['range_m']['max']} m |",
        f"| Design authority p50 | {throw['sim_p50_m']} m |",
        f"| MC stressed p10 / p50 / p90 | {throw_stats['throw_p10_m']:.1f} / {throw_stats['throw_p50_m']:.1f} / {throw_stats['throw_p90_m']:.1f} m |",
        f"| Lateral dispersion p50 / p90 | {throw_stats['lateral_p50_m']:.2f} / {throw_stats['lateral_p90_m']:.2f} m |",
        "",
        "Source: [`models/system/kinematics.py`](../models/system/kinematics.py) + phase2 deployment model.",
        "",
        "## Pouch fit (typical MOLLE grenade pouch)",
        "",
        "| Check | Pass | Clearance |",
        "|-------|------|-----------|",
        f"| Width | {'✓' if pouch_fit.fits_width else '✗'} | {pouch_fit.clearance_width_mm:.0f} mm |",
        f"| Depth | {'✓' if pouch_fit.fits_depth else '✗'} | {pouch_fit.clearance_depth_mm:.0f} mm |",
        f"| Height | {'✓' if pouch_fit.fits_height else '✗'} | {pouch_fit.clearance_height_mm:.0f} mm |",
        f"| Mass | {'✓' if pouch_fit.fits_mass else '✗'} | ≤ {spec['pouch']['max_recommended_mass_g']} g |",
        "",
        f"**Overall:** {'PASS (estimate)' if pouch_fit.fits_all else 'REVIEW REQUIRED'}",
        "",
        "## Assets",
        "",
    ]
    for p in paths:
        lines.append(f"- `{p.relative_to(ROOT).as_posix()}`")
    for name, p in stl_paths.items():
        lines.append(f"- STL `{name}`: `{p.relative_to(ROOT).as_posix()}`")
    lines.extend([
        "",
        "OpenSCAD source: `models/system/openscad/ms-v_body.scad`",
        "",
        "Annex: [`annexes/F-form-factor-and-ergonomics.md`](../annexes/F-form-factor-and-ergonomics.md)",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {REPORT}")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    STL.mkdir(parents=True, exist_ok=True)
    spec = load_form_factor("v2_kpp")
    env = derive_envelope(spec)
    pouch_fit = check_pouch_fit(env, spec["ms_v"]["mass_g"], spec["pouch"])
    throw_stats = impact_dispersion_summary()

    fig_paths = [
        plot_scale_comparison(FIG, spec),
        plot_cutaway(FIG, spec, env),
        plot_employment(FIG, spec),
        plot_load_layout(FIG, spec),
        plot_pouch_fit(FIG, env, pouch_fit),
    ]
    stl_paths = {
        "ms_v_assembly": export_ms_v_stl(STL / "ms_v_assembly.stl"),
        **export_comparison_stl(STL),
    }
    write_report(spec, env, pouch_fit, fig_paths, stl_paths, throw_stats)
    for p in fig_paths:
        print(f"Wrote {p}")
    for k, p in stl_paths.items():
        print(f"STL {k}: {p}")

    from analysis.generate_3d_renders import main as render_main  # noqa: E402

    render_main()


if __name__ == "__main__":
    main()
