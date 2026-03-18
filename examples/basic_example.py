"""
Example: Basic EV Calculation and Monte Carlo Simulation

This example demonstrates:
1. Computing analytical expected value
2. Running a Monte Carlo simulation
3. Analyzing win rate sensitivity
4. Visualizing results
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ev_calculator import EVCalculator, TradeParameters
from monte_carlo import MonteCarloSimulator
from market_model import MarketModel, MarketCondition, GeometricBrownianMotion
from visualization import EVVisualizer
import numpy as np


def example_basic_ev():
    """Example 1: Basic EV calculation for a single trade scenario."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic EV Calculation")
    print("="*60)
    
    # Define trade parameters
    trade_params = TradeParameters(
        win_rate=0.55,           # 55% win rate
        win_amount=100.0,        # $100 profit per win
        loss_amount=80.0,        # $80 loss per loss
        num_trades=100
    )
    
    # Create calculator and compute metrics
    calculator = EVCalculator(trade_params)
    metrics = calculator.calculate_metrics()
    
    # Display results
    print(f"\nTrade Parameters:")
    print(f"  Win Rate: {trade_params.win_rate:.2%}")
    print(f"  Win Amount: ${trade_params.win_amount}")
    print(f"  Loss Amount: ${trade_params.loss_amount}")
    print(f"  Risk/Reward Ratio: {trade_params.risk_reward_ratio:.2f}")
    print(f"  Number of Trades: {trade_params.num_trades}")
    
    print(f"\nEV Metrics:")
    print(f"  Single Trade EV: ${metrics['single_trade_ev']:.2f}")
    print(f"  Total EV ({trade_params.num_trades} trades): ${metrics['total_ev']:.2f}")
    print(f"  EV per Risk Unit: {metrics['ev_per_risk_unit']:.2f}")
    print(f"  Expected Return %: {calculator.expected_return_percentage():.2f}%")
    print(f"  Breakeven Win Rate: {metrics['breakeven_win_rate']:.2%}")
    print(f"  Profitable Trade? {'✓ YES' if calculator.is_profitable() else '✗ NO'}")


def example_monte_carlo_simulation():
    """Example 2: Monte Carlo simulation of trading outcomes."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Monte Carlo Simulation")
    print("="*60)
    
    # Create simulator
    simulator = MonteCarloSimulator(
        win_rate=0.55,
        win_amount=100.0,
        loss_amount=80.0,
        initial_balance=1000.0,
        random_seed=42
    )
    
    # Run simulation
    num_trades = 50
    num_simulations = 10000
    print(f"\nRunning {num_simulations} simulations with {num_trades} trades each...")
    results = simulator.simulate(num_trades, num_simulations)
    
    # Display results
    print(f"\nSimulation Results:")
    print(f"  Mean Final Balance: ${results.statistics['mean_final_balance']:.2f}")
    print(f"  Median Final Balance: ${results.statistics['median_final_balance']:.2f}")
    print(f"  Std Dev: ${results.statistics['std_final_balance']:.2f}")
    print(f"  Min Final Balance: ${results.statistics['min_final_balance']:.2f}")
    print(f"  Max Final Balance: ${results.statistics['max_final_balance']:.2f}")
    print(f"  Mean Return %: {results.statistics['mean_return_pct']:.2f}%")
    print(f"  Winning Simulations: {results.statistics['winning_simulations_pct']:.2f}%")
    print(f"  Losing Simulations: {results.statistics['losing_simulations_pct']:.2f}%")
    print(f"  Mean Max Drawdown: {results.statistics['mean_max_drawdown_pct']:.2f}%")
    print(f"  Worst Drawdown: {results.statistics['worst_drawdown_pct']:.2f}%")
    print(f"  Value at Risk (95%): {results.statistics['value_at_risk_95']:.2f}%")
    print(f"  Expected Shortfall: ${simulator.expected_shortfall(results, 0.95):.2f}")
    
    return results


def example_win_rate_sensitivity():
    """Example 3: Sensitivity analysis across different win rates."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Win Rate Sensitivity Analysis")
    print("="*60)
    
    # Create simulator
    simulator = MonteCarloSimulator(
        win_rate=0.50,
        win_amount=100.0,
        loss_amount=80.0,
        initial_balance=1000.0,
        random_seed=42
    )
    
    # Test different win rates
    win_rates = np.arange(0.30, 0.71, 0.05)
    print(f"\nTesting win rates: {win_rates}")
    
    results = simulator.win_rate_analysis(
        num_trades=50,
        win_rates=list(win_rates),
        num_simulations=5000
    )
    
    print(f"\n{'Win Rate':<12} {'Mean Return %':<18} {'Win Sim %':<15} {'Mean DD %':<15}")
    print("-" * 60)
    for wr in sorted(results.keys()):
        stats = results[wr]
        print(f"{wr:.2%}        {stats['mean_return_pct']:>12.2f}%    "
              f"{stats['winning_simulations_pct']:>10.2f}%    "
              f"{stats['mean_max_drawdown_pct']:>10.2f}%")


def example_market_modeling():
    """Example 4: Market regime modeling."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Market Regime Modeling")
    print("="*60)
    
    # Create market model
    market = MarketModel()
    
    # Define a market regime sequence
    regimes = [
        (MarketCondition.BULLISH, 20),    # 20 trades in bullish market
        (MarketCondition.SIDEWAYS, 15),   # 15 trades in sideways market
        (MarketCondition.BEARISH, 15),    # 15 trades in bearish market
    ]
    
    print("\nMarket Regime Sequence:")
    for condition, num_trades in regimes:
        params = market.get_trading_params(condition)
        print(f"  {condition.value.upper()}: {num_trades} trades (WR: {params['win_rate']:.0%})")
    
    # Simulate the regime
    np.random.seed(42)
    results = market.simulate_market_regime(regimes, initial_balance=5000.0)
    
    final_balance = results['balances'][-1]
    total_return = final_balance - 5000.0
    return_pct = (total_return / 5000.0) * 100
    
    print(f"\nRegime Simulation Results:")
    print(f"  Initial Balance: $5000.00")
    print(f"  Final Balance: ${final_balance:.2f}")
    print(f"  Total Return: ${total_return:.2f}")
    print(f"  Return %: {return_pct:.2f}%")
    print(f"  Total Trades: {len(results['trades'])}")


def example_price_simulation():
    """Example 5: Geometric Brownian Motion price simulation."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Price Simulation (Geometric Brownian Motion)")
    print("="*60)
    
    # Create GBM model
    gbm = GeometricBrownianMotion(
        initial_price=100.0,      # Start at $100
        drift=0.15,               # 15% annual expected return
        volatility=0.4            # 40% annual volatility
    )
    
    # Simulate price paths
    print(f"\nSimulating 1000 price paths over 252 trading days...")
    price_sim = gbm.simulate(
        num_steps=252,
        time_horizon=1.0,
        num_paths=1000,
        random_seed=42
    )
    
    print(f"\nPrice Simulation Results:")
    print(f"  Initial Price: $100.00")
    print(f"  Mean Final Price: ${np.mean(price_sim.prices[:, -1]):.2f}")
    print(f"  Median Final Price: ${np.median(price_sim.prices[:, -1]):.2f}")
    print(f"  5th Percentile: ${np.percentile(price_sim.prices[:, -1], 5):.2f}")
    print(f"  95th Percentile: ${np.percentile(price_sim.prices[:, -1], 95):.2f}")
    print(f"  Mean Realized Volatility: {np.mean(price_sim.volatility):.2%}")
    print(f"  Mean Realized Drift: {np.mean(price_sim.drift):.2%}")
    
    return price_sim


def example_visualization(mc_results):
    """Example 6: Visualizing results."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Data Visualization")
    print("="*60)
    
    visualizer = EVVisualizer()
    
    print("\nGenerating visualizations...")
    
    # Create simulation results visualization
    fig1 = visualizer.plot_simulation_results(mc_results, num_paths=50)
    print("  ✓ Simulation results plot created")
    
    # Create return distribution plot
    fig2 = visualizer.plot_return_distribution(mc_results)
    print("  ✓ Return distribution plot created")
    
    # Win rate sensitivity plot
    simulator = MonteCarloSimulator(0.55, 100, 80, random_seed=42)
    wr_results = simulator.win_rate_analysis(50, list(np.arange(0.30, 0.71, 0.05)), 2000)
    fig3 = visualizer.plot_win_rate_analysis(wr_results)
    print("  ✓ Win rate sensitivity plot created")
    
    print("\nNote: Plots are ready for display. Call visualizer.show() to view them.")
    return fig1, fig2, fig3


def main():
    """Run all examples."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    Crypto EV Simulator - Comprehensive Examples            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Run examples
    example_basic_ev()
    mc_results = example_monte_carlo_simulation()
    example_win_rate_sensitivity()
    example_market_modeling()
    price_sim = example_price_simulation()
    figs = example_visualization(mc_results)
    
    print("\n" + "="*60)
    print("All examples completed successfully!")
    print("="*60)
    print("\nKey Insights:")
    print("1. Always validate that your trade has positive expected value")
    print("2. Use Monte Carlo to understand drawdown and risk exposure")
    print("3. Different win rates yield different risk/reward profiles")
    print("4. Market conditions significantly impact trading outcomes")
    print("5. Visualizations help identify patterns and extreme scenarios")


if __name__ == "__main__":
    main()
