"""RunPod parallelism helpers — max utilization, one core reserved."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")

_BLAS_VARS = (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)


def runpod_worker_count() -> int:
    """Rented pod policy: use every core except one."""
    return max(1, (os.cpu_count() or 1) - 1)


def pin_blas_threads(n: int) -> None:
    s = str(n)
    for var in _BLAS_VARS:
        os.environ[var] = s


def _pool_worker_init() -> None:
    pin_blas_threads(1)


def log_runpod_capacity() -> int:
    cores = os.cpu_count() or 1
    workers = runpod_worker_count()
    print(f"[RunPod] vCPU={cores} -> workers={workers} (max parallel, minus 1)")
    return workers


def run_parallel(
    tasks: Iterable[T],
    fn: Callable[[T], R],
    *,
    max_workers: int | None = None,
) -> list[R]:
    """Run independent tasks across n-1 worker processes."""
    workers = max_workers or runpod_worker_count()
    task_list = list(tasks)
    if not task_list:
        return []
    if workers <= 1 or len(task_list) == 1:
        pin_blas_threads(workers)
        return [fn(t) for t in task_list]

    results: list[R | None] = [None] * len(task_list)
    with ProcessPoolExecutor(max_workers=workers, initializer=_pool_worker_init) as pool:
        futures = {pool.submit(fn, task): i for i, task in enumerate(task_list)}
        for fut in as_completed(futures):
            results[futures[fut]] = fut.result()
    return results  # type: ignore[return-value]
