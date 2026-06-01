#!/usr/bin/env python3
"""Summarize Sobol results → markdown report + assumption register patch data."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOBOL_JSON = ROOT / "analysis" / "results" / "sobol" / "sobol_results.json"
OUT_MD = ROOT / "analysis" / "SOBOL_SENSITIVITY_REPORT.md"
OUT_RANK = ROOT / "analysis" / "results" / "sobol" / "sobol_rankings.json"


def main() -> None:
    if not SOBOL_JSON.exists():
        raise SystemExit(f"Missing {SOBOL_JSON} — run sim/run_sobol.py first")

    data = json.loads(SOBOL_JSON.read_text(encoding="utf-8"))
    duration = data["outputs"]["duration_s"]
    build_up = data["outputs"]["build_up_s"]
    moe = data["outputs"].get("moe_met", {})

    def _rank_rows(metric: dict) -> list:
        if metric.get("status", "OK") != "OK":
            return []
        return metric.get("rank_by_ST", [])

    lines = [
        "# Sobol Global Sensitivity Report — MS-V Phase 1",
        "",
        "> **MATURITY:** Literature-parameter deterministic physics — **NOT VALIDATION**",
        f"> **Method:** {data['method']} · N={data['n_base']:,} · evaluations={data['n_evaluations']:,}",
        f"> **Scenario:** {data['n_grenades']} grenades · seed={data['seed']}",
        "",
        "## Interpretation",
        "",
        "- **S1** = first-order Sobol index (direct effect share of variance)",
        "- **ST** = total-order index (direct + interaction effects)",
        "- Duration indices are **actionable** for TRL 3 burn-cup / chamber testing",
        "- MoE indices may be **depressed** when surrogate saturates (see A-013)",
        "",
        "## KPP-03 Duration — ranked by ST",
        "",
        "| Rank | Parameter | S1 | ST | TRL 3 priority |",
        "|------|-----------|-----|-----|----------------|",
    ]

    kpp_map = {
        "burn_rate_g_s": "P0 burn cup",
        "filler_mass_g": "P0 burn cup",
        "temp_c": "P0 chamber T",
        "humidity_rh": "P1 chamber RH",
        "build_up_time_s": "P1 high-speed video",
        "yield_factor": "P0 gravimetric yield",
        "screening_area_sqft": "P1 lidar geometry",
        "cloud_depth_m": "P1 geometry",
        "wind_mph": "P2 range plume",
        "alpha_vis": "P0 spectrometry",
        "alpha_nir": "P0 spectrometry",
        "alpha_mwir": "P0 spectrometry",
    }

    for i, row in enumerate(_rank_rows(duration), 1):
        pri = kpp_map.get(row["name"], "P1")
        lines.append(f"| {i} | `{row['name']}` | {row['S1']:.4f} | {row['ST']:.4f} | {pri} |")

    lines.extend([
        "",
        f"- Duration Y: mean={duration['Y_mean']:.1f}s p10={duration['Y_p10']:.1f}s p50={duration['Y_p50']:.1f}s p90={duration['Y_p90']:.1f}s",
        "",
        "## KPP-02 Build-up — top 5 by ST",
        "",
        "| Parameter | S1 | ST |",
        "|-----------|-----|-----|",
    ])
    for row in _rank_rows(build_up)[:5]:
        lines.append(f"| `{row['name']}` | {row['S1']:.4f} | {row['ST']:.4f} |")

    lines.extend([
        "",
        "## MOE-01 lock-break (binary surrogate) — top 5 by ST",
        "",
        "| Parameter | S1 | ST | Note |",
        "|-----------|-----|-----|------|",
    ])
    moe_rows = _rank_rows(moe)
    if not moe_rows:
        lines.append("| — | — | — | **DEGENERATE** — 100% pass, surrogate saturation (A-013) |")
    for row in moe_rows[:5]:
        note = "may reflect CL/threshold not saturation" if row["ST"] > 0.05 else "low — surrogate may saturate"
        lines.append(f"| `{row['name']}` | {row['S1']:.4f} | {row['ST']:.4f} | {note} |")

    lines.extend([
        "",
        "## TRL 3 test plan (Sobol-driven)",
        "",
        "1. **Burn rate + filler mass** — highest expected ST on duration; burn cup DOE",
        "2. **Temperature** — coupled to burn; environmental chamber",
        "3. **Build-up time** — if ST > 0.1, prioritize streamer imaging",
        "4. **α(λ) bands** — spectrometry regardless of low ST (surrogate limitation)",
        "",
        f"Auto-generated from `{SOBOL_JSON.relative_to(ROOT)}`.",
    ])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    rankings = {
        "duration_rank_ST": duration["rank_by_ST"],
        "build_up_rank_ST": build_up["rank_by_ST"],
        "moe_rank_ST": moe["rank_by_ST"],
    }
    OUT_RANK.write_text(json.dumps(rankings, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_RANK}")


if __name__ == "__main__":
    main()
