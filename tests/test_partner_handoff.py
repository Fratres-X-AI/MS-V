"""Partner handoff schema and required repo artifacts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PARTNER_DOCS = [
    "LICENSE",
    "LICENSE-COMMERCIAL.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "docs/licensing-and-partnership.md",
    "docs/MS-V-one-pager.md",
    "docs/pitch-deck-outline.md",
    "docs/10-phase-1-prototype-gates.md",
    "docs/11-partner-validation-and-trl-gates.md",
    "visuals/README.md",
    "visuals/grenade/V2-KPP-SPEC.md",
    ".github/ISSUE_TEMPLATE/partnership_inquiry.yml",
]

TEMPLATE = ROOT / "data" / "partner_validation_results.template.json"


def test_partner_handoff_artifacts_exist() -> None:
    for rel in PARTNER_DOCS:
        path = ROOT / rel
        assert path.is_file(), f"missing partner handoff artifact: {rel}"


def test_partner_validation_template_is_valid_json() -> None:
    data = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert data["status"] == "pending"
    assert data["schema_version"]
    assert "phase_1_prototype" in data
    assert "phase_2_validation" in data
