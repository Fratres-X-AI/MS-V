#!/usr/bin/env python3
"""RunPod mega suite — baseline scale-up + parameter sweeps.

Usage:
  python sim/run_mega_suite.py
  python sim/run_mega_suite.py --workers 31 --quick   # smoke test locally
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402
from sim.run_runpod import ScenarioJob, _run_job  # noqa: E402
from sim.runpod_util import log_runpod_capacity, pin_blas_threads, run_parallel  # noqa: E402


def _deepcopy_params(p: dict) -> dict:
    return json.loads(json.dumps(p))


def _set_nested(d: dict, path: str, value: Any) -> None:
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        cur = cur[p]
    cur[parts[-1]] = value


@dataclass(frozen=True)
class SweepSpec:
    label: str
    n_samples: int
    seed: int
    n_grenades: int
    mutate: Callable[[dict], None]


def _adversarial(p: dict) -> None:
    p["environment"]["wind_speed_mph"] = {"min": 12, "max": 15}
    p["environment"]["temperature_c"] = {"min": 35, "max": 50}
    p["environment"]["humidity_rh_pct"] = {"min": 80, "max": 95}
    p["grenade"]["filler_mass_g"] = {"min": 624, "max": 640}
    p["grenade"]["burn_rate_g_s"] = {"min": 4.0, "max": 4.2}
    p["grenade"]["yield_factor"] = {"min": 0.22, "max": 0.30}


def _wind(wmin: float, wmax: float) -> Callable[[dict], None]:
    def fn(p: dict) -> None:
        p["environment"]["wind_speed_mph"] = {"min": wmin, "max": wmax}

    return fn


def build_sweep_jobs(params: dict, quick: bool = False) -> list[SweepSpec]:
    n_main = 50_000 if quick else 10_000_000
    n_sweep = 25_000 if quick else 2_000_000
    n_conv = 25_000 if quick else 2_000_000
    jobs: list[SweepSpec] = []

    # --- 10M baseline employment ---
    for ng in (1, 2, 3):
        jobs.append(SweepSpec(f"baseline_10M_g{ng}", n_main, 42 + ng, ng, lambda p, g=ng: None))

    # --- 10M wind bins (3 grenade) ---
    for label, wmin, wmax in [("calm", 0, 5), ("moderate", 5, 10), ("high", 10, 15)]:
        jobs.append(
            SweepSpec(
                f"baseline_10M_wind_{label}_g3",
                n_main,
                200 + hash(label) % 1000,
                3,
                _wind(wmin, wmax),
            )
        )

    # --- 10M adversarial stress ---
    jobs.append(SweepSpec("baseline_10M_adversarial_g3", n_main, 999, 3, _adversarial))

    # --- Visual smoke factor sweep (3 grenade, 2M) ---
    for vsf in (1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6):
        def mut(p: dict, v=vsf) -> None:
            p["employment"]["visual_smoke_factor"] = v

        jobs.append(SweepSpec(f"sweep_vis_smoke_{vsf:.1f}_g3", n_sweep, 300 + int(vsf * 10), 3, mut))

    # --- Yield factor lower-bound sweep (pessimistic aerosol production) ---
    for ylo in (0.18, 0.22, 0.26, 0.30, 0.34):
        def mut(p: dict, lo=ylo) -> None:
            p["grenade"]["yield_factor"]["min"] = lo
            p["grenade"]["yield_factor"]["max"] = min(lo + 0.20, 0.52)

        jobs.append(SweepSpec(f"sweep_yield_lo_{ylo:.2f}_g3", n_sweep, 400 + int(ylo * 100), 3, mut))

    # --- Burn rate upper-bound sweep ---
    for br in (3.6, 3.8, 4.0, 4.2, 4.4):
        def mut(p: dict, hi=br) -> None:
            p["grenade"]["burn_rate_g_s"]["max"] = hi
            p["grenade"]["burn_rate_g_s"]["min"] = max(2.9, hi - 1.3)

        jobs.append(SweepSpec(f"sweep_burn_hi_{br:.1f}_g3", n_sweep, 500 + int(br * 10), 3, mut))

    # --- Extinction band scenarios (2M) ---
    def alpha_tight(p: dict) -> None:
        for band in ("VIS", "NIR", "MWIR"):
            mid = p["extinction_coefficient_m2_per_g"][band]["mid"]
            p["extinction_coefficient_m2_per_g"][band]["low"] = mid * 0.85
            p["extinction_coefficient_m2_per_g"][band]["high"] = mid * 1.15

    def alpha_wide(p: dict) -> None:
        for band in ("VIS", "NIR", "MWIR"):
            spec = p["extinction_coefficient_m2_per_g"][band]
            spec["low"] = spec["low"] * 0.7
            spec["high"] = spec["high"] * 1.3

    def alpha_pessimistic(p: dict) -> None:
        for band in ("VIS", "NIR", "MWIR"):
            spec = p["extinction_coefficient_m2_per_g"][band]
            spec["low"] = spec["low"]
            spec["high"] = (spec["low"] + spec["mid"]) / 2  # sample lower alphas only

    jobs.append(SweepSpec("sweep_alpha_tight_g3", n_sweep, 601, 3, alpha_tight))
    jobs.append(SweepSpec("sweep_alpha_wide_g3", n_sweep, 602, 3, alpha_wide))
    jobs.append(SweepSpec("sweep_alpha_pessimistic_g3", n_sweep, 603, 3, alpha_pessimistic))

    # --- Multi-seed convergence (3 grenade, 2M) ---
    for seed in (42, 137, 271, 999, 2027, 4099, 8191):
        jobs.append(SweepSpec(f"convergence_seed_{seed}_g3", n_conv, seed, 3, lambda p: None))

    # --- Temperature stress bins (3 grenade, 2M) ---
    for label, tmin, tmax in [("cold", -20, 0), ("nominal", 5, 35), ("hot", 35, 50)]:
        def mut(p: dict, a=tmin, b=tmax) -> None:
            p["environment"]["temperature_c"] = {"min": a, "max": b}

        jobs.append(SweepSpec(f"sweep_temp_{label}_g3", n_sweep, 700 + abs(tmin), 3, mut))

    # --- Single-grenade duration margin (10M) ---
    jobs.append(SweepSpec("baseline_10M_single_g1_duration", n_main, 51, 1, lambda p: None))

    return jobs


def spec_to_job(base_params: dict, spec: SweepSpec) -> ScenarioJob:
    p = _deepcopy_params(base_params)
    spec.mutate(p)
    return ScenarioJob(
        label=f"{spec.label}_n{spec.n_samples}",
        params=p,
        n_samples=spec.n_samples,
        seed=spec.seed,
        n_grenades=spec.n_grenades,
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V RunPod mega suite")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "mega_suite")
    p.add_argument("--quick", action="store_true", help="Small n for smoke test")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    workers = args.workers or log_runpod_capacity()
    pin_blas_threads(workers)

    base = load_params(ROOT)
    specs = build_sweep_jobs(base, quick=args.quick)
    jobs = [spec_to_job(base, s) for s in specs]

    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    print(f"[MegaSuite] {len(jobs)} jobs, workers={workers}")
    total_samples = sum(j.n_samples for j in jobs)
    print(f"[MegaSuite] Total samples across all jobs: {total_samples:,}")

    completed = run_parallel(jobs, _run_job, max_workers=workers)

    summary_rows: list[dict] = []
    manifest: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "model_version": "phase1_v3_cl_ramp",
        "workers": workers,
        "vcpu": __import__("os").cpu_count(),
        "total_jobs": len(jobs),
        "total_samples": total_samples,
        "elapsed_s": None,
        "outputs": [],
        "summary": [],
    }

    for item in completed:
        label = item["label"]
        result = item["result"]
        out_path = args.out / f"{label}.json"
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        rel = str(out_path.relative_to(ROOT))
        manifest["outputs"].append(rel)

        row = {
            "label": label,
            "n_samples": result["config"]["n_samples"],
            "n_grenades": result["config"]["n_grenades"],
            "kpp_checks": result["kpp_checks"],
            "all_kpp_pass": all(result["kpp_checks"].values()),
            "duration_p10": result["kpp_03_duration_effective_s"]["p10"],
            "duration_p50": result["kpp_03_duration_effective_s"]["p50"],
            "build_up_p90": result["kpp_02_build_up_s"]["p90"],
            "moe_lock_frac": result["moe"]["lock_break_ge_60s_fraction"],
            "good_thickness_frac": result["physics_diagnostics"]["good_thickness_fraction"],
        }
        summary_rows.append(row)
        status = "PASS" if row["all_kpp_pass"] else "FAIL"
        print(
            f"[MegaSuite] {label} [{status}] "
            f"dur_p10={row['duration_p10']:.1f}s moe={row['moe_lock_frac']:.3f} "
            f"checks={result['kpp_checks']}"
        )

    manifest["summary"] = sorted(summary_rows, key=lambda r: r["label"])
    manifest["elapsed_s"] = round(time.perf_counter() - t0, 2)
    manifest["jobs_pass"] = sum(1 for r in summary_rows if r["all_kpp_pass"])
    manifest["jobs_fail"] = len(summary_rows) - manifest["jobs_pass"]

    with (args.out / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    with (args.out / "summary.csv").open("w", encoding="utf-8") as f:
        f.write("label,n_samples,n_grenades,all_kpp_pass,duration_p10,duration_p50,build_up_p90,moe_lock_frac,good_thickness_frac\n")
        for r in summary_rows:
            f.write(
                f"{r['label']},{r['n_samples']},{r['n_grenades']},{r['all_kpp_pass']},"
                f"{r['duration_p10']:.4f},{r['duration_p50']:.4f},{r['build_up_p90']:.4f},"
                f"{r['moe_lock_frac']:.6f},{r['good_thickness_frac']:.6f}\n"
            )

    print(
        f"\n[MegaSuite] Done in {manifest['elapsed_s']}s — "
        f"{manifest['jobs_pass']}/{len(summary_rows)} jobs all-KPP-pass"
    )
    print(f"Manifest: {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
