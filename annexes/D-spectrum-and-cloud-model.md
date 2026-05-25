# Annex D — Spectrum and Cloud Model (v2)

Electromagnetic spectrum bands, cloud development phases, and planning metrics for MS-V. Revised for v2 priorities: **density + duration**, 12–15 s build-up, 120+ s uniform phase, combined employment with visual smoke.

---

## Target Bands for MS-V

| Band | Wavelength (µm) | Threat Sensors | MS-V Priority |
|------|-----------------|----------------|---------------|
| VIS | 0.4 – 0.7 | Day cameras, FPV video | Required |
| NIR | 0.7 – 1.4 | Low-light, NVGs, some FPV | Required |
| MWIR | 3 – 5 | Cooled thermal, military UAS FLIR | Required |

MS-V must work in combination with standard visual smoke to defeat drones that fuse visible and thermal channels (FPV, fiber-optic guided).

---

## FPV and Fiber-Optic Drone Considerations

| Drone Type | Primary Sensors | Jam Resistance | MS-V + Visual Smoke Role |
|------------|----------------|----------------|--------------------------|
| RF-linked FPV | Visible camera + often uncooled thermal | EW may jam RF | MS-V breaks thermal; visual smoke breaks video link quality |
| Fiber-optic guided | Visible + thermal (no RF datalink) | **Immune to EW** | **Obscuration primary** — MS-V + visual smoke combined |
| Loitering munition (EO/IR) | Fused EO/IR seeker | Partial EW effect | Combined multispectral screen degrades seeker |
| Commercial quadcopter | Visible + uncooled LWIR | Variable | MS-V MWIR/NIR + AN-M8 VIS |

Fiber-optic and FPV drones that rely on both visual and thermal observation are the **primary MoE target** for combined MS-V + signal smoke employment.

---

## Cloud Development Phases

Per FM 3-50 Appendix G: **Streamer → Build-up → Uniform → Terminal**

### MS-V v2 Cloud Timing (Notional)

| Phase | AN-M8 HC (typical) | MS-V v2 Target | Notes |
|-------|-------------------|----------------|-------|
| Streamer | 3–5 s | 3–5 s | Comparable |
| Build-up | 5–15 s | 5–10 s | Thicker fill; slightly slower initial aerosolization |
| **Time to effective density** | **10–20 s** | **12–15 s** | Moderate priority |
| Uniform (effective thickness) | 80–120 s | **120+ s** | **High priority** |
| Terminal | 10–20 s | 10–15 s | Comparable |

### Planning Timeline

```
T+0 s     Pin pull, throw (MS-V + visual smoke pattern)
T+2 s     Ignition (fuze delay)
T+2–12 s  Streamer + build-up
T+12–15 s Effective density achieved — MOVEMENT WINDOW OPENS
T+15–135 s Effective screening (120+ s at good thickness)
T+135 s+  Terminal phase — plan for rescreen or completion of maneuver
```

**Planning rule:** Plan movement and CASEVAC actions between **T+15 s and T+135 s**. Do not rely on single grenade beyond terminal phase without rescreen.

---

## Combined Employment Pattern

MS-V alone does not meet full MoE against FPV/fiber-optic drones. Standard employment:

| Element | Grenade Type | Function |
|---------|-------------|----------|
| Multispectral core | 2–3 × MS-V | VIS + NIR + MWIR attenuation |
| Visual supplement | 1–2 × AN-M8 or M83 | Enhanced visible opacity; signaling if needed |
| Pattern | Triangular or linear overlap | 30–40 sq ft per MS-V; combined area covers fire team |

Throw MS-V slightly **upwind** of protected position when wind is present. Visual smoke may be thrown at same point or offset for coverage extension.

---

## Sensor Degradation Matrix

| Sensor | Visual Smoke Only | MS-V Only | MS-V + Visual Smoke |
|--------|------------------|-----------|---------------------|
| Visible FPV camera | Degraded | Partial | **Degraded** |
| Uncooled thermal (commercial) | **None** | Degraded | **Degraded** |
| Cooled MWIR (military) | **None** | Degraded | **Degraded** |
| Fused EO/IR tracker | Partial | Partial | **Significantly degraded** |
| Fiber-optic guided | Partial (VIS only) | Partial (IR only) | **Primary defeat mechanism** |

---

## Friendly Force Impact

MS-V multispectral clouds degrade friendly thermal optics inside or near the cloud. Employment doctrine:

- Throw **between threat sensor and friendly force**
- Brief friendly UAS operators on cloud location
- Mask when passing through dense cloud; brief exposure tolerable per KPP-12
- Combined visual smoke further degrades friendly visible optics — coordinate employment

---

## Atmospheric Effects

| Factor | Effect on MS-V v2 | Planning Guidance |
|--------|------------------|-------------------|
| Wind ≤ 15 mph | Effective for majority of burn | Throw upwind |
| Wind > 15 mph | Rapid dissipation | Not recommended |
| Temperature −20 to +50°C | Full performance | Standard range |
| Rain | Washout; duration reduced | Degraded employment |
| Urban canyon | Channeling; extended visible opacity | Useful for FPV defeat in streets |

See [docs/04-conops-use-cases.md](../docs/04-conops-use-cases.md) for scenario application.
