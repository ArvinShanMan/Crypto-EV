"""Crypto EV simulator package."""

from .models import TradeParameters, SimulationResult
from .ev import expected_value_per_trade, expected_value_over_series
from .simulation import monte_carlo_simulation
from .metrics import equity_curve, max_drawdown, sharpe_ratio

__all__ = [
    "TradeParameters",
    "SimulationResult",
    "expected_value_per_trade",
    "expected_value_over_series",
    "monte_carlo_simulation",
    "equity_curve",
    "max_drawdown",
    "sharpe_ratio",
]
