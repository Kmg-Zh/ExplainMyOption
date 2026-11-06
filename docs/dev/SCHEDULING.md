# Scheduled jobs (macOS launchd)

Two unattended jobs run Monday-Friday on the machine that hosts this checkout.
Both are launched from `~/Library/LaunchAgents/` plists (examples in
`scripts/launchd/`) and run whatever branch is checked out in the working
tree; each pushes `origin <current branch>`.

| Job | Time (local) | Script | What it does |
|-----|--------------|--------|--------------|
| `com.explainmyoption.daily-refresh` | 21:00 | `scripts/daily-live-refresh.sh` | Runs the pinned 10-leg live e2e reconciliation (`evals/live_book/`) and refreshes the local t-1 cache. Auto-commits only `evals/live_book/pinned_books/`. |
| `com.explainmyoption.daily-runlog` | 21:15 | `scripts/daily-runlog-run.sh` | Runs `scripts/daily_run.py` on `docs/runlog/book.json` (8 real legs) through the real graph, writes `docs/runlog/YYYY-MM-DD/` and appends one row to `docs/runlog/metrics.jsonl`. Settles expired legs and rolls them in `book.json` by its `roll_rule`; the commit carries the new contracts. |

## Install

```bash
cp scripts/launchd/com.explainmyoption.daily-runlog.plist.example \
   ~/Library/LaunchAgents/com.explainmyoption.daily-runlog.plist
# edit the absolute path inside, then:
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.explainmyoption.daily-runlog.plist
launchctl print gui/$UID/com.explainmyoption.daily-runlog | head
```

Repeat for `daily-refresh`. Logs: `~/Library/Logs/explainmyoption/daily-runlog/YYYY-MM-DD.log`
and `~/Library/Logs/explainmyoption/daily-refresh/YYYY-MM-DD.log`, outside the
checkout. In an OneDrive folder, appends to a log there failed with "Resource
deadlock avoided" and killed both jobs with exit 120. Output from before the
wrapper redirects goes to the plist's `/tmp/com.explainmyoption.*.log` files,
which a reboot clears.

## Failure behaviour

- Both wrappers exit non-zero when the underlying run fails, so `launchctl
  print` shows a real last exit code.
- The refresh job logs `PINNED BOOK EXPIRED` when its pinned expiries have
  passed. Re-pinning is a deliberate manual step (below), never automatic.
  The run-log book is different: `daily_run.py` rolls it by rule
  (`docs/runlog/README.md#expiry-and-rolls`). A failed roll is listed under
  Errors and retried by the next run.
- The run-log wrapper skips if today's `report.md` already exists (one entry
  per day). It does not know market holidays; a holiday entry must be removed
  by hand.
- Both wrappers check and stage their paths with `core.fileMode=false`, so a
  mode-only change (OneDrive flips 644 to 755) is not committed.

## Re-pinning the refresh book

1. Discover contracts with a minimum DTE, e.g.
   `python evals/live_book/portfolio_e2e.py --resolve-moneyness` (the
   `min_days` argument of `resolve_live_contract` selects far-dated monthlies).
2. Write `evals/live_book/pinned_books/book_<date>.json` and point
   `DEFAULT_PINNED_BOOK` in `evals/live_book/portfolio_book.py` at it.
3. The first day on new contracts has no cached t-1, so IV change falls back to
   the HV20 proxy; read that day's output with that in mind.

## Run-log rule

One entry per real trading day, committed that day. No backfilling, no
simulated days (see `docs/runlog/README.md`). Do not run `daily_run.py`
without `--dry-run` on a non-trading day.
