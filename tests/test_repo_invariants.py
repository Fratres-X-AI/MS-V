"""Repository quality invariants — fast gate for external-review readiness."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "LICENSE",
    "LICENSE-COMMERCIAL.md",
    "REPRODUCE.md",
    "rtm/verification_matrix.md",
    "analysis/MEGA_SUITE_REPORT.md",
    "analysis/FORM_FACTOR_REPORT.md",
    "analysis/results/mega_suite/manifest.json",
    "models/system/form_factor.yaml",
    "models/system/kinematics.py",
    "models/sensors/INTEGRATION.md",
    "proposals/capture-brief.md",
    "proposals/partner-evaluation-faq.md",
    "proposals/srd/MS-V-SRD.md",
    "proposals/temp/MS-V-TEMP-outline.md",
    "docs/EXTERNAL_REVIEW_READY.md",
    "proposals/README.md",
    "docs/linkedin-posting-guide.md",
    "tests/test_canonical_renders.py",
]


def test_required_artifacts_exist() -> None:
    missing = [p for p in REQUIRED_PATHS if not (ROOT / p).is_file()]
    assert not missing, f"missing required artifacts: {missing}"


def test_license_is_cel_not_mit() -> None:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Concept Evaluation License" in text or "CEL" in text
    assert re.search(r"^MIT License", text, re.M) is None


def test_readme_v2_kpp_and_cel() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "850 g" in text
    assert "7.1" in text
    assert "CEL" in text
    assert "NOT validation" in text or "NOT VALIDATION" in text


def test_form_factor_report_v2_authority() -> None:
    text = (ROOT / "analysis/FORM_FACTOR_REPORT.md").read_text(encoding="utf-8")
    assert "v2_kpp" in text
    assert "850" in text
    assert "7.1" in text


def test_form_factor_yaml_v2_mass() -> None:
    data = yaml.safe_load((ROOT / "models/system/form_factor.yaml").read_text(encoding="utf-8"))
    v2 = data["variants"]["v2_kpp"]
    assert int(v2["ms_v"]["mass_g"]) == 850


def test_params_default_phase2_v6() -> None:
    data = yaml.safe_load((ROOT / "models/cloud_physics/params.yaml").read_text(encoding="utf-8"))
    sim = data["sim"]
    assert sim["physics_tier"] == "phase2"
    assert sim["sensor_model"] == "v6_probabilistic_lock"


def test_mega_manifest_golden() -> None:
    m = json.loads((ROOT / "analysis/results/mega_suite/manifest.json").read_text(encoding="utf-8"))
    assert m["physics_tier"] == "phase2"
    assert m["total_samples"] == 140_000_000
    assert m["total_jobs"] == 38


def test_masterplan_not_stale_phase1b() -> None:
    text = (ROOT / "MasterPlan.md").read_text(encoding="utf-8")
    assert "Phase 1B active" not in text
    assert "1B-3 planned" not in text
    assert "MoE saturates 100% in v3" not in text
    assert "Delivered vs planned" in text


def test_proposals_maturity_line_counts() -> None:
    srd = (ROOT / "proposals/srd/MS-V-SRD.md").read_text(encoding="utf-8")
    temp = (ROOT / "proposals/temp/MS-V-TEMP-outline.md").read_text(encoding="utf-8")
    assert len(srd.splitlines()) >= 130
    assert len(temp.splitlines()) >= 150
    assert "SENSITIVITY_PASS" in srd
    assert "2A" in temp and "P0-1" in temp


def test_assumption_a013_v6_framing() -> None:
    text = (ROOT / "rtm/assumption_register.md").read_text(encoding="utf-8")
    assert "A-013" in text
    assert "80%" in text or "55%" in text


def test_verification_matrix_saturation_disclaimer() -> None:
    text = (ROOT / "rtm/verification_matrix.md").read_text(encoding="utf-8")
    assert "surrogate_saturated" in text
