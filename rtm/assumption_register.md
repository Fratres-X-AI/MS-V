# Assumption Register

All assumptions must be tagged **VALIDATED**, **LITERATURE**, or **UNVALIDATED** in sim outputs.

| ID | Assumption | Category | Basis | Status |
|----|------------|----------|-------|--------|
| A-001 | MS-V fill achieves VIS + NIR + MWIR attenuation | Performance | ECBC 2014 bispectral program | LITERATURE |
| A-002 | 22–24 oz fill in ~850 g body burns 120+ s at good thickness | Performance | Design target; MS-V burn 2.9–4.5 g/s in params.yaml | UNVALIDATED — sim PASS nominal envelope |
| A-003 | Build-up to effective density in 12–15 s | Performance | v2 KPP; HC baseline ~10–20 s | UNVALIDATED |
| A-004 | 30–40 sq ft screening area per grenade | Performance | Scaled from larger body | UNVALIDATED |
| A-005 | Mass extinction α from open literature applies to MS-V fill | Modeling | COMBIC/FM 3-50/ECBC | LITERATURE |
| A-006 | Beer-Lambert T = exp(−α·CL) adequate for planning | Modeling | FM 3-50 / Annex D | LITERATURE |
| A-007 | Wind 0–15 mph envelope sufficient for infantry ops | Environmental | User requirement | VALIDATED (req) |
| A-008 | FPV + fiber-optic drones fuse VIS + thermal | Threat | Open threat reporting | LITERATURE |
| A-009 | Combined MS-V + AN-M8 required for MoE | Employment | docs/04, doc 07 | VALIDATED (doctrine) |
| A-010 | Respiratory irritation non-lethal at standard standoff | Safety | Design acceptance; no tox data | UNVALIDATED |
| A-011 | M201A1 fuze compatible without modification | Interface | Inventory commonality requirement | UNVALIDATED (engineering) |
| A-012 | Throw range 20–25 m for 850 g grenade under stress | Human factors | Heavier than AN-M8; no test | UNVALIDATED |
