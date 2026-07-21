# MS-V Veil — Multispectral Obscurant Grenade

**Hand-thrown · Pin-pull · VIS + NIR + MWIR · Squad / site magazine**

**MS-V** is a multispectral obscurant **concept** that generates a dense visual + infrared cloud to degrade fused FPV/thermal UAS observation when **paired with standard visual smoke**. Employed as **2–3 MS-V + visual smoke**. Not a standalone smoke replacement.

| | |
|--|--|
| **Maturity** | TRL 2 — literature-parameter M&S complete (**not** field validation) |
| **Version** | **2.2.0** |
| **Envelope** | **850 g · 7.1 × 3.1 in** (v2 KPP design authority) |
| **License** | [CEL](LICENSE) evaluation · [PCA](LICENSE-COMMERCIAL.md) production |
| **Repository** | https://github.com/Fratres-X-AI/MS-V |

> **Reviewers:** [External review ready](docs/EXTERNAL_REVIEW_READY.md) → [Capture brief](proposals/capture-brief.md) → [Verification matrix](rtm/verification_matrix.md)  
> **Program status:** M&S digital gates G0–G4 **PASS** · Empirical E-1–E-5 **OPEN** · [SOTA Pass 1](docs/SOTA_PASS_1.md) · [E-1 partner ask](docs/E1_FILL_PARTNER_ASK.md)  
> **Quality gate:** `.\scripts\check.ps1` or `make check`

---

## Concept art (authoritative v2 KPP)

| **Product hero** | **True-scale vs inventory** | **Cutaway interior** |
|:---:|:---:|:---:|
| ![MS-V v2 hero](analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png) | ![Scale comparison](analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png) | ![MS-V v2 cutaway](analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png) |

*Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*  
Catalog: [visuals/README.md](visuals/README.md) · [VISUAL_VERIFICATION.md](analysis/VISUAL_VERIFICATION.md)

---

## Locked specifications (v2 KPP)

| Item | Spec | Status |
|------|------|--------|
| Role | Squad/site-layer obscuration vs fused EO/IR UAS | Locked |
| Mass | **850 g** | Design authority |
| Envelope | **7.1 × 3.1 in** (180 × 79 mm) | Design authority |
| Spectrum | **VIS + NIR + MWIR** | Locked |
| Duration | **≥ 120 s** dense (p10) | M&S sensitivity pass |
| Employment | **2–3 MS-V + visual smoke** | Locked |
| Throw (KPP-08) | **≥ 20 m** p10 (objective 25 m) | MC model; range TBD |
| Fuze | **M201A1-compatible** | Locked |
| Build-up | **≤ 15 s** p90 | M&S sensitivity pass |
| Cost target | **$75–150** at scale | PLANNED |

| Evidence class | Status |
|----------------|--------|
| 140M mega suite, RTM, Sobol, CONOPS | **Complete (M&S)** |
| Duration / MoE under literature bounds | **Sensitivity pass** (see A-013 for MoE) |
| Canonical concept art | **SHA256-pinned** |
| Fill α(λ), burn, tox, throw (empirical) | **OPEN — partner gates** |
| Field validation / military ready | **Forbidden claim** |

Full matrix: [rtm/verification_matrix.md](rtm/verification_matrix.md)

---

## M&S evidence (140M samples)

| Metric | Value | Framing |
|--------|-------|---------|
| Mega suite | **38/38** KPP rows pass in model | Literature bounds only |
| Duration p10 (3× g3) | **~170 s** (+42% vs 120 s KPP) | Model p10 — not measured |
| MoE lock-met ≥60 s | **~80%** nominal · **~55%** adversarial | **Planning surrogate (A-013)** — not defeat rate; check `surrogate_saturated` |
| Top Sobol driver | **burn_rate** ST ≈ 0.83 | Prioritizes E-1 burn cup |

```bash
pip install -r requirements-lock.txt
python -m sim.reproduce --validate-only   # fast gate
pytest tests/ -q
```

Reproduce: [REPRODUCE.md](REPRODUCE.md) · Campaign: [RUNPOD.md](RUNPOD.md)

---

## Comparison snapshot

| | AN-M8 HC | **MS-V Veil (v2)** |
|--|----------|---------------------|
| Weight | 680 g | **850 g** |
| Spectrum | VIS | **VIS + NIR + MWIR** |
| vs thermal UAS | Transparent | **Attenuation (concept)** |
| Employment | As needed | **2–3 + visual smoke** |
| TTP | Pin-pull throw | **Same** |

---

## Kill chain slot

```
Detect → EW → MS-V + smoke → kinetic / hold window
```

[CONOPS](docs/04-conops-use-cases.md) · [Limitations](docs/07-limitations-and-risks.md) · Stack catalog: [docs/laundry_list/](docs/laundry_list/)

---

## Document map

| # | Document |
|---|----------|
| 00–08 | [Concept docs](docs/) |
| 10–11 | [Prototype gates](docs/10-phase-1-prototype-gates.md) · [Partner TRL gates](docs/11-partner-validation-and-trl-gates.md) |
| Annex F | [Form factor](annexes/F-form-factor-and-ergonomics.md) |
| RTM | [verification_matrix.md](rtm/verification_matrix.md) |
| Analysis | [MEGA_SUITE_REPORT](analysis/MEGA_SUITE_REPORT.md) · [SOBOL](analysis/SOBOL_SENSITIVITY_REPORT.md) · [CONOPS_REPORT](analysis/CONOPS_REPORT.md) |

### Partner diligence

| Doc | Purpose |
|-----|---------|
| [External review ready](docs/EXTERNAL_REVIEW_READY.md) | Onboarding path |
| [SOTA Pass 1](docs/SOTA_PASS_1.md) | Problem framing & keep/kill |
| [E-1 fill partner ask](docs/E1_FILL_PARTNER_ASK.md) | Chemistry / tox solicitation |
| [Capture brief](proposals/capture-brief.md) | 30s pitch + ask |
| [SRD / TEMP](proposals/README.md) | Requirements + test outline |
| [Licensing & partnership](docs/licensing-and-partnership.md) | CEL / PCA |

---

## Open (external only)

- Fill chemistry down-select (Annex C) — **E-1**
- Empirical α(λ), burn rate, tox — **E-1**
- Throw range n≥30 — **E-2**
- UAS surrogate lock-break — **E-4** (A-013)
- Unit cost model — KPP-13 / Phase 4

---

## License

| Tier | Document |
|------|----------|
| Evaluation | [LICENSE](LICENSE) — CEL |
| Commercial / PCA | [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) |

Inquiry: [partnership template](https://github.com/Fratres-X-AI/MS-V/issues/new?template=partnership_inquiry.yml)

All specs, M&S outputs, and art are **notional** — not authorization to procure, manufacture, export, or field any munition or obscurant system.
