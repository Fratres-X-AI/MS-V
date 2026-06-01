#!/usr/bin/env python3
"""Patch assumption register Sobol column from sobol_results.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOBOL = ROOT / "analysis" / "results" / "sobol" / "sobol_results.json"
REGISTER = ROOT / "rtm" / "assumption_register.md"

# Map assumption IDs to Sobol parameter names
ASSUMPTION_PARAM = {
    "A-002": "burn_rate_g_s",
    "A-003": "build_up_time_s",
    "A-004": "screening_area_sqft",
    "A-006": "alpha_vis",  # representative for alpha trio
    "A-007": "wind_mph",
    "A-014": "yield_factor",
    "A-015": "temp_c",
    "A-016": "humidity_rh",
    "A-018": "cloud_depth_m",
}


def _sobol_rank(duration: dict, param: str) -> str:
    if duration.get("status") != "OK":
        return "pending"
    rank = {r["name"]: i + 1 for i, r in enumerate(duration["rank_by_ST"])}
    st = duration["ST"].get(param, 0.0)
    r = rank.get(param, 99)
    if r <= 3:
        return f"**Sobol #{r}** ST={st:.3f}"
    if st > 0.05:
        return f"Sobol #{r} ST={st:.3f}"
    return f"Low ST={st:.4f}"


def main() -> None:
    if not SOBOL.exists():
        print(f"No {SOBOL} — skip")
        return
    data = json.loads(SOBOL.read_text(encoding="utf-8"))
    duration = data["outputs"]["duration_s"]
    text = REGISTER.read_text(encoding="utf-8")

    # Replace sensitivity method header
    text = text.replace(
        "**Sensitivity method:** One-at-a-time (OAT) sweep ranks from mega suite — **not Sobol indices** (planned TRL 3)",
        f"**Sensitivity method:** OAT (38-job mega suite) + **Saltelli Sobol** (N={data['n_base']:,}, "
        f"{data['n_evaluations']:,} evals, seed={data['seed']}) — see `analysis/SOBOL_SENSITIVITY_REPORT.md`",
    )

    # Append Sobol section if not present
    if "## Sobol global sensitivity (duration ST rank)" not in text:
        lines = [
            "",
            "## Sobol global sensitivity (duration ST rank)",
            "",
            f"> Campaign: `{SOBOL.relative_to(ROOT)}` · generated {data['generated_at']}",
            "",
            "| Rank | Parameter | ST | S1 | TRL 3 focus |",
            "|------|-----------|-----|-----|-------------|",
        ]
        for i, row in enumerate(duration.get("rank_by_ST", [])[:12], 1):
            lines.append(
                f"| {i} | `{row['name']}` | {row['ST']:.4f} | {row['S1']:.4f} | see verification matrix |"
            )
        if duration.get("status") != "OK":
            lines.append("| — | moe_met | DEGENERATE | — | A-013 surrogate saturation |")
        text = text.rstrip() + "\n" + "\n".join(lines) + "\n"

    REGISTER.write_text(text, encoding="utf-8")
    print(f"Updated {REGISTER}")


if __name__ == "__main__":
    main()
