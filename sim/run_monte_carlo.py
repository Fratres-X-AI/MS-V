#!/usr/bin/env python3
"""Legacy entry — delegates to physics-based engine (single scenario)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sim.engine import SimConfig, load_params, run_vectorized  # noqa: E402


def main() -> None:
    params = load_params(ROOT)
    n = params["monte_carlo"]["n_samples"]
    cfg = SimConfig(n_samples=n, seed=params["monte_carlo"]["seed"], n_grenades=3, label="baseline_3_grenade")
    result = run_vectorized(params, cfg)
    out_dir = ROOT / "analysis" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "monte_carlo_baseline.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
