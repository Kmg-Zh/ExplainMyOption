#!/usr/bin/env bash
# Test-only live portfolio e2e — pinned contracts (comparable day-over-day).
# Archives under tests/live_book/output/; SQLite t-1 under .cache/.
#
# Usage (from repo root):
#   ./scripts/run-portfolio-e2e.sh
#   ./scripts/run-portfolio-e2e.sh --live --compare-to-baseline
#   ./scripts/run-portfolio-e2e.sh --offline
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv/bin ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

if [[ $# -eq 0 ]]; then
  exec python tests/live_book/portfolio_e2e.py --live --compare-to-baseline
fi
exec python tests/live_book/portfolio_e2e.py "$@"
