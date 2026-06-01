# MS-V System Geometry (Parametric)

Phase 2 digital representation — not CAD.

## Envelope Tracks

| Track | Mass | L × D | Authority |
|-------|------|-------|-----------|
| **v2_kpp** (primary) | 850 g | 7.1 × 3.1 in (180 × 79 mm) | Annex B, MasterPlan, KPP-01/09 |
| **v3_existing_container** | 680 g | 5.7 × 2.5 in (145 × 64 mm) | Production reuse — AN-M8/M18 shell |

See [`form_factor.yaml`](form_factor.yaml) · [`analysis/VISUAL_CONCEPT_ASSESSMENT.md`](../../analysis/VISUAL_CONCEPT_ASSESSMENT.md)

## v2 KPP Envelope (Primary)

| Parameter | Value | Source |
|-----------|-------|--------|
| Length | 7.1 in (180 mm) | KPP-09 |
| Diameter | 3.1 in (79 mm) | KPP-09 |
| Mass | 850 g | KPP-01 |
| Filler volume (est.) | ~670 cm³ | 650 g fill @ ~0.97 g/cm³ |
| Spectrum | VIS + NIR + MWIR | KPP-06 |

## Emission

| Parameter | Value |
|-----------|-------|
| Top ports | 4 |
| Bottom ports | 1 |
| Total port area (est.) | 0.0012 m² — UNVALIDATED |

## Fuze Interface

| Parameter | Value |
|-----------|-------|
| Fuze | M201A1-compatible |
| Delay | 0.7–2.0 s |

## Human Factors (Unvalidated)

| Parameter | Target | Notes |
|-----------|--------|-------|
| Throw range | 20–25 m | 850 g v2; no test data |
| Carry load (2× MS-V) | 1.7 kg | Plus standard smoke |
| Pouch fit | Standard grenade pouch (snug at v2) | Review required at 7.1 × 3.1 in |

## Figures

- Engineering (dimensioned): `analysis/figures/form_factor/engineering/`
- Concept renders (caption required): `analysis/figures/form_factor/renders/`

Regenerate engineering set: `python analysis/generate_engineering_drawings.py`

See [params.yaml](../cloud_physics/params.yaml) for simulation inputs.
