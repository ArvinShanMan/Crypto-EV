from __future__ import annotations

import random
from typing import Optional


class MarketModel:
    """Minimal market model that samples trade outcomes from a Bernoulli process."""

    def __init__(self, seed: Optional[int] = None) -> None:
        self._rng = random.Random(seed)

    def sample_trade_pnl(self, win_rate: float, profit_per_win: float, loss_per_trade: float) -> float:
        return profit_per_win if self._rng.random() < win_rate else -loss_per_trade
