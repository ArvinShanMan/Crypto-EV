from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean, pstdev
from typing import Sequence


@dataclass(slots=True)
class TradeParameters:
    """Configuration for a single trade model and repeated simulations."""

    win_rate: float
    profit_per_win: float
    loss_per_trade: float
    trades_per_run: int = 100
    iterations: int = 10_000
    initial_capital: float = 0.0

    def __post_init__(self) -> None:
        if not 0 <= self.win_rate <= 1:
            raise ValueError("win_rate must be between 0 and 1")
        if self.profit_per_win < 0:
            raise ValueError("profit_per_win must be non-negative")
        if self.loss_per_trade < 0:
            raise ValueError("loss_per_trade must be non-negative")
        if self.trades_per_run <= 0:
            raise ValueError("trades_per_run must be positive")
        if self.iterations <= 0:
            raise ValueError("iterations must be positive")


@dataclass(slots=True)
class SimulationResult:
    """Aggregated outcome of Monte Carlo simulation runs."""

    params: TradeParameters
    run_returns: Sequence[float]
    ending_balances: Sequence[float]
    risk_of_loss: float
    average_return: float = field(init=False)
    return_std_dev: float = field(init=False)
    best_run: float = field(init=False)
    worst_run: float = field(init=False)

    def __post_init__(self) -> None:
        if not self.run_returns:
            raise ValueError("run_returns cannot be empty")
        self.average_return = mean(self.run_returns)
        self.return_std_dev = pstdev(self.run_returns)
        self.best_run = max(self.run_returns)
        self.worst_run = min(self.run_returns)
