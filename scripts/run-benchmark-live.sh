#!/usr/bin/env bash
# Live LLM benchmark runs (OPENAI_API_KEY required). From repo root:
#   ./scripts/run-benchmark-live.sh
#   ./scripts/run-benchmark-live.sh --case vow_float_squeeze_2008
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv/bin ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is required for live benchmark runs." >&2
  exit 1
fi

export EMO_BENCHMARK_LIVE=1

echo "=== historical (5 cases) ==="
python tests/historical/run.py "$@"

echo ""
echo "=== historical compare (governed vs baseline) ==="
python tests/historical/compare.py "$@"

echo ""
echo "OK — live benchmark artifacts under tests/historical/output/<case>/"
