# MS-V Program Narrative (Submission Brief)

> **Maturity:** TRL 2–3 literature-parameter sensitivity — **NOT field validation**

MS-V Veil is a squad-portable multispectral obscurant grenade concept (~850 g, v2 KPP envelope) designed to test whether a paired visual + infrared cloud can degrade fused EO/IR UAS observation. The 2–3 MS-V + visual-smoke case is a model scenario, not a cleared employment method or measured lock-break claim.

## Evidence summary

- **140M-sample** mega suite under **phase2 microphysics + v6 probabilistic sensor** ([`rtm/verification_matrix.md`](../../rtm/verification_matrix.md))
- **Sobol global sensitivity** on 12 literature-bound parameters
- **CONOPS** five use cases, with MOE-02 explicitly not closed for movement
- **Form factor** design authority: Annex F, STL, canonical renders

## Differentiation

Unlike inventory HC/TA smokes (VIS-only or single-band), MS-V targets **VIS + NIR + MWIR** simultaneously while preserving squad portability vs vehicle systems.

## Honest limits

- No MS-V fill empirical data — all aerosol parameters from open literature
- Toxicology (KPP-12) and cost (KPP-13) planned Phase 4
- Sim pass ≠ design confirmation — see [`proposals/trl_gate_external.md`](../trl_gate_external.md)

## Traceability path for reviewers

1. [`rtm/verification_matrix.md`](../../rtm/verification_matrix.md) — KPP/MoE margins  
2. [`analysis/MEGA_SUITE_REPORT.md`](../../analysis/MEGA_SUITE_REPORT.md) — campaign summary  
3. [`sim/config/seeds.yaml`](../../sim/config/seeds.yaml) — reproducible seeds  
4. `python -m sim.reproduce` — golden checksum gate
