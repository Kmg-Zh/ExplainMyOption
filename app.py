"""Explain My Option — entrypoint.

Two ways to run:

    # CLI
    python app.py --ticker AAPL --type call
    python app.py --fixture vol_crush

    # Streamlit UI
    streamlit run app.py
"""

from __future__ import annotations

import argparse
import sys

from dotenv import load_dotenv

load_dotenv()

from explain_my_option.agent_graph import run_pipeline
from explain_my_option.pipeline.book_schema import load_book_json
from explain_my_option.pipeline.portfolio_graph import run_book_pipeline
from explain_my_option.report_generator import contract_id, scale_greeks, scale_pnl


def run_cli() -> None:
    parser = argparse.ArgumentParser(description="Explain My Option (MVP)")
    parser.add_argument(
        "--ticker",
        default=None,
        help="e.g. AAPL (required unless --fixture)",
    )
    parser.add_argument(
        "--type",
        default=None,
        choices=["call", "put"],
        help="call or put (default: call, or the fixture's right)",
    )
    parser.add_argument("--strike", type=float, default=None, help="defaults to ATM")
    parser.add_argument("--expiry", default=None, help="YYYY-MM-DD; defaults to nearest")
    parser.add_argument("--quantity", type=float, default=1.0, help="position size (options)")
    parser.add_argument(
        "--multiplier",
        type=float,
        default=1.0,
        help="contract multiplier (1 = per option; 100 = US listed lot)",
    )
    parser.add_argument(
        "--fixture",
        default=None,
        metavar="NAME",
        help="synthetic fixture (no network; skips live news). e.g. vol_crush",
    )
    parser.add_argument(
        "--book",
        default=None,
        metavar="PATH",
        help="JSON book file for multi-leg run (unified graph path).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        metavar="PATH",
        help="write report Markdown to PATH (default: stdout). Eval suites use tests/live_book/output/ and tests/historical/output/<case>/.",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help=(
            "B4: run the quant path only (data fetch, pricing, PnL attribution) — "
            "zero LLM calls, no OPENAI_API_KEY needed. The report's narrative "
            "section is the same deterministic fallback used when no key is "
            "configured (report.synthesis.fallback_synthesis)."
        ),
    )
    args = parser.parse_args()

    if args.no_llm and args.book:
        parser.error("--no-llm does not support --book yet (single-leg/fixture only)")

    deps = None
    if args.book and (args.ticker or args.fixture):
        parser.error("--book cannot be combined with --ticker or --fixture")
    if args.book:
        try:
            book = load_book_json(args.book)
            state = run_book_pipeline(book)
        except RuntimeError as exc:
            parser.error(str(exc))
        report = state.get("report", "") + "\n"
        if args.output:
            from explain_my_option.paths import ReportPathError, resolve_report_output_path

            try:
                out = resolve_report_output_path(args.output)
            except ReportPathError as exc:
                parser.error(str(exc))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(report, encoding="utf-8")
            print(f"Wrote report to {out}", file=sys.stderr)
        else:
            print("\n" + report)
        return

    ticker = args.ticker
    option_type = args.type
    if args.fixture:
        from explain_my_option.data.synthetic import list_fixtures, load_fixture
        from explain_my_option.graph.deps import fixture_deps

        names = list_fixtures()
        if args.fixture not in names:
            parser.error(
                f"unknown fixture {args.fixture!r}; choose one of: {', '.join(names)}"
            )
        snap, _ = load_fixture(args.fixture)
        ticker = ticker or snap.ticker
        option_type = args.type or snap.option_type
        deps = fixture_deps(args.fixture)
    elif not ticker:
        parser.error("--ticker is required unless --fixture is set")
    else:
        option_type = args.type or "call"

    if args.no_llm:
        from explain_my_option.graph.deps import OfficialFdmPnlSource, YFinanceMarketLoader
        from explain_my_option.report.facts import build_position_facts
        from explain_my_option.report.synthesis import fallback_synthesis
        from explain_my_option.report.template import render_position_report

        loader = deps.market if deps is not None else YFinanceMarketLoader()
        loaded = loader.load(
            ticker=ticker, option_type=option_type, strike=args.strike, expiry=args.expiry
        )
        loaded.snapshot.quantity = args.quantity
        loaded.snapshot.multiplier = args.multiplier
        pricing = OfficialFdmPnlSource().attribute(
            loaded.snapshot, loaded.surface, loaded.surface_prev
        )
        facts = build_position_facts(loaded.snapshot, pricing)
        synthesis = fallback_synthesis(facts, llm_unavailable=True, news=loaded.news)
        report = render_position_report(facts, synthesis, news=loaded.news) + "\n"
    else:
        result = run_pipeline(
            ticker=ticker,
            option_type=option_type,
            strike=args.strike,
            expiry=args.expiry,
            quantity=args.quantity,
            multiplier=args.multiplier,
            deps=deps,
        )
        report = result["report"] + "\n"
    if args.output:
        from explain_my_option.paths import ReportPathError, resolve_report_output_path

        try:
            out = resolve_report_output_path(args.output)
        except ReportPathError as exc:
            parser.error(str(exc))
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"Wrote report to {out}", file=sys.stderr)
    else:
        print("\n" + report)


def _render_mermaid(code: str, *, height: int = 420) -> None:
    """Render Mermaid in the browser (CDN). Falls back to a code block if embed fails."""
    import json

    import streamlit as st
    import streamlit.components.v1 as components

    payload = json.dumps(code)
    try:
        components.html(
            f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <style>body {{ margin: 0; font-family: system-ui, sans-serif; }}</style>
</head>
<body>
  <div id="diagram"></div>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{ startOnLoad: false, theme: "neutral", securityLevel: "loose" }});
    const code = {payload};
    const {{ svg }} = await mermaid.render("pipeline", code);
    document.getElementById("diagram").innerHTML = svg;
  </script>
</body>
</html>
            """,
            height=height,
            scrolling=True,
        )
    except Exception:
        st.code(code, language="mermaid")


def run_streamlit() -> None:
    import streamlit as st

    from explain_my_option.graph.topology import pipeline_mermaid

    st.set_page_config(page_title="Explain My Option", page_icon="📈", layout="wide")
    st.title("📈 Explain My Option")
    st.caption("Diagnose *why* an option's price moved — Greeks + PnL attribution + news.")

    with st.expander("How this diagnosis runs", expanded=False):
        st.caption(
            "Live topology from the compiled LangGraph — not a hand-drawn diagram. "
            "It updates when pipeline nodes or edges change."
        )
        _render_mermaid(pipeline_mermaid())

    with st.sidebar:
        st.header("Inputs")
        ticker = st.text_input("Ticker", value="AAPL").strip().upper()
        option_type = st.selectbox("Option type", ["call", "put"])
        strike_raw = st.text_input("Strike (blank = ATM)", value="")
        expiry = st.text_input("Expiry YYYY-MM-DD (blank = nearest)", value="").strip()
        quantity = st.number_input("Quantity (options)", min_value=0.0, value=1.0, step=1.0)
        multiplier = st.number_input(
            "Multiplier",
            min_value=0.0,
            value=1.0,
            step=1.0,
            help="1 = per option. Set 100 for a US listed contract lot.",
        )
        run = st.button("Diagnose", type="primary")

    if run and ticker:
        strike = float(strike_raw) if strike_raw.strip() else None
        with st.spinner("Fetching data, pricing option, reasoning…"):
            try:
                result = run_pipeline(
                    ticker=ticker,
                    option_type=option_type,
                    strike=strike,
                    expiry=expiry or None,
                    quantity=float(quantity),
                    multiplier=float(multiplier),
                )
            except Exception as exc:  # surface errors to the UI rather than crashing
                st.error(f"Failed to run pipeline: {exc}")
                return

        snap = result["snapshot"]
        pricing = result["pricing"]
        scale = snap.position_scale()
        pos_pnl = scale_pnl(pricing.pnl, scale)
        pos_greeks = scale_greeks(pricing.greeks_prev, scale)

        st.subheader(contract_id(snap))
        st.caption(
            f"qty {snap.quantity:g} × multiplier {snap.multiplier:g}  ·  "
            f"engine `{pricing.diagnostics.engine}`  ·  {pricing.diagnostics.data_source}"
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Spot", f"{snap.spot_now:.2f}", f"{pricing.pnl.d_spot:+.2f}")
        m2.metric(
            "IV",
            f"{snap.iv_now * 100:.2f}%",
            f"{pricing.pnl.d_vol * 100:+.2f} pts",
        )
        m3.metric("Delta (pos)", f"{pos_greeks.delta:.4f}")
        m4.metric("Vega (pos)", f"{pos_greeks.vega:.4f}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total PnL", f"{pos_pnl.total_pnl:+.4f}")
        c2.metric("Delta PnL", f"{pos_pnl.delta_pnl:+.4f}")
        c3.metric("Vega PnL", f"{pos_pnl.vega_pnl:+.4f}")
        c4.metric("Theta PnL", f"{pos_pnl.theta_pnl:+.4f}")

        st.markdown(result["report"])


def _is_streamlit_runtime() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


if __name__ == "__main__":
    if _is_streamlit_runtime():
        run_streamlit()
    else:
        run_cli()
else:
    # `streamlit run app.py` imports the module rather than running __main__.
    if _is_streamlit_runtime():
        run_streamlit()
