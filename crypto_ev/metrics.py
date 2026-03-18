from __future__ import annotations

from statistics import mean, pstdev
from typing import Iterable, List



def equity_curve(starting_balance: float, trade_results: Iterable[float]) -> List[float]:
    balance = starting_balance
    curve = [balance]
    for pnl in trade_results:
        balance += pnl
        curve.append(balance)
    return curve



def max_drawdown(curve: Iterable[float]) -> float:
    peak = None
    max_dd = 0.0
    for value in curve:
        peak = value if peak is None else max(peak, value)
        if peak != 0:
            max_dd = min(max_dd, (value - peak) / peak)
    return abs(max_dd)



def sharpe_ratio(returns: Iterable[float], risk_free_rate: float = 0.0) -> float:
    returns = list(returns)
    if len(returns) < 2:
        return 0.0
    excess_returns = [value - risk_free_rate for value in returns]
    volatility = pstdev(excess_returns)
    if volatility == 0:
        return 0.0
    return mean(excess_returns) / volatility
