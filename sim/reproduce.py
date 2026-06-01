#!/usr/bin/env python3
"""Reproducibility harness — regenerate baseline results and validate golden checksums.

Usage:
  python -m sim.reproduce
  python -m sim.reproduce --validate-only
  python -m sim.reproduce --help

MATURITY: Sensitivity Study Complete (baseline profile)
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402
from sim.manifest_util import environment_spec, write_run_manifest  # noqa: E402

GOLDEN = ROOT / "analysis" / "reproduce_golden.json"
RESULTS = ROOT / "analysis" / "results"
TOLERANCE = 1e-4  # relative for float metrics

logging.basicConfig(level=logging.INFO, format="[reproduce] %(message)s")
log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MS-V reproducibility harness")
    p.add_argument("--validate-only", action="store_true", help="Skip run; validate existing outputs")
    p.add_argument("--tolerance", type=float, default=TOLERANCE)
    return p.parse_args()


def _rel_close(a: float, b: float, tol: float) -> bool:
    if a == b:
        return True
    scale = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / scale <= tol


def _extract_metrics(result: dict) -> dict[str, float]:
    return {
        "duration_p10": result["kpp_03_duration_effective_s"]["p10"],
        "duration_p50": result["kpp_03_duration_effective_s"]["p50"],
        "build_up_p90": result["kpp_02_build_up_s"]["p90"],
        "area_p10": result["kpp_04_screening_area_sqft"]["p10"],
        "moe_lock_frac": result["moe"]["lock_break_ge_60s_fraction"],
        "moe_degraded_frac": result["moe"]["fused_eoir_degraded_fraction"],
    }


def run_baseline_jobs() -> dict[str, dict]:
    params = load_params(ROOT)
    local_n = params["profiles"]["local"]["n_samples"]
    seed = params["monte_carlo"]["seed"]
    jobs = {
        "three_grenade_group": SimConfig(local_n, seed + 2, 3, "three_grenade_group"),
        "single_grenade": SimConfig(local_n, seed, 1, "single_grenade"),
    }
    out: dict[str, dict] = {}
    for name, cfg in jobs.items():
        log.info("Running %s (n=%s, seed=%s)...", name, cfg.n_samples, cfg.seed)
        result = run_vectorized(params, cfg)
        path = RESULTS / f"{name}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        out[name] = result
    return out


def validate_against_golden(results: dict[str, dict], tol: float) -> list[str]:
    if not GOLDEN.exists():
        return [f"Missing golden file: {GOLDEN}"]
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    errors: list[str] = []
    for job, expected in golden["jobs"].items():
        if job not in results:
            errors.append(f"Missing job result: {job}")
            continue
        got = _extract_metrics(results[job])
        for key, exp_val in expected["metrics"].items():
            if key not in got:
                errors.append(f"{job}: missing metric {key}")
                continue
            if not _rel_close(got[key], exp_val, tol):
                errors.append(f"{job}.{key}: got {got[key]}, expected {exp_val}")
    return errors


def run_downstream_summaries() -> None:
    for script in (
        "analysis/summarize_results.py",
        "analysis/analyze_tail_risk.py",
    ):
        log.info("Running %s...", script)
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def main() -> None:
    args = parse_args()
    manifest = {
        "harness": "sim.reproduce",
        "environment": environment_spec(),
        "golden_file": str(GOLDEN.relative_to(ROOT)).replace("\\", "/"),
        "tolerance": args.tolerance,
    }

    if args.validate_only:
        results = {}
        for name in ("three_grenade_group", "single_grenade"):
            path = RESULTS / f"{name}.json"
            if not path.exists():
                log.error("Missing %s — run without --validate-only", path)
                sys.exit(1)
            results[name] = json.loads(path.read_text(encoding="utf-8"))
    else:
        results = run_baseline_jobs()
        run_downstream_summaries()

    errors = validate_against_golden(results, args.tolerance)
    manifest["validation_errors"] = errors
    manifest["validation_pass"] = len(errors) == 0
    write_run_manifest(RESULTS / "reproduce_manifest.json", manifest)

    if errors:
        log.error("Reproducibility validation FAILED:")
        for e in errors:
            log.error("  %s", e)
        sys.exit(1)
    log.info("Reproducibility validation PASSED (%s)", GOLDEN.name)


if __name__ == "__main__":
    main()
