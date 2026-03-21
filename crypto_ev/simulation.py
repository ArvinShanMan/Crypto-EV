from __future__ import annotations

from .market import MarketModel
from .metrics import equity_curve, max_drawdown
from .models import SimulationResult, TradeParameters



def monte_carlo_simulation(params: TradeParameters, seed: int | None = None) -> SimulationResult:
    """Run repeated simulations of a trading strategy under uncertainty."""
    market = MarketModel(seed=seed)
    run_returns = []
    ending_balances = []
    losing_runs = 0

    for _ in range(params.iterations):
        trade_results = [
            market.sample_trade_pnl(
                win_rate=params.win_rate,
                profit_per_win=params.profit_per_win,
                loss_per_trade=params.loss_per_trade,
            )
            for _ in range(params.trades_per_run)
        ]
        total_return = sum(trade_results)
        ending_balance = params.initial_capital + total_return
        run_returns.append(total_return)
        ending_balances.append(ending_balance)
        if ending_balance < params.initial_capital:
            losing_runs += 1
        _ = max_drawdown(equity_curve(params.initial_capital, trade_results))

    return SimulationResult(
        params=params,
        run_returns=run_returns,
        ending_balances=ending_balances,
        risk_of_loss=losing_runs / params.iterations,
    )
