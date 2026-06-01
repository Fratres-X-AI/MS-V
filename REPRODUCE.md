# Reproducibility — MS-V

## Quick gate

```bash
python -m sim.reproduce
```

Validates golden checksums in [`analysis/reproduce_golden.json`](analysis/reproduce_golden.json) against regenerated baseline jobs.

## Dual profile policy

| Profile | physics_tier | sensor_model | Purpose |
|---------|--------------|--------------|---------|
| **reproduce** (CI gate) | v4 | v4_band_integrated | Stable golden checksums — fast local/CI |
| **default / mega suite** | phase2 | v6_probabilistic_lock | 140M submission campaign on RunPod |

Configured in [`models/cloud_physics/params.yaml`](models/cloud_physics/params.yaml) (`reproduce:` block vs `sim:` defaults).

## RunPod full campaign

```bash
export RUNPOD_CPU_COUNT=32   # when nproc shows host CPUs (e.g. 256)
bash one_pass.sh 31 8192     # 31 workers = 32 vCPU − 1
```

Pull artifacts: `bash pull_from_pod.sh 91.199.227.82 15218`

## Seeds & deps

| Artifact | Role |
|----------|------|
| `sim/config/seeds.yaml` | 38 mega-suite job seeds (authoritative) |
| `requirements-lock.txt` | Pinned Python deps |
| `analysis/results/reproduce_manifest.json` | Last harness run metadata |

## Maturity label (mandatory)

All outputs: **LITERATURE-PARAMETER SENSITIVITY STUDY — NOT VALIDATION**
