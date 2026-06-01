#!/usr/bin/env python3
"""Generate summary markdown and optional plots from simulation results."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "analysis" / "results"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def fmt_checks(checks: dict) -> str:
    return " | ".join(f"{k}: {'PASS' if v else 'FAIL'}" for k, v in checks.items())


def main() -> None:
    lines = [
        "# MS-V Simulation Results Summary",
        "",
        "> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "",
    ]

    for path in sorted(RESULTS.glob("*.json")):
        if path.name in ("suite_summary.json", "wind_sensitivity.json", "monte_carlo_baseline.json"):
            continue
        data = load_json(path)
        if "kpp_checks" not in data or "moe" not in data:
            continue
        lines.append(f"## {path.stem}")
        lines.append("")
        lines.append(f"- MoE fused EO/IR degraded: **{data['moe']['fused_eoir_degraded_fraction']:.1%}**")
        lines.append(f"- MoE lock >= 60s: **{data['moe']['lock_break_ge_60s_fraction']:.1%}**")
        lines.append(f"- Build-up p50: {data['kpp_02_build_up_s']['p50']:.1f}s (p90: {data['kpp_02_build_up_s']['p90']:.1f}s)")
        lines.append(f"- Duration p50: {data['kpp_03_duration_effective_s']['p50']:.1f}s (p10: {data['kpp_03_duration_effective_s']['p10']:.1f}s)")
        lines.append(f"- Area p50: {data['kpp_04_screening_area_sqft']['p50']:.1f} sq ft")
        lines.append(f"- KPP checks: {fmt_checks(data['kpp_checks'])}")
        lines.append("")

    if (RESULTS / "wind_sensitivity.json").exists():
        wind = load_json(RESULTS / "wind_sensitivity.json")
        lines.append("## Wind Sensitivity (3 grenade)")
        lines.append("")
        for label, data in wind.items():
            moe = data["moe"]["lock_break_ge_60s_fraction"]
            dur = data["kpp_03_duration_effective_s"]["p50"]
            lines.append(f"- **{label}**: MoE lock>=60s {moe:.1%}, duration p50 {dur:.0f}s")
        lines.append("")

    out = ROOT / "analysis" / "RESULTS_SUMMARY.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")

    try:
        import matplotlib.pyplot as plt  # noqa: PLC0415

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        names, moe_frac, dur_p10 = [], [], []
        for path in ["single_grenade.json", "two_grenade_group.json", "three_grenade_group.json"]:
            p = RESULTS / path
            if not p.exists():
                continue
            d = load_json(p)
            names.append(path.replace(".json", ""))
            moe_frac.append(d["moe"]["lock_break_ge_60s_fraction"])
            dur_p10.append(d["kpp_03_duration_effective_s"]["p10"])
        if names:
            axes[0].bar(names, moe_frac, color="#4a6741")
            axes[0].set_title("MoE lock >= 60s")
            axes[0].set_ylim(0, 1)
            axes[1].bar(names, dur_p10, color="#6b5b4f")
            axes[1].axhline(120, color="red", linestyle="--", label="KPP 120s")
            axes[1].set_title("Duration p10 (s)")
            axes[1].legend()
            wind_labels, wind_moe = [], []
            if (RESULTS / "wind_sensitivity.json").exists():
                w = load_json(RESULTS / "wind_sensitivity.json")
                for k, v in w.items():
                    wind_labels.append(k)
                    wind_moe.append(v["moe"]["lock_break_ge_60s_fraction"])
                axes[2].bar(wind_labels, wind_moe, color="#3d5a80")
                axes[2].set_title("Wind vs MoE (3 grenade)")
                axes[2].tick_params(axis="x", rotation=15)
            fig.tight_layout()
            plot_path = RESULTS / "suite_charts.png"
            fig.savefig(plot_path, dpi=120)
            print(f"Wrote {plot_path}")
    except ImportError:
        print("matplotlib not installed — skipping charts")


if __name__ == "__main__":
    main()
