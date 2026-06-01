#!/usr/bin/env python3
"""Summarize mega_suite manifest into markdown report."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEGA = ROOT / "analysis" / "results" / "mega_suite"


def main() -> None:
    manifest_path = MEGA / "manifest.json"
    if not manifest_path.exists():
        print(f"Missing {manifest_path}")
        return

    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    lines = [
        "# Mega Suite Results",
        "",
        "> LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "",
        f"- **Model:** {m.get('model_version', 'unknown')}",
        f"- **Physics tier:** {m.get('physics_tier', '—')} · **Sensor:** {m.get('sensor_model', '—')}",
        f"- **Jobs:** {m['total_jobs']} | **Total samples:** {m['total_samples']:,}",
        f"- **Pass:** {m['jobs_pass']}/{m['total_jobs']} all-KPP-pass",
        f"- **Workers:** {m.get('workers', '—')} (RunPod policy: vCPU−1)",
        "",
        "## Summary Table",
        "",
        "| Job | Samples | Pass | Dur p10 | Dur p50 | MoE |",
        "|-----|---------|------|---------|---------|-----|",
    ]

    for r in sorted(m["summary"], key=lambda x: x["label"]):
        ok = "YES" if r["all_kpp_pass"] else "**NO**"
        lines.append(
            f"| {r['label']} | {r['n_samples']:,} | {ok} | "
            f"{r['duration_p10']:.1f}s | {r['duration_p50']:.1f}s | {r['moe_lock_frac']:.1%} |"
        )

    fails = [r for r in m["summary"] if not r["all_kpp_pass"]]
    if fails:
        lines.extend(["", "## Failures", ""])
        for r in fails:
            lines.append(f"- **{r['label']}**: {r['kpp_checks']}")

    out = ROOT / "analysis" / "MEGA_SUITE_REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
