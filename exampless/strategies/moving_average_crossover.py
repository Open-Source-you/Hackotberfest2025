import pandas as pd

def moving_average_crossover(data, short_window=3, long_window=5):
    df = data.copy()
    if df.empty:
        print("[moving_average_crossover] Warning: input DataFrame is empty")
    df['short_ma'] = df['close'].rolling(short_window).mean()
    df['long_ma'] = df['close'].rolling(long_window).mean()
    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
    return df
