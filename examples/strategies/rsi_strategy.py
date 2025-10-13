import pandas as pd

def compute_rsi(data, period=3):
    df = data.copy()
    if df.empty:
        print("[compute_rsi] Warning: input DataFrame is empty")
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

def rsi_strategy(data, low_threshold=40, high_threshold=60, period=3):
    df = compute_rsi(data.copy(), period)
    if df.empty:
        print("[rsi_strategy] Warning: intermediate DataFrame is empty")
    df['signal'] = 0
    df.loc[df['rsi'] < low_threshold, 'signal'] = 1
    df.loc[df['rsi'] > high_threshold, 'signal'] = -1
    return df
