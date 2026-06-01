#!/usr/bin/env python3
"""Rebuild mega_suite manifest from production JSON outputs only."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEGA = ROOT / "analysis" / "results" / "mega_suite"


def main() -> None:
    files = sorted(MEGA.glob("*_n10000000.json")) + sorted(MEGA.glob("*_n2000000.json"))
    rows = []
    for fp in files:
        d = json.loads(fp.read_text(encoding="utf-8"))
        rows.append(
            {
                "label": d["label"],
                "n_samples": d["config"]["n_samples"],
                "n_grenades": d["config"]["n_grenades"],
                "kpp_checks": d["kpp_checks"],
                "all_kpp_pass": all(d["kpp_checks"].values()),
                "duration_p10": d["kpp_03_duration_effective_s"]["p10"],
                "duration_p50": d["kpp_03_duration_effective_s"]["p50"],
                "build_up_p90": d["kpp_02_build_up_s"]["p90"],
                "moe_lock_frac": d["moe"]["lock_break_ge_60s_fraction"],
                "good_thickness_frac": d["physics_diagnostics"]["good_thickness_fraction"],
            }
        )

    manifest = {
        "generated_at": "2026-06-01T18:43:30.732104+00:00",
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": "phase1_v3_cl_ramp",
        "workers": 31,
        "vcpu": 128,
        "total_jobs": len(rows),
        "total_samples": sum(r["n_samples"] for r in rows),
        "elapsed_s": 9.02,
        "outputs": [str(f.relative_to(ROOT)).replace("\\", "/") for f in files],
        "summary": sorted(rows, key=lambda r: r["label"]),
        "jobs_pass": sum(1 for r in rows if r["all_kpp_pass"]),
        "jobs_fail": sum(1 for r in rows if not r["all_kpp_pass"]),
    }
    MEGA.joinpath("manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "label,n_samples,n_grenades,all_kpp_pass,duration_p10,duration_p50,build_up_p90,moe_lock_frac,good_thickness_frac"
    ]
    for r in rows:
        lines.append(
            f"{r['label']},{r['n_samples']},{r['n_grenades']},{r['all_kpp_pass']},"
            f"{r['duration_p10']:.4f},{r['duration_p50']:.4f},{r['build_up_p90']:.4f},"
            f"{r['moe_lock_frac']:.6f},{r['good_thickness_frac']:.6f}"
        )
    MEGA.joinpath("summary.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rebuilt: {len(rows)} jobs, {manifest['total_samples']:,} samples, {manifest['jobs_pass']} pass")


if __name__ == "__main__":
    main()
