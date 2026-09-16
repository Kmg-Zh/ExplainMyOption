# Quiet days (Task A7.1)

`quiet_days_2023.json` is the output of `scripts/find_quiet_days.py --min 3 --year 2023`
(AAPL, MSFT, SPY candidates) -- not hand-picked. Every date in the
candidate window was checked against the same deterministic filter
(|close-to-close return| < 0.3%, no earnings/ex-div within ±3 trading
days, no FOMC/CPI release that week, quote tier tight or normal on both
dates); only the output is a small survivor set.

5 quiet days survived, across 2 distinct underlyings (AAPL, SPY). **MSFT
never produced a survivor** within the script's checked-candidate budget
(60 candidates across all three tickers, round-robin) -- every MSFT
candidate that passed the cheap local checks (return/earnings/ex-div/
macro) failed the DoltHub quote-tier check. Not investigated further:
each DoltHub day-chain query takes 45-55s, and the 60-candidate budget
was already calibrated against that cost. This is recorded here rather
than silently working around it.

Three of the five were converted into full historical cases (real quotes,
near-ATM, ~25-45 DTE) via `scripts/fetch_chains.py`, committed under
`tests/ci/fixtures/historical/`:

| Case | Ticker | As-of / T-1 | Contract |
|---|---|---|---|
| `quiet_aapl_2023-04-24` | AAPL | 2023-04-24 / 2023-04-21 | 165C, exp 2023-05-19 |
| `quiet_spy_2023-03-06` | SPY | 2023-03-06 / 2023-03-03 | 404C, exp 2023-03-31 |
| `quiet_spy_2023-04-24` | SPY | 2023-04-24 / 2023-04-21 | 404C, exp 2023-05-19 |

(A fourth candidate, `AAPL 2023-10-23` at strike 172.5C/exp 2023-11-17, was
dropped: A3's continuity gate correctly caught that contract as
`CONTRACT_MISSING` on the prior date -- a real data-coverage gap, not a
bug -- and was substituted with `quiet_spy_2023-04-24` instead.)

Exercised by `tests/ci/test_quiet_day_non_escalation.py`.
