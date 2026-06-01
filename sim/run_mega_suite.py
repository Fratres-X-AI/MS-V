#!/usr/bin/env python3
"""RunPod mega suite — baseline scale-up + parameter sweeps.

Usage:
  python sim/run_mega_suite.py
  python sim/run_mega_suite.py --workers 31 --quick   # smoke test locally
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import load_params  # noqa: E402
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


def load_seed_manifest(quick: bool = False) -> list[dict]:
    """Load authoritative job list from sim/config/seeds.yaml."""
    import yaml

    path = ROOT / "sim" / "config" / "seeds.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    jobs = data["jobs"]
    if quick:
        scaled = []
        for j in jobs:
            j = dict(j)
            j["n_samples"] = 25_000 if j["n_samples"] > 100_000 else j["n_samples"]
            if j["n_samples"] >= 1_000_000:
                j["n_samples"] = 50_000
            scaled.append(j)
        return scaled
    return jobs


def _mutator_for_job(meta: dict) -> Callable[[dict], None]:
    """Return parameter mutation closure for a seed-manifest job entry."""
    label = meta.get("label", "")

    if meta.get("category") == "baseline_wind":
        w = meta["wind_mph"]
        return _wind(w[0], w[1])
    if meta.get("category") == "stress_adversarial":
        return _adversarial
    if meta.get("category") == "sweep_visual_smoke":
        vsf = float(meta["visual_smoke_factor"])

        def mut(p: dict, v=vsf) -> None:
            p["employment"]["visual_smoke_factor"] = v

        return mut
    if meta.get("category") == "sweep_yield":
        ylo = float(meta["yield_min"])

        def mut(p: dict, lo=ylo) -> None:
            p["grenade"]["yield_factor"]["min"] = lo
            p["grenade"]["yield_factor"]["max"] = min(lo + 0.20, 0.52)

        return mut
    if meta.get("category") == "sweep_burn_rate":
        hi = float(meta["burn_max_g_s"])

        def mut(p: dict, h=hi) -> None:
            p["grenade"]["burn_rate_g_s"]["max"] = h
            p["grenade"]["burn_rate_g_s"]["min"] = max(2.9, h - 1.3)

        return mut
    if meta.get("category") == "sweep_alpha":
        if "pessimistic" in label:

            def mut(p: dict) -> None:
                for band in ("VIS", "NIR", "MWIR"):
                    spec = p["extinction_coefficient_m2_per_g"][band]
                    spec["high"] = (spec["low"] + spec["mid"]) / 2

            return mut
        if "tight" in label:

            def mut(p: dict) -> None:
                for band in ("VIS", "NIR", "MWIR"):
                    mid = p["extinction_coefficient_m2_per_g"][band]["mid"]
                    p["extinction_coefficient_m2_per_g"][band]["low"] = mid * 0.85
                    p["extinction_coefficient_m2_per_g"][band]["high"] = mid * 1.15

            return mut
        if "wide" in label:

            def mut(p: dict) -> None:
                for band in ("VIS", "NIR", "MWIR"):
                    spec = p["extinction_coefficient_m2_per_g"][band]
                    spec["low"] = spec["low"] * 0.7
                    spec["high"] = spec["high"] * 1.3

            return mut
    if meta.get("category") == "sweep_temperature":
        t = meta["temp_c"]

        def mut(p: dict, a=t[0], b=t[1]) -> None:
            p["environment"]["temperature_c"] = {"min": a, "max": b}

        return mut
    return lambda p: None


def build_sweep_jobs(params: dict, quick: bool = False) -> list[SweepSpec]:
    jobs: list[SweepSpec] = []
    for meta in load_seed_manifest(quick):
        label = meta["label"]
        n = int(meta["n_samples"])
        jobs.append(
            SweepSpec(
                label=label,
                n_samples=n,
                seed=int(meta["seed"]),
                n_grenades=int(meta["n_grenades"]),
                mutate=_mutator_for_job(meta),
            )
        )
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


def load_mega_params(root: Path) -> dict:
    """Mega suite uses current engine defaults (phase2 + v6 sensor)."""
    p = load_params(root)
    p.setdefault("sim", {})
    tier = p["sim"].get("physics_tier", "phase2")
    sensor = p["sim"].get("sensor_model", "v6_probabilistic_lock")
    p["sim"]["physics_tier"] = tier
    p["sim"]["sensor_model"] = sensor
    return p


def main() -> None:
    args = parse_args()
    workers = args.workers or log_runpod_capacity()
    pin_blas_threads(workers)

    base = load_mega_params(ROOT)
    campaign_tier = base["sim"]["physics_tier"]
    campaign_sensor = base["sim"]["sensor_model"]
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
        "model_version": "phase2_v1_full_physics",
        "physics_tier": campaign_tier,
        "sensor_model": campaign_sensor,
        "workers": workers,
        "effective_vcpu": int(__import__("os").environ.get("RUNPOD_CPU_COUNT") or 0) or None,
        "host_cpus": __import__("os").cpu_count(),
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
            "throw_p10_m": result.get("kpp_08_throw_range_m", {}).get("p10"),
            "sensor_saturation": result.get("sensor_diagnostics", {}).get("surrogate_saturated"),
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
