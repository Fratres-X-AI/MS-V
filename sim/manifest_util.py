"""Manifest and traceability helpers for MS-V simulation outputs."""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


def params_sha256(params_path: Path) -> str:
    return hashlib.sha256(params_path.read_bytes()).hexdigest()[:16]


def environment_spec() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "numpy": np.__version__,
    }


def build_traceability(
    *,
    job_id: str,
    seed: int,
    n_samples: int,
    n_grenades: int,
    model_version: str,
    params_path: Path,
    assumption_ids: list[str],
) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "seed": seed,
        "n_samples": n_samples,
        "n_grenades": n_grenades,
        "model_version": model_version,
        "params_file": str(params_path.relative_to(params_path.parents[2])).replace("\\", "/"),
        "params_sha256_16": params_sha256(params_path),
        "assumption_ids": assumption_ids,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def write_run_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
