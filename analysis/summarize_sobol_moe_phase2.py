#!/usr/bin/env python3
"""Summarize phase2 MoE Sobol → markdown."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_JSON = ROOT / "analysis" / "results" / "sobol_moe_phase2" / "sobol_moe_phase2_results.json"
OUT_MD = ROOT / "analysis" / "SOBOL_MOE_PHASE2_REPORT.md"


def main() -> None:
    if not IN_JSON.exists():
        raise SystemExit(f"Missing {IN_JSON}")

    data = json.loads(IN_JSON.read_text(encoding="utf-8"))
    moe = data["outputs"]["moe_met"]
    lines = [
        "# MoE Sobol Report — Phase2 + v6 Probabilistic Lock",
        "",
        "> **MATURITY:** Literature-parameter sensitivity — **NOT VALIDATION**",
        f"> **Engine:** {data.get('method', 'phase2/v6')}",
        f"> **Saltelli N={data['n_base']:,}** · **MC per row={data['mc_n_per_row']:,}** · "
        f"evaluations={data['n_evaluations']:,} · workers={data.get('workers')}",
        "",
        "## MOE-01 lock-break fraction — ranked by ST",
        "",
        f"- Y mean={moe['Y_mean']:.3f} p10={moe['Y_p10']:.3f} p50={moe['Y_p50']:.3f} p90={moe['Y_p90']:.3f}",
        "",
        "| Rank | Parameter | S1 | ST |",
        "|------|-----------|-----|-----|",
    ]
    for i, row in enumerate(moe.get("rank_by_ST", []), 1):
        lines.append(f"| {i} | `{row['name']}` | {row['S1']:.4f} | {row['ST']:.4f} |")

    lines.extend([
        "",
        "Unlike v4 lumped Sobol, this campaign uses **full phase2 physics + v6 probabilistic lock-break**.",
        "",
        f"Auto-generated from `{IN_JSON.relative_to(ROOT)}`.",
    ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
