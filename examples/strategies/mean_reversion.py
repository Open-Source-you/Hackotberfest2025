import pandas as pd

def mean_reversion(data, window=3, threshold=0.5):
    df = data.copy()
    if df.empty:
        print("[mean_reversion] Warning: input DataFrame is empty")
    df['rolling_mean'] = df['close'].rolling(window).mean()
    df['rolling_std'] = df['close'].rolling(window).std()
    df['zscore'] = (df['close'] - df['rolling_mean']) / df['rolling_std']
    df['signal'] = 0
    df.loc[df['zscore'] > threshold, 'signal'] = -1  # Sell
    df.loc[df['zscore'] < -threshold, 'signal'] = 1  # Buy
    return df
