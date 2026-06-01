#!/usr/bin/env python3
"""RunPod-scale Monte Carlo — run after renting CPU pod.

Usage:
  python sim/run_runpod.py
  python sim/run_runpod.py --samples 5000000 --scenarios all
  python sim/run_runpod.py --samples 1000000 --grenades 3

Outputs to analysis/results/runpod/
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402
from sim.runpod_util import log_runpod_capacity, pin_blas_threads, run_parallel  # noqa: E402


@dataclass(frozen=True)
class ScenarioJob:
    label: str
    params: dict
    n_samples: int
    seed: int
    n_grenades: int


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V RunPod Monte Carlo")
    p.add_argument("--samples", type=int, default=None, help="Override n_samples")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--grenades", type=int, nargs="+", default=[1, 2, 3])
    p.add_argument("--scenarios", choices=["all", "employment", "wind"], default="all")
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "runpod")
    p.add_argument("--workers", type=int, default=None, help="Override auto n-1 workers")
    return p.parse_args()


def _run_job(job: ScenarioJob) -> dict:
    cfg = SimConfig(
        n_samples=job.n_samples,
        seed=job.seed,
        n_grenades=job.n_grenades,
        label=job.label,
    )
    result = run_vectorized(job.params, cfg)
    return {"label": job.label, "result": result}


def _build_jobs(args: argparse.Namespace, params: dict, n: int, seed: int) -> list[ScenarioJob]:
    jobs: list[ScenarioJob] = []

    if args.scenarios in ("all", "employment"):
        for ng in args.grenades:
            jobs.append(
                ScenarioJob(
                    label=f"grenades_{ng}_n{n}",
                    params=params,
                    n_samples=n,
                    seed=seed + ng,
                    n_grenades=ng,
                )
            )

    if args.scenarios in ("all", "wind"):
        for wind_label, wmin, wmax in [("calm", 0, 5), ("moderate", 5, 10), ("high", 10, 15)]:
            p = json.loads(json.dumps(params))
            p["environment"]["wind_speed_mph"] = {"min": wmin, "max": wmax}
            jobs.append(
                ScenarioJob(
                    label=f"wind_{wind_label}_3grenade_n{n}",
                    params=p,
                    n_samples=n,
                    seed=seed + 100,
                    n_grenades=3,
                )
            )

    return jobs


def main() -> None:
    args = parse_args()
    workers = args.workers or log_runpod_capacity()
    pin_blas_threads(workers)

    params = load_params(ROOT)
    profile = params.get("profiles", {}).get("runpod", {})
    n = args.samples or profile.get("n_samples", 2_000_000)
    seed = args.seed or params["monte_carlo"]["seed"]

    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    manifest: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "n_samples": n,
        "seed": seed,
        "vcpu": __import__("os").cpu_count(),
        "workers": workers,
        "elapsed_s": None,
        "outputs": [],
    }

    jobs = _build_jobs(args, params, n, seed)
    print(f"[RunPod] {len(jobs)} scenario(s), max_workers={workers}")

    completed = run_parallel(jobs, _run_job, max_workers=workers)
    for item in completed:
        label = item["label"]
        result = item["result"]
        out_path = args.out / f"{label}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        manifest["outputs"].append(str(out_path.relative_to(ROOT)))
        print(f"[RunPod] {label} — MoE lock>=60s: {result['moe']['lock_break_ge_60s_fraction']:.3f}")
        print(f"  KPP checks: {result['kpp_checks']}")

    manifest["elapsed_s"] = round(time.perf_counter() - t0, 2)
    with (args.out / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDone in {manifest['elapsed_s']}s. Manifest: {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
