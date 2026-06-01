#!/usr/bin/env python3
"""High-N tail-risk deep dives — burn worst, adversarial, baseline confirmation.

Run on RunPod:
  python sim/run_deep_dive.py --workers 3
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.run_mega_suite import _adversarial, _deepcopy_params, load_mega_params  # noqa: E402
from sim.run_runpod import ScenarioJob, _run_job  # noqa: E402
from sim.runpod_util import log_runpod_capacity, pin_blas_threads, run_parallel  # noqa: E402


@dataclass(frozen=True)
class DeepDiveSpec:
    label: str
    n_samples: int
    seed: int
    n_grenades: int
    mutate: Callable[[dict], None] | None = None


def _burn_worst(p: dict) -> None:
    p["grenade"]["burn_rate_g_s"]["max"] = 4.4
    p["grenade"]["burn_rate_g_s"]["min"] = 3.1


def _spec_to_job(base: dict, spec: DeepDiveSpec) -> ScenarioJob:
    p = _deepcopy_params(base)
    if spec.mutate:
        spec.mutate(p)
    return ScenarioJob(
        label=spec.label,
        params=p,
        n_samples=spec.n_samples,
        seed=spec.seed,
        n_grenades=spec.n_grenades,
    )


def default_specs() -> list[DeepDiveSpec]:
    return [
        DeepDiveSpec("burn_worst_50M_g3", 50_000_000, 544, 3, _burn_worst),
        DeepDiveSpec("adversarial_20M_g3", 20_000_000, 999, 3, _adversarial),
        DeepDiveSpec("baseline_confirm_50M_g3", 50_000_000, 45, 3, None),
        DeepDiveSpec("burn_worst_seed137_10M_g3", 10_000_000, 137, 3, _burn_worst),
        DeepDiveSpec("burn_worst_seed4099_10M_g3", 10_000_000, 4099, 3, _burn_worst),
    ]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V tail-risk deep dives")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "deep_dive")
    p.add_argument("--quick", action="store_true", help="500k samples per job for smoke test")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    workers = args.workers or min(3, log_runpod_capacity())
    pin_blas_threads(1)

    base = load_mega_params(ROOT)
    specs = default_specs()
    if args.quick:
        specs = [
            DeepDiveSpec(s.label.replace("_50M", "_500k").replace("_20M", "_500k"), 500_000, s.seed, s.n_grenades, s.mutate)
            for s in specs
        ]

    jobs = [_spec_to_job(base, s) for s in specs]
    args.out.mkdir(parents=True, exist_ok=True)

    total_n = sum(j.n_samples for j in jobs)
    print(f"[DeepDive] {len(jobs)} jobs, {total_n:,} total samples, workers={workers}")

    t0 = time.perf_counter()
    completed = run_parallel(jobs, _run_job, max_workers=workers)

    manifest: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "physics_tier": base["sim"].get("physics_tier"),
        "sensor_model": base["sim"].get("sensor_model"),
        "total_samples": total_n,
        "elapsed_s": None,
        "jobs": [],
    }

    for item in completed:
        label = item["label"]
        result = item["result"]
        out_path = args.out / f"{label}.json"
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        row = {
            "label": label,
            "n_samples": result["config"]["n_samples"],
            "seed": result["config"]["seed"],
            "duration_p10": result["kpp_03_duration_effective_s"]["p10"],
            "duration_p50": result["kpp_03_duration_effective_s"]["p50"],
            "build_up_p90": result["kpp_02_build_up_s"]["p90"],
            "moe_lock_frac": result["moe"]["lock_break_ge_60s_fraction"],
            "throw_p10_m": result.get("kpp_08_throw_range_m", {}).get("p10"),
            "all_kpp_pass": all(result["kpp_checks"].values()),
            "kpp_checks": result["kpp_checks"],
        }
        manifest["jobs"].append(row)
        print(
            f"[DeepDive] {label} dur_p10={row['duration_p10']:.1f}s "
            f"moe={row['moe_lock_frac']:.3f} pass={row['all_kpp_pass']}"
        )

    manifest["elapsed_s"] = round(time.perf_counter() - t0, 2)
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"[DeepDive] Done in {manifest['elapsed_s']}s -> {args.out}")


if __name__ == "__main__":
    main()
