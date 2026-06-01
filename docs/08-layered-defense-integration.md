# 08 — Layered Defense Integration

MS-V = **multispectral obscuration layer**. Always with visual smoke. Never alone for MoE.

```
Detect → EW (optional) → MS-V + Signal Smoke → Kinetic (MKFS)
```

| Layer | MS-V role |
|-------|-----------|
| Detection | Cues when to throw — MS-V does not detect |
| EW | Jams RF; MS-V defeats EO/IR — complementary |
| Visual smoke | **Required partner** for FPV/fiber-optic MoE |
| Kinetic | MS-V buys time; kinetic closes kill chain |

**Primary target:** FPV and fiber-optic drones (EW-resistant → obscuration is the answer).

---

## Layer 1: Detection

MS-V does **not** detect threats. Detection cues the decision to employ MS-V.

| System | Cues MS-V Employment When... |
|--------|------------------------------|
| Acoustic | Drone audible overhead |
| RF detector | Control link detected (employ MS-V + EW) |
| Soldier observation | Visual contact with UAS |
| EO/IR spotter | Thermal signature of orbiting UAS |

---

## Layer 2: Non-Kinetic — Electronic Warfare

| Aspect | Detail |
|--------|--------|
| EW role | Jam RF datalink; degrade RF-controlled drones |
| MS-V role | Degrade EO/IR sensors |
| Combined | EW + MS-V + visual smoke for RF-linked FPV drones |
| Fiber-optic drones | **EW ineffective** — MS-V + visual smoke is primary defeat |
| Redundancy | Complementary, not redundant — different kill chain links |

---

## Layer 2: Non-Kinetic — Signal Smoke + MS-V (Combined Obscuration Package)

MS-V is **never the sole obscurant**. Standard employment pairs:

| Component | System | Function |
|-----------|--------|----------|
| Multispectral core | 2–3 × MS-V | VIS + NIR + MWIR attenuation |
| Visual supplement | 1–2 × AN-M8 / M83 | Enhanced visible opacity; signaling |
| Combined MoE | Both | Defeat/degrade FPV and fiber-optic drones |

### Why Both Are Required

| Drone Type | Visual Smoke Alone | MS-V Alone | Combined |
|------------|-------------------|------------|----------|
| FPV (visible + thermal) | Partial | Partial | **Effective** |
| Fiber-optic guided | Partial (VIS) | Partial (IR) | **Effective** |
| Thermal-only loitering | None | Partial | **Effective** |
| Visible-only commercial | Effective | Overkill | Effective |

AN-M8/M18/M83 remain in the basic load for signaling, marking, and visual screening. MS-V adds the IR channel inventory smoke cannot provide.

---

## Layer 2: Non-Kinetic — MS-V Unique Contribution

| Capability | Signal Smoke | MS-V | Combined |
|------------|-------------|------|----------|
| Defeat visible camera | Yes | Partial | Yes |
| Defeat thermal imager | **No** | Yes | Yes |
| 120+ s dense multispectral | No | Yes | Yes |
| FPV / fiber-optic MoE | No | Partial | **Yes** |
| Squad-portable | Yes | Yes | Yes |
| Signaling / marking | Yes | No | Via signal smoke |

---

## Layer 3: Kinetic (MKFS)

| Aspect | Detail |
|--------|--------|
| Role | Physically defeat UAS threats |
| MS-V relationship | MS-V creates obscuration window; kinetic closes kill chain |
| Sequence | MS-V + smoke deployed → lock degraded → kinetic engages if threat persists or attacks |
| Analog | IonStrike-class interceptors integrated with FAAD/IBCS C2 |
| CONOPS | Kinetic handoff not in standard MS-V CONOPS — reserved for attack profiles |

MS-V does not replace kinetic defeat. It buys time and degrades sensors so kinetic layers engage more effectively.

---

## Integration Matrix

| Threat Profile | Detection | EW | Visual Smoke | MS-V | Kinetic |
|---------------|-----------|-----|-------------|------|---------|
| FPV drone (RF + EO/IR) | Required | Recommended | **Required** | **Required (2–3×)** | If attack |
| Fiber-optic guided | Required | N/A | **Required** | **Required (2–3×)** | If attack |
| Observation UAS (EO/IR) | Required | Optional | Recommended | **Required (2–3×)** | No |
| Loitering munition | Required | Optional | **Required** | **Required (2–3×)** | **Required** |
| CASEVAC under UAS | Required | Optional | **Required** | **Required (2–3×)** | If attack |
| Break contact | Required | Optional | **Required** | **Required (2–3×)** | If attack |

---

## Issue Doctrine

### Basic Load (per soldier)

| Item | Quantity | Notes |
|------|----------|-------|
| AN-M8 / M83 (standard smoke) | Per unit SOP | Unchanged |
| M18 (signaling) | Per unit SOP | Unchanged |
| **MS-V** | **1–2** | Added to load; ~850 g each |
| EW device | Per TOE | Not every soldier |

**Load impact:** Two MS-V = 1.7 kg additional weight. Commanders must balance MS-V issue against mission duration and soldier load.

### Employment Authority

| Echelon | Authority |
|---------|-----------|
| Team leader | Immediate self-defense against drone observation |
| Squad leader | Per approved CONOPS |
| **Platoon sergeant** | **Primary employment authority** |
| Company | Allocation and resupply |

### Resupply

Company-level resupply through standard ammunition chain. MS-V expenditure tracked separately from signal smoke.

---

## Coordination Procedures

### Pre-Mission

1. Brief MS-V availability and combined employment requirement (MS-V + visual smoke)
2. Identify expected drone types (FPV, fiber-optic, RF-linked, attack)
3. Assign MS-V grenadiers (minimum 2 per platoon)
4. Coordinate EW if attached
5. Brief respiratory irritation and PPE guidance

### During Mission

1. Detection cues employment decision
2. Throw 2–3 MS-V + 1–2 visual smoke per event
3. Wait 12–15 s for effective density before movement
4. Report expenditure for resupply

### Post-Mission

1. Report MS-V and smoke expenditure separately
2. Debrief effectiveness (drone type, wind, combined employment, outcome)

See [04 — CONOPS / Use Cases](04-conops-use-cases.md) for scenario-level detail.
