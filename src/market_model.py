"""
Market Modeling Module

This module provides market modeling capabilities including price generation,
volatility modeling, and scenario-based market simulations for crypto trading.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum


class MarketCondition(Enum):
    """Enumeration of market conditions."""
    BULLISH = "bullish"
    BEARISH = "bearish"
    SIDEWAYS = "sideways"


@dataclass
class PriceSimulation:
    """
    Container for price simulation results.
    
    Attributes:
        prices: 2D array of simulated prices (num_paths × num_steps)
        returns: 2D array of returns (num_paths × num_steps)
        volatility: Realized volatility for each path
        drift: Trend/drift for each path
    """
    prices: np.ndarray
    returns: np.ndarray
    volatility: np.ndarray
    drift: np.ndarray


class GeometricBrownianMotion:
    """
    Geometric Brownian Motion model for cryptocurrency price simulation.
    
    dS/S = μ dt + σ dW
    where:
    - S is the price
    - μ is the drift (expected return)
    - σ is the volatility
    - dW is a Wiener process increment
    """
    
    def __init__(self, initial_price: float, drift: float, volatility: float):
        """
        Initialize GBM model.
        
        Args:
            initial_price: Initial asset price
            drift: Expected return (annualized)
            volatility: Price volatility (annualized)
        """
        self.initial_price = initial_price
        self.drift = drift
        self.volatility = volatility
    
    def simulate(self, num_steps: int, time_horizon: float = 1.0,
                num_paths: int = 1000, random_seed: Optional[int] = None) -> PriceSimulation:
        """
        Simulate price paths using GBM.
        
        Args:
            num_steps: Number of time steps
            time_horizon: Time horizon in years
            num_paths: Number of simulation paths
            random_seed: Random seed for reproducibility
        
        Returns:
            PriceSimulation object containing price paths and statistics
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        dt = time_horizon / num_steps
        
        # Initialize price array
        prices = np.zeros((num_paths, num_steps + 1))
        prices[:, 0] = self.initial_price
        
        # Generate random normal increments
        dW = np.random.normal(0, np.sqrt(dt), (num_paths, num_steps))
        
        # Simulate price paths
        for t in range(num_steps):
            prices[:, t + 1] = prices[:, t] * np.exp(
                (self.drift - 0.5 * self.volatility ** 2) * dt +
                self.volatility * dW[:, t]
            )
        
        # Calculate returns
        returns = np.diff(prices, axis=1) / prices[:, :-1]
        
        # Calculate realized volatility and drift for each path
        realized_volatility = np.std(returns, axis=1) * np.sqrt(252)  # Annualize
        realized_drift = np.mean(returns, axis=1) * 252  # Annualize
        
        return PriceSimulation(
            prices=prices,
            returns=returns,
            volatility=realized_volatility,
            drift=realized_drift
        )


class MarketModel:
    """
    Market model for cryptocurrency trading scenarios.
    Links market conditions to trading parameters.
    """
    
    def __init__(self):
        """Initialize the market model."""
        self.condition_params = {
            MarketCondition.BULLISH: {
                'win_rate': 0.65,
                'win_amount': 2.0,
                'loss_amount': 1.0,
                'volatility': 0.3,
            },
            MarketCondition.BEARISH: {
                'win_rate': 0.35,
                'win_amount': 1.0,
                'loss_amount': 2.0,
                'volatility': 0.5,
            },
            MarketCondition.SIDEWAYS: {
                'win_rate': 0.50,
                'win_amount': 1.5,
                'loss_amount': 1.5,
                'volatility': 0.25,
            },
        }
    
    def get_trading_params(self, condition: MarketCondition) -> Dict[str, float]:
        """
        Get trading parameters for a specific market condition.
        
        Args:
            condition: MarketCondition enum value
        
        Returns:
            Dictionary of trading parameters
        """
        return self.condition_params[condition].copy()
    
    def simulate_market_regime(self, transitions: List[Tuple[MarketCondition, int]],
                             initial_balance: float = 1000.0) -> Dict:
        """
        Simulate trading across different market regimes.
        
        Args:
            transitions: List of (MarketCondition, num_trades) tuples
            initial_balance: Starting balance
        
        Returns:
            Simulation results for the regime
        """
        balance = initial_balance
        results = {
            'balances': [balance],
            'trades': [],
            'regimes': [],
        }
        
        for regime, num_trades in transitions:
            params = self.get_trading_params(regime)
            
            for _ in range(num_trades):
                # Simulate trade outcome
                if np.random.random() < params['win_rate']:
                    pnl = params['win_amount']
                else:
                    pnl = -params['loss_amount']
                
                balance += pnl
                results['balances'].append(balance)
                results['trades'].append(pnl)
                results['regimes'].append(regime.value)
        
        return results
    
    def estimate_market_condition(self, recent_returns: np.ndarray,
                                 threshold: float = 0.02) -> MarketCondition:
        """
        Estimate market condition from recent returns.
        
        Args:
            recent_returns: Array of recent log returns
            threshold: Threshold for determining market direction
        
        Returns:
            Estimated MarketCondition
        """
        mean_return = np.mean(recent_returns)
        std_return = np.std(recent_returns)
        
        if mean_return > threshold:
            return MarketCondition.BULLISH
        elif mean_return < -threshold:
            return MarketCondition.BEARISH
        else:
            return MarketCondition.SIDEWAYS


class CorrelationModel:
    """
    Model correlations between multiple cryptocurrency assets.
    """
    
    def __init__(self, num_assets: int, correlation_matrix: Optional[np.ndarray] = None):
        """
        Initialize correlation model.
        
        Args:
            num_assets: Number of assets to model
            correlation_matrix: Optional correlation matrix (must be symmetric)
        """
        self.num_assets = num_assets
        
        if correlation_matrix is None:
            # Default: low correlation between assets
            self.correlation_matrix = np.eye(num_assets) * 0.3 + np.ones((num_assets, num_assets)) * 0.1
            np.fill_diagonal(self.correlation_matrix, 1.0)
        else:
            self.correlation_matrix = correlation_matrix
        
        # Validate correlation matrix
        self._validate_correlation_matrix()
    
    def _validate_correlation_matrix(self):
        """Validate that correlation matrix is symmetric and PSD."""
        if self.correlation_matrix.shape != (self.num_assets, self.num_assets):
            raise ValueError("Correlation matrix dimensions don't match num_assets")
        
        if not np.allclose(self.correlation_matrix, self.correlation_matrix.T):
            raise ValueError("Correlation matrix must be symmetric")
        
        eigenvalues = np.linalg.eigvals(self.correlation_matrix)
        if np.any(eigenvalues < -1e-10):
            raise ValueError("Correlation matrix must be positive semi-definite")
    
    def generate_correlated_returns(self, num_steps: int, returns_mean: np.ndarray,
                                   returns_std: np.ndarray,
                                   random_seed: Optional[int] = None) -> np.ndarray:
        """
        Generate correlated returns for multiple assets.
        
        Args:
            num_steps: Number of time steps
            returns_mean: Mean returns for each asset
            returns_std: Standard deviation for each asset
            random_seed: Random seed for reproducibility
        
        Returns:
            Array of correlated returns (num_assets × num_steps)
        """
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Generate uncorrelated normal returns
        uncorrelated_returns = np.random.normal(0, 1, (self.num_assets, num_steps))
        
        # Apply Cholesky decomposition to induce correlation
        L = np.linalg.cholesky(self.correlation_matrix)
        correlated_returns = L @ uncorrelated_returns
        
        # Scale to desired mean and std
        for i in range(self.num_assets):
            correlated_returns[i] = correlated_returns[i] * returns_std[i] + returns_mean[i]
        
        return correlated_returns
