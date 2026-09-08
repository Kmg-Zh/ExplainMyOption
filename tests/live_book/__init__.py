"""Test-only portfolio books and e2e runners — not part of the product ``src/`` package."""

from live_book.portfolio_book import LIVE_LEGS, OFFLINE_AS_OF, OFFLINE_LEGS

__all__ = [
    "LIVE_LEGS",
    "OFFLINE_AS_OF",
    "OFFLINE_LEGS",
    "run_live_portfolio_e2e",
    "run_offline_portfolio_e2e",
]


def __getattr__(name: str):
    if name in {"run_live_portfolio_e2e", "run_offline_portfolio_e2e"}:
        from live_book import portfolio_e2e

        return getattr(portfolio_e2e, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
