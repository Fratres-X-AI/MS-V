# LinkedIn Campaign Brief — MS-V Veil

> **Use this for posting.** All numbers from pod campaign `2026-06-01T22:06:57Z` @ 31 workers.  
> **Mandatory disclaimer:** Literature-parameter sensitivity study — **NOT field validation.**

## Pod Round 3 (2026-06-01T23:22:46Z)

| Job | N | Dur p10 | MoE |
|-----|---|---------|-----|
| burn_worst_50M | 50M | **161.8s** | 80.3% |
| adversarial_20M | 20M | **152.3s** | **55.1%** |
| baseline_confirm_50M | 50M | **169.9s** | 80.1% |
| burn seed stability | 2×10M | 161.8s ±0.01s | stable |

**140M focused tail-risk samples** — burn-worst p10 stable at 50M (seed spread 0.01s).

See `analysis/DEEP_DIVE_REPORT.md`

```bash
bash sim/run_pod_round3.sh
```

---

## Pod Round 2 (2026-06-01T23:18:21Z)

| Campaign | Scale | Notes |
|----------|-------|-------|
| Mega refresh | 140M | phase2/v6, 38/38 pass |
| CONOPS | **1M** samples × 5 cases | Stable lock-met fractions |
| MoE Sobol phase2 | N=**8192**, mc_n=**5000** → **573M** inner MC | burn_rate ST=0.82 on MoE |
| Duration Sobol | N=**32768** | Tighter burn-rate indices |
| Wind deep-dive | 2M × 3 wind bins × 3 grenade counts | `analysis/results/runpod/` |

```bash
export RUNPOD_CPU_COUNT=32
bash sim/run_pod_round2.sh
```

---

## Headline metrics (safe to cite)

| Metric | Value | Source |
|--------|-------|--------|
| Mega-suite samples | **140M** (38 jobs, all pass) | `manifest.json` |
| Physics stack | **phase2** microphysics + **v6** probabilistic EO/IR lock-break | engine |
| Duration margin (p10, 3× MS-V) | **+41.6%** vs 120 s KPP | verification matrix |
| MoE lock-break ≥60 s (baseline g3) | **80.1%** (discriminative — not saturated) | mega suite |
| Adversarial stack MoE | **55.1%** (stress case) | mega suite |
| CONOPS Monte Carlo | **500k** samples × 5 use cases | pod campaign |
| MoE Sobol (phase2 engine) | **172M** inner MC (57k Saltelli × 3k) | `sobol_moe_phase2` |
| Top MoE driver (ST) | **burn_rate_g_s 0.82** · α_MWIR 0.68 · humidity 0.68 | MoE Sobol report |

## What changed vs earlier posts

- MoE is **no longer 100% saturated** — v6 probabilistic sensor + phase2 physics gives **real spread** (55–98% across wind/employment cases).
- **KPP-08 throw** closed in MC (p10 ≥ 20 m stressed).
- Full **KPP-01–14 + MOE-01/02** traceability matrix published.

## Still do NOT claim

- Field validation, TRL 4+, military ready
- Empirical MS-V fill performance
- Toxicology (KPP-12) or cost (KPP-13) — Phase 4

## Canonical visuals (repo — user-approved trio)

**Carousel order:** hero → scale → cutaway

| # | File | Raw GitHub URL |
|---|------|----------------|
| 1 | `ms_v_v2_hero.png` | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_hero.png |
| 2 | `scale_comparison_v2_inventory.png` | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/engineering/scale_comparison_v2_inventory.png |
| 3 | `ms_v_v2_cutaway_photoreal.png` | https://raw.githubusercontent.com/Fratres-X-AI/MS-V/main/analysis/figures/form_factor/renders/v2_kpp/ms_v_v2_cutaway_photoreal.png |

Local paths: `analysis/figures/form_factor/` · Index: `CANONICAL_RENDERS.md` · Gallery: `renders/v2_kpp/index.html`

**Caption (required on every slide):** *Concept visualization only — v2 KPP (850 g, 7.1 × 3.1 in). Not validation.*

---

## Draft LinkedIn post (copy/edit)

**Option A — technical audience**

We just closed a 140-million-sample sensitivity campaign on MS-V Veil — a squad-portable multispectral obscurant grenade concept (~850 g, VIS+NIR+MWIR) designed to break fused FPV/thermal UAS lock when paired with standard visual smoke.

This is **modeling & simulation**, not field validation. But the rigor is real:

→ **140M Monte Carlo** runs across 38 scenarios (burn, temp, wind, adversarial stacks)  
→ **Phase 2 microphysics** — aerosol PSD, humidity growth, plume merge, deployment kinematics  
→ **Probabilistic EO/IR lock-break** — MoE now **discriminates** (80% nominal, 55% adversarial — not fake 100%)  
→ **Global sensitivity (Sobol)** — burn rate dominates duration *and* lock-break; MWIR extinction second for MoE  
→ **500k-sample CONOPS** — five kill-chain use cases with honest lock-met fractions  

Key result: at literature-bound parameters, MS-V holds **~170 s p10 effective duration** (3-grenade employment) with **+42% headroom** on the 120 s KPP — while showing where stress breaks MoE (high wind + adversarial stack).

Next gate: TRL 3 bench (burn cup, α(λ), throw range, UAS surrogate) — sim points the experiments.

Repo: github.com/Fratres-X-AI/MS-V  
#defense #modeling #counterUAS #smoke #simulation

---

**Option B — shorter / executive**

MS-V Veil: hand-thrown multispectral smoke for the drone era.

We ran **140M+ Monte Carlo samples** on cloud physics, sensor degradation, and five CONOPS kill chains — a literature-parameter **sensitivity study**, not field proof.

What the model says at bounded assumptions:
• ~**2.8 min** effective screen (p10) with 3 grenades + visual smoke  
• **80%** fused EO/IR lock-break under nominal conditions — **55%** under adversarial stress  
• Burn rate and MWIR extinction drive both duration and MoE — guides TRL 3 test priority  

Form factor: ~850 g, AN-M8-class employment. Full traceability matrix in repo.

Looking for partners on fill characterization + range validation.  
#defenseinnovation #counterUAS

---

## Pod re-run command

```bash
export RUNPOD_CPU_COUNT=32
bash sim/run_linkedin_campaign.sh
```
