#!/usr/bin/env python3
"""Generate versioned figures from mega suite manifest + Sobol results."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis" / "results" / "mega_suite" / "manifest.json"
SOBOL = ROOT / "analysis" / "results" / "sobol" / "sobol_results.json"
OUT = ROOT / "analysis" / "figures"
PROVENANCE = OUT / "FIGURE_PROVENANCE.md"


def _load_manifest() -> list[dict]:
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["summary"]


def plot_duration_tornado(rows: list[dict], sobol: dict | None) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    if sobol and sobol.get("outputs", {}).get("duration_s", {}).get("status") == "OK":
        rank = sobol["outputs"]["duration_s"]["rank_by_ST"][:8]
        names = [r["name"] for r in rank]
        st = [r["ST"] for r in rank]
        ax.barh(names[::-1], st[::-1], color="#2c5282")
        ax.set_xlabel("Sobol total-order index (ST)")
        ax.set_title("KPP-03 Duration — global sensitivity (Sobol ST)")
        subtitle = f"N={sobol['n_base']:,} evals={sobol['n_evaluations']:,}"
    else:
        burn = [r for r in rows if "sweep_burn_hi" in r["label"]]
        burn.sort(key=lambda x: x["duration_p10"])
        names = [r["label"].replace("_n2000000", "") for r in burn]
        vals = [r["duration_p10"] for r in burn]
        ax.barh(names[::-1], vals[::-1], color="#744210")
        ax.axvline(120, color="red", linestyle="--", label="KPP-03 threshold")
        ax.set_xlabel("Duration p10 (s)")
        ax.set_title("Burn-rate sweep — OAT duration p10")
        subtitle = "mega_suite/manifest.json"
    ax.text(0.02, 0.02, subtitle, transform=ax.transAxes, fontsize=8, alpha=0.7)
    fig.tight_layout()
    path = OUT / "duration_sensitivity.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_job_duration_scatter(rows: list[dict]) -> Path:
    fig, ax = plt.subplots(figsize=(10, 4))
    labels = [r["label"].replace("_n10000000", "").replace("_n2000000", "") for r in rows]
    p10 = [r["duration_p10"] for r in rows]
    ax.scatter(range(len(p10)), p10, s=20, alpha=0.7)
    ax.axhline(120, color="red", linestyle="--", label="KPP-03 p10 ≥ 120 s")
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=6)
    ax.set_ylabel("Duration p10 (s)")
    ax.set_title("All 38 mega-suite jobs — duration p10")
    ax.legend()
    fig.tight_layout()
    path = OUT / "mega_suite_duration_p10.png"
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = _load_manifest()
    sobol = json.loads(SOBOL.read_text(encoding="utf-8")) if SOBOL.exists() else None

    paths = []
    if rows:
        paths.append(plot_job_duration_scatter(rows))
    paths.append(plot_duration_tornado(rows, sobol))

    lines = [
        "# Figure Provenance",
        "",
        "| Figure | Source | Command |",
        "|--------|--------|---------|",
    ]
    for p in paths:
        lines.append(f"| `{p.name}` | manifest + sobol | `python analysis/generate_figures.py` |")

    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for p in paths:
        print(f"Wrote {p}")
    print(f"Wrote {PROVENANCE}")


if __name__ == "__main__":
    main()
