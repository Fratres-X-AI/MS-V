"""LinkedIn / public posting readiness artifacts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/linkedin-posting-guide.md",
    "analysis/LINKEDIN_CAMPAIGN_BRIEF.md",
    "analysis/LINKEDIN_VISUAL_VERIFICATION.md",
    "proposals/capture-brief.md",
    "proposals/partner-evaluation-faq.md",
]

REQUIRED_CAPTION = "Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation."

BRIEF_REQUIRED_PHRASES = [
    "NOT field validation",
    "planning surrogate",
    "Option C",
    "Option B",
    "A-013",
    REQUIRED_CAPTION,
    "surrogate_saturated",
]


def test_linkedin_readiness_files_exist() -> None:
    for rel in REQUIRED_FILES:
        assert (ROOT / rel).is_file(), f"missing LinkedIn readiness file: {rel}"


def test_campaign_brief_has_conservative_framing() -> None:
    text = (ROOT / "analysis/LINKEDIN_CAMPAIGN_BRIEF.md").read_text(encoding="utf-8")
    for phrase in BRIEF_REQUIRED_PHRASES:
        assert phrase in text, f"LINKEDIN_CAMPAIGN_BRIEF missing required phrase: {phrase}"
    assert "Do not say" in text or "do NOT claim" in text.lower()


def test_visual_verification_pass_status() -> None:
    text = (ROOT / "analysis/LINKEDIN_VISUAL_VERIFICATION.md").read_text(encoding="utf-8")
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
    paths = [
        "visuals/README.md",
        "visuals/grenade/CAPTIONS.md",
        "analysis/LINKEDIN_VISUAL_VERIFICATION.md",
        "analysis/LINKEDIN_CAMPAIGN_BRIEF.md",
        "analysis/figures/form_factor/CANONICAL_RENDERS.md",
    ]
    for rel in paths:
        assert REQUIRED_CAPTION in (ROOT / rel).read_text(encoding="utf-8"), f"missing caption in {rel}"
