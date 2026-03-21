<<<<<<< ours
=======
# Crypto Expected Value (EV) Simulator

A Python project for evaluating whether a cryptocurrency trade setup is statistically favorable. The simulator combines analytical expected value calculations with Monte Carlo experimentation so you can compare theoretical edge with observed distributions of outcomes.

## Features

- Analytical expected value per trade and across a sequence of trades.
- Monte Carlo simulation for repeated trade runs under uncertainty.
- Basic risk metrics including run-level volatility, risk of loss, Sharpe ratio, and equity curve helpers.
- Command-line interface for quick scenario analysis.
- Modular package layout that can be extended with API integrations, richer market models, and portfolio logic.

## Project structure

- `crypto_ev/models.py`: dataclasses for strategy inputs and aggregated simulation output.
- `crypto_ev/ev.py`: deterministic expected value formulas.
- `crypto_ev/market.py`: minimal stochastic market model for trade outcome sampling.
- `crypto_ev/simulation.py`: Monte Carlo engine.
- `crypto_ev/metrics.py`: performance and drawdown utilities.
- `crypto_ev/cli.py`: command-line interface.
- `tests/test_crypto_ev.py`: regression tests for calculations and CLI behavior.

## Expected value model

For a trade with:

- win probability `p`
- profit on success `W`
- loss on failure `L`

The expected value is:

`EV = p * W - (1 - p) * L`

This value can be scaled by the number of trades in a run to estimate long-run expectation before simulation.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
crypto-ev --win-rate 0.55 --profit 120 --loss 80 --trades 100 --iterations 5000 --seed 42
```

## Example output

```text
Crypto EV Simulation
====================
Expected value per trade: 30.0000
Expected value over 100 trades: 3000.0000
Average simulated return: 2979.8400
Simulated standard deviation: 993.6084
Best run: 6400.0000
Worst run: -400.0000
Risk of loss: 0.06%
Sharpe ratio (run-level): 2.9990
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s tests -v
```

## Next extensions

- Integrate live market data from exchange APIs.
- Add position sizing, fees, slippage, and portfolio-level EV analysis.
- Support richer return distributions beyond binary win/loss outcomes.
- Plot histograms and equity curves with NumPy/Pandas/Matplotlib-based workflows.
>>>>>>> theirs
