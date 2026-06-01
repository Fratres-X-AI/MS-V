#!/usr/bin/env python3
"""Run CONOPS Monte Carlo for all five use cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.conops.kill_chain import run_all_use_cases  # noqa: E402
from sim.engine import load_params  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="MS-V CONOPS kill-chain Monte Carlo")
    p.add_argument("--samples", type=int, default=100_000)
    p.add_argument("--seed", type=int, default=4242)
    p.add_argument("--out", type=Path, default=ROOT / "analysis" / "results" / "conops")
    args = p.parse_args()

    params = load_params(ROOT)
    result = run_all_use_cases(params, n_samples=args.samples, seed=args.seed)

    args.out.mkdir(parents=True, exist_ok=True)
    out_path = args.out / "conops_summary.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"Wrote {out_path}")
    for uc in result["use_cases"]:
        print(
            f"  {uc['use_case_id']:22s} lock_met={uc['moe']['lock_met_fraction']:.3f} "
            f"obscured={uc['moe']['obscured_fraction']:.3f} "
            f"friendly_blind={uc['moe']['friendly_blinded_fraction']:.3f}"
        )


if __name__ == "__main__":
    main()
