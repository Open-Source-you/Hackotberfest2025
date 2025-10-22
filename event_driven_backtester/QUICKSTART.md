# Quick Start Guide

Get up and running with the Event-Driven Backtesting Engine in 5 minutes!

## Prerequisites

```bash
# Python 3.7 or higher
python --version

# Install required packages
pip install pandas numpy

# Optional: For visualization
pip install matplotlib
```

## Step 1: Navigate to the Directory

```bash
cd event_driven_backtester
```

## Step 2: Generate Sample Data

```bash
python generate_sample_data.py
```

**Expected Output:**
```
Generating data for AAPL...
Saved 1461 rows to data/AAPL.csv
Generating data for MSFT...
Saved 1461 rows to data/MSFT.csv
Generating data for GOOG...
Saved 1461 rows to data/GOOG.csv

Sample data generation complete!
```

## Step 3: Run Your First Backtest

```bash
python run_backtest.py
```

This will run backtests for all three included strategies:
- Buy and Hold
- Moving Average Crossover
- RSI

**Expected Output:**
```
============================================================
Event-Driven Backtesting Engine
============================================================

============================================================
Testing Strategy: BUY HOLD
============================================================

============================================================
Running Backtest with buy_hold strategy
============================================================
Symbol List: ['AAPL']
Initial Capital: $100,000.00
Start Date: 2020-01-01
Data Directory: ./data
============================================================
Creating DataHandler, Strategy, Portfolio and ExecutionHandler
Processing bar 1461...

============================================================
Backtest Complete!
============================================================
Signals: 1
Orders: 1
Fills: 1
============================================================

Performance Summary:
------------------------------------------------------------
Total Return                           12.45%
Sharpe Ratio                             1.23
Max Drawdown                             5.67%
Drawdown Duration                          32
============================================================

Results saved to: backtest_results_buy_hold.csv
```

## Step 4: Run a Specific Strategy

Create a simple Python script:

```python
# my_backtest.py
from run_backtest import run_backtest

# Run Moving Average Crossover strategy
results = run_backtest('ma_cross')

# Print first few rows
print(results.head())
```

Run it:
```bash
python my_backtest.py
```

## Step 5: Customize Your Strategy

Edit `config.py` to customize parameters:

```python
# config.py

# Choose your strategy
STRATEGY = 'ma_cross'  # or 'rsi', 'buy_hold'

# Moving Average parameters
MA_SHORT_WINDOW = 20   # Faster signals
MA_LONG_WINDOW = 100   # Changed from 200

# Test with different symbols
SYMBOL_LIST = ['MSFT']  # Changed from AAPL

# Adjust capital
INITIAL_CAPITAL = 50000.0  # Changed from 100000
```

Then run your custom backtest:

```python
# custom_backtest.py
import config
from run_backtest import run_backtest

results = run_backtest(config.STRATEGY)
```

## Step 6: Visualize Results (Optional)

If you have matplotlib installed:

```bash
python visualize_results.py
```

This creates plots in the `reports/` directory.

## Step 7: Create Your Own Strategy

1. Open `strategy.py`
2. Add your custom strategy class:

```python
class MyStrategy(Strategy):
    def __init__(self, bars, events, my_param=10):
        self.bars = bars
        self.events = events
        self.symbol_list = bars.symbol_list
        self.my_param = my_param
        
    def calculate_signals(self, event):
        if event.type == 'MARKET':
            for symbol in self.symbol_list:
                # Your strategy logic here
                bars = self.bars.get_latest_bars(symbol, N=20)
                
                # Example: Simple price momentum
                if len(bars) >= 2:
                    current_price = bars[-1][1].close
                    prev_price = bars[-2][1].close
                    
                    if current_price > prev_price * 1.01:  # 1% gain
                        signal = SignalEvent(
                            symbol, 
                            bars[-1][0], 
                            'LONG', 
                            1.0
                        )
                        self.events.put(signal)
```

3. Test your strategy:

```python
# test_my_strategy.py
import datetime
from backtest import Backtest
from data_handler import HistoricalCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import NaivePortfolio
from strategy import MyStrategy

backtest = Backtest(
    csv_dir='data',
    symbol_list=['AAPL'],
    initial_capital=100000.0,
    heartbeat=0.0,
    start_date=datetime.datetime(2020, 1, 1),
    data_handler_cls=HistoricalCSVDataHandler,
    execution_handler_cls=SimulatedExecutionHandler,
    portfolio_cls=NaivePortfolio,
    strategy_cls=MyStrategy,
    my_param=15  # Custom parameter
)

results = backtest.simulate_trading()
```

## Common Commands

```bash
# Generate sample data
python generate_sample_data.py

# Run all strategies
python run_backtest.py

# Run tests
python test_backtest.py

# Create visualizations
python visualize_results.py

# View help
python run_backtest.py --help
```

## Troubleshooting

### "No module named 'pandas'"
```bash
pip install pandas numpy
```

### "Sample data not found"
```bash
python generate_sample_data.py
```

### "Permission denied" on Windows
Run PowerShell as Administrator or use:
```bash
python -m pip install --user pandas numpy
```

### Import errors
Make sure you're in the `event_driven_backtester` directory:
```bash
cd event_driven_backtester
python run_backtest.py
```

## Next Steps

1. **Read the full documentation**: Check `README.md`
2. **Understand the architecture**: Read `ARCHITECTURE.md`
3. **Experiment with parameters**: Edit `config.py`
4. **Try different symbols**: Modify `SYMBOL_LIST`
5. **Create custom strategies**: Add to `strategy.py`
6. **Optimize parameters**: Test different values
7. **Add risk management**: Enhance `portfolio.py`

## Getting Help

- Check the `README.md` for detailed documentation
- Read `ARCHITECTURE.md` for system design
- Review example strategies in `strategy.py`
- Run tests with `python test_backtest.py`

## Tips for Success

✅ **Do:**
- Start with simple strategies
- Test on multiple time periods
- Compare against buy-and-hold baseline
- Account for transaction costs
- Use realistic assumptions

❌ **Don't:**
- Over-optimize on historical data
- Ignore transaction costs
- Use future information
- Test only on bull markets
- Risk too much per trade

Happy Backtesting! 🚀📈
