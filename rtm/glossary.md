# MS-V Model Glossary

> Units and symbols used in M&S. Traceability: `models/cloud_physics/params.yaml`

| Symbol / Term | Units | Definition | Source file |
|---------------|-------|------------|-------------|
| **CL** | g/m² | Concentration-length (mass per unit area along LOS) | `cloud_evolution.py` |
| **α(λ)** | m²/g | Mass extinction coefficient at band λ | `extinction.py` |
| **T(λ)** | — | Spectral transmittance, Beer–Lambert: exp(−α·CL) | `extinction.py` |
| **τ** | — | Transmittance threshold for obscuration (default 0.15) | `params.yaml` moe |
| **VSF** | — | Visual smoke factor (AN-M8 partner boost, default 1.3) | `params.yaml` employment |
| **MoE** | — | Measure of Effectiveness | docs/02 |
| **KPP** | — | Key Performance Parameter | annexes/B |
| **Build-up** | s | Time to effective cloud density (KPP-02) | `cloud_evolution.py` |
| **Duration (effective)** | s | Seconds at good thickness during burn (KPP-03) | `cloud_evolution.py` |
| **Good thickness** | — | CL_peak ≥ CL_required for fused bands | `good_thickness_mask` |
| **Lock-break** | s | MoE window when fused EO/IR degraded ≥ threshold | `lock_break_*` |
| **Burn rate** | g/s | Mass consumption rate of fill | `burn_model.py` |
| **Yield factor** | — | Fraction of fill converted to airborne aerosol | `burn_model.py` |
| **Screening area** | sq ft / m² | Ground footprint of effective cloud | `screening_area_m2` |
| **Cloud depth** | m | Representative LOS depth through cloud | `params.yaml` |
| **Overlap efficiency** | — | Multi-grenade aerosol overlap (0.85) | `params.yaml` |
| **S1 / ST** | — | Sobol first-order / total-order sensitivity indices | `sim/run_sobol.py` |
| **OAT** | — | One-at-a-time parameter sweep | mega suite jobs |
| **Saltelli** | — | Quasi-random sampling scheme for Sobol analysis | SALib |

## Abbreviations

| Abbr | Meaning |
|------|---------|
| MS-V | Multispectral obscurant grenade (Veil) |
| VIS / NIR / MWIR | Visible / near-IR / mid-wave IR bands |
| HC | Hexachloroethane (AN-M8 smoke) |
| ECBC | Edgewood Chemical Biological Center |
| COMBIC | Combined obscuration planning doctrine |
| TRL | Technology Readiness Level |
| RTM | Requirements Traceability Matrix |
| TEMP | Test & Evaluation Master Plan |
| SRD | System Requirements Document |
| CONOPS | Concept of operations |
| UAS | Uncrewed aircraft system |
| FPV | First-person-view (visible EO) |
| DIU | Defense Innovation Unit |
| OTA | Other Transaction Authority |
| SBIR | Small Business Innovation Research |

## Job ID naming convention

`{category}_{scale}_{variant}_g{n}_n{samples}` — e.g. `baseline_10M_g3_n10000000`

Seeds and mutations: `sim/config/seeds.yaml`
