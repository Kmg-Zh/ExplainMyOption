#!/usr/bin/env bash
# Offline test suite: no network, no API keys. From the repo root:
#   ./scripts/run-tests.sh            # everything
#   ./scripts/run-tests.sh -k report  # any pytest arguments
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [[ -d .venv/bin ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
exec python -m pytest "$@"
