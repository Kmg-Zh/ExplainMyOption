# QuantLib — curated references (in use)

Pricing lives in [`src/pricing/`](../../src/pricing/) behind `price_and_attribute`. Synthetic fixtures are the primary eval path; yfinance is optional live.

## Engines we use

| Use | Type |
|-----|------|
| Official American PnL | `FdBlackScholesVanillaEngine` (local vol or flat) |
| Official fallback / override | same FDM flat, or `BinomialVanillaEngine` CRR via env |
| European analytic (EE premium) | `AnalyticEuropeanEngine` |
| Smile + term structure | `BlackVarianceSurface` + Dupire probe (`LocalVolSurface`) |
| Stochastic vol (diagnostics) | `HestonModel` + `FdHestonVanillaEngine` |
| LSM-BS (analysis API) | `MCAmericanEngine` |
| LSM-Merton (analysis API) | numpy paths + Longstaff–Schwartz; European series in `engines/merton.py` |

Install: `pip install QuantLib` (see `requirements.txt`). Import failure must be loud — no silent SciPy fallback.

## Official

- QuantLib site: https://www.quantlib.org/
- Python docs: https://quantlib-python-docs.readthedocs.io/
- Reference: https://www.quantlib.org/reference/
- Option engines: https://quantlib-python-docs.readthedocs.io/en/latest/pricing_engines/options.html

## Implementation checklist

1. Set `ql.Settings.instance().evaluationDate` **before** building curves.
2. Wrap spot / rate / vol / dividend in Handles.
3. Keep fetchers outside `src/pricing/` (no yfinance inside the engine).
4. Probe Dupire before `localVol=True`; wrap `DividendVanillaOption` NPV.
5. 1-day PnL via in-repo `attribute_pnl`; Heston stays diagnostic.

## Related

- Map: [docs/knowledge/pricing-engine.md](../knowledge/pricing-engine.md)
