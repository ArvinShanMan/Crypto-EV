"""
Expected Value (EV) Calculator Module

This module provides deterministic EV calculations for cryptocurrency trades.
It computes the expected value based on probability of success, profit/loss amounts,
and trade frequency.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class TradeParameters:
    """
    Parameters defining a single cryptocurrency trade scenario.
    
    Attributes:
        win_rate: Probability of successful trade (0.0 to 1.0)
        win_amount: Profit per winning trade
        loss_amount: Loss per losing trade (as positive value)
        num_trades: Number of trades to simulate
        risk_reward_ratio: Ratio of loss to win (loss_amount / win_amount)
    """
    win_rate: float
    win_amount: float
    loss_amount: float
    num_trades: int = 1
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        if not 0 <= self.win_rate <= 1:
            raise ValueError("win_rate must be between 0 and 1")
        if self.win_amount <= 0:
            raise ValueError("win_amount must be positive")
        if self.loss_amount < 0:
            raise ValueError("loss_amount must be non-negative")
        if self.num_trades <= 0:
            raise ValueError("num_trades must be positive")
    
    @property
    def risk_reward_ratio(self) -> float:
        """Calculate the risk-to-reward ratio."""
        if self.win_amount == 0:
            return float('inf')
        return self.loss_amount / self.win_amount
    
    @property
    def loss_rate(self) -> float:
        """Calculate the probability of loss (1 - win_rate)."""
        return 1 - self.win_rate


class EVCalculator:
    """
    Deterministic Expected Value calculator for trading scenarios.
    """
    
    def __init__(self, trade_params: TradeParameters):
        """
        Initialize the EV calculator with trade parameters.
        
        Args:
            trade_params: TradeParameters object defining the trade scenario
        """
        self.params = trade_params
    
    def calculate_single_trade_ev(self) -> float:
        """
        Calculate expected value for a single trade.
        
        Formula: EV = (win_rate × win_amount) - (loss_rate × loss_amount)
        
        Returns:
            Expected value of a single trade
        """
        win_ev = self.params.win_rate * self.params.win_amount
        loss_ev = self.params.loss_rate * self.params.loss_amount
        return win_ev - loss_ev
    
    def calculate_total_ev(self) -> float:
        """
        Calculate total expected value across all trades.
        
        Returns:
            Total EV for the specified number of trades
        """
        single_trade_ev = self.calculate_single_trade_ev()
        return single_trade_ev * self.params.num_trades
    
    def calculate_ev_per_risk_unit(self) -> float:
        """
        Calculate EV relative to risk amount (loss per trade).
        
        Returns:
            Expected value per unit of risk (per potential loss amount)
        """
        if self.params.loss_amount == 0:
            return float('inf') if self.params.win_rate > 0 else 0
        return self.calculate_single_trade_ev() / self.params.loss_amount
    
    def calculate_breakeven_win_rate(self) -> float:
        """
        Calculate the breakeven win rate (EV = 0).
        
        Formula: breakeven_rate = loss_amount / (win_amount + loss_amount)
        
        Returns:
            Win rate needed for zero expected value
        """
        total = self.params.win_amount + self.params.loss_amount
        if total == 0:
            return 0.5
        return self.params.loss_amount / total
    
    def calculate_metrics(self) -> Dict[str, float]:
        """
        Calculate comprehensive EV metrics.
        
        Returns:
            Dictionary containing all calculated metrics
        """
        return {
            'single_trade_ev': self.calculate_single_trade_ev(),
            'total_ev': self.calculate_total_ev(),
            'ev_per_risk_unit': self.calculate_ev_per_risk_unit(),
            'breakeven_win_rate': self.calculate_breakeven_win_rate(),
            'win_rate': self.params.win_rate,
            'loss_rate': self.params.loss_rate,
            'risk_reward_ratio': self.params.risk_reward_ratio,
            'num_trades': self.params.num_trades,
        }
    
    def is_profitable(self) -> bool:
        """
        Determine if the trade scenario is profitable on average.
        
        Returns:
            True if expected value is positive
        """
        return self.calculate_single_trade_ev() > 0
    
    def expected_profit_per_trade(self) -> float:
        """
        Return the expected profit for a single trade.
        
        Returns:
            Expected value for a single trade
        """
        return self.calculate_single_trade_ev()
    
    def expected_return_percentage(self) -> float:
        """
        Calculate expected return as a percentage of risk.
        
        Returns:
            Return percentage relative to the loss amount
        """
        if self.params.loss_amount == 0:
            return 0
        return (self.calculate_single_trade_ev() / self.params.loss_amount) * 100
