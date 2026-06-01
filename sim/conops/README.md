# CONOPS Kill-Chain Simulation (Phase 3 skeleton)

Timeline model for doc 04 use cases — not yet coupled to full physics engine.

## Sequence

```
T-0   Detection cue (acoustic/RF/visual)
T+0   Employment decision (2-3 MS-V + 1-2 visual smoke)
T+2   Ignition (fuze delay)
T+12-15  Screen effective (from Phase 1 build-up distribution)
T+15-135 Movement / CASEVAC / exfil window
T+135+  Rescreen or complete
```

## Placeholder

Full CONOPS Monte Carlo will sample build-up and duration from Phase 1 distributions per use case.

Implementation: `sim/conops/kill_chain.py` (Phase 3)
