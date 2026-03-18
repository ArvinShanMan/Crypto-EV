"""
Unit Tests for Crypto EV Simulator

Basic tests for core functionality. Can be expanded with pytest.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import numpy as np
from ev_calculator import EVCalculator, TradeParameters
from monte_carlo import MonteCarloSimulator
from market_model import MarketCondition, MarketModel, GeometricBrownianMotion
from utilities import kelly_criterion, profit_factor, sortino_ratio


class TestEVCalculator(unittest.TestCase):
    """Test EV Calculator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.params = TradeParameters(
            win_rate=0.55,
            win_amount=100,
            loss_amount=100,
            num_trades=100
        )
        self.calculator = EVCalculator(self.params)
    
    def test_positive_ev(self):
        """Test that a profitable trade has positive EV."""
        ev = self.calculator.calculate_single_trade_ev()
        self.assertGreater(ev, 0, "55% win rate should have positive EV")
    
    def test_breakeven_win_rate(self):
        """Test breakeven calculation."""
        breakeven = self.calculator.calculate_breakeven_win_rate()
        self.assertEqual(breakeven, 0.5, "With 1:1 ratio, breakeven should be 50%")
    
    def test_is_profitable(self):
        """Test profitability check."""
        self.assertTrue(self.calculator.is_profitable())
    
    def test_total_ev(self):
        """Test total EV calculation."""
        single_ev = self.calculator.calculate_single_trade_ev()
        total_ev = self.calculator.calculate_total_ev()
        expected_total = single_ev * self.params.num_trades
        self.assertEqual(total_ev, expected_total)
    
    def test_parameter_validation(self):
        """Test that invalid parameters are rejected."""
        with self.assertRaises(ValueError):
            TradeParameters(win_rate=1.5, win_amount=100, loss_amount=100)
        
        with self.assertRaises(ValueError):
            TradeParameters(win_rate=0.5, win_amount=-100, loss_amount=100)


class TestMonteCarloSimulator(unittest.TestCase):
    """Test Monte Carlo Simulator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.simulator = MonteCarloSimulator(
            win_rate=0.55,
            win_amount=100,
            loss_amount=100,
            initial_balance=1000,
            random_seed=42
        )
    
    def test_simulation_runs(self):
        """Test that simulation completes without errors."""
        results = self.simulator.simulate(num_trades=10, num_simulations=100)
        self.assertEqual(len(results.final_balances), 100)
    
    def test_expected_output_shape(self):
        """Test that outputs have correct shape."""
        results = self.simulator.simulate(num_trades=10, num_simulations=50)
        self.assertEqual(results.final_balances.shape, (50,))
        self.assertEqual(results.trade_outcomes.shape, (50, 10))
    
    def test_statistics_computed(self):
        """Test that statistics are computed."""
        results = self.simulator.simulate(num_trades=50, num_simulations=100)
        self.assertIn('mean_final_balance', results.statistics)
        self.assertIn('worst_drawdown_pct', results.statistics)


class TestMarketModel(unittest.TestCase):
    """Test Market Modeling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.market = MarketModel()
    
    def test_market_conditions(self):
        """Test all market conditions are valid."""
        for condition in MarketCondition:
            params = self.market.get_trading_params(condition)
            self.assertIn('win_rate', params)
            self.assertIn('win_amount', params)
            self.assertIn('loss_amount', params)
    
    def test_bullish_higher_win_rate(self):
        """Test that bullish markets have higher win rates."""
        bullish = self.market.get_trading_params(MarketCondition.BULLISH)
        bearish = self.market.get_trading_params(MarketCondition.BEARISH)
        self.assertGreater(bullish['win_rate'], bearish['win_rate'])
    
    def test_regime_simulation(self):
        """Test market regime simulation."""
        regimes = [
            (MarketCondition.BULLISH, 10),
            (MarketCondition.BEARISH, 10),
        ]
        results = self.market.simulate_market_regime(regimes)
        self.assertEqual(len(results['balances']), 21)  # 1 initial + 20 trades


class TestGeometricBrownianMotion(unittest.TestCase):
    """Test GBM price simulation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.gbm = GeometricBrownianMotion(
            initial_price=100,
            drift=0.1,
            volatility=0.2
        )
    
    def test_simulation_output(self):
        """Test that simulation produces correct output shape."""
        results = self.gbm.simulate(num_steps=50, num_paths=100)
        self.assertEqual(results.prices.shape, (100, 51))  # 100 paths, 51 steps (0-50)
    
    def test_initial_price(self):
        """Test that initial price is preserved."""
        results = self.gbm.simulate(num_steps=50, num_paths=100)
        np.testing.assert_array_almost_equal(results.prices[:, 0], 100)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_kelly_criterion(self):
        """Test Kelly Criterion calculation."""
        kelly_frac = kelly_criterion(win_rate=0.55, win_amount=100, loss_amount=100)
        self.assertTrue(0 < kelly_frac < 1)
    
    def test_kelly_negative_ev(self):
        """Test Kelly Criterion returns 0 for negative EV."""
        kelly_frac = kelly_criterion(win_rate=0.40, win_amount=100, loss_amount=200)
        self.assertEqual(kelly_frac, 0)
    
    def test_profit_factor(self):
        """Test profit factor calculation."""
        trades = np.array([100, 50, -30, 75, -40])
        pf = profit_factor(trades)
        expected_pf = 225 / 70  # wins / losses
        self.assertAlmostEqual(pf, expected_pf)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEVCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestMonteCarloSimulator))
    suite.addTests(loader.loadTestsFromTestCase(TestMarketModel))
    suite.addTests(loader.loadTestsFromTestCase(TestGeometricBrownianMotion))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilityFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
