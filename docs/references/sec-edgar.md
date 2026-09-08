# SEC EDGAR — curated references

App integration: `SecEdgar8KSource` in `src/intel/sec_edgar.py` (`source_id=sec_8k`).

Residual / large unexplained PnL cues may add a bounded 8-K lookup on the **`search`** node — not a dedicated EDGAR graph node.

## Env

```bash
# Free — no API key. SEC requires a descriptive User-Agent (name + contact).
EMO_SEC_USER_AGENT="ExplainMyOption you@example.com"
```

Paste into local `.env` only. Never commit personal email if you prefer a project alias.

If unset, `sec_8k` queries are **skipped** (same pattern as missing `TAVILY_API_KEY`).

## Official docs

- EDGAR API overview: https://www.sec.gov/edgar/sec-api-documentation  
- Fair access / User-Agent: https://www.sec.gov/os/accessing-edgar-data  
- Submissions JSON: `https://data.sec.gov/submissions/CIK{cik10}.json`  
- Ticker → CIK map: `https://www.sec.gov/files/company_tickers.json`

## Fit for this repo

| Today | Notes |
|-------|--------|
| Recent **Form 8-K / 8-K/A** titles + filing links | Newest filings from `filings.recent`; not full-text parse |
| Residual cue only | Planner cap still applies (`max_queries=3`) |

Do **not** scrape HTML in `data_loader` or add edgartools unless explicitly asked — use the official JSON endpoints.

## Related

- Tavily (vega cue): [tavily.md](tavily.md)
