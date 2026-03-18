# Crypto EV Simulator - Quick Start Guide

Get started with the Crypto EV Simulator in 5 minutes.

## Installation

```bash
# Navigate to project directory
cd "Crypto EV"

# Install dependencies
pip install -r requirements.txt
```

## Run Examples

### Basic Example (5-10 minutes)

```bash
python examples/basic_example.py
```

This runs 6 examples covering:
1. Simple EV calculation
2. Monte Carlo simulation
3. Win rate sensitivity
4. Market regimes
5. Price simulation
6. Visualization

### Advanced Example (10-15 minutes)

```bash
python examples/advanced_example.py
```

This runs advanced analyses:
1. Multi-strategy comparison
2. Portfolio optimization
3. Risk analysis
4. Market stress testing
5. Correlation impact

### Run Unit Tests

```bash
python tests/test_simulator.py
```

## Common Use Cases

### 1. Calculate EV for a Trade

```python
from src.ev_calculator import EVCalculator, TradeParameters

# Your trade: 60% win rate, $100 profit, $80 loss
params = TradeParameters(
    win_rate=0.60,
    win_amount=100,
    loss_amount=80,
    num_trades=100
)

calc = EVCalculator(params)
print(f"EV per trade: ${calc.calculate_single_trade_ev():.2f}")
print(f"Total EV (100 trades): ${calc.calculate_total_ev():.2f}")
print(f"Profitable? {calc.is_profitable()}")
```

### 2. Run Monte Carlo Simulation

```python
from src.monte_carlo import MonteCarloSimulator

simulator = MonteCarloSimulator(
    win_rate=0.60,
    win_amount=100,
    loss_amount=80,
    initial_balance=10000
)

results = simulator.simulate(num_trades=50, num_simulations=10000)

print(f"Average Final Balance: ${results.statistics['mean_final_balance']:.2f}")
print(f"Worst Case: ${results.statistics['min_final_balance']:.2f}")
print(f"Best Case: ${results.statistics['max_final_balance']:.2f}")
print(f"Worst Drawdown: {results.statistics['worst_drawdown_pct']:.2f}%")
```

### 3. Analyze Win Rate Sensitivity

```python
from src.monte_carlo import MonteCarloSimulator
import numpy as np

simulator = MonteCarloSimulator(0.5, 100, 80, initial_balance=10000)

win_rates = np.arange(0.30, 0.71, 0.05)
results = simulator.win_rate_analysis(50, list(win_rates), 5000)

for wr, stats in results.items():
    print(f"{wr:.0%}: Mean Return {stats['mean_return_pct']:.2f}%")
```

### 4. Visualize Results

```python
from src.visualization import EVVisualizer

visualizer = EVVisualizer()
fig = visualizer.plot_simulation_results(results)
visualizer.save_figure(fig, 'results.png')
visualizer.show()
```

### 5. Use Kelly Criterion for Position Sizing

```python
from src.utilities import kelly_criterion

kelly_fraction = kelly_criterion(
    win_rate=0.60,
    win_amount=100,
    loss_amount=80
)

print(f"Optimal Risk: {kelly_fraction:.2%} of account")
```

## Key Metrics Reference

| Metric | Meaning | Formula |
|--------|---------|---------|
| **EV** | Expected profit/loss | (WR × Win) - (LR × Loss) |
| **Profit Factor** | Total wins / Total losses | PF > 1.5 is good |
| **Win Rate** | % of profitable trades | Wins / Total Trades |
| **Max Drawdown** | Largest peak-to-trough decline | Important for risk |
| **Sharpe Ratio** | Return per unit of risk | Return / Volatility |
| **Kelly Criterion** | Optimal position size | (WR × odds - LR) / odds |

## Trading Strategy Evaluation

### Is a Trade Worth Taking?

```
1. Calculate EV > 0? 
   If NO → Don't take it
   If YES → Check #2
   
2. Is EV/Risk positive?
   (EV per Risk Unit > 0?)
   If NO → Reconsider
   If YES → Check #3
   
3. Run Monte Carlo simulation
   Is probability of profit acceptable?
   (Usually want > 55%)
   If YES → Check #4
   
4. Is max drawdown acceptable?
   (Usually want < 20-30%)
   If YES → Trade is eligible
```

## Common Mistakes to Avoid

1. **Forgetting transaction costs** - Add to loss amount
2. **Overestimating win rate** - Backtest thoroughly first
3. **Ignoring correlation** - Markets move together
4. **Risking too much** - Use Kelly Criterion or fractional Kelly
5. **Not accounting for slippage** - Assume worse prices

## Tips for Best Results

- ✅ Use historical data to estimate realistic win rates
- ✅ Test across different market conditions
- ✅ Always account for fees and slippage
- ✅ Compare multiple strategies
- ✅ Use Kelly Criterion for position sizing
- ✅ Monitor for regime changes
- ✅ Never risk more than 2% per trade

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Explore [examples/](examples/) directory
3. Check [src/](src/) for module documentation
4. Run [tests/test_simulator.py](tests/test_simulator.py) to verify setup

## Troubleshooting

**Q: Import errors?**
A: Make sure you're importing with correct path:
```python
import sys
sys.path.insert(0, 'src')
from ev_calculator import EVCalculator
```

**Q: Plots not showing?**
A: Add `visualizer.show()` at end of script or use Jupyter notebooks

**Q: Wrong results?**
A: Check that:
- Win rate is between 0 and 1
- Amounts are positive
- Random seed is consistent (if reproducibility needed)

## Project Structure

```
src/               → Core modules
├── ev_calculator.py
├── monte_carlo.py
├── market_model.py
├── visualization.py
└── utilities.py

examples/          → Example scripts
├── basic_example.py
└── advanced_example.py

tests/             → Unit tests
└── test_simulator.py

notebooks/         → Jupyter notebooks (future)
```

## Performance Tips

- Use `num_simulations=1000` for quick testing
- Use `num_simulations=10000+` for accurate results
- For large portfolios, may need more simulations
- Most operations complete in seconds

## Support

For issues or questions:
1. Check docstrings: `help(EVCalculator)`
2. Review example files
3. Check test file for usage patterns
4. Refer to README.md for full documentation

---

**Happy Analyzing! 📊📈**
