from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .ev import expected_value_over_series, expected_value_per_trade
from .metrics import sharpe_ratio
from .models import TradeParameters
from .simulation import monte_carlo_simulation



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crypto Expected Value simulator")
    parser.add_argument("--win-rate", type=float, required=True, help="Probability of a winning trade, from 0 to 1")
    parser.add_argument("--profit", type=float, required=True, help="Profit on a winning trade")
    parser.add_argument("--loss", type=float, required=True, help="Loss on an unsuccessful trade")
    parser.add_argument("--trades", type=int, default=100, help="Trades per simulated run")
    parser.add_argument("--iterations", type=int, default=10000, help="Number of Monte Carlo runs")
    parser.add_argument("--initial-capital", type=float, default=0.0, help="Starting capital for each run")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for deterministic simulation")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    return parser



def main() -> None:
    args = build_parser().parse_args()
    params = TradeParameters(
        win_rate=args.win_rate,
        profit_per_win=args.profit,
        loss_per_trade=args.loss,
        trades_per_run=args.trades,
        iterations=args.iterations,
        initial_capital=args.initial_capital,
    )
    result = monte_carlo_simulation(params, seed=args.seed)

    payload = {
        "parameters": asdict(params),
        "expected_value_per_trade": expected_value_per_trade(params),
        "expected_value_over_series": expected_value_over_series(params),
        "monte_carlo": {
            "average_return": result.average_return,
            "return_std_dev": result.return_std_dev,
            "best_run": result.best_run,
            "worst_run": result.worst_run,
            "risk_of_loss": result.risk_of_loss,
            "sharpe_ratio": sharpe_ratio(result.run_returns),
        },
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    print("Crypto EV Simulation")
    print("====================")
    print(f"Expected value per trade: {payload['expected_value_per_trade']:.4f}")
    print(f"Expected value over {params.trades_per_run} trades: {payload['expected_value_over_series']:.4f}")
    print(f"Average simulated return: {result.average_return:.4f}")
    print(f"Simulated standard deviation: {result.return_std_dev:.4f}")
    print(f"Best run: {result.best_run:.4f}")
    print(f"Worst run: {result.worst_run:.4f}")
    print(f"Risk of loss: {result.risk_of_loss:.2%}")
    print(f"Sharpe ratio (run-level): {payload['monte_carlo']['sharpe_ratio']:.4f}")


if __name__ == "__main__":
    main()
