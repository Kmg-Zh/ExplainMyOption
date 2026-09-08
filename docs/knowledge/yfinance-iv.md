# yfinance IV and option chain

## Takeaway

yfinance exposes a **live** option chain and a current `impliedVolatility` on each row. It does not give a reliable historical vol surface. Live `iv_prev` is **not** copied from today when we can do better: SQLite t-1 snapshot, else 20-day realized-vol (HV20) proxy.

## Details

- `Ticker.option_chain(expiry)` → `calls` / `puts` DataFrames. Yahoo does **not** ship Greeks; we compute them in `src/pricing/`.
- Live chain only — `fetch_vol_surface()` builds today's multi-expiry grid; no historical surface from Yahoo.
- Quotes: bid/ask mid when both positive; else last. Volume / OI stored on the snapshot.
- News: `Ticker.news` is ticker-level; query text is not applied. Fetch is fail-soft.
- Rate: `^IRX` last / 100; failure → 4.5%.
- **dividendYield:** Yahoo sometimes stores 0.35 meaning **0.35%**, not 35%. `normalize_dividend_yield` divides by 100 when `q > 1` or (after that) `q > 0.15`. Live AAPL/MSFT 2026-08-18 were the latter. **Unless** a name has a true continuous yield above 15% (not our demo set).
- Discrete cash dividends still come from `tk.dividends` / info (at most next two amounts).
- If `impliedVolatility` is missing or non-positive, `data_loader.py` uses `0.30`.
- **Δσ:** `chain_t1` from `.cache/explain-my-option/market.sqlite` if a prior as_of exists; else `σ_prev = σ_now − (HV20_t − HV20_{t-1})` (`hv20_proxy`). If HV20 cannot be computed, `iv_prev = iv_now` and source is `copied`.
- Yesterday's local-vol grid is the t-1 cache or a **parallel shift** of today's IVs by `(iv_prev − iv_now)`, floored at 1e-4.
- Strike default: closest to spot (ATM).
- Empty/short spot history currently **raises**.

Do not add edgartools, scraping, or paid vendors unless asked.

## Source

- `src/data_loader.py`, `src/data/realized.py`, `src/data/cache.py` (Aug 2026)
- Links: [../references/yfinance.md](../references/yfinance.md)
