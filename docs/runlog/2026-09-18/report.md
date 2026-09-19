# Live book run — 2026-09-18

Run `2026-09-18-1789780502`. 0/8 legs completed, 8 failed. `legs_narrated=0` `legs_silent=0` `llm_calls=0`.

**No leg in this run has a cached t-1 snapshot yet** (`iv_prev_source` is `hv20_proxy` or `copied` for every leg below) -- this is the book's opening day, or the first run since a leg changed. Every `ΔP`/residual/terminal-state figure below is comparing today's quote against a statistically-derived proxy for yesterday, not a real prior trading day, and should be read as noisy. This run still caches each leg's snapshot (`data.cache.upsert_snapshot`), so tomorrow's run compares against today for real.


_Empty portfolio — no positions to diagnose._

## Errors

- **aapl_vertical_long** (AAPL): RuntimeError: negative or null underlying given
- **aapl_vertical_short** (AAPL): RuntimeError: negative or null underlying given
- **jpm_straddle_call** (JPM): RuntimeError: negative or null underlying given
- **jpm_straddle_put** (JPM): RuntimeError: negative or null underlying given
- **spy_reversal_put** (SPY): RuntimeError: negative or null underlying given
- **spy_reversal_call** (SPY): RuntimeError: negative or null underlying given
- **vz_div_call** (VZ): RuntimeError: negative or null underlying given
- **plug_deep_otm** (PLUG): RuntimeError: negative or null underlying given
