#!/usr/bin/env python3
"""Generate analysis/CONOPS_REPORT.md from conops_summary.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_PATH = ROOT / "analysis" / "results" / "conops" / "conops_summary.json"
OUT_PATH = ROOT / "analysis" / "CONOPS_REPORT.md"


def main() -> None:
    if not IN_PATH.exists():
        raise SystemExit(f"Missing {IN_PATH} — run sim/run_conops.py first")

    data = json.loads(IN_PATH.read_text(encoding="utf-8"))
    lines = [
        "# CONOPS Monte Carlo Report — Five Use Cases",
        "",
        "> **MATURITY:** Phase 2 full physics + probabilistic MoE — **NOT VALIDATION**",
        f"> **Model:** {data['model_version']} · {data['n_samples_per_case']:,} samples per case",
        "",
        "| Use Case | MS-V | HC | Window (s) | Lock Met | Obscured | Edge Plume | Core | Friendly Blind |",
        "|----------|------|-----|------------|----------|----------|------------|------|----------------|",
    ]

    for uc in data["use_cases"]:
        w = uc["window_s"]
        m = uc["moe"]
        lines.append(
            f"| {uc['use_case_name']} | {uc['config']['n_ms_v']} | {uc['config']['n_hc']} | "
            f"{w[0]:.0f}–{w[1]:.0f} | **{m['lock_met_fraction']*100:.1f}%** | "
            f"{m['obscured_fraction']*100:.1f}% | {m.get('edge_of_plume_fraction', 0)*100:.1f}% | "
            f"{m.get('in_plume_core_fraction', 0)*100:.1f}% | {m['friendly_blinded_fraction']*100:.1f}% |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- **Lock Met** — threat lock broken for ≥ min_lock_s inside CONOPS window with build-up complete",
        "- **Obscured** — v6 probabilistic lock-break at **threat LOS** (Phase 2 microphysics + edge geometry)",
        "- **Edge Plume** — fraction of samples where threat sits at r/R ≥ 0.75",
        "- **Core** — threat inside dense core (r/R ≤ 0.35)",
        "- **Friendly Blind** — squad inside dense MWIR cloud (hard constraint on movement)",
        "- Values **< 100%** indicate hardened MoE is discriminating (A-013 partially addressed)",
        "",
        "Source: `sim/conops/kill_chain.py` · `docs/04-conops-use-cases.md`",
    ])

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
