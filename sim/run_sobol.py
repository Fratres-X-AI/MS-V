#!/usr/bin/env python3
"""Global sensitivity analysis — Saltelli + Sobol indices (SALib).

Run on RunPod at scale:
  python sim/run_sobol.py --n-base 8192 --workers 255
  python sim/run_sobol.py --quick   # CI smoke (n-base=256)

Outputs: analysis/results/sobol/sobol_results.json + param_values.npy
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import load_params  # noqa: E402
from sim.runpod_util import _pool_worker_init, log_runpod_capacity, pin_blas_threads  # noqa: E402
from sim.sobol_model import (  # noqa: E402
    build_sobol_problem,
    evaluate_physics_batch,
    outputs_to_Y,
)

OUTPUT_METRICS = [
    "duration_s",
    "build_up_s",
    "lock_break_s",
    "moe_met",
    "cl_peak",
]


def _eval_chunk(args: tuple) -> tuple[int, dict[str, np.ndarray]]:
    chunk_idx, X_chunk, params_path, n_grenades = args
    params = load_params(ROOT)
    out = evaluate_physics_batch(params, X_chunk, n_grenades=n_grenades)
    return chunk_idx, out


def evaluate_saltelli_matrix(
    X: np.ndarray,
    params: dict[str, Any],
    *,
    n_grenades: int,
    workers: int,
) -> dict[str, np.ndarray]:
    n = X.shape[0]
    if workers <= 1 or n < 10_000:
        return evaluate_physics_batch(params, X, n_grenades=n_grenades)

    chunk_size = max(500, (n + workers - 1) // workers)
    chunks: list[tuple[int, np.ndarray]] = []
    for i in range(0, n, chunk_size):
        chunks.append((i // chunk_size, X[i : i + chunk_size]))

    merged: dict[str, list[np.ndarray]] = {k: [] for k in OUTPUT_METRICS}
    order: list[tuple[int, dict[str, np.ndarray]]] = []

    # Params passed via load in worker to avoid pickle issues
    tasks = [(idx, chunk, str(ROOT / "models" / "cloud_physics" / "params.yaml"), n_grenades) for idx, chunk in chunks]

    with ProcessPoolExecutor(max_workers=workers, initializer=_pool_worker_init) as pool:
        futs = {pool.submit(_eval_chunk, t): t[0] for t in tasks}
        for fut in as_completed(futs):
            order.append(fut.result())

    order.sort(key=lambda x: x[0])
    for _, out in order:
        for k in OUTPUT_METRICS:
            merged[k].append(out[k])

    return {k: np.concatenate(v) for k, v in merged.items()}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V Sobol global sensitivity (Saltelli)")
    p.add_argument("--n-base", type=int, default=4096, help="Saltelli base sample size N")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--n-grenades", type=int, default=3)
    p.add_argument("--seed", type=int, default=4242)
    p.add_argument("--calc-second-order", action="store_true", default=True)
    p.add_argument("--no-second-order", action="store_true")
    p.add_argument("--quick", action="store_true", help="n-base=256 for CI")
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "sobol")
    return p.parse_args()


def main() -> None:
    from SALib.analyze import sobol
    try:
        from SALib.sample import sobol as sobol_sample
    except ImportError:
        from SALib.sample import saltelli as sobol_sample  # noqa: F401 — SALib <1.5

    args = parse_args()
    if args.quick:
        args.n_base = 256
    if args.no_second_order:
        args.calc_second_order = False

    workers = args.workers or log_runpod_capacity()
    pin_blas_threads(workers)

    params = load_params(ROOT)
    problem = build_sobol_problem(params)
    n_evals = args.n_base * (2 * problem["num_vars"] + 2)

    print(f"[Sobol] N={args.n_base} D={problem['num_vars']} -> {n_evals:,} evaluations")
    print(f"[Sobol] workers={workers} n_grenades={args.n_grenades} seed={args.seed}")

    t0 = time.perf_counter()
    np.random.seed(args.seed)
    param_values = sobol_sample.sample(
        problem,
        args.n_base,
        calc_second_order=args.calc_second_order,
    )

    outputs = evaluate_saltelli_matrix(
        param_values, params, n_grenades=args.n_grenades, workers=workers
    )

    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    np.save(args.out / "param_values.npy", param_values)

    results: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "method": "Saltelli + Sobol (SALib)",
        "n_base": args.n_base,
        "n_evaluations": int(param_values.shape[0]),
        "seed": args.seed,
        "n_grenades": args.n_grenades,
        "workers": workers,
        "problem": problem,
        "outputs": {},
        "elapsed_s": None,
    }

    for metric in OUTPUT_METRICS:
        Y = outputs_to_Y(outputs, metric)
        entry: dict[str, Any] = {
            "Y_mean": float(np.mean(Y)),
            "Y_std": float(np.std(Y)),
            "Y_p10": float(np.percentile(Y, 10)),
            "Y_p50": float(np.percentile(Y, 50)),
            "Y_p90": float(np.percentile(Y, 90)),
        }
        if float(np.std(Y)) < 1e-12:
            entry["status"] = "DEGENERATE — zero variance (surrogate saturation)"
            entry["rank_by_ST"] = []
            results["outputs"][metric] = entry
            print(f"\n[Sobol] {metric} — DEGENERATE (zero variance, likely surrogate saturation)")
            continue

        Si = sobol.analyze(
            problem,
            Y,
            calc_second_order=args.calc_second_order,
            conf_level=0.95,
            print_to_console=False,
        )
        ranked = sorted(
            zip(problem["names"], Si["S1"], Si["ST"]),
            key=lambda x: x[2],
            reverse=True,
        )
        entry.update({
            "status": "OK",
            "S1": {n: float(v) for n, v in zip(problem["names"], Si["S1"])},
            "ST": {n: float(v) for n, v in zip(problem["names"], Si["ST"])},
            "S1_conf": {n: float(v) for n, v in zip(problem["names"], Si["S1_conf"])},
            "ST_conf": {n: float(v) for n, v in zip(problem["names"], Si["ST_conf"])},
            "rank_by_ST": [{"name": n, "S1": float(s1), "ST": float(st)} for n, s1, st in ranked],
        })
        results["outputs"][metric] = entry
        print(f"\n[Sobol] {metric} — top 3 by ST:")
        for row in ranked[:3]:
            print(f"  {row[0]:22s} S1={row[1]:.4f} ST={row[2]:.4f}")

    results["elapsed_s"] = round(time.perf_counter() - t0, 2)
    out_json = args.out / "sobol_results.json"
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[Sobol] Done in {results['elapsed_s']}s -> {out_json}")


if __name__ == "__main__":
    main()
