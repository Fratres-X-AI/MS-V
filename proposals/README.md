# Proposals Package — MS-V Veil

> **Defense Projects HQ / Fratres-X-AI**  
> **Package maturity:** TRL 2–3 **literature-parameter M&S** — **NOT field validation**  
> **License:** [CEL](../LICENSE) public evaluation · [PCA](../LICENSE-COMMERCIAL.md) for production

This folder holds **draft submission and partner-diligence artifacts**. They are written to be read by primes, sponsors, and technical reviewers — not as placeholders. Every performance statement must trace to [`rtm/verification_matrix.md`](../rtm/verification_matrix.md), [`rtm/assumption_register.md`](../rtm/assumption_register.md), or be labeled **notional** / **design authority**.

---

## How to use this package

| Audience | Start here | Then |
|----------|------------|------|
| **Capture / prime** | [`capture-brief.md`](capture-brief.md) | SRD → verification matrix → TEMP |
| **Repo technical reviewer** | [`../docs/EXTERNAL_REVIEW_READY.md`](../docs/EXTERNAL_REVIEW_READY.md) | Partner FAQ → reproduce |
| **Lab / range partner** | [`temp/MS-V-TEMP-outline.md`](temp/MS-V-TEMP-outline.md) | DOC-11 gates 2A–2E |

---

## Document inventory and purpose

| Document | Purpose | State | Lines (approx.) |
|----------|---------|-------|-----------------|
| [`capture-brief.md`](capture-brief.md) | 30s pitch, ask, have/have-not | **External-ready** | Brief |
| [`partner-evaluation-faq.md`](partner-evaluation-faq.md) | Repo diligence (CEL, MoE, reproduce) | **External-ready** | FAQ |
| [`srd/MS-V-SRD.md`](srd/MS-V-SRD.md) | Requirements, traceability, limitations, gaps | **Review-ready draft** | 160+ |
| [`temp/MS-V-TEMP-outline.md`](temp/MS-V-TEMP-outline.md) | TRL 3 test cards, resources, risks | **Review-ready outline** | 200+ |
| [`trl_gate_external.md`](trl_gate_external.md) | E-1..E-5 empirical gates | **Review-ready** | Gates |
| [`narratives/MS-V-program-narrative.md`](narratives/MS-V-program-narrative.md) | Submission narrative | **Draft** | Narrative |

**Not in this folder but required for claims:** [`rtm/verification_matrix.md`](../rtm/verification_matrix.md) (quantitative authority), [`analysis/MEGA_SUITE_REPORT.md`](../analysis/MEGA_SUITE_REPORT.md), [`MasterPlan.md`](../MasterPlan.md).

---

## Traceability rule (non-negotiable)

1. **KPP/MoE numbers** → matrix row + job ID (or `N/A` with status DESIGN_AUTHORITY / UNVERIFIED).
2. **MoE percentages** → disclose **A-013**; never “drone defeat rate.”
3. **Form factor** → **v2_kpp** only for external MS-V claims: **850 g**, **7.1 × 3.1 in**.
4. **Fill / range / tox** → TEMP gates until partner JSON populated.

---

## What is closed vs open

| Closed in-repo (M&S) | Open (external) |
|----------------------|-----------------|
| 140M phase2/v6 campaign | MS-V fill bench (E-1 / 2A–2B) |
| RTM + assumption register | UAS surrogate range (E-4 / 2D) |
| SRD/TEMP drafts | Throw trials n≥30 (E-2 / 2C) |
| Form factor + kinematics MC | Prototype mass/drawing (E-3) |
| CONOPS scenario MC | Tox KPP-12, cost KPP-13 |

---

## External visuals

| Doc | Role |
|-----|------|
| [Visual verification](../analysis/VISUAL_VERIFICATION.md) | v2 KPP canonical trio checklist |
| [Canonical renders](../analysis/figures/form_factor/CANONICAL_RENDERS.md) | Approved paths + caption |

**Required visual caption:** *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

---

## Maintenance

When updating KPP/MoE evidence: regenerate matrix (`python analysis/generate_verification_matrix.py`), update SRD §3.1 job table if primary jobs change, and bump TEMP only if gate definitions change.

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION*
