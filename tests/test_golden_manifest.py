"""Golden mega-suite manifest — committed 140M campaign integrity."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis" / "results" / "mega_suite" / "manifest.json"


def test_mega_suite_manifest_golden_fields() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["physics_tier"] == "phase2"
    assert data["sensor_model"] == "v6_probabilistic_lock"
    assert data["total_jobs"] == 38
    assert data["total_samples"] == 140_000_000
    outputs = data.get("outputs", [])
    assert len(outputs) == 38
    assert all("mega_suite" in p for p in outputs)
