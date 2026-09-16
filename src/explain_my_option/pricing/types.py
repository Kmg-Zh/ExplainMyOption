"""Plain dataclasses for the pricing facade (no vendor imports)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Literal, Optional, Sequence

OptionType = Literal["call", "put"]
ExerciseStyle = Literal["american", "european"]
DataSource = Literal["synthetic", "yfinance", "historical"]
IvPrevSource = Literal["fixture", "chain_t1", "hv20_proxy", "copied"]
RateSource = Literal["fixture", "irx", "default"]
EngineId = Literal[
    "fdm_local_vol",
    "fdm_flat",
    "crr",
    "lsm_bs",
    "lsm_merton",
    "merton_european",
]


@dataclass
class Greeks:
    """First-order Greeks plus the option's model price.

    Delta is per $1 move in the underlying. Vega is per 1 *percentage point*
    (0.01) change in implied volatility. Theta is per calendar day.
    """

    price: float
    delta: float
    gamma: float
    vega: float
    theta: float

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class PnLAttribution:
    """Decomposition of a 1-day option price change into risk factors."""

    total_pnl: float
    delta_pnl: float
    gamma_pnl: float
    vega_pnl: float
    theta_pnl: float
    residual_pnl: float
    d_spot: float
    d_vol: float

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class DiscreteDividend:
    """Cash dividend with an ex-date (ISO ``YYYY-MM-DD``)."""

    ex_date: str
    amount: float


@dataclass
class MarketSnapshot:
    """Everything the pricing facade needs about one option today + yesterday.

    Produced by fetchers (yfinance or synthetic). Never constructed inside
    QuantLib modules from network calls.
    """

    ticker: str
    option_type: str  # "call" or "put"
    strike: float
    expiry: str  # ISO date "YYYY-MM-DD"

    spot_now: float
    spot_prev: float

    iv_now: float  # implied vol as a decimal, e.g. 0.28
    iv_prev: float

    option_price_now: float
    option_price_prev: float

    time_to_expiry_years: float
    risk_free_rate: float = 0.045

    dividend_yield: float = 0.0
    discrete_dividends: list[DiscreteDividend] = field(default_factory=list)
    exercise_style: ExerciseStyle = "american"
    data_source: DataSource = "yfinance"
    as_of: Optional[str] = None  # ISO date for evaluation; default = today
    prev_as_of: Optional[str] = None  # ISO date for T-1 observation (day-count)
    risk_free_rate_prev: Optional[float] = None  # prior rate for rho / sequential reval

    iv_prev_source: IvPrevSource = "fixture"
    hv20_now: Optional[float] = None
    hv20_prev: Optional[float] = None
    bid: Optional[float] = None
    ask: Optional[float] = None
    mid: Optional[float] = None
    volume: Optional[float] = None
    open_interest: Optional[float] = None
    risk_free_rate_source: RateSource = "fixture"

    # Display / blotter scale. Engine PnL stays per 1 option.
    quantity: float = 1.0
    multiplier: float = 1.0

    def position_scale(self) -> float:
        """Contracts × contract multiplier. Default 1 = per option."""
        return float(self.quantity) * float(self.multiplier)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class VolSurfaceData:
    """Implied-vol grid for smile + term structure (synthetic or live).

    ``matrix[i][j]`` is IV (decimal) for ``expiries[i]`` × ``strikes[j]``.
    Non-finite / non-positive entries should be filtered by the fetcher;
    the surface builder drops remaining bad cells and may flag limitations.
    """

    as_of: str  # ISO evaluation date
    expiries: list[str]  # ISO dates, ascending
    strikes: list[float]  # ascending
    matrix: list[list[float]]  # shape (len(expiries), len(strikes))
    data_source: DataSource = "yfinance"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class PricingSpec:
    """Single-date pricing request consumed by ``PricingEngine`` implementations."""

    spot: float
    strike: float
    rate: float
    dividend_yield: float
    vol: float
    expiry: str
    eval_date: date | str
    option_type: OptionType = "call"
    exercise_style: ExerciseStyle = "american"
    discrete_dividends: Sequence[DiscreteDividend] = ()
    surface: Optional[VolSurfaceData] = None


@dataclass
class PricingDiagnostics:
    """Attribution diagnostics for the LLM narrative."""

    data_source: DataSource
    exercise_style: ExerciseStyle
    engine: EngineId = "fdm_flat"
    ql_version: Optional[str] = None
    iv_prev_source: Optional[IvPrevSource] = None
    local_vol_used: bool = False
    # True when official PnL used flat vols inverted to market mid at T and T-1.
    mark_calibrated: bool = False
    effective_iv_now: Optional[float] = None
    effective_iv_prev: Optional[float] = None
    european_price: Optional[float] = None
    american_price: Optional[float] = None
    early_exercise_premium: Optional[float] = None
    # P_eu_div - P_eu_nodiv (signed, same FDM grid both sides). Together
    # with early_exercise_premium this reconstructs the legacy
    # American-minus-no-div-European figure to 1e-9 (see facade.py).
    dividend_pv_effect: Optional[float] = None
    # True when early_exercise_premium < -1e-6*S -- a numerical anomaly
    # (engine/grid inconsistency), not a genuine negative exercise value.
    # Never clamped; commentary must not narrate this as a real signal.
    ee_premium_anomaly: bool = False
    limitations: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SurfaceDiagnostics:
    """Surface + Heston diagnostics (not official PnL)."""

    term_slope: Optional[float] = None
    skew_proxy: Optional[float] = None
    heston_params: Optional[dict] = None
    heston_rmse: Optional[float] = None
    american_surface_price: Optional[float] = None
    american_heston_price: Optional[float] = None
    limitations: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class PricingResult:
    """Full AI-surveillable output of ``price_and_attribute``."""

    greeks_prev: Greeks
    greeks_now: Greeks
    pnl: PnLAttribution
    diagnostics: PricingDiagnostics
    surface_diagnostics: Optional[SurfaceDiagnostics] = None

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SecondOrderTaylorResult:
    """Vanna/Volga second-order Taylor contribution (Layer 3)."""

    vanna: float
    volga: float
    vanna_pnl: float
    volga_pnl: float
    combined_pnl: float
    residual_after: float
    limitations: list[str] = field(default_factory=list)
    # A5.2: named per the spec, alongside (not replacing) the fields above.
    # second_order_explained is combined_pnl under the spec's own name;
    # residual_first_order is the *first-order Taylor* residual (pnl.residual_pnl)
    # this correction is applied against, distinct from residual_after's
    # existing (total_pnl - combined_pnl) definition.
    residual_first_order: float = 0.0
    second_order_explained: float = 0.0
    residual_reduction_pct: float = 0.0

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SequentialRevalStep:
    factor: str
    pnl_usd: float
    price_before: float
    price_after: float


@dataclass
class SequentialRevalResult:
    """Sequential full revaluation buckets (Layer 4), order t → S → σ → r."""

    steps: list[SequentialRevalStep]
    model_total_pnl: float
    step_sum: float
    residual_vs_model: float
    order: list[str] = field(default_factory=lambda: ["time", "spot", "vol", "rate"])
    limitations: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "steps": [asdict(s) for s in self.steps],
            "model_total_pnl": self.model_total_pnl,
            "step_sum": self.step_sum,
            "residual_vs_model": self.residual_vs_model,
            "order": list(self.order),
            "limitations": list(self.limitations),
        }


@dataclass
class CrossCheckResult:
    """Official FDM vs LSM / Merton analysis-API comparison."""

    official_price: float
    engine_used_for_official: EngineId
    lsm_bs: Optional[float] = None
    lsm_merton: Optional[float] = None
    european_merton: Optional[float] = None
    rel_diff: Optional[float] = None
    limitations: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)
