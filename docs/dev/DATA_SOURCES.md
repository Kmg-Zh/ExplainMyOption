# Data sources — real historical option chains (Work Order v3, Task A3)

Status: **A3.0-bis gate FAILED for GME. Work stopped before A3.3 per the
amendment's instruction ("If the bases differ, STOP and report — do not
attempt a correction factor").** A3.2-bis, A3.3 and A3.4-bis are not started.

## Source inventory

### Selected: DoltHub `post-no-preference/options`

- Access: HTTP SQL API, no auth, no `dolt` CLI, no bulk download.
  `https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master?q=<urlencoded-sql>`
- Branch is `master`. (`main` returns `branch not found`.)
- Tables: `option_chain`, `volatility_history`.
- `option_chain` columns: `date, act_symbol, expiration, strike, call_put`
  (PK), then `bid, ask, vol, delta, gamma, theta, vega, rho`.
- License: **CC BY-SA 4.0** (from `dolt_docs`.`LICENSE.md`). Redistribution
  permitted with attribution; adapted data inherits ShareAlike.
- Actively maintained — latest commit `2026-09-15`.
- Contains **no underlying price**, no volume, no open interest. The
  underlying must come from a separate source; that is what A3.0-bis is about.

### Rejected

| Source | Why rejected |
|---|---|
| `dolthub/options` | Same two tables; `post-no-preference` is the maintained copy. |
| HistoricalData.net | Paid (archives from ~$99). Retained as the fallback for pre-2019 US names. |
| ORATS | Paid (~$599 one-time for 2007+ backfill). Fallback for pre-2019 US names. |
| OptionMetrics / WRDS | Institutional/academic licence only. |
| Eurex 2008 (VOW.DE) | No retail source located at any price. |

## A3.0-bis — split-basis verification

### Method

The dataset carries no underlying price, so the question "are the dataset's
underlying prices and option strikes on the same split basis" is really: **is
the underlying source we would pair with it on the same basis as its strikes?**

Two independent checks were used, neither relying on the other:

1. **Put–call parity implied from the dataset's own quotes.** For each strike
   with both a call and a put, `S_implied = C_mid − P_mid + K·e^{−rT}`. This
   asks the dataset what underlying level its own quotes are consistent with,
   with no external price source involved. (With `q = 0` assumed, so the
   result is a lower bound when borrow is expensive — see the GME note.)
2. **An external quote for the as-traded close**, to pin the true level.

### Result — AAPL: bases AGREE

exp `2023-11-24`, `r = 0.054`, ATM band K ∈ [165, 200], 11 strike pairs each day.

| Date | Parity-implied `S − PV(D)` (median) | Spread across strikes | yfinance `auto_adjust=False` Close | yfinance `auto_adjust=True` Close |
|---|---|---|---|---|
| 2023-11-08 | 182.456 | 182.291 – 182.947 | **182.89** | 180.45 |
| 2023-11-09 | 182.100 | 181.767 – 182.494 | **182.41** | 179.98 |

AAPL goes ex-dividend `2023-11-10` for `$0.24`, inside the option's life, so
parity implies `S − PV(D)`. Adding back `0.24`: 182.70 vs 182.89 (−0.10%) and
182.34 vs 182.41 (−0.04%). Agreement is within the bid/ask-midpoint noise.

**AAPL strikes and yfinance unadjusted closes are on the same basis.** AAPL's
last split was 2020-08-31, before this window.

Note that `auto_adjust=True` (the yfinance default) is wrong here by ~1.3% —
dividend back-adjustment. Any loader must pass `auto_adjust=False`.

### Result — GME: bases DIFFER

exp `2021-02-19`, `r = 0.0008`.

| Date | Parity-implied `S` (median) | Spread | yfinance Close (`auto_adjust` **True and False — identical**) | As-traded close |
|---|---|---|---|---|
| 2021-01-22 | 61.597 | 60.921 – 61.747 | 16.25 | 65.01 |
| 2021-01-25 | 73.795 | 73.047 – 74.570 | 19.20 | **76.79** (independently confirmed) |

- The dataset's strike range on those dates (46–60, then 54–100) brackets
  ~61–74, not ~16–19.
- Ratio of parity-implied to yfinance: 61.60/16.25 = **3.79**,
  73.80/19.20 = **3.84**.
- `yf.Ticker("GME").splits` reports a **4.0 split on 2022-07-22**.
- `auto_adjust=False` does **not** undo a split in yfinance — it returned
  values identical to `auto_adjust=True` for GME. It only affects dividend
  adjustment (visible in the AAPL table above).

**The dataset's strikes are on the as-traded (pre-split) basis; yfinance's
underlying is on the post-split basis. The two differ by the 4-for-1 split.**

The implied values sit ~5% *below* the as-traded closes (61.60 vs 65.01;
73.80 vs 76.79) rather than exactly on them. That gap is not a basis error —
it is the omitted borrow cost, the `q = 0` assumption in check 1 above. It is
precisely the effect A3.2-bis exists to imply. It does not affect the
basis conclusion, which turns on a factor of ~4, not ~5%.

### Verdict

- `aapl_exdiv_2023_real` — **not blocked** by A3.0-bis.
- `gme_squeeze_2021_real` — **blocked**. Stopped and reported; no correction
  factor applied.

The mismatch is a property of the *underlying price source*, not of the option
dataset — the dataset is internally consistent and on the as-traded basis for
both names. Resolving it means choosing an underlying source that serves
as-traded prices for 2021, which is a data-source decision, not a code change.

### Reproducing these numbers

```
# parity-implied spot, per strike, from the dataset's own quotes
curl -s --data-urlencode \
  "q=select strike, call_put, bid, ask from option_chain \
      where act_symbol='GME' and date='2021-01-22' and expiration='2021-02-19'" \
  -G https://www.dolthub.com/api/v1alpha1/post-no-preference/options/master

# yfinance underlying, both adjustment modes
python -c "import yfinance as yf; \
  print(yf.Ticker('GME').history(start='2021-01-20',end='2021-01-27',auto_adjust=False)['Close']); \
  print(yf.Ticker('GME').splits)"
```

## Coverage limits already established (not yet the full A3.4-bis writeup)

- Data begins ~2019. Verified **0 rows** for Q1 of 2008, 2012, 2016 and 2018.
- US listings only.
- Roughly 3 expirations per date, on a strike window that tracks spot.
- Whole days can be absent dataset-wide: **2022-02-03 returns 0 rows** for
  AAPL, SPY and TSLA alike.
- `vol` is unreliable deep ITM (AAPL 130-strike call on 2023-11-09 carries
  `vol = 0.8036`); ATM values are sane.
