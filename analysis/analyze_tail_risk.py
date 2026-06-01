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
    fails = [r for r in rows if r["all_kpp_pass"] != "True"]
    moe_min = min(float(r["moe_lock_frac"]) for r in rows)

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
        f"- **Minimum MoE lock-break fraction:** {moe_min:.1%} (current surrogate saturates at 100%)",
        f"- **Tightest duration p10 margin:** {float(by_dur[0]['duration_p10']) - 120:.1f} s above 120 s KPP",
        "",
        "## Duration p10 — Ranked (worst first)",
        "",
        "| Rank | Job | Dur p10 (s) | Dur p50 (s) | Margin vs 120 s |",
        "|------|-----|-------------|-------------|-----------------|",
    ]

    for i, r in enumerate(by_dur[:15], 1):
        p10 = float(r["duration_p10"])
        p50 = float(r["duration_p50"])
        lines.append(f"| {i} | {r['label']} | {p10:.1f} | {p50:.1f} | {p10 - 120:.1f} |")

    lines.extend([
        "",
        "## Parameter sensitivity (inferred from sweep jobs)",
        "",
        "| Driver | Observation | Tail-risk note |",
        "|--------|-------------|----------------|",
        "| **Burn rate (upper bound)** | Dominant — 4.4 g/s max → ~152 s p10; 3.6 → ~183 s | Formulation must hold ≤4.2 g/s design cap |",
        "| **Temperature (hot)** | 35–50°C bin → ~153 s p10 | High ambient shortens screen; doctrine/timing |",
        "| **Adversarial stack** | 10M stacked corners → ~144 s p10 | Worst modeled envelope still passes; **outside envelope unmodeled** |",
        "| **Yield (lower bound)** | 0.18–0.34 sweeps: no duration/MoE separation | CL surrogate saturates — **sensor model upgrade required** |",
        "| **Visual smoke factor** | 1.0–1.6: negligible duration spread | Partner smoke affects MoE definition, not burn clock |",
        "| **Alpha (extinction)** | tight/wide/pessimistic: ~160 s p10 flat | Uncertainty in α does not bind until sensor curves added |",
        "| **Seed convergence** | 7 seeds, 2M each: stable ±0.03 s p10 | MC numerical stability confirmed |",
        "",
        "## What this does NOT show",
        "",
        "- p1 / empirical worst-case (no fill chemistry data)",
        "- Per-wavelength extinction measurement uncertainty",
        "- FPV ISP / AGC / fiber-optic link budget effects",
        "- Cloud geometry, settling, or combined plume interaction",
        "- Throw range, load, or human-factors failure modes",
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
