"""
Crypto EV Simulator Package

A comprehensive expected value simulator for cryptocurrency trading decisions.
Includes analytical EV calculations, Monte Carlo simulations, and market modeling.
"""

from .ev_calculator import EVCalculator, TradeParameters
from .monte_carlo import MonteCarloSimulator, SimulationResults
from .market_model import GeometricBrownianMotion, MarketModel, MarketCondition, CorrelationModel
from .visualization import EVVisualizer
from .utilities import (
    kelly_criterion,
    optimal_position_size,
    calculate_portfolio_var,
    sortino_ratio,
    sharpe_ratio,
    calmar_ratio,
    profit_factor,
)

__version__ = "1.0.0"
__author__ = "Crypto EV Team"

__all__ = [
    'EVCalculator',
    'TradeParameters',
    'MonteCarloSimulator',
    'SimulationResults',
    'GeometricBrownianMotion',
    'MarketModel',
    'MarketCondition',
    'CorrelationModel',
    'EVVisualizer',
    'kelly_criterion',
    'optimal_position_size',
    'calculate_portfolio_var',
    'sortino_ratio',
    'sharpe_ratio',
    'calmar_ratio',
    'profit_factor',
]
