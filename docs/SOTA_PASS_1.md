# SOTA Pass 1 — Multispectral Obscurant for Homeland CUAS (MS-V Veil)

**Document ID:** MS-V-SOTA-001  
**Pass:** 1 of N · **Date:** 2026-07-21  
**Maturity:** Literature / M&S survey — **not** empirical fill validation  
**Related:** [EXTERNAL_REVIEW_READY.md](EXTERNAL_REVIEW_READY.md) · [E1_FILL_PARTNER_ASK.md](E1_FILL_PARTNER_ASK.md) · TRL gates E-1–E-5 **OPEN**

---

## 1. Problem

Densified homeland and critical-infrastructure sites face Group 1–2 UAS that retain fused **EO + IR** sensors. Inventory visual smoke often fails against thermal imagers. RF electronic warfare fails against fiber-optic or autonomous guidance. Soft sites need a **transient obscuration** rung that is squad- or site-magazine portable — not a new exquisite launcher.

**Primary site classes (planning):** stadium · utility · data-center pad.

---

## 2. Practice classes (do not conflate)

| Class | Function | Gap vs MS-V intent |
|-------|----------|-------------------|
| Inventory visual smoke (AN-M8-class) | VIS obscure | Thermal often sees through |
| RF jammer / EW | Link disrupt | Fiber / autonomy bypass |
| Laser dazzler (MPL-D class) | Directed EO deny | Not IR cloud; NHZ / cue dependent |
| Persistent site camo (MS-C) | Always-on deny | Not transient engagement |
| Kinetic / nets | Hard stop | Magazine / ROE cost at densified scale |

**MS-V slot:** transient **VIS + NIR + MWIR** obscurant **paired with** visual smoke — soft-kill rung in a layered detect → deny → hold chain. Catalog ID: `MSV-VEIL-G1` ([effector_catalog.yaml](laundry_list/effector_catalog.yaml)).

---

## 3. Keep / replace / kill hypotheses

| ID | Hypothesis | Decision |
|----|------------|----------|
| H1 | IR channel required when thermal FPV is present | **Keep** |
| H2 | Paired visual smoke may improve MoE | **Keep as test hypothesis, not doctrine** |
| H3 | Hand-thrown / magazine form factor for homeland densification | **Keep** |
| H4 | Invent proprietary fill without a chemistry partner | **Kill** — E-1 requires fill/tox partner |
| H5 | Claim field MoE from M&S alone | **Kill** — A-013 |

---

## 4. Evidence today vs next gate

| Evidence | Status |
|----------|--------|
| 140M-sample sensitivity / verification matrix | **Digital sensitivity study** (literature bounds; several KPP/MoE rows not closed) |
| Form-factor v2 KPP (850 g, 7.1 × 3.1 in) | **Design authority** |
| Fill α(λ), burn, tox | **E-1 OPEN** |
| Throw / UAS surrogate / chamber | **E-2–E-5 OPEN** |

---

## 5. Layered concept (not doctrine)

```text
Detect → persistent deny (optional) → EW (optional) → MS-V + visual smoke (concept) → directed EO deny (optional) → kinetic / hold
```

Not a doctrine. No throw is authorized. Placement / magazine tools may list `MSV-VEIL-G1` as a planning schema entry only — not certified engagement performance, not a wind gate that has been validated. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).

---

## 6. Ask of reviewers

1. Review the homeland magazine paired-cloud hypothesis (2–3 Veil + smoke) for stadium / utility / data-center classes; do not treat it as employment.  
2. Name fill / tox partners for gate **E-1** ([partner ask](E1_FILL_PARTNER_ASK.md)).  
3. State what evidence earns manufacture LOI interest (inert mockup vs chamber).

---

*Traceability: [rtm/verification_matrix.md](../rtm/verification_matrix.md) · M&S: NOT VALIDATION*
