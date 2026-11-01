"""Run the governed agent on your own PnL explain: no QuantLib, no yfinance.

The agent needs two adapters (the contract is in docs/INTEGRATION.md):
  * a market loader, returning today's and yesterday's observation of the option;
  * a PnL source, returning your risk system's 1-day attribution for it.
The fixed workflow does the rest: diagnostic pass, search plan, the four LLM
roles, the code checks and the report. From the repo root:

    python examples/bring_your_own_pnl.py

With OPENAI_API_KEY set the LLM roles run (four calls); without it the report
carries the code-only narrative.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from explain_my_option import ExplainMyOption, PipelineConfig  # noqa: E402
from explain_my_option.graph.deps import GraphDeps  # noqa: E402
from explain_my_option.intel.sources import IntelRegistry  # noqa: E402
from explain_my_option.pricing.types import (  # noqa: E402
    Greeks,
    LoadedData,
    MarketSnapshot,
    PnLAttribution,
    PricingDiagnostics,
    PricingResult,
)


class DeskMarketLoader:
    """Marks for one option on T-1 and T. Replace the literals with a read from your marks store."""

    def load(self, *, ticker, option_type, strike, expiry) -> LoadedData:
        return LoadedData(
            snapshot=MarketSnapshot(
                ticker=ticker,
                option_type=option_type,
                strike=strike,
                expiry=expiry,
                as_of="2026-10-14",
                prev_as_of="2026-10-13",
                spot_prev=100.00,
                spot_now=103.00,
                iv_prev=0.30,
                iv_now=0.28,
                option_price_prev=4.10,  # option marks (mid), per option
                option_price_now=5.65,
                bid=5.60,
                ask=5.70,
                volume=1200,
                open_interest=5400,
                quote_tier_prev="reliable",  # T-1 mark quality, from your marks store
                time_to_expiry_years=37 / 365,
                risk_free_rate=0.045,
                iv_prev_source="chain_t1",
                data_source="desk",
            )
        )


class DeskPnlSource:
    """Your risk system's PnL explain, per option. Replace the literals with a call into it."""

    methodology = (
        "**Official model ΔP:** the desk risk system's American pricer on the desk vol surface; "
        "the blotter shows its prices, T-1 Greeks and PnL explain."
    )

    def attribute(self, snapshot, surface_data=None, surface_prev=None) -> PricingResult:
        t1 = Greeks(price=4.0894, delta=0.5386, gamma=0.0410, vega=0.1281, theta=-0.0567)
        t = Greeks(price=5.5885, delta=0.6654, gamma=0.0397, vega=0.1194, theta=-0.0529)
        delta, gamma, vega, theta = 1.6157, 0.1846, -0.2562, -0.0567  # explain buckets
        total = t.price - t1.price
        return PricingResult(
            greeks_prev=t1,
            greeks_now=t,
            pnl=PnLAttribution(
                total_pnl=total,
                delta_pnl=delta,
                gamma_pnl=gamma,
                vega_pnl=vega,
                theta_pnl=theta,
                residual_pnl=total - (delta + gamma + vega + theta),
                d_spot=snapshot.spot_now - snapshot.spot_prev,
                d_vol=snapshot.iv_now - snapshot.iv_prev,
            ),
            diagnostics=PricingDiagnostics(
                data_source="desk", exercise_style=snapshot.exercise_style, engine="desk_risk"
            ),
        )


def main() -> str:
    # No news feed is registered, so every planned query is skipped; see
    # docs/INTEGRATION.md to add your own.
    deps = GraphDeps(market=DeskMarketLoader(), pnl=DeskPnlSource(), intel=IntelRegistry({}))
    agent = ExplainMyOption(config=PipelineConfig(require_openai=False), deps=deps)
    result = agent.diagnose_leg(
        "ACME", option_type="call", strike=100.0, expiry="2026-11-20", quantity=10, multiplier=100
    )
    return result.report


if __name__ == "__main__":
    print(main())
