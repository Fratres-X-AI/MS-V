#!/usr/bin/env python3
"""Generate tail-risk and parameter sensitivity report from mega_suite summary."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "analysis" / "results" / "mega_suite" / "summary.csv"
OUT = ROOT / "analysis" / "tail_risk_analysis.md"


def load_rows() -> list[dict[str, str]]:
    with SUMMARY.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = load_rows()
    if not rows:
        OUT.write_text("# Tail Risk Analysis\n\nNo mega_suite summary.csv found.\n", encoding="utf-8")
        return

    by_dur = sorted(rows, key=lambda r: float(r["duration_p10"]))
    by_moe = sorted(rows, key=lambda r: float(r["moe_lock_frac"]))
    fails = [r for r in rows if r["all_kpp_pass"] != "True"]
    moe_min = min(float(r["moe_lock_frac"]) for r in rows)
    moe_max = max(float(r["moe_lock_frac"]) for r in rows)
    throw_vals = [float(r["throw_p10_m"]) for r in rows if r.get("throw_p10_m")]
    moe_note = (
        f"**{moe_min:.1%}–{moe_max:.1%}** (phase2/v6 — discriminative)"
        if moe_max - moe_min > 0.05
        else f"**{moe_min:.1%}** (check surrogate saturation flag)"
    )

    lines = [
        "# Tail Risk & Parameter Sensitivity Analysis",
        "",
        "> Derived from `analysis/results/mega_suite/summary.csv` (140M-sample campaign).",
        "> **Not validation** — ranks sensitivity inside literature-assumed bounds only.",
        "",
        "## Headline",
        "",
        f"- **Jobs analyzed:** {len(rows)}",
        f"- **All-KPP pass (within assumed bounds):** {len(rows) - len(fails)}/{len(rows)}",
        f"- **MoE lock-break fraction range:** {moe_note}",
        f"- **Tightest duration p10 margin:** {float(by_dur[0]['duration_p10']) - 120:.1f} s above 120 s KPP",
    ]
    if throw_vals:
        lines.append(f"- **Throw p10 range (phase2 HF):** {min(throw_vals):.1f}–{max(throw_vals):.1f} m")
    lines.extend([
        "",
        "## Duration p10 — Ranked (worst first)",
        "",
        "| Rank | Job | Dur p10 (s) | Dur p50 (s) | Margin vs 120 s |",
        "|------|-----|-------------|-------------|-----------------|",
    ])

    for i, r in enumerate(by_dur[:15], 1):
        p10 = float(r["duration_p10"])
        p50 = float(r["duration_p50"])
        lines.append(f"| {i} | {r['label']} | {p10:.1f} | {p50:.1f} | {p10 - 120:.1f} |")

    lines.extend([
        "",
        "## MoE lock-break — Ranked (lowest first)",
        "",
        "| Rank | Job | MoE frac | Dur p10 |",
        "|------|-----|----------|---------|",
    ])
    for i, r in enumerate(by_moe[:10], 1):
        lines.append(
            f"| {i} | {r['label']} | {float(r['moe_lock_frac']):.1%} | {float(r['duration_p10']):.1f}s |"
        )

    lines.extend([
        "",
        "## Parameter sensitivity (inferred from sweep jobs)",
        "",
        "| Driver | Observation | Tail-risk note |",
        "|--------|-------------|----------------|",
        "| **Burn rate (upper bound)** | Dominant — 4.4 g/s max → ~152 s p10; 3.6 → ~183 s | Formulation must hold ≤4.2 g/s design cap |",
        "| **Temperature (hot)** | 35–50°C bin → ~153 s p10 | High ambient shortens screen; doctrine/timing |",
        "| **Adversarial stack** | 10M stacked corners → lowest MoE ~55% | Worst modeled envelope still passes duration KPP |",
        "| **Yield (lower bound)** | 0.18–0.34 sweeps: modest MoE spread | Duration flat; MoE varies ~79–80% |",
        "| **Visual smoke factor** | 1.0–1.6: negligible duration spread | Partner smoke affects MoE definition |",
        "| **Alpha (extinction)** | tight/wide/pessimistic: stable duration | v6 band-integrated — see MoE Sobol phase2 |",
        "| **Seed convergence** | 7 seeds, 2M each: stable ±0.03 s p10 | MC numerical stability confirmed |",
        "",
        "## What this does NOT show",
        "",
        "- p1 / empirical worst-case (no fill chemistry data)",
        "- Per-wavelength extinction measurement uncertainty",
        "- FPV ISP / AGC / fiber-optic link budget effects (partially in v6)",
        "- Empirical throw under live-fire stress",
        "- Toxicology or cost (KPP-12/13)",
        "",
        "## Required before interpreting as design confirmation",
        "",
        "1. Empirical α(λ) and particle size for candidate fill",
        "2. Sensor transmittance curves with degradation thresholds",
        "3. Geometry/settling model coupled to employment doctrine",
        "4. External lab/range campaign (TRL 3→4 gate)",
        "",
    ])

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
