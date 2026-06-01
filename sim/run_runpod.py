#!/usr/bin/env python3
"""RunPod-scale Monte Carlo — run after renting GPU/CPU pod.

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
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V RunPod Monte Carlo")
    p.add_argument("--samples", type=int, default=None, help="Override n_samples")
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--grenades", type=int, nargs="+", default=[1, 2, 3])
    p.add_argument("--scenarios", choices=["all", "employment", "wind"], default="all")
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "runpod")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    params = load_params(ROOT)
    profile = params.get("profiles", {}).get("runpod", {})
    n = args.samples or profile.get("n_samples", 2_000_000)
    seed = args.seed or params["monte_carlo"]["seed"]

    args.out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    manifest: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "n_samples": n,
        "seed": seed,
        "elapsed_s": None,
        "outputs": [],
    }

    if args.scenarios in ("all", "employment"):
        for ng in args.grenades:
            label = f"grenades_{ng}_n{n}"
            print(f"[RunPod] {label}...")
            cfg = SimConfig(n_samples=n, seed=seed + ng, n_grenades=ng, label=label)
            result = run_vectorized(params, cfg)
            out_path = args.out / f"{label}.json"
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            manifest["outputs"].append(str(out_path.relative_to(ROOT)))
            print(f"  MoE lock>=60s: {result['moe']['lock_break_ge_60s_fraction']:.3f}")
            print(f"  KPP checks: {result['kpp_checks']}")

    if args.scenarios in ("all", "wind"):
        for wind_label, wmin, wmax in [("calm", 0, 5), ("moderate", 5, 10), ("high", 10, 15)]:
            p = json.loads(json.dumps(params))
            p["environment"]["wind_speed_mph"] = {"min": wmin, "max": wmax}
            label = f"wind_{wind_label}_3grenade_n{n}"
            cfg = SimConfig(n_samples=n, seed=seed + 100, n_grenades=3, label=label)
            result = run_vectorized(p, cfg)
            out_path = args.out / f"{label}.json"
            with out_path.open("w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            manifest["outputs"].append(str(out_path.relative_to(ROOT)))

    manifest["elapsed_s"] = round(time.perf_counter() - t0, 2)
    with (args.out / "manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nDone in {manifest['elapsed_s']}s. Manifest: {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
