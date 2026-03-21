import json
import subprocess
import sys
import unittest

from crypto_ev.ev import expected_value_over_series, expected_value_per_trade
from crypto_ev.metrics import equity_curve, max_drawdown, sharpe_ratio
from crypto_ev.models import TradeParameters
from crypto_ev.simulation import monte_carlo_simulation


class EVTests(unittest.TestCase):
    def test_expected_value_calculation(self):
        params = TradeParameters(win_rate=0.55, profit_per_win=120, loss_per_trade=80, trades_per_run=10, iterations=100)
        self.assertAlmostEqual(expected_value_per_trade(params), 30.0)
        self.assertAlmostEqual(expected_value_over_series(params), 300.0)

    def test_simulation_is_repeatable_with_seed(self):
        params = TradeParameters(win_rate=0.5, profit_per_win=100, loss_per_trade=100, trades_per_run=5, iterations=50)
        first = monte_carlo_simulation(params, seed=7)
        second = monte_carlo_simulation(params, seed=7)
        self.assertEqual(list(first.run_returns), list(second.run_returns))
        self.assertEqual(first.risk_of_loss, second.risk_of_loss)

    def test_metrics(self):
        curve = equity_curve(1000, [100, -50, -25, 200])
        self.assertEqual(curve, [1000, 1100, 1050, 1025, 1225])
        self.assertAlmostEqual(max_drawdown(curve), (1100 - 1025) / 1100)
        self.assertGreater(sharpe_ratio([0.1, 0.2, 0.15, 0.05]), 0)

    def test_cli_json_output(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "crypto_ev.cli",
                "--win-rate",
                "0.55",
                "--profit",
                "120",
                "--loss",
                "80",
                "--trades",
                "10",
                "--iterations",
                "100",
                "--seed",
                "42",
                "--json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertIn("expected_value_per_trade", payload)
        self.assertIn("monte_carlo", payload)


if __name__ == "__main__":
    unittest.main()
