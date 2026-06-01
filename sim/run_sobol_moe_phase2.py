#!/usr/bin/env python3
"""Phase2 + v6 MoE Sobol — discriminative lock-break sensitivity (RunPod).

Uses full engine MC per Saltelli row (literature-bound pin values).

  python sim/run_sobol_moe_phase2.py --n-base 4096 --mc-n 3000 --workers 31
  python sim/run_sobol_moe_phase2.py --quick   # CI smoke
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

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402
from sim.runpod_util import _pool_worker_init, log_runpod_capacity, pin_blas_threads  # noqa: E402
from sim.sobol_phase2_engine import (  # noqa: E402
    _pin_params,
    build_moe_sobol_problem,
)


def _eval_row(row: np.ndarray, params: dict, mc_n: int, n_grenades: int, seed: int) -> dict[str, float]:
    p = _pin_params(params, row)
    result = run_vectorized(p, SimConfig(mc_n, seed, n_grenades, "sobol_moe_phase2"))
    return {
        "moe_met": float(result["moe"]["lock_break_ge_60s_fraction"]),
        "duration_p50": float(result["kpp_03_duration_effective_s"]["p50"]),
    }


def _worker_eval(args: tuple) -> tuple[int, dict[str, np.ndarray]]:
    chunk_idx, rows, mc_n, n_grenades, base_seed = args
    params = load_params(ROOT)
    moe: list[float] = []
    dur: list[float] = []
    for i, row in enumerate(rows):
        r = _eval_row(row, params, mc_n, n_grenades, base_seed + chunk_idx * 50_000 + i)
        moe.append(r["moe_met"])
        dur.append(r["duration_p50"])
    return chunk_idx, {"moe_met": np.asarray(moe), "duration_p50": np.asarray(dur)}


def evaluate_matrix(X: np.ndarray, mc_n: int, n_grenades: int, seed: int, workers: int) -> dict[str, np.ndarray]:
    n = X.shape[0]
    chunk_size = max(32, (n + workers - 1) // workers)
    chunks = [(i // chunk_size, X[i : i + chunk_size], mc_n, n_grenades, seed) for i in range(0, n, chunk_size)]
    merged: dict[str, list[np.ndarray]] = {"moe_met": [], "duration_p50": []}
    order: list[tuple[int, dict[str, np.ndarray]]] = []
    with ProcessPoolExecutor(max_workers=workers, initializer=_pool_worker_init) as pool:
        futs = {pool.submit(_worker_eval, c): c[0] for c in chunks}
        for fut in as_completed(futs):
            order.append(fut.result())
    order.sort(key=lambda x: x[0])
    for _, out in order:
        for k in merged:
            merged[k].append(out[k])
    return {k: np.concatenate(v) for k, v in merged.items()}


def main() -> None:
    from SALib.analyze import sobol

    try:
        from SALib.sample import sobol as sobol_sample
    except ImportError:
        from SALib.sample import saltelli as sobol_sample

    p = argparse.ArgumentParser(description="MS-V phase2 MoE Sobol")
    p.add_argument("--n-base", type=int, default=4096)
    p.add_argument("--mc-n", type=int, default=3000, help="MC samples per Saltelli row")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--n-grenades", type=int, default=3)
    p.add_argument("--seed", type=int, default=4242)
    p.add_argument("--quick", action="store_true")
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "sobol_moe_phase2")
    args = p.parse_args()
    if args.quick:
        args.n_base = 128
        args.mc_n = 500

    workers = args.workers or log_runpod_capacity()
    pin_blas_threads(workers)
    params = load_params(ROOT)
    problem = build_moe_sobol_problem(params)
    n_evals = args.n_base * (2 * problem["num_vars"] + 2)

    print(f"[MoE-Sobol phase2] N={args.n_base} D={problem['num_vars']} mc_n={args.mc_n} -> {n_evals:,} rows")
    print(f"[MoE-Sobol phase2] workers={workers} total MC ~ {n_evals * args.mc_n:,}")

    t0 = time.perf_counter()
    np.random.seed(args.seed)
    X = sobol_sample.sample(problem, args.n_base, calc_second_order=True)
    outputs = evaluate_matrix(X, args.mc_n, args.n_grenades, args.seed, workers)

    args.out.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "disclaimer": "LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION",
        "method": "Saltelli + Sobol (SALib) on phase2_v1_full_physics + v6_probabilistic_lock",
        "physics_tier": "phase2",
        "sensor_model": "v6_probabilistic_lock",
        "n_base": args.n_base,
        "mc_n_per_row": args.mc_n,
        "n_evaluations": int(X.shape[0]),
        "seed": args.seed,
        "n_grenades": args.n_grenades,
        "workers": workers,
        "problem": problem,
        "outputs": {},
        "elapsed_s": None,
    }

    for metric, Y in outputs.items():
        entry: dict[str, Any] = {
            "Y_mean": float(np.mean(Y)),
            "Y_std": float(np.std(Y)),
            "Y_p10": float(np.percentile(Y, 10)),
            "Y_p50": float(np.percentile(Y, 50)),
            "Y_p90": float(np.percentile(Y, 90)),
        }
        if float(np.std(Y)) < 1e-9:
            entry["status"] = "DEGENERATE"
            entry["rank_by_ST"] = []
            results["outputs"][metric] = entry
            continue
        Si = sobol.analyze(problem, Y, calc_second_order=True, conf_level=0.95, print_to_console=False)
        ranked = sorted(
            zip(problem["names"], Si["S1"], Si["ST"]),
            key=lambda x: x[2],
            reverse=True,
        )
        entry.update({
            "status": "OK",
            "rank_by_ST": [{"name": n, "S1": float(s1), "ST": float(st)} for n, s1, st in ranked],
        })
        results["outputs"][metric] = entry
        print(f"\n[MoE-Sobol] {metric} top 3 ST:")
        for n, s1, st in ranked[:3]:
            print(f"  {n:18s} S1={s1:.4f} ST={st:.4f}")

    results["elapsed_s"] = round(time.perf_counter() - t0, 2)
    out_json = args.out / "sobol_moe_phase2_results.json"
    out_json.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n[MoE-Sobol] Done in {results['elapsed_s']}s -> {out_json}")


if __name__ == "__main__":
    main()
