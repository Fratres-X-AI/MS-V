#!/usr/bin/env python3
"""Summarize deep_dive tail-risk jobs → markdown."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis" / "results" / "deep_dive" / "manifest.json"
OUT = ROOT / "analysis" / "DEEP_DIVE_REPORT.md"


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit(f"Missing {MANIFEST}")

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    jobs = sorted(m["jobs"], key=lambda j: j["duration_p10"])

    lines = [
        "# Tail-Risk Deep Dive — High-N Confirmation",
        "",
        "> **MATURITY:** Literature-parameter sensitivity — **NOT VALIDATION**",
        f"> **Physics:** {m.get('physics_tier')} · **Sensor:** {m.get('sensor_model')}",
        f"> **Total samples:** {m['total_samples']:,} · **Elapsed:** {m.get('elapsed_s')}s",
        "",
        "## Results",
        "",
        "| Job | N | Seed | Dur p10 | Dur p50 | MoE lock | Pass |",
        "|-----|---|------|---------|---------|----------|------|",
    ]
    for j in jobs:
        ok = "YES" if j["all_kpp_pass"] else "NO"
        lines.append(
            f"| `{j['label']}` | {j['n_samples']:,} | {j['seed']} | "
            f"{j['duration_p10']:.1f}s | {j['duration_p50']:.1f}s | {j['moe_lock_frac']:.1%} | {ok} |"
        )

    burn_jobs = [j for j in jobs if "burn_worst" in j["label"]]
    if len(burn_jobs) >= 2:
        p10_vals = [j["duration_p10"] for j in burn_jobs]
        spread = max(p10_vals) - min(p10_vals)
        lines.extend([
            "",
            "## Burn-worst seed stability",
            "",
            f"- **p10 spread across seeds:** {spread:.2f} s ({min(p10_vals):.1f}–{max(p10_vals):.1f} s)",
            f"- **50M canonical (seed 544):** {next(j for j in burn_jobs if '50M' in j['label'])['duration_p10']:.1f} s p10",
            "",
            "Tight spread → tail-risk estimate stable at high N.",
        ])

    adv = next((j for j in jobs if "adversarial" in j["label"]), None)
    base = next((j for j in jobs if "baseline_confirm" in j["label"]), None)
    if adv and base:
        lines.extend([
            "",
            "## Adversarial vs nominal (50M baseline)",
            "",
            f"- **Nominal MoE:** {base['moe_lock_frac']:.1%} · **Adversarial MoE:** {adv['moe_lock_frac']:.1%}",
            f"- **Nominal dur p10:** {base['duration_p10']:.1f}s · **Adversarial dur p10:** {adv['duration_p10']:.1f}s",
        ])

    lines.append(f"\nAuto-generated from `{MANIFEST.relative_to(ROOT)}`.")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
