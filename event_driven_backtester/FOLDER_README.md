# Event-Driven Backtesting Engine 📈

**A minimal yet powerful event-driven backtesting framework for running trading strategies against historical OHLCV data.**

Created for Hacktoberfest 2025 - Issue #425

---

## 🎯 What's Inside

A complete backtesting system with:
- ✅ Event-driven architecture
- ✅ Multiple trading strategies (MA Cross, RSI, Buy & Hold)
- ✅ Performance metrics (Sharpe ratio, max drawdown, returns)
- ✅ Sample data generator
- ✅ Visualization tools
- ✅ Comprehensive documentation
- ✅ Unit tests

## 📁 Location

```
event_driven_backtester/
```

## 🚀 Quick Start

```bash
cd event_driven_backtester
pip install -r requirements.txt
python generate_sample_data.py
python run_backtest.py
```

## 📚 Documentation

Full documentation available in the `event_driven_backtester` folder:

- **[QUICKSTART.md](event_driven_backtester/QUICKSTART.md)** - Get started in 5 minutes
- **[README.md](event_driven_backtester/README.md)** - Complete user guide
- **[ARCHITECTURE.md](event_driven_backtester/ARCHITECTURE.md)** - Technical details
- **[DOCUMENTATION_INDEX.md](event_driven_backtester/DOCUMENTATION_INDEX.md)** - Documentation navigator

## 📊 What You Get

```
Processing bar 1461...

============================================================
Backtest Complete!
============================================================
Signals: 8
Orders: 8
Fills: 8
============================================================

Performance Summary:
------------------------------------------------------------
Total Return                           15.23%
Sharpe Ratio                             1.45
Max Drawdown                             8.32%
Drawdown Duration                          45
============================================================
```

## 🎓 Features

- **Event-Driven**: Mimics real-time trading
- **Extensible**: Easy to add custom strategies
- **Realistic**: Models commissions and execution
- **Complete**: Full documentation and examples
- **Tested**: Unit tests included

## 📈 Strategies Included

1. **Buy and Hold** - Baseline strategy
2. **Moving Average Crossover** - Classic trend-following
3. **RSI Strategy** - Momentum-based trading

## 💡 Create Your Own

```python
class MyStrategy(Strategy):
    def calculate_signals(self, event):
        # Your strategy logic here
        pass
```

## 📦 Contents

- Core engine (~1,200 lines)
- Documentation (~2,500 lines)
- Tests & utilities (~500 lines)
- **Total: ~4,200 lines of code**

## 🔧 Requirements

```
pandas>=1.3.0
numpy>=1.20.0
```

Optional: `matplotlib` for visualizations

## 🎯 Use Cases

- Algorithmic trading research
- Strategy development
- Backtesting education
- Performance analysis
- Portfolio optimization

## 📝 License

Part of Hacktoberfest 2025 contributions

## 🆘 Support

Run the verification script:
```bash
python event_driven_backtester/verify_setup.py
```

---

**Ready to start?** → Navigate to `event_driven_backtester/` and read [QUICKSTART.md](event_driven_backtester/QUICKSTART.md)

**Issue #425**: ✅ COMPLETE
