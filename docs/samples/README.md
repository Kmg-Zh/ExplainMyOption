# Sample reports

Frozen captures of the product Markdown report. These are **not** eval archives.

Suite `output/` folders stay gitignored (`tests/live_book/output/`, `tests/historical/output/`). Regenerate a sample only when the report template changes in a way hiring readers would notice.

| File | What it shows |
|------|----------------|
| [live.md](live.md) | Live public ticker, quantity 1 (redacted: not a client book) |
| [historical.md](historical.md) | META 2022-02-03 earnings gap + IV crush, frozen as-of headlines |
| [unexplained_break.md](unexplained_break.md) | VW 2008 squeeze — large Taylor residual, then `terminal_unexplained_break` |

All dollar amounts come from QuantLib. The LLM only writes the verdict / watchlist against that blotter.
