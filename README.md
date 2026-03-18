# Crypto EV Simulator

A comprehensive **Expected Value (EV) Simulator** for cryptocurrency trading decisions. Uses Python with NumPy, Pandas, and Matplotlib to compute expected values analytically and simulate trading outcomes using Monte Carlo methods.

## 📋 Project Overview

This simulator bridges **probability theory**, **quantitative finance**, and **programming** to evaluate whether cryptocurrency trades are statistically favorable over time. It provides:

- **Analytical EV Calculations**: Deterministic computation of expected value based on win rates and reward ratios
- **Monte Carlo Simulations**: Generate thousands of randomized trade outcomes to estimate return distributions
- **Market Modeling**: Geometric Brownian Motion for price simulation and market regime analysis
- **Risk Metrics**: Maximum drawdown, Value at Risk (VaR), Expected Shortfall, and more
- **Visualization**: Comprehensive plots for analyzing simulation results and sensitivity

## 🎯 Key Features

### 1. EV Calculation Module (`ev_calculator.py`)
- **TradeParameters**: Data class for defining trade scenarios
- **EVCalculator**: Computes expected value metrics
  - Single trade EV
  - Total EV across multiple trades
  - EV per unit of risk
  - Breakeven win rate
  - Profitability analysis

**Example:**
```python
from ev_calculator import EVCalculator, TradeParameters

# Define a trade: 55% win rate, $100 profit, $80 loss
params = TradeParameters(win_rate=0.55, win_amount=100, loss_amount=80, num_trades=100)
calc = EVCalculator(params)

print(f"Single Trade EV: ${calc.calculate_single_trade_ev():.2f}")
print(f"Is Profitable? {calc.is_profitable()}")  # True if EV > 0
```

### 2. Monte Carlo Simulator (`monte_carlo.py`)
- **MonteCarloSimulator**: Runs simulations of trading outcomes
- **SimulationResults**: Container for results with detailed statistics
  - Final balance distribution
  - Cumulative return paths
  - Drawdown analysis
  - Risk metrics (VaR, Expected Shortfall)

**Example:**
```python
from monte_carlo import MonteCarloSimulator

simulator = MonteCarloSimulator(
    win_rate=0.55, 
    win_amount=100, 
    loss_amount=80,
    initial_balance=1000
)

results = simulator.simulate(num_trades=50, num_simulations=10000)
print(f"Mean Final Balance: ${results.statistics['mean_final_balance']:.2f}")
print(f"Worst Drawdown: {results.statistics['worst_drawdown_pct']:.2f}%")
```

### 3. Market Modeling (`market_model.py`)
- **GeometricBrownianMotion**: Price simulation using GBM stochastic process
- **MarketModel**: Models different market conditions (bullish, bearish, sideways)
- **CorrelationModel**: Handle correlations between multiple assets

**Example:**
```python
from market_model import GeometricBrownianMotion, MarketCondition, MarketModel

# Simulate price paths
gbm = GeometricBrownianMotion(initial_price=100, drift=0.15, volatility=0.40)
prices = gbm.simulate(num_steps=252, num_paths=1000)

# Analyze market regimes
market = MarketModel()
results = market.simulate_market_regime([
    (MarketCondition.BULLISH, 20),
    (MarketCondition.BEARISH, 15),
])
```

### 4. Visualization (`visualization.py`)
- **EVVisualizer**: Creates comprehensive plots
  - Cumulative return paths
  - Final balance distributions
  - Drawdown paths
  - Win rate sensitivity analysis
  - Price path simulations

**Example:**
```python
from visualization import EVVisualizer

visualizer = EVVisualizer()
fig1 = visualizer.plot_simulation_results(results)
fig2 = visualizer.plot_win_rate_analysis(win_rate_results)
visualizer.save_figure(fig1, 'simulation_results.png')
```

## 📂 Project Structure

```
Crypto EV/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── ev_calculator.py           # EV calculation module
│   ├── monte_carlo.py             # Monte Carlo simulator
│   ├── market_model.py            # Market modeling
│   └── visualization.py           # Visualization tools
├── examples/
│   └── basic_example.py           # Comprehensive example script
├── tests/                         # Unit tests (to be added)
├── notebooks/                     # Jupyter notebooks (to be added)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd "Crypto EV"

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Basic Example

```bash
python examples/basic_example.py
```

This runs 6 comprehensive examples:
1. Basic EV calculation
2. Monte Carlo simulation
3. Win rate sensitivity analysis
4. Market regime modeling
5. Price simulation
6. Data visualization

### 3. Use in Your Own Code

```python
import sys
from src.ev_calculator import EVCalculator, TradeParameters
from src.monte_carlo import MonteCarloSimulator

# Calculate EV
params = TradeParameters(win_rate=0.60, win_amount=150, loss_amount=100, num_trades=200)
ev_calc = EVCalculator(params)
print(f"Expected Value: ${ev_calc.calculate_single_trade_ev():.2f}")

# Run simulation
simulator = MonteCarloSimulator(0.60, 150, 100, initial_balance=5000)
results = simulator.simulate(num_trades=200, num_simulations=10000)
print(f"Mean Profit: ${results.statistics['mean_final_balance'] - 5000:.2f}")
```

## 📊 Core Concepts

### Expected Value (EV)
For a single trade:
$$EV = (P_{win} \times R_{win}) - (P_{loss} \times R_{loss})$$

Where:
- $P_{win}$ = Probability of winning
- $R_{win}$ = Profit amount per win
- $P_{loss}$ = Probability of losing (1 - $P_{win}$)
- $R_{loss}$ = Loss amount per loss

### Risk-Reward Ratio
$$R/R = \frac{\text{Potential Loss}}{\text{Potential Profit}}$$

### Breakeven Win Rate
$$P_{breakeven} = \frac{R_{loss}}{R_{win} + R_{loss}}$$

### Return on Risk
$$\text{RoR} = \frac{EV}{R_{loss}} \times 100\%$$

## 📈 Key Metrics

| Metric | Definition |
|--------|-----------|
| **Expected Value** | Average profit per trade |
| **Win Rate** | Probability of profitable trade |
| **Risk-Reward Ratio** | Loss amount / Profit amount |
| **Maximum Drawdown** | Largest peak-to-trough decline |
| **Value at Risk (VaR)** | Loss at given confidence level |
| **Sharpe Ratio** | Return per unit of risk (future) |
| **Winning Simulations %** | Percentage of runs that end in profit |

## 🔬 Advanced Usage

### Portfolio Simulation

```python
# Model multiple asset correlations
from market_model import CorrelationModel

correlation_matrix = np.array([
    [1.0, 0.5, 0.3],
    [0.5, 1.0, 0.4],
    [0.3, 0.4, 1.0],
])

correlation_model = CorrelationModel(3, correlation_matrix)
returns = correlation_model.generate_correlated_returns(100, [0.1, 0.12, 0.08], [0.2, 0.25, 0.15])
```

### Win Rate Sensitivity

```python
# Analyze how different win rates affect outcomes
simulator = MonteCarloSimulator(0.50, 100, 80)
win_rates = np.arange(0.30, 0.71, 0.05)
results = simulator.win_rate_analysis(num_trades=50, win_rates=list(win_rates))

for wr, stats in results.items():
    print(f"Win Rate {wr:.0%}: Mean Return {stats['mean_return_pct']:.2f}%")
```

### Market Regime Analysis

```python
# Simulate different market conditions
market = MarketModel()
regimes = [
    (MarketCondition.BULLISH, 30),
    (MarketCondition.SIDEWAYS, 20),
    (MarketCondition.BEARISH, 30),
]
results = market.simulate_market_regime(regimes)
```

## 🎓 Learning Resources

The simulator is designed to teach and explore:
- **Probability theory**: Win rates, expected values, distributions
- **Risk management**: Drawdowns, value at risk, position sizing
- **Stochastic processes**: Geometric Brownian Motion, Monte Carlo methods
- **Quantitative analysis**: Statistical metrics and backtesting
- **Python programming**: Data structures, numerical computation, visualization

## 🚧 Future Extensions

Planned enhancements:

- [ ] Real-time cryptocurrency market data integration (API connections)
- [ ] Portfolio-level simulations (multiple correlated strategies)
- [ ] Advanced risk metrics (Sharpe ratio, Sortino ratio, Calmar ratio)
- [ ] Machine learning-based win rate prediction
- [ ] Rule-based trading decision agent
- [ ] Interactive web dashboard (Streamlit)
- [ ] Unit tests and continuous integration
- [ ] Jupyter notebook examples
- [ ] Optimization algorithms for position sizing
- [ ] Backtesting framework for historical data

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional risk metrics
- Real market data integration
- Performance optimization
- Extended test coverage
- Documentation improvements

## ⚠️ Disclaimer

This simulator is for **educational and research purposes only**. Past performance does not guarantee future results. Always conduct thorough due diligence and risk management before engaging in cryptocurrency trading. Cryptocurrency trading carries substantial risk of loss.

## 📧 Questions?

For questions, issues, or suggestions:
1. Review the example files in `examples/`
2. Check the docstrings in source modules
3. Refer to the project documentation

---

**Happy Analyzing! 📊📈**
