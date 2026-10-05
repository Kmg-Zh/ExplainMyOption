#!/usr/bin/env bash
# Daily unattended run of the Task C3 live-book run log, launched by
# ~/Library/LaunchAgents/com.explainmyoption.daily-runlog.plist at 9:15pm
# local time (Mon-Fri, 15min after the other daily job so they don't fight
# over the same OneDrive-synced working tree at once).
#
# Runs scripts/daily_run.py, which prices+diagnoses docs/runlog/book.json's
# 8 legs through the real graph and writes docs/runlog/YYYY-MM-DD/report.md
# + appends one line to docs/runlog/metrics.jsonl.
#
# docs/runlog/README.md's rule is "one entry per real trading day,
# committed that day -- no backfilling, no simulated days, no generated
# entry for a day the script did not actually run." This wrapper enforces
# the "one entry per day" half of that: if today's report.md already
# exists (a manual run already happened today), it skips instead of
# overwriting it and double-appending metrics.jsonl. It does NOT know
# about market holidays -- the plist only skips weekends. A holiday run
# will still fire; daily_run.py itself doesn't detect that, so a bad
# holiday entry would need removing by hand (same "enforced by hand, not
# by the script" rule the README already states).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/.cache/daily-runlog-logs"
mkdir -p "$LOG_DIR"
TODAY="$(date +%Y-%m-%d)"
LOG_FILE="$LOG_DIR/$TODAY.log"

cd "$ROOT" || exit 1

{
  echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily runlog run start ==="

  if [[ -f "docs/runlog/$TODAY/report.md" ]]; then
    echo "docs/runlog/$TODAY/report.md already exists -- a run already happened today. Skipping."
    echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily runlog run end (skipped) ==="
    exit 0
  fi

  if [[ -d .venv/bin ]]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi

  python scripts/daily_run.py
  status=$?
  echo "=== daily_run.py exit code: $status ==="

  if [[ $status -ne 0 ]]; then
    echo "Non-zero exit -- not committing. Check the log above for the traceback."
    echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily runlog run end (failed) ==="
    exit "$status"
  fi

  TRACKED_PATHS=(docs/runlog/book.json docs/runlog/metrics.jsonl "docs/runlog/$TODAY")
  if [[ -n "$(git status --porcelain -- "${TRACKED_PATHS[@]}")" ]]; then
    echo "New runlog entry — committing and pushing."
    git add -- "${TRACKED_PATHS[@]}"
    git commit -m "runlog: $TODAY daily live-book run"
    CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
    if git push origin "$CURRENT_BRANCH"; then
      echo "Pushed."
    else
      echo "PUSH FAILED — changes are committed locally only, check manually."
    fi
  else
    echo "No tracked file changes from today's run — nothing to commit."
  fi

  echo "=== $(date '+%Y-%m-%d %H:%M:%S') daily runlog run end ==="
} >> "$LOG_FILE" 2>&1
