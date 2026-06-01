"""RunPod parallelism helpers — max utilization, one core reserved."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
R = TypeVar("R")

_BLAS_VARS = (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)

_CGROUP_QUOTA = Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
_CGROUP_PERIOD = Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
_CGROUP_V2_MAX = Path("/sys/fs/cgroup/cpu.max")


def _cgroup_vcpu() -> int | None:
    """Return vCPU cap from cgroup when the host exposes more cores than rented."""
    try:
        if _CGROUP_QUOTA.is_file() and _CGROUP_PERIOD.is_file():
            quota = int(_CGROUP_QUOTA.read_text(encoding="utf-8").strip())
            period = int(_CGROUP_PERIOD.read_text(encoding="utf-8").strip())
            if quota > 0 and period > 0:
                return max(1, round(quota / period))
    except (OSError, ValueError):
        pass
    try:
        if _CGROUP_V2_MAX.is_file():
            parts = _CGROUP_V2_MAX.read_text(encoding="utf-8").strip().split()
            if len(parts) == 2 and parts[0] != "max":
                quota, period = int(parts[0]), int(parts[1])
                if quota > 0 and period > 0:
                    return max(1, round(quota / period))
    except (OSError, ValueError):
        pass
    return None


def effective_vcpu() -> int:
    """Authoritative rented vCPU count: env override > cgroup > os.cpu_count()."""
    raw = os.environ.get("RUNPOD_CPU_COUNT", "").strip()
    if raw:
        return max(1, int(raw))
    cgroup = _cgroup_vcpu()
    if cgroup is not None:
        return cgroup
    return os.cpu_count() or 1


def runpod_worker_count() -> int:
    """Rented pod policy: use every core except one."""
    return max(1, effective_vcpu() - 1)


def pin_blas_threads(n: int) -> None:
    s = str(n)
    for var in _BLAS_VARS:
        os.environ[var] = s


def _pool_worker_init() -> None:
    pin_blas_threads(1)


def log_runpod_capacity() -> int:
    host = os.cpu_count() or 1
    vcpu = effective_vcpu()
    workers = runpod_worker_count()
    src = "RUNPOD_CPU_COUNT" if os.environ.get("RUNPOD_CPU_COUNT") else (
        "cgroup" if vcpu != host else "host"
    )
    print(
        f"[RunPod] host_cpus={host} effective_vcpu={vcpu} ({src}) "
        f"-> workers={workers} (max parallel, minus 1)"
    )
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
