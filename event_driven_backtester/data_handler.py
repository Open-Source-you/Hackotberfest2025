"""
Data handler for loading and managing historical OHLCV data.
"""

import os
import pandas as pd
from abc import ABCMeta, abstractmethod
from .events import MarketEvent


class DataHandler(metaclass=ABCMeta):
    """
    Abstract base class for handling market data.
    """

    @abstractmethod
    def get_latest_bar(self, symbol):
        """
        Returns the last bar from the latest_symbol list.
        """
        raise NotImplementedError("Should implement get_latest_bar()")

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        raise NotImplementedError("Should implement get_latest_bar_datetime()")

    @abstractmethod
    def get_latest_bar_value(self, symbol, val_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        raise NotImplementedError("Should implement get_latest_bar_value()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")


class HistoricalCSVDataHandler(DataHandler):
    """
    Reads CSV files from the local filesystem and provides an interface
    to obtain the "latest" bar in a manner identical to a live trading interface.
    """

    def __init__(self, events, csv_dir, symbol_list):
        """
        Initialize the data handler.
        
        Parameters:
        -----------
        events : Queue
            The Event Queue
        csv_dir : str
            Absolute directory path to the CSV files
        symbol_list : list
            A list of symbol strings
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self.bar_index = 0

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        
        CSV format expected:
        timestamp,open,high,low,close,volume
        """
        comb_index = None
        for s in self.symbol_list:
            # Load the CSV file with no header information, indexed on timestamp
            self.symbol_data[s] = pd.read_csv(
                os.path.join(self.csv_dir, f'{s}.csv'),
                header=0,
                index_col=0,
                parse_dates=True,
                names=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            ).sort_index()

            # Combine the index to pad forward values
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index = comb_index.union(self.symbol_data[s].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[s] = []

        # Reindex the dataframes
        for s in self.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(
                index=comb_index, method='pad'
            ).iterrows()

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple of
        (datetime, open, high, low, close, volume).
        """
        for b in self.symbol_data[symbol]:
            yield b

    def get_latest_bar(self, symbol):
        """
        Returns the last bar from the latest_symbol list.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print(f"That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print(f"That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print(f"That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol, val_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print(f"That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], val_type)

    def get_latest_bars_values(self, symbol, val_type, N=1):
        """
        Returns the last N bar values from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)
        except KeyError:
            print(f"That symbol is not available in the historical data set.")
            raise
        else:
            return [getattr(b[1], val_type) for b in bars_list]

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for s in self.symbol_list:
            try:
                bar = next(self._get_new_bar(s))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        
        self.bar_index += 1
