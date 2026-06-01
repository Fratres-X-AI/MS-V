"""Pin the three user-approved v2 concept renders — do not regenerate over these."""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Approved trio from user upload (2026-05); see CANONICAL_RENDERS.md
CANONICAL_RENDERS: dict[str, str] = {
    "analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png": (
        "552e59d6318e212ae8422704f04f76cf492502f5882d4f61fdb6e0cfa610ec3a"
    ),
    "analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png": (
        "707e5e7eea08aa3a726e4ad6b76b4cae81102a78229eabd42d6910c7f5d4ce3c"
    ),
    "analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png": (
        "f48fc98431130c468bbf1d4f582c49b7b5eb5caec34cb80d4999e9de79d4b667"
    ),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_canonical_renders_exist_and_match_pins() -> None:
    for rel, expected in CANONICAL_RENDERS.items():
        path = ROOT / rel
        assert path.is_file(), f"missing canonical render: {rel}"
        assert path.stat().st_size > 10_000, f"canonical render too small: {rel}"
        assert _sha256(path) == expected, (
            f"canonical render changed (user-approved asset): {rel}\n"
            "Update CANONICAL_RENDERS.md and this test only after explicit approval."
        )
