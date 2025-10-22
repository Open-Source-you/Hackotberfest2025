"""
Configuration file for the backtesting engine.
Modify these settings to customize your backtest.
"""

import datetime

# Data Configuration
DATA_DIR = 'data'
SYMBOL_LIST = ['AAPL']  # List of symbols to backtest

# Backtest Configuration
INITIAL_CAPITAL = 100000.0  # Starting capital in USD
START_DATE = datetime.datetime(2020, 1, 1)
HEARTBEAT = 0.0  # Delay between bars (0 for fastest)

# Strategy Configuration
STRATEGY = 'ma_cross'  # Options: 'ma_cross', 'rsi', 'buy_hold'

# Moving Average Crossover Strategy Parameters
MA_SHORT_WINDOW = 50
MA_LONG_WINDOW = 200

# RSI Strategy Parameters
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

# Execution Configuration
ENABLE_SLIPPAGE = False  # Use realistic execution handler with slippage
SLIPPAGE_PCT = 0.0005  # Slippage percentage (0.05%)

# Portfolio Configuration
POSITION_SIZE = 100  # Number of shares per trade

# Output Configuration
SAVE_RESULTS = True
RESULTS_DIR = 'results'
GENERATE_PLOTS = False  # Requires matplotlib

# Advanced Configuration
DEBUG_MODE = False
PRINT_SIGNALS = True
PRINT_ORDERS = True
PRINT_FILLS = True
