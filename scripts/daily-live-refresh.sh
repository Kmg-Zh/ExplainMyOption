#!/usr/bin/env bash
# Daily unattended run of the live e2e reconciliation test, launched by
# ~/Library/LaunchAgents/com.explainmyoption.daily-refresh.plist at 9pm local time.
#
# Runs evals/live_book/portfolio_e2e.py against today's live market close and
# refreshes the local .cache/ + evals/live_book/output/ (both gitignored — this
# is the "get new data" the test needs day to day).
#
# Re-pinning a new contract (when the current pin expires) is a judgment call
# made manually via --resolve-moneyness, NOT done here. If today's pinned
# contract can't price (e.g. it expired), this run fails and logs it below —
# check the log and re-pin by hand, same as every earlier pinned book was.
#
# Only auto-commits/pushes if the run itself changed the specific tracked
# files a manual re-pin touches, so a normal day is a no-op on git.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Outside the checkout: when it sits in OneDrive, appends to a log there can
# fail with "Resource deadlock avoided" (EDEADLK) and kill the run mid-way.
LOG_DIR="$HOME/Library/Logs/explainmyoption/daily-refresh"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

cd "$ROOT" || exit 1

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily live refresh start ==="

  if [[ -d .venv/bin ]]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi

  ./scripts/run-portfolio-e2e.sh --live --compare-to-baseline
  status=$?
  echo "=== run-portfolio-e2e.sh exit code: $status ==="
  if [[ $status -ne 0 ]] && grep -q -e "cannot be found. Available expirations" -e "pinned book needs a re-pin" "$LOG_FILE"; then
    echo "PINNED BOOK EXPIRED -- re-pin by hand (see docs/dev/SCHEDULING.md)."
  fi

  # OneDrive flips file modes (644 -> 755); a mode-only change is not a re-pin.
  TRACKED_PATHS=(evals/live_book/pinned_books)
  if [[ -n "$(git -c core.fileMode=false status --porcelain -- "${TRACKED_PATHS[@]}")" ]]; then
    echo "Tracked pinned-book/report files changed — committing and pushing."
    git -c core.fileMode=false add -- "${TRACKED_PATHS[@]}"
    git commit -m "Auto-refresh: $(date +%Y-%m-%d) daily live e2e run"
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    if git push origin "$CURRENT_BRANCH"; then
      echo "Pushed."
    else
      echo "PUSH FAILED — changes are committed locally only, check manually."
    fi
  else
    echo "No tracked file changes from today's run — nothing to commit."
  fi

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily live refresh end ==="
} >> "$LOG_FILE" 2>&1
exit "${status:-1}"
