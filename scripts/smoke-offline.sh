#!/usr/bin/env bash
# Offline end-to-end smoke: fixture report to stdout (not suite output/).
#   ./scripts/smoke-offline.sh [fixture_name]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv/bin ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

FIXTURE="${1:-vol_crush}"
python app.py --fixture "$FIXTURE"
