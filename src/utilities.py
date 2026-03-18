"""
Utility Functions for Crypto EV Simulator

Helper functions for common operations.
"""

import numpy as np
from typing import List, Dict, Tuple
from ev_calculator import TradeParameters, EVCalculator


def validate_probabilities(*probs: float) -> bool:
    """
    Validate that probabilities are between 0 and 1.
    
    Args:
        *probs: Variable number of probability values
    
    Returns:
        True if all are valid probabilities
    """
    return all(0 <= p <= 1 for p in probs)


def kelly_criterion(win_rate: float, win_amount: float, loss_amount: float) -> float:
    """
    Calculate Kelly Criterion for optimal position sizing.
    
    Formula: f* = (bp - q) / b
    where:
    - b = win_amount / loss_amount (odds)
    - p = win_rate
    - q = 1 - p (loss_rate)
    
    Args:
        win_rate: Probability of winning
        win_amount: Profit amount per win
        loss_amount: Loss amount per loss
    
    Returns:
        Optimal fraction of capital to risk (between 0 and 1)
        Returns 0 if negative (strategy is negative EV)
    """
    if loss_amount == 0:
        return 0
    
    b = win_amount / loss_amount
    p = win_rate
    q = 1 - p
    
    kelly_frac = (b * p - q) / b
    
    # Never risk more than 100%, and never negative
    return max(0, min(kelly_frac, 1))


def optimal_position_size(account_size: float, risk_percent: float, loss_per_trade: float) -> float:
    """
    Calculate optimal position size based on risk percentage.
    
    Args:
        account_size: Total account balance
        risk_percent: Percentage of account willing to risk (0-1)
        loss_per_trade: Maximum loss per individual trade
    
    Returns:
        Position size in dollars
    """
    risk_amount = account_size * risk_percent
    return risk_amount / loss_per_trade


def calculate_portfolio_var(returns: np.ndarray, confidence: float = 0.95) -> float:
    """
    Calculate Value at Risk (VaR) for portfolio returns.
    
    Args:
        returns: Array of returns
        confidence: Confidence level (default 0.95 for 95%)
    
    Returns:
        VaR (worst case return at given confidence level)
    """
    var_percentile = (1 - confidence) * 100
    return np.percentile(returns, var_percentile)


def calculate_cvar(returns: np.ndarray, confidence: float = 0.95) -> float:
    """
    Calculate Conditional Value at Risk (Expected Shortfall).
    
    Args:
        returns: Array of returns
        confidence: Confidence level (default 0.95)
    
    Returns:
        CVaR (average return of worst outcomes)
    """
    var_threshold = calculate_portfolio_var(returns, confidence)
    return np.mean(returns[returns <= var_threshold])


def sortino_ratio(returns: np.ndarray, annual_target_return: float = 0.0) -> float:
    """
    Calculate Sortino Ratio (downside risk adjusted return).
    
    Formula: (Mean Return - Target Return) / Downside Deviation
    
    Args:
        returns: Array of returns
        annual_target_return: Target annual return (default 0%)
    
    Returns:
        Sortino Ratio
    """
    excess_returns = returns - annual_target_return
    downside_returns = excess_returns[excess_returns < 0]
    
    if len(downside_returns) == 0:
        return float('inf')  # No downside risk
    
    downside_std = np.std(downside_returns)
    
    if downside_std == 0:
        return float('inf')
    
    return np.mean(excess_returns) / downside_std


def sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
    """
    Calculate Sharpe Ratio (risk-adjusted return).
    
    Formula: (Mean Return - Risk-Free Rate) / Std Dev
    
    Args:
        returns: Array of returns (should be daily or period returns)
        risk_free_rate: Annual risk-free rate (default 2%)
    
    Returns:
        Sharpe Ratio (annualized if using daily returns)
    """
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    
    if std_return == 0:
        return 0
    
    sharpe = (mean_return - risk_free_rate / 252) / std_return
    
    # Annualize if daily returns
    return sharpe * np.sqrt(252)


def calmar_ratio(returns: np.ndarray) -> float:
    """
    Calculate Calmar Ratio (return relative to max drawdown).
    
    Args:
        returns: Array of returns
    
    Returns:
        Calmar Ratio
    """
    cumulative = np.cumprod(1 + returns)
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = np.min(drawdown)
    
    if max_drawdown == 0:
        return float('inf')
    
    total_return = cumulative[-1] - 1
    return total_return / abs(max_drawdown)


def profit_factor(trades: np.ndarray) -> float:
    """
    Calculate Profit Factor (total wins / total losses).
    
    Args:
        trades: Array of individual trade P&L values
    
    Returns:
        Profit Factor
    """
    wins = np.sum(trades[trades > 0])
    losses = np.abs(np.sum(trades[trades < 0]))
    
    if losses == 0:
        return float('inf')
    
    return wins / losses


def create_trade_scenarios(base_params: TradeParameters, 
                          variations: Dict[str, List]) -> Dict[str, TradeParameters]:
    """
    Create multiple trade parameter scenarios for sensitivity analysis.
    
    Args:
        base_params: Base TradeParameters object
        variations: Dictionary with keys 'win_rate', 'win_amount', etc. 
                   mapping to lists of values to test
    
    Returns:
        Dictionary of scenario names to TradeParameters
    """
    scenarios = {}
    
    # Get all variation combinations
    keys = list(variations.keys())
    value_lists = [variations[k] for k in keys]
    
    import itertools
    
    for values in itertools.product(*value_lists):
        params_dict = {
            'win_rate': base_params.win_rate,
            'win_amount': base_params.win_amount,
            'loss_amount': base_params.loss_amount,
            'num_trades': base_params.num_trades,
        }
        
        for key, value in zip(keys, values):
            params_dict[key] = value
        
        scenario_name = '_'.join(f"{k}_{v}" for k, v in zip(keys, values))
        scenarios[scenario_name] = TradeParameters(**params_dict)
    
    return scenarios


def risk_metrics_summary(final_balances: np.ndarray, 
                        cumulative_returns: np.ndarray,
                        initial_balance: float = 1000.0) -> Dict[str, float]:
    """
    Calculate comprehensive risk metrics summary.
    
    Args:
        final_balances: Array of final account balances
        cumulative_returns: 2D array of cumulative returns over time
        initial_balance: Initial account balance
    
    Returns:
        Dictionary of risk metrics
    """
    returns_pct = (final_balances - initial_balance) / initial_balance
    
    # Calculate drawdown metrics
    max_drawdowns = []
    for path in cumulative_returns:
        cumbal = initial_balance + path
        running_max = np.maximum.accumulate(cumbal)
        drawdown = (cumbal - running_max) / running_max
        max_drawdowns.append(np.min(drawdown))
    
    return {
        'mean_return': np.mean(returns_pct),
        'median_return': np.median(returns_pct),
        'std_return': np.std(returns_pct),
        'skewness': np.mean((returns_pct - np.mean(returns_pct))**3) / (np.std(returns_pct)**3 + 1e-10),
        'kurtosis': np.mean((returns_pct - np.mean(returns_pct))**4) / (np.std(returns_pct)**4 + 1e-10) - 3,
        'min_return': np.min(returns_pct),
        'max_return': np.max(returns_pct),
        'percentile_5': np.percentile(returns_pct, 5),
        'percentile_95': np.percentile(returns_pct, 95),
        'prob_profit': np.sum(returns_pct > 0) / len(returns_pct),
        'mean_max_drawdown': np.mean(max_drawdowns),
        'worst_drawdown': np.min(max_drawdowns),
    }
