# strategy.py

import pandas as pd

from events import SignalEvent


class MovingAverageCrossStrategy:
    def __init__(self, data_handler, short_window=40, long_window=100):
        self.data_handler = data_handler
        self.short_window = short_window
        self.long_window = long_window
        self.bought = False

    def calculate_signals(self, event):
        if event.type == "MARKET":
            data = self.data_handler.get_latest_bars("AAPL", N=self.long_window)
            df = pd.DataFrame(data, columns=["datetime", "close"])
            short_ma = df["close"].rolling(window=self.short_window).mean().iloc[-1]
            long_ma = df["close"].rolling(window=self.long_window).mean().iloc[-1]

            if short_ma > long_ma and not self.bought:
                return SignalEvent("AAPL", df["datetime"].iloc[-1], "BUY", 1.0)
            elif short_ma < long_ma and self.bought:
                return SignalEvent("AAPL", df["datetime"].iloc[-1], "SELL", 1.0)
