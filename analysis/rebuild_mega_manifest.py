#!/usr/bin/env python3
"""Rebuild mega_suite manifest from production JSON outputs only."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEGA = ROOT / "analysis" / "results" / "mega_suite"


def main() -> None:
    files = sorted(MEGA.glob("*_n10000000.json")) + sorted(MEGA.glob("*_n2000000.json"))
    rows = []
    model_version = "unknown"
    physics_tier = "unknown"
    sensor_model = "unknown"
    for fp in files:
        d = json.loads(fp.read_text(encoding="utf-8"))
        if model_version == "unknown":
            model_version = d.get("model_version", model_version)
            physics_tier = d.get("physics_diagnostics", {}).get("physics_tier", physics_tier)
            if physics_tier == "phase2":
                sensor_model = "v6_probabilistic_lock"
        throw_p10 = d.get("kpp_08_throw_range_m", {}).get("p10")
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
                "throw_p10_m": throw_p10,
                "sensor_saturation": d.get("sensor_diagnostics", {}).get("surrogate_saturated"),
            }
        )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": model_version,
        "physics_tier": physics_tier,
        "sensor_model": sensor_model,
        "workers": None,
        "total_jobs": len(rows),
        "total_samples": sum(r["n_samples"] for r in rows),
        "outputs": [str(f.relative_to(ROOT)).replace("\\", "/") for f in files],
        "summary": sorted(rows, key=lambda r: r["label"]),
        "jobs_pass": sum(1 for r in rows if r["all_kpp_pass"]),
        "jobs_fail": sum(1 for r in rows if not r["all_kpp_pass"]),
    }
    MEGA.joinpath("manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    lines = [
        "label,n_samples,n_grenades,all_kpp_pass,duration_p10,duration_p50,build_up_p90,"
        "moe_lock_frac,good_thickness_frac,throw_p10_m"
    ]
    for r in rows:
        tp = r.get("throw_p10_m")
        tp_s = "" if tp is None else f"{tp:.4f}"
        lines.append(
            f"{r['label']},{r['n_samples']},{r['n_grenades']},{r['all_kpp_pass']},"
            f"{r['duration_p10']:.4f},{r['duration_p50']:.4f},{r['build_up_p90']:.4f},"
            f"{r['moe_lock_frac']:.6f},{r['good_thickness_frac']:.6f},{tp_s}"
        )
    MEGA.joinpath("summary.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rebuilt: {len(rows)} jobs, {manifest['total_samples']:,} samples, {manifest['jobs_pass']} pass")


if __name__ == "__main__":
    main()
