#!/usr/bin/env bash
# Pull one-pass artifacts from RunPod to local repo
# Usage: bash pull_from_pod.sh [host] [port]
set -euo pipefail
HOST="${1:-91.199.227.82}"
PORT="${2:-40566}"
KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519}"
REMOTE="/workspace/MS-V"
LOCAL="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$LOCAL/analysis/results/mega_suite" "$LOCAL/analysis/results/sobol" "$LOCAL/analysis/figures" "$LOCAL/rtm"

FILES=(
  "analysis/results/mega_suite/manifest.json"
  "analysis/results/mega_suite/summary.csv"
  "analysis/results/sobol/sobol_results.json"
  "analysis/results/sobol/sobol_rankings.json"
  "analysis/results/one_pass_complete.json"
  "analysis/MEGA_SUITE_REPORT.md"
  "analysis/SOBOL_SENSITIVITY_REPORT.md"
  "analysis/tail_risk_analysis.md"
  "analysis/one_pass.log"
  "rtm/verification_matrix.md"
  "rtm/verification_matrix.csv"
  "rtm/assumption_register.md"
  "analysis/figures/duration_sensitivity.png"
  "analysis/figures/mega_suite_duration_p10.png"
  "analysis/figures/FIGURE_PROVENANCE.md"
)

for f in "${FILES[@]}"; do
  dir=$(dirname "$f")
  mkdir -p "$LOCAL/$dir"
  scp -P "$PORT" -i "$KEY" -o StrictHostKeyChecking=accept-new "root@${HOST}:${REMOTE}/${f}" "$LOCAL/$f" 2>/dev/null || echo "WARN: missing $f"
done

echo "=== Pull complete. Verify: analysis/results/one_pass_complete.json ==="
