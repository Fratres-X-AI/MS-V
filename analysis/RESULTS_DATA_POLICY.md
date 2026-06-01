# Results Data Policy

Large Monte Carlo campaigns produce many JSON files. This policy keeps the repo useful without unbounded bloat.

## What belongs in git (default)

| Artifact | Path | Reason |
|----------|------|--------|
| Summary reports | `analysis/RESULTS_SUMMARY.md`, `MEGA_SUITE_REPORT.md`, `tail_risk_analysis.md` | Human-readable evidence |
| Manifest + CSV | `analysis/results/*/manifest.json`, `summary.csv` | Compact index of all jobs |
| Local profile results | `single_grenade.json`, `three_grenade_group.json`, `suite_summary.json`, `wind_sensitivity.json` | CI baseline (~100k) |
| Charts | `suite_charts.png` | Quick visual |

## What should NOT be committed (going forward)

| Artifact | Path pattern | Action |
|----------|--------------|--------|
| Mega suite raw JSON | `analysis/results/mega_suite/*_n10000000.json`, `*_n2000000.json` | **Gitignore** — regenerate on RunPod |
| RunPod scale dumps | `analysis/results/runpod*/**/*.json` (except manifest) | **Gitignore** |
| Quick-test artifacts | `*_n50000.json`, `*_n25000.json` | Delete locally; never commit |
| Stale baselines | `monte_carlo_baseline.json` (old schema) | Remove or archive |

## Regeneration

```bash
# On RunPod
python sim/run_mega_suite.py --workers 31
python analysis/rebuild_mega_manifest.py
python analysis/summarize_mega_suite.py
python analysis/analyze_tail_risk.py
```

## Archive option

For milestone retention, attach `manifest.json` + `summary.csv` + report markdown to **GitHub Releases** instead of tracking 40+ JSON blobs on `main`.

## Current repo state (2026-06-01)

Mega suite and RunPod JSON were committed once for milestone `a884452`. Future campaigns follow gitignore below; summaries remain on `main`.
