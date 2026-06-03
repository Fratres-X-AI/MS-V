"""Canonical visuals and mandatory caption standards."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_CAPTION = "Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation."

CAPTION_PATHS = [
    "visuals/README.md",
    "visuals/grenade/CAPTIONS.md",
    "analysis/VISUAL_VERIFICATION.md",
    "analysis/figures/form_factor/CANONICAL_RENDERS.md",
]


def test_visual_verification_pass_status() -> None:
    text = (ROOT / "analysis/VISUAL_VERIFICATION.md").read_text(encoding="utf-8")
    assert "PASS" in text
    assert "850 g" in text
    assert "7.1" in text


def test_form_factor_report_v2_kpp_numbers() -> None:
    text = (ROOT / "analysis/FORM_FACTOR_REPORT.md").read_text(encoding="utf-8")
    assert "850" in text
    assert "7.1" in text
    assert "v2_kpp" in text
    assert "3.1" in text


def test_mandatory_visual_caption_in_key_docs() -> None:
    for rel in CAPTION_PATHS:
        assert REQUIRED_CAPTION in (ROOT / rel).read_text(encoding="utf-8"), f"missing caption in {rel}"


def test_capture_brief_disclaims_validation() -> None:
    text = (ROOT / "proposals/capture-brief.md").read_text(encoding="utf-8")
    assert "NOT field validation" in text or "NOT VALIDATION" in text
