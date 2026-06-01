# MS-V System Geometry (Parametric)

Phase 2 digital representation — not CAD.

## Envelope

| Parameter | Value | Source |
|-----------|-------|--------|
| Length | 7.1 in (180 mm) | v2 design target (~25% > AN-M8) |
| Diameter | 3.1 in (79 mm) | v2 design target |
| Mass | 850 g | KPP-01 |
| Filler volume (est.) | ~710 cm³ | 650 g fill @ ~0.92 g/cm³ mean density |

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
| Throw range | 20–25 m | Heavier than AN-M8; no test data |
| Carry load (2× MS-V) | 1.7 kg | Plus standard smoke |
| Pouch fit | Standard grenade pouch (snug) | Phase 2 ergonomic review needed |

## Tier B Digital Representation

Parametric envelope, figures, and STL live under:

- [`form_factor.yaml`](form_factor.yaml) — machine-readable envelope
- [`envelope.py`](envelope.py) — volume budget + pouch fit
- [`analysis/figures/form_factor/`](../../analysis/figures/form_factor/) — scale, cutaway, employment, load, pouch
- [`annexes/F-form-factor-and-ergonomics.md`](../../annexes/F-form-factor-and-ergonomics.md) — one-page annex

Regenerate: `python analysis/generate_form_factor_assets.py` or `make form-factor`

See [params.yaml](../cloud_physics/params.yaml) for simulation inputs.
