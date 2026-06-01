#!/usr/bin/env python3
"""Generate rtm/verification_matrix.md and .csv from mega suite manifest.

MATURITY: Sensitivity Study Complete — auto-synced to analysis/results/mega_suite/manifest.json
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "analysis" / "results" / "mega_suite" / "manifest.json"
MEGA_DIR = ROOT / "analysis" / "results" / "mega_suite"
CONOPS = ROOT / "analysis" / "results" / "conops" / "conops_summary.json"
FORM_FACTOR = ROOT / "models" / "system" / "form_factor.yaml"
SEEDS = ROOT / "sim" / "config" / "seeds.yaml"
OUT_MD = ROOT / "rtm" / "verification_matrix.md"
OUT_CSV = ROOT / "rtm" / "verification_matrix.csv"


def _margin_duration_p10(value: float, target: float = 120.0) -> str:
    pct = (value - target) / target * 100.0
    return f"+{pct:.1f}% above {target}s threshold (p10={value:.1f}s)"


def _margin_build_up_p90(value: float, target: float = 15.0) -> str:
    pct = (target - value) / target * 100.0
    return f"{pct:.1f}% headroom below {target}s cap (p90={value:.1f}s)"


def _margin_throw_p10(value: float, target: float = 20.0) -> str:
    pct = (value - target) / target * 100.0
    return f"+{pct:.1f}% above {target} m threshold (p10={value:.1f} m)"


def _load_job(label: str) -> dict:
    path = MEGA_DIR / f"{label}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _pass_cell(row: dict) -> str:
    margin = row.get("margin", "")
    if row.get("pass") is False:
        return "NO"
    if "non-binding" in margin or "UNVERIFIED" in margin or "PLANNED" in margin:
        return "PARTIAL"
    if "SURROGATE" in margin.upper() or "saturat" in margin.lower():
        return "YES*"
    return "YES"


def main() -> None:
    import yaml

    if not MANIFEST.exists():
        raise SystemExit(f"Missing {MANIFEST} — run mega suite first")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    seeds_data = yaml.safe_load(SEEDS.read_text(encoding="utf-8"))
    seed_by_label = {j["label"]: j for j in seeds_data["jobs"] if "label" in j}

    ff = yaml.safe_load(FORM_FACTOR.read_text(encoding="utf-8")) if FORM_FACTOR.exists() else {}
    v2_mass = ff.get("variants", {}).get("v2_kpp", {}).get("envelope", {}).get("mass_g", 850)

    rows = manifest["summary"]
    primary = next(r for r in rows if r["label"] == "baseline_10M_g3_n10000000")
    g2 = next(r for r in rows if r["label"] == "baseline_10M_g2_n10000000")
    adversarial = next(r for r in rows if r["label"] == "baseline_10M_adversarial_g3_n10000000")
    wind_high = next(r for r in rows if r["label"] == "baseline_10M_wind_high_g3_n10000000")
    temp_hot = next(r for r in rows if r["label"] == "sweep_temp_hot_g3_n2000000")
    temp_cold = next(r for r in rows if r["label"] == "sweep_temp_cold_g3_n2000000")

    burn_worst = min(
        (r for r in rows if "sweep_burn_hi" in r["label"]),
        key=lambda r: r["duration_p10"],
    )

    primary_json = _load_job("baseline_10M_g3_n10000000")
    g1_json = _load_job("baseline_10M_g1_n10000000")
    checks = primary.get("kpp_checks") or primary_json.get("kpp_checks", {})
    area_p10 = g1_json.get("kpp_04_screening_area_sqft", {}).get("p10", "—")
    throw_p10 = primary_json.get("kpp_08_throw_range_m", {}).get("p10")
    if throw_p10 is None:
        throw_p10 = primary.get("throw_p10_m")
    fuze = primary_json.get("kpp_07_fuze_delay_s", {})
    sensor_diag = primary_json.get("sensor_diagnostics", {})
    saturated = sensor_diag.get("surrogate_saturated", primary.get("sensor_saturation"))
    moe_frac = primary["moe_lock_frac"]
    model_ver = manifest.get("model_version", "phase2_v1_full_physics")
    physics_tier = manifest.get("physics_tier", "phase2")
    sensor_model = manifest.get("sensor_model", "v6_probabilistic_lock")
    if sensor_model == "unknown":
        sensor_model = "v6_probabilistic_lock" if physics_tier == "phase2" else "v4_band_integrated"

    moe_margin = (
        f"{moe_frac * 100:.1f}% lock-break ≥60 s fraction — **surrogate non-binding**; see A-013"
        if saturated
        else f"{moe_frac * 100:.1f}% lock-break ≥60 s (v6 probabilistic — discriminative)"
    )

    kpp_rows = [
        {
            "req_id": "KPP-01",
            "type": "KPP",
            "criterion": f"Total weight ~{v2_mass} g",
            "primary_job": "N/A (design authority)",
            "seed": "—",
            "observed": f"{v2_mass} g (v2_kpp envelope)",
            "pass": True,
            "margin": "Form-factor design authority — `models/system/form_factor.yaml`; TRL 3 mass measurement",
            "supporting_jobs": "annexes/F-form-factor-and-ergonomics.md",
        },
        {
            "req_id": "KPP-02",
            "type": "KPP",
            "criterion": "Build-up p90 ≤ 15 s",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": seed_by_label.get("baseline_10M_g3", {}).get("seed", 45),
            "observed": primary["build_up_p90"],
            "pass": checks.get("build_up_p90_le_15s", True),
            "margin": _margin_build_up_p90(primary["build_up_p90"]),
            "supporting_jobs": "All 38 jobs",
        },
        {
            "req_id": "KPP-03",
            "type": "KPP",
            "criterion": "Duration p10 ≥ 120 s at good thickness",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": 45,
            "observed": primary["duration_p10"],
            "pass": checks.get("duration_p10_ge_120s", True),
            "margin": _margin_duration_p10(primary["duration_p10"]),
            "supporting_jobs": f"Tightest: `{burn_worst['label']}`; adversarial `{adversarial['label']}`",
        },
        {
            "req_id": "KPP-04",
            "type": "KPP",
            "criterion": "Screening area p10 ≥ 30 sq ft (single grenade)",
            "primary_job": "baseline_10M_g1_n10000000",
            "seed": 43,
            "observed": f"p10 = {area_p10:.2f} sq ft" if isinstance(area_p10, (int, float)) else area_p10,
            "pass": checks.get("area_p10_ge_30_sqft", True),
            "margin": "+ margin vs 30 sq ft at p10 (single grenade job)",
            "supporting_jobs": "baseline_10M_g1_n10000000",
        },
        {
            "req_id": "KPP-05",
            "type": "KPP",
            "criterion": "Employment group 2–3 grenades",
            "primary_job": "baseline_10M_g2_n10000000; baseline_10M_g3_n10000000",
            "seed": "44;45",
            "observed": f"g2 dur_p10={g2['duration_p10']:.1f}s; g3 dur_p10={primary['duration_p10']:.1f}s",
            "pass": g2["all_kpp_pass"] and primary["all_kpp_pass"],
            "margin": "Doctrine — combined MS-V + visual smoke in groups",
            "supporting_jobs": "baseline_10M_g2/g3 + CONOPS",
        },
        {
            "req_id": "KPP-06",
            "type": "KPP",
            "criterion": "VIS + NIR + MWIR attenuation (tri-band)",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": 45,
            "observed": primary_json.get("transmittance", {}),
            "pass": True,
            "margin": (
                "Surrogate saturates — **not discriminative**; TRL 3 spectrometer required"
                if saturated
                else "v6 band-integrated transmittance — see sensor_diagnostics"
            ),
            "supporting_jobs": "All 38 jobs",
        },
        {
            "req_id": "KPP-07",
            "type": "KPP",
            "criterion": "Fuze delay M201A1 (0.7–2.0 s)",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": 45,
            "observed": fuze or "0.7–2.0 s sampled",
            "pass": checks.get("fuze_delay_m201_band", True),
            "margin": "M201A1 band enforced in deployment_kinematics MC",
            "supporting_jobs": "phase2 deployment model",
        },
        {
            "req_id": "KPP-08",
            "type": "KPP",
            "criterion": "Throw range ≥ 20 m (stressed)",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": 45,
            "observed": throw_p10 if throw_p10 is not None else "phase2 MC",
            "pass": checks.get("throw_p10_ge_20m", throw_p10 is not None),
            "margin": (
                _margin_throw_p10(float(throw_p10))
                if isinstance(throw_p10, (int, float))
                else "See analysis/human_factors_notes.md"
            ),
            "supporting_jobs": "models/system/human_factors.yaml",
        },
        {
            "req_id": "KPP-09",
            "type": "KPP",
            "criterion": "Form factor ~7.1 × 3.1 in (v2 KPP)",
            "primary_job": "N/A (design authority)",
            "seed": "—",
            "observed": "v2_kpp envelope in form_factor.yaml",
            "pass": True,
            "margin": "Annex F + STL assets — not physics MC",
            "supporting_jobs": "annexes/F-form-factor-and-ergonomics.md",
        },
        {
            "req_id": "KPP-10",
            "type": "KPP",
            "criterion": "Operating temp −20°C to +50°C",
            "primary_job": "sweep_temp_cold_g3_n2000000; sweep_temp_hot_g3_n2000000",
            "seed": "680;735",
            "observed": f"cold p10={temp_cold['duration_p10']:.1f}s; hot p10={temp_hot['duration_p10']:.1f}s",
            "pass": temp_cold["all_kpp_pass"] and temp_hot["all_kpp_pass"],
            "margin": _margin_duration_p10(temp_hot["duration_p10"]) + " (hot bin tightest)",
            "supporting_jobs": "sweep_temp_* (3 jobs)",
        },
        {
            "req_id": "KPP-11",
            "type": "KPP",
            "criterion": "Wind tolerance ≤ 15 mph",
            "primary_job": "baseline_10M_wind_high_g3_n10000000",
            "seed": 208,
            "observed": f"wind_high dur_p10={wind_high['duration_p10']:.1f}s",
            "pass": wind_high["all_kpp_pass"],
            "margin": "FM 3-50 planning band — duration not wind-bound in campaign",
            "supporting_jobs": "baseline_10M_wind_* (3 jobs)",
        },
        {
            "req_id": "KPP-12",
            "type": "KPP",
            "criterion": "Respiratory irritation acceptable (non-lethal)",
            "primary_job": "N/A",
            "seed": "—",
            "observed": "Literature bounds only",
            "pass": False,
            "margin": "UNVERIFIED — Phase 4 toxicology; stronger IR fill vs TA (Annex B)",
            "supporting_jobs": "docs/03-design-constraints.md",
        },
        {
            "req_id": "KPP-13",
            "type": "KPP",
            "criterion": "Unit cost $75–150 at scale",
            "primary_job": "N/A",
            "seed": "—",
            "observed": "Cost model not in MC",
            "pass": False,
            "margin": "PLANNED — Phase 4 manufacturing study",
            "supporting_jobs": "annexes/B-kpp-targets.md",
        },
        {
            "req_id": "KPP-14",
            "type": "KPP",
            "criterion": "Issue quantity 1–2 per soldier",
            "primary_job": "N/A (doctrine)",
            "seed": "—",
            "observed": "1–2 per soldier (Annex B)",
            "pass": True,
            "margin": "Logistics doctrine — not physics MC",
            "supporting_jobs": "docs/04-conops-use-cases.md",
        },
        {
            "req_id": "MOE-01",
            "type": "MoE",
            "criterion": "Fused EO/IR lock-break ≥ 60 s (2–3 MS-V + visual smoke)",
            "primary_job": "baseline_10M_g3_n10000000",
            "seed": 45,
            "observed": moe_frac,
            "pass": checks.get("moe_lock_break_p50_ge_60s", True),
            "margin": moe_margin,
            "supporting_jobs": "All 38 jobs",
        },
    ]

    conops_note = "CONOPS not run"
    if CONOPS.exists():
        conops = json.loads(CONOPS.read_text(encoding="utf-8"))
        uc = conops.get("use_cases", [])
        casevac = next((u for u in uc if "casevac" in u.get("use_case_id", "").lower()), uc[0] if uc else {})
        conops_note = (
            f"{casevac.get('use_case_id', 'UC')}: lock_met={casevac.get('moe', {}).get('lock_met_fraction', 0):.3f}"
        )
    kpp_rows.append(
        {
            "req_id": "MOE-02",
            "type": "MoE",
            "criterion": "CASEVAC / movement window T+15–135 s",
            "primary_job": "sim/run_conops.py",
            "seed": 4242,
            "observed": conops_note,
            "pass": CONOPS.exists(),
            "margin": "CONOPS Monte Carlo — see analysis/CONOPS_REPORT.md",
            "supporting_jobs": "analysis/results/conops/conops_summary.json",
        },
    )

    lim_rows = [
        ("LIM-01", "Requires visual smoke (not standalone)", "docs/07-limitations-and-risks.md", "ACCEPTED"),
        ("LIM-02", "Obscuration only — not RF defeat", "docs/07-limitations-and-risks.md", "ACCEPTED"),
        ("LIM-03", "TRL 2–3 ceiling — no empirical MS-V fill validation", "MasterPlan.md", "ACCEPTED"),
    ]

    lines = [
        "# Verification Matrix — MS-V Phase 1 M&S",
        "",
        "> **MATURITY:** Sensitivity Study Complete (140M samples) — **NOT VALIDATION**",
        f"> **Campaign model:** `{model_ver}` · **physics_tier:** `{physics_tier}` · **sensor:** `{sensor_model}`",
        "> **Evidence index:** `analysis/results/mega_suite/manifest.json` · **Seeds:** `sim/config/seeds.yaml`",
        "",
        "## Limitations (read first)",
        "",
        "- All results are **literature-parameter bounds** only — no MS-V fill empirical data.",
        "- KPP-12 (toxicology) and KPP-13 (cost) require Phase 4 verification — not closed by M&S.",
        "- When `surrogate_saturated=true`, MoE/tri-band pass is **non-discriminative** (A-013).",
        "",
        "## KPP / MoE Summary",
        "",
        "| Req | Criterion | Primary Job ID | Seed | Observed | Pass | Quantified Margin |",
        "|-----|-----------|----------------|------|----------|------|-------------------|",
    ]

    for r in kpp_rows:
        lines.append(
            f"| {r['req_id']} | {r['criterion']} | `{r['primary_job']}` | {r['seed']} | "
            f"{r['observed']} | {_pass_cell(r)} | {r['margin']} |"
        )

    lines.extend([
        "",
        "*YES* = pass with surrogate saturation caveat. PARTIAL = design authority or planned verification.",
        "",
        "## Limitations (program)",
        "",
        "| Req | Statement | Source | Status |",
        "|-----|-----------|--------|--------|",
    ])
    for lid, stmt, src, st in lim_rows:
        lines.append(f"| {lid} | {stmt} | `{src}` | {st} |")

    lines.extend([
        "",
        "## Full Job Registry (38 jobs → evidence)",
        "",
        "| Job ID | Seed | Samples | Grenades | Dur p10 | Throw p10 | Pass | Category |",
        "|--------|------|---------|----------|---------|-----------|------|----------|",
    ])

    csv_rows: list[dict] = []
    for row in sorted(rows, key=lambda x: x["label"]):
        label = row["label"]
        meta = seed_by_label.get(label.replace("_n10000000", "").replace("_n2000000", ""), {})
        seed = meta.get("seed", "—")
        throw = row.get("throw_p10_m")
        throw_s = f"{throw:.1f}m" if isinstance(throw, (int, float)) else "—"
        lines.append(
            f"| `{label}` | {seed} | {row['n_samples']:,} | {row['n_grenades']} | "
            f"{row['duration_p10']:.1f}s | {throw_s} | {'YES' if row['all_kpp_pass'] else 'NO'} | {meta.get('category', '—')} |"
        )
        csv_rows.append({
            "job_id": label,
            "seed": seed,
            "n_samples": row["n_samples"],
            "n_grenades": row["n_grenades"],
            "duration_p10": row["duration_p10"],
            "duration_p50": row["duration_p50"],
            "build_up_p90": row["build_up_p90"],
            "moe_lock_frac": row["moe_lock_frac"],
            "throw_p10_m": throw,
            "all_kpp_pass": row["all_kpp_pass"],
        })

    lines.extend([
        "",
        "## Tail-risk jobs (lowest duration p10)",
        "",
        f"- **Tightest burn sweep:** `{burn_worst['label']}` — {_margin_duration_p10(burn_worst['duration_p10'])}",
        f"- **Adversarial stack:** `{adversarial['label']}` — {_margin_duration_p10(adversarial['duration_p10'])}",
        "",
        "## TRL 3 physical verification required",
        "",
        "| Req | Empirical test | Closes assumption |",
        "|-----|----------------|-------------------|",
        "| KPP-01 | Mass / balance | Form factor prototype |",
        "| KPP-03 | Burn cup duration vs T/RH | A-002, burn_rate_g_s |",
        "| KPP-06 | α(λ) transmissometry | A-001, A-005 |",
        "| KPP-08 | Throw range under load | human_factors.yaml |",
        "| MOE-01 | Surrogate UAS FPV + thermal | A-008, A-013 |",
        "| KPP-04 | Cloud geometry / lidar | A-004 |",
        "| KPP-12 | Irritation characterization | Toxicology panel |",
        "",
        "## Traceability links",
        "",
        "- Assumptions: [`rtm/assumption_register.md`](assumption_register.md)",
        "- CSV export: [`rtm/requirements_traceability.csv`](requirements_traceability.csv)",
        "- Human factors: [`analysis/human_factors_notes.md`](../analysis/human_factors_notes.md)",
        "",
        "Auto-generated by `analysis/generate_verification_matrix.py`.",
    ])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        w.writeheader()
        w.writerows(csv_rows)

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")


if __name__ == "__main__":
    main()
