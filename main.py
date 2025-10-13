"""
Main entry point to quickly test example strategies.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from examples.strategies.moving_average_crossover import moving_average_crossover
from examples.strategies.rsi_strategy import rsi_strategy
from examples.strategies.mean_reversion import mean_reversion

# Simple logging helpers
def _reset_debug_log():
    with open('debug_output.txt', 'w', encoding='utf-8') as f:
        f.write('')

def _log(text):
    print(text, flush=True)
    with open('debug_output.txt', 'a', encoding='utf-8') as f:
        f.write(str(text) + '\n')

# Reset log at start
_reset_debug_log()

# -------------------------
# Generate mock price data (random walk)
# -------------------------
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100)
prices = pd.Series(100 + np.random.normal(0, 1, 100).cumsum(), index=dates)
data = pd.DataFrame({'close': prices})
_log("=== Input Data (summary) ===")
_log(f"shape: {data.shape}")
_log("dtypes:\n" + str(data.dtypes))
_log("head(5):\n" + data.head().to_string())
data.head().to_csv('input_head.csv')

# -------------------------
# Run Moving Average Crossover
# -------------------------
ma_result = moving_average_crossover(data, short_window=3, long_window=5)
_log("=== Moving Average Crossover ===")
_log("-- Before dropna() --")
_log(f"shape: {ma_result.shape}")
_log("NaNs per column: " + str(ma_result.isna().sum().to_dict()))
_log(ma_result.head(15).to_string())
_log(ma_result.dropna().head(15).to_string())
ma_result.head(15).to_csv('ma_head.csv')

# Plot
plt.figure(figsize=(12, 4))
plt.plot(ma_result.index, ma_result['close'], label='Price')
plt.plot(ma_result.index, ma_result['short_ma'], label='Short MA')
plt.plot(ma_result.index, ma_result['long_ma'], label='Long MA')
plt.title('Moving Average Crossover Strategy')
plt.legend()
plt.tight_layout()
plt.savefig('plot_ma.png')
print("Saved Moving Average plot to: plot_ma.png", flush=True)
plt.close()

# -------------------------
# Run RSI Strategy
# -------------------------
rsi_result = rsi_strategy(data, period=3, low_threshold=40, high_threshold=60)
_log("\n=== RSI Strategy ===")
_log("-- Before dropna() --")
_log(f"shape: {rsi_result.shape}")
_log("NaNs per column: " + str(rsi_result.isna().sum().to_dict()))
_log(rsi_result.head(15).to_string())
_log(rsi_result.dropna().head(15).to_string())
rsi_result.head(15).to_csv('rsi_head.csv')

# Plot
fig, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(rsi_result.index, rsi_result['close'], label='Price', color='blue')
ax2 = ax1.twinx()
ax2.plot(rsi_result.index, rsi_result['rsi'], label='RSI', color='orange')
ax1.set_title('RSI Strategy')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig('plot_rsi.png')
print("Saved RSI plot to: plot_rsi.png", flush=True)
plt.close()

# -------------------------
# Run Mean Reversion
# -------------------------
mr_result = mean_reversion(data, window=3, threshold=0.5)
_log("\n=== Mean Reversion ===")
_log("-- Before dropna() --")
_log(f"shape: {mr_result.shape}")
_log("NaNs per column: " + str(mr_result.isna().sum().to_dict()))
_log(mr_result.head(15).to_string())
_log(mr_result.dropna().head(15).to_string())
mr_result.head(15).to_csv('mr_head.csv')

# Plot
plt.figure(figsize=(12, 4))
plt.plot(mr_result.index, mr_result['close'], label='Price')
plt.plot(mr_result.index, mr_result['rolling_mean'], label='Rolling Mean')
plt.title('Mean Reversion Strategy')
plt.legend()
plt.tight_layout()
plt.savefig('plot_mr.png')
print("Saved Mean Reversion plot to: plot_mr.png", flush=True)
plt.close()
