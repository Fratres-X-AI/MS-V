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

BRIEF_REQUIRED_PHRASES = [
    "NOT field validation",
    "planning surrogate",
    "Option C",
    "Option B",
    "A-013",
    "Concept visualization only",
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
