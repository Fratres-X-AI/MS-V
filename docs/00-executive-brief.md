# MS-V Veil — Executive Brief

**One page.** For briefings, collaboration, and external sharing.

---

## What It Is

**MS-V (Veil)** is a hand-thrown multispectral obscurant grenade — a **squad-layer tool for drone manipulation**. Pin-pull, hand-throw, same basic TTP as smoke grenades. Generates a dense **visual + infrared** cloud to break drone observation when other layers fail or are saturated.

**Not** a detector. **Not** a jammer. **Not** a kinetic kill system. **Obscuration only.**

---

## The Gap

| Today (AN-M8 / M83) | With MS-V + visual smoke |
|---------------------|--------------------------|
| Defeats naked eye / day optics | Same |
| **Thermal sees through smoke** | **Thermal attenuated** |
| FPV / fiber-optic drones still track | **Both channels degraded** |
| EW can jam RF-linked drones | Fiber-optic drones: **obscuration is the answer** |

Soldiers have smoke. They do not have a **squad-portable multispectral screen** in the inventory.

---

## How It Works (Employment)

1. Detection or visual contact cues drone overwatch
2. Grenadier throws **2–3 MS-V + 1–2 standard visual smoke** (AN-M8/M83)
3. Effective screen in **~12–15 seconds**; dense coverage for **2+ minutes**
4. Squad moves, recovers casualty, breaks contact, or repositions under cover
5. Other layers (EW, kinetic) engage if threat persists or attacks

**Always pair MS-V with visual smoke** — required for FPV and fiber-optic drone MoE.

---

## Key Numbers (Design Targets)

| | MS-V Veil | AN-M8 (baseline) |
|--|-----------|------------------|
| Weight | ~850 g | 680 g |
| Duration | 120+ s dense | 105–150 s (VIS only) |
| Spectrum | VIS + NIR + MWIR | VIS only |
| Issue | +1–2 per soldier | Standard smoke load |
| Cost target | $75–150 | ~$15–25 |
| Fuze | M201A1-compatible | M201A1 |

---

## Design Philosophy

- **Soldier-first** — no new launchers, no new kill chain
- **Complementary** — carried *in addition to* signal smoke
- **Honest trades** — acceptable non-lethal respiratory irritation; heavier than standard smoke; 12–15 s build-up (not instant)
- **Built on precedent** — ECBC bispectral obscurant research; inventory grenade architecture

---

## Primary Use Cases

1. Casualty recovery under drone observation  
2. Break contact / exfil under drone pressure  
3. Mask movement across open ground  
4. Bounding overwatch / repositioning  
5. Hasty defense while improving a position  

---

## What It Will Not Do

- Jam RF or defeat autonomous navigation alone  
- Stop a committed one-way attack drone (needs kinetic layer)  
- Replace standard smoke for marking and signaling  
- Work as a single grenade against FPV/fiber-optic MoE  
- Perform in high wind (> 15 mph) or heavy rain without degradation  

---

## Layered Defense Position

```
Detect → EW (optional) → MS-V + Visual Smoke → Kinetic
```

MS-V is the **multispectral obscuration layer** at squad level. Vehicle systems (M56/M58, ROSY) prove the concept works — MS-V brings it to dismounted soldiers.

---

## Status

**TRL 2** — literature-parameter sensitivity study complete (140M samples, 38 jobs, Saltelli Sobol). **NOT field validation.**

| Finding | Evidence |
|---------|----------|
| Duration KPP (p10 ≥ 120 s) | +~42% margin in model (3× g3); literature bounds |
| Dominant variance driver | Burn rate (Sobol ST ≈ 0.83) → TRL 3 burn cup first |
| MoE surrogate (planning metric) | ~80% nominal / ~55% adversarial stack in v6 MC — **not field lock-break** |

**Limitations upfront:** No MS-V fill empirical data. MoE is a **planning surrogate** (A-013), not UAS test data.

**Repository:** https://github.com/Fratres-X-AI/MS-V (CEL — evaluation only) · **Public posts:** [`linkedin-posting-guide.md`](linkedin-posting-guide.md) · **Audit trail:** [`rtm/verification_matrix.md`](../rtm/verification_matrix.md)

---

## Traceability

- Verification matrix: [
tm/verification_matrix.md](../rtm/verification_matrix.md)
- Requirements CSV: [
tm/requirements_traceability.csv](../rtm/requirements_traceability.csv)
- Assumptions: [
tm/assumption_register.md](../rtm/assumption_register.md)
- Mega suite report: [nalysis/MEGA_SUITE_REPORT.md](../analysis/MEGA_SUITE_REPORT.md)
- Sobol sensitivity: [nalysis/SOBOL_SENSITIVITY_REPORT.md](../analysis/SOBOL_SENSITIVITY_REPORT.md)
- Reproduce gate: [REPRODUCE.md](../REPRODUCE.md)

