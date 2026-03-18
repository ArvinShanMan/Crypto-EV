"""
Monte Carlo Simulation Module

This module provides Monte Carlo simulation for cryptocurrency trading scenarios.
It generates randomized trading outcomes to estimate return distributions,
drawdown scenarios, and risk metrics.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import warnings


@dataclass
class SimulationResults:
    """
    Container for Monte Carlo simulation results.
    
    Attributes:
        final_balances: Array of final account balance for each simulation run
        trade_outcomes: 2D array of individual trade outcomes (num_runs × num_trades)
        cumulative_returns: 2D array of cumulative returns over time
        drawdowns: 2D array of drawdown paths for each run
        max_drawdowns: Maximum drawdown for each run
        statistics: Dictionary of computed statistics
    """
    final_balances: np.ndarray
    trade_outcomes: np.ndarray
    cumulative_returns: np.ndarray
    drawdowns: np.ndarray
    max_drawdowns: np.ndarray
    statistics: Dict[str, float]


class MonteCarloSimulator:
    """
    Monte Carlo simulator for trading scenarios.
    Generates random trading outcomes to estimate return distributions.
    """
    
    def __init__(self, win_rate: float, win_amount: float, loss_amount: float,
                 initial_balance: float = 1000.0, random_seed: Optional[int] = None):
        """
        Initialize the Monte Carlo simulator.
        
        Args:
            win_rate: Probability of successful trade (0.0 to 1.0)
            win_amount: Profit per winning trade
            loss_amount: Loss per losing trade (as positive value)
            initial_balance: Starting account balance
            random_seed: Random seed for reproducibility
        """
        self.win_rate = win_rate
        self.win_amount = win_amount
        self.loss_amount = loss_amount
        self.initial_balance = initial_balance
        
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def simulate(self, num_trades: int, num_simulations: int = 10000) -> SimulationResults:
        """
        Run Monte Carlo simulations.
        
        Args:
            num_trades: Number of trades per simulation
            num_simulations: Number of independent simulation runs
        
        Returns:
            SimulationResults object containing all results and statistics
        """
        # Initialize arrays
        trade_outcomes = np.zeros((num_simulations, num_trades))
        cumulative_returns = np.zeros((num_simulations, num_trades + 1))
        drawdowns = np.zeros((num_simulations, num_trades + 1))
        balances = np.zeros((num_simulations, num_trades + 1))
        
        # Set initial balance
        balances[:, 0] = self.initial_balance
        cumulative_returns[:, 0] = 0
        drawdowns[:, 0] = 0
        
        # Generate random trades for all simulations
        for i in range(num_simulations):
            # Generate random trade outcomes (1 = win, 0 = loss)
            wins = np.random.binomial(1, self.win_rate, num_trades)
            
            # Calculate profit/loss for each trade
            trade_outcomes[i, :] = np.where(wins == 1, self.win_amount, -self.loss_amount)
            
            # Calculate cumulative returns and balances
            cumulative_pnl = np.cumsum(trade_outcomes[i, :])
            balances[i, 1:] = self.initial_balance + cumulative_pnl
            cumulative_returns[i, 1:] = cumulative_pnl
            
            # Calculate drawdowns
            running_max = np.maximum.accumulate(balances[i, :])
            drawdowns[i, :] = (balances[i, :] - running_max) / running_max * 100
        
        # Calculate statistics
        final_balances = balances[:, -1]
        max_drawdowns = np.min(drawdowns, axis=1)
        
        statistics = self._calculate_statistics(
            final_balances, cumulative_returns[:, -1], max_drawdowns
        )
        
        return SimulationResults(
            final_balances=final_balances,
            trade_outcomes=trade_outcomes,
            cumulative_returns=cumulative_returns,
            drawdowns=drawdowns,
            max_drawdowns=max_drawdowns,
            statistics=statistics
        )
    
    def _calculate_statistics(self, final_balances: np.ndarray, 
                            total_returns: np.ndarray,
                            max_drawdowns: np.ndarray) -> Dict[str, float]:
        """
        Calculate comprehensive statistics from simulation results.
        
        Args:
            final_balances: Final balance for each run
            total_returns: Total return for each run
            max_drawdowns: Maximum drawdown for each run
        
        Returns:
            Dictionary of statistics
        """
        returns_pct = ((final_balances - self.initial_balance) / self.initial_balance) * 100
        
        return {
            'mean_final_balance': np.mean(final_balances),
            'median_final_balance': np.median(final_balances),
            'std_final_balance': np.std(final_balances),
            'min_final_balance': np.min(final_balances),
            'max_final_balance': np.max(final_balances),
            'mean_return_pct': np.mean(returns_pct),
            'median_return_pct': np.median(returns_pct),
            'std_return_pct': np.std(returns_pct),
            'winning_simulations_pct': np.sum(final_balances > self.initial_balance) / len(final_balances) * 100,
            'losing_simulations_pct': np.sum(final_balances < self.initial_balance) / len(final_balances) * 100,
            'mean_max_drawdown_pct': np.mean(max_drawdowns),
            'worst_drawdown_pct': np.min(max_drawdowns),
            'best_case_return_pct': np.max(returns_pct),
            'worst_case_return_pct': np.min(returns_pct),
            'value_at_risk_95': np.percentile(returns_pct, 5),  # 95% confidence
            'value_at_risk_99': np.percentile(returns_pct, 1),  # 99% confidence
        }
    
    def expected_shortfall(self, results: SimulationResults, confidence: float = 0.95) -> float:
        """
        Calculate expected shortfall (conditional value at risk).
        
        Args:
            results: SimulationResults object
            confidence: Confidence level (default 0.95 for 95% confidence)
        
        Returns:
            Expected shortfall value
        """
        threshold = np.percentile(results.final_balances, (1 - confidence) * 100)
        return np.mean(results.final_balances[results.final_balances <= threshold])
    
    def win_rate_analysis(self, num_trades: int, win_rates: List[float],
                         num_simulations: int = 1000) -> Dict[float, Dict[str, float]]:
        """
        Analyze outcomes across different win rates.
        
        Args:
            num_trades: Number of trades per simulation
            win_rates: List of win rates to test
            num_simulations: Number of simulations per win rate
        
        Returns:
            Dictionary mapping win rates to their statistics
        """
        results = {}
        current_win_rate = self.win_rate
        
        for wr in win_rates:
            self.win_rate = wr
            sim_results = self.simulate(num_trades, num_simulations)
            results[wr] = sim_results.statistics
        
        # Restore original win rate
        self.win_rate = current_win_rate
        
        return results
