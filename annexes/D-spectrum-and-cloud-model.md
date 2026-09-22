# Annex D — Spectrum and Cloud Model (v2)

Electromagnetic spectrum bands, cloud development phases, and planning metrics for MS-V. Revised for v2 priorities: **density + duration**, 12–15 s build-up, and 120+ s model duration. Pairing with visual smoke is a model scenario, not employment doctrine.

---

## Target Bands for MS-V

| Band | Wavelength (µm) | Threat Sensors | MS-V Priority |
|------|-----------------|----------------|---------------|
| VIS | 0.4 – 0.7 | Day cameras, FPV video | Required |
| NIR | 0.7 – 1.4 | Low-light, NVGs, some FPV | Required |
| MWIR | 3 – 5 | Cooled thermal, military UAS FLIR | Required |

MS-V would need measured performance in combination with standard visual smoke before any claim against drones that fuse visible and thermal channels (FPV, fiber-optic guided).

---

## FPV and Fiber-Optic Drone Considerations

| Drone Type | Primary Sensors | Jam Resistance | MS-V + Visual Smoke Role |
|------------|----------------|----------------|--------------------------|
| RF-linked FPV | Visible camera + often uncooled thermal | EW may jam RF | Targeted; not shown |
| Fiber-optic guided | Visible + thermal (no RF datalink) | **Immune to EW** | Targeted; not shown |
| Loitering munition (EO/IR) | Fused EO/IR seeker | Partial EW effect | Targeted; not shown |
| Commercial quadcopter | Visible + uncooled LWIR | Variable | Targeted; not shown |

Fiber-optic and FPV drones that rely on both visual and thermal observation are the **primary MoE target** for a future paired-cloud test.

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

### Notional Model Timing

```
T+0 s     Modeled release event
T+2 s     Modeled ignition delay
T+2–12 s  Streamer + build-up
T+12–15 s Model density threshold reached
T+15–135 s Model duration window, not cover time
T+135 s+  Terminal phase
```

**Safety rule:** Do not plan movement or CASEVAC from these times. MOE-02 is not closed.

---

## Paired-Cloud Scenario

MS-V alone does not close the MoE. The paired-cloud scenario remains unvalidated:

| Element | Grenade Type | Function |
|---------|-------------|----------|
| Multispectral core | 2–3 × MS-V | Modeled VIS + NIR + MWIR attenuation |
| Visual supplement | 1–2 × AN-M8 or M83 | Modeled visible-opacity supplement |
| Pattern | Not written | No cleared throw pattern |

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

MS-V multispectral clouds degrade friendly thermal optics inside or near the cloud (model puts friendly blackout near 70% on most use cases). There is no cleared employment doctrine. See [SOLDIER_SAFETY.md](../SOLDIER_SAFETY.md).

- No throw is cleared.
- Do not enter the cloud. KPP-12 does not clear any exposure.

---

## Atmospheric Effects

| Factor | Effect on MS-V v2 | Planning Guidance |
|--------|------------------|-------------------|
| Wind ≤ 15 mph | Effective for majority of burn | Throw upwind |
| Wind > 15 mph | Rapid dissipation | Not recommended |
| Temperature −20 to +50°C | Full performance | Standard range |
| Rain | Washout; duration reduced | Not measured |
| Urban canyon | Channeling; extended visible opacity | Useful for FPV defeat in streets |

See [docs/04-conops-use-cases.md](../docs/04-conops-use-cases.md) for scenario application.
