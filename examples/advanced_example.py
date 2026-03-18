"""
Advanced Example: Portfolio Strategy Analysis

This example demonstrates:
1. Multi-strategy portfolio analysis
2. Correlated asset modeling
3. Risk-adjusted metrics
4. Sensitivity analysis across multiple parameters
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ev_calculator import EVCalculator, TradeParameters
from monte_carlo import MonteCarloSimulator
from market_model import MarketModel, MarketCondition, CorrelationModel, GeometricBrownianMotion
from visualization import EVVisualizer
import numpy as np
import pandas as pd


def strategy_comparison():
    """Compare multiple trading strategies."""
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE 1: Multi-Strategy Comparison")
    print("="*70)
    
    strategies = {
        'Conservative': {
            'win_rate': 0.60,
            'win_amount': 50,
            'loss_amount': 100,
            'description': 'High win rate, small wins, larger losses'
        },
        'Aggressive': {
            'win_rate': 0.40,
            'win_amount': 200,
            'loss_amount': 50,
            'description': 'Low win rate, large wins, small losses'
        },
        'Balanced': {
            'win_rate': 0.55,
            'win_amount': 100,
            'loss_amount': 100,
            'description': '1:1 risk-reward ratio'
        },
        'High-Probability': {
            'win_rate': 0.70,
            'win_amount': 30,
            'loss_amount': 100,
            'description': 'Very high win rate but poor reward'
        },
    }
    
    results_summary = {}
    
    for strategy_name, params in strategies.items():
        print(f"\n{strategy_name}:")
        print(f"  Description: {params['description']}")
        
        # Calculate EV
        trade_params = TradeParameters(
            win_rate=params['win_rate'],
            win_amount=params['win_amount'],
            loss_amount=params['loss_amount'],
            num_trades=100
        )
        
        calc = EVCalculator(trade_params)
        ev = calc.calculate_single_trade_ev()
        ror = calc.expected_return_percentage()
        breakeven = calc.calculate_breakeven_win_rate()
        
        # Run simulation
        simulator = MonteCarloSimulator(
            win_rate=params['win_rate'],
            win_amount=params['win_amount'],
            loss_amount=params['loss_amount'],
            initial_balance=10000,
            random_seed=42
        )
        
        sim_results = simulator.simulate(num_trades=100, num_simulations=5000)
        
        results_summary[strategy_name] = {
            'EV': ev,
            'RoR%': ror,
            'Breakeven': breakeven,
            'Mean_Return%': sim_results.statistics['mean_return_pct'],
            'Winning_Sims%': sim_results.statistics['winning_simulations_pct'],
            'Worst_DD%': sim_results.statistics['worst_drawdown_pct'],
            'Std_Dev': sim_results.statistics['std_return_pct'],
        }
        
        print(f"    EV per trade: ${ev:.2f}")
        print(f"    Return on Risk: {ror:.2f}%")
        print(f"    Breakeven Win Rate: {breakeven:.2%}")
        print(f"    Simulated Mean Return: {sim_results.statistics['mean_return_pct']:.2f}%")
        print(f"    Win Probability: {sim_results.statistics['winning_simulations_pct']:.2f}%")
        print(f"    Worst Drawdown: {sim_results.statistics['worst_drawdown_pct']:.2f}%")
    
    # Create comparison DataFrame
    df = pd.DataFrame(results_summary).T
    print("\n" + "="*70)
    print("STRATEGY COMPARISON SUMMARY")
    print("="*70)
    print(df.to_string())
    print("\nRanking by Expected Value per Trade:")
    for i, (name, ev) in enumerate(sorted(results_summary.items(), key=lambda x: x[1]['EV'], reverse=True), 1):
        print(f"  {i}. {name}: ${results_summary[name]['EV']:.2f}")


def portfolio_optimization():
    """Analyze portfolio combinations of strategies."""
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE 2: Portfolio Optimization")
    print("="*70)
    
    # Define individual strategies
    strategy_a = TradeParameters(win_rate=0.55, win_amount=100, loss_amount=100, num_trades=50)
    strategy_b = TradeParameters(win_rate=0.60, win_amount=80, loss_amount=120, num_trades=50)
    
    # Analyze different allocation combinations
    allocations = [
        ('100% A, 0% B', 1.0, 0.0),
        ('75% A, 25% B', 0.75, 0.25),
        ('50% A, 50% B', 0.5, 0.5),
        ('25% A, 75% B', 0.25, 0.75),
        ('0% A, 100% B', 0.0, 1.0),
    ]
    
    print("\nPortfolio Allocation Analysis:")
    print(f"Strategy A: WR={strategy_a.win_rate:.0%}, Win=${strategy_a.win_amount}, Loss=${strategy_a.loss_amount}")
    print(f"Strategy B: WR={strategy_b.win_rate:.0%}, Win=${strategy_b.win_amount}, Loss=${strategy_b.loss_amount}")
    
    for name, alloc_a, alloc_b in allocations:
        # Combine expected values
        ev_a = EVCalculator(strategy_a).calculate_single_trade_ev() * alloc_a
        ev_b = EVCalculator(strategy_b).calculate_single_trade_ev() * alloc_b
        total_ev = ev_a + ev_b
        
        # Combined metrics
        combined_wr = strategy_a.win_rate * alloc_a + strategy_b.win_rate * alloc_b
        
        print(f"\n{name}")
        print(f"  Combined EV: ${total_ev:.2f}")
        print(f"  Blended Win Rate: {combined_wr:.2%}")


def risk_analysis():
    """Perform detailed risk analysis across scenarios."""
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE 3: Risk Analysis")
    print("="*70)
    
    # Base parameters
    base_wr = 0.55
    base_win = 100
    base_loss = 80
    
    # Test different account positions
    trade_counts = [10, 25, 50, 100, 200]
    
    print(f"\nRisk Analysis: Impact of Trade Number on Portfolio Volatility")
    print(f"(Base: {base_wr:.0%} WR, ${base_win} win, ${base_loss} loss, $10k initial)\n")
    
    simulator = MonteCarloSimulator(base_wr, base_win, base_loss, 10000, random_seed=42)
    
    print(f"{'Trades':<8} {'Mean Return%':<16} {'Std Dev%':<15} {'Best Case%':<15} {'Worst Case%':<15}")
    print("-" * 70)
    
    for num_trades in trade_counts:
        results = simulator.simulate(num_trades, 5000)
        stats = results.statistics
        print(f"{num_trades:<8} {stats['mean_return_pct']:>12.2f}%  "
              f"{stats['std_return_pct']:>11.2f}%  "
              f"{stats['best_case_return_pct']:>11.2f}%  "
              f"{stats['worst_case_return_pct']:>11.2f}%")
    
    # VAR analysis
    print("\n" + "-"*70)
    print("Value at Risk (VaR) Analysis at Different Confidence Levels")
    print("-"*70)
    
    results = simulator.simulate(100, 10000)
    var_95 = results.statistics['value_at_risk_95']
    var_99 = results.statistics['value_at_risk_99']
    
    print(f"95% Confidence Level (5% chance of worse): {var_95:.2f}%")
    print(f"99% Confidence Level (1% chance of worse): {var_99:.2f}%")
    
    # Expected shortfall
    es_95 = simulator.expected_shortfall(results, 0.95)
    print(f"Expected Shortfall (95%): ${es_95:.2f}")


def market_stress_test():
    """Stress test trading strategy under different market conditions."""
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE 4: Market Stress Testing")
    print("="*70)
    
    market = MarketModel()
    
    # Define different stress scenarios
    scenarios = {
        'Bull Run': [
            (MarketCondition.BULLISH, 100),
        ],
        'Bear Market': [
            (MarketCondition.BEARISH, 100),
        ],
        'Volatile': [
            (MarketCondition.BULLISH, 30),
            (MarketCondition.BEARISH, 30),
            (MarketCondition.BULLISH, 40),
        ],
        'Extended Bear': [
            (MarketCondition.BEARISH, 50),
            (MarketCondition.BEARISH, 50),
        ],
        'Recovery': [
            (MarketCondition.BEARISH, 40),
            (MarketCondition.SIDEWAYS, 30),
            (MarketCondition.BULLISH, 30),
        ],
    }
    
    print("\nMarket Stress Test Results (Starting with $100,000):\n")
    print(f"{'Scenario':<20} {'Final Balance':<18} {'Total Return%':<18} {'Status':<15}")
    print("-" * 70)
    
    for scenario_name, regime_sequence in scenarios.items():
        np.random.seed(42)
        results = market.simulate_market_regime(regime_sequence, initial_balance=100000)
        final = results['balances'][-1]
        return_pct = ((final - 100000) / 100000) * 100
        status = "✓ PROFIT" if final > 100000 else "✗ LOSS"
        
        print(f"{scenario_name:<20} ${final:>15,.2f}  {return_pct:>15.2f}%  {status:<15}")


def correlation_impact():
    """Analyze impact of asset correlations."""
    print("\n" + "="*70)
    print("ADVANCED EXAMPLE 5: Correlation Impact on Portfolio")
    print("="*70)
    
    print("\nGenerating correlated returns for 3 crypto assets...")
    
    # Different correlation scenarios
    scenarios = {
        'Low Correlation': np.array([
            [1.0, 0.1, 0.05],
            [0.1, 1.0, 0.1],
            [0.05, 0.1, 1.0],
        ]),
        'High Correlation': np.array([
            [1.0, 0.8, 0.7],
            [0.8, 1.0, 0.85],
            [0.7, 0.85, 1.0],
        ]),
        'Perfect Correlation': np.array([
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
        ]),
    }
    
    print("\nPortfolio Diversification Benefit Analysis:\n")
    
    for scenario_name, corr_matrix in scenarios.items():
        corr_model = CorrelationModel(3, corr_matrix)
        
        # Generate returns
        mean_returns = np.array([0.1, 0.12, 0.08])
        std_returns = np.array([0.2, 0.25, 0.15])
        
        corr_returns = corr_model.generate_correlated_returns(252, mean_returns, std_returns, random_seed=42)
        
        # Calculate portfolio metrics
        portfolio_returns = np.mean(corr_returns, axis=0)
        portfolio_volatility = np.std(portfolio_returns)
        
        print(f"{scenario_name}:")
        print(f"  Portfolio Daily Volatility: {portfolio_volatility:.4f}")
        print(f"  Annualized Volatility: {portfolio_volatility * np.sqrt(252):.2%}")
        print(f"  Diversification Ratio: {np.mean(std_returns) / portfolio_volatility:.2f}")
        print()


def main():
    """Run all advanced examples."""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║    Crypto EV Simulator - Advanced Analysis Examples       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    strategy_comparison()
    portfolio_optimization()
    risk_analysis()
    market_stress_test()
    correlation_impact()
    
    print("\n" + "="*70)
    print("All advanced examples completed!")
    print("="*70)


if __name__ == "__main__":
    main()
