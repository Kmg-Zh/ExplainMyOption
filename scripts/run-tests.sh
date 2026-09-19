#!/usr/bin/env bash
# Run the full offline test suite (no network). From repo root:
#   ./scripts/run-tests.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d .venv/bin ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

TESTS=(
  ci/test_pricing_invariants
  ci/test_pricing_facade
  ci/test_data_pipeline
  ci/test_lsm_merton
  ci/test_planner
  ci/test_intel
  ci/test_agent_graph
  ci/test_report_template
  ci/test_meta_earnings_gap
  ci/test_ladder_regression
  ci/test_pipeline_send
  ci/test_pipeline_diagnostic_loop
  ci/test_pipeline_leg_graph
  ci/test_pipeline_topology
  ci/test_pipeline_verifier
  ci/test_governance_scorecard
  ci/test_exdiv_attribution
  ci/test_news_digest
  ci/test_diagnostic_pass
  ci/test_report_reconciliation
  ci/test_repo_layout
  ci/test_observation_preconditions
  ci/test_basis_guard
  ci/test_implied_borrow
  ci/test_historical_chain
  ci/test_historical_real_cases
  ci/test_regime_rule
  ci/test_residual_split
  ci/test_quiet_day_non_escalation
  ci/test_llm_call_budget
  ci/test_prompt_schema_sync
  ci/test_injection_containment
  ci/test_redteam_framework
  ci/test_determinism_quant
  ci/test_no_llm_flag
  ci/test_runlog_book
  ci/test_data_robustness
  historical/test_synthesis_prompt
  historical/test_benchmark_scoring
  historical/test_news_lineage
  historical/test_desk_packet
  live_book/test_portfolio_mixed
  live_book/test_desk_pnl_reconciliation
)

for name in "${TESTS[@]}"; do
  echo "=== ${name} ==="
  python "tests/${name}.py"
done

echo ""
echo "OK — all ${#TESTS[@]} test modules passed"
