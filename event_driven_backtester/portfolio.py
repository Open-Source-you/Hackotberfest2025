"""
Portfolio class for managing positions and tracking performance.
"""

from abc import ABCMeta, abstractmethod
import datetime
import numpy as np
import pandas as pd
from .events import FillEvent, OrderEvent


class Portfolio(metaclass=ABCMeta):
    """
    The Portfolio class handles the positions and market
    value of all instruments at a resolution of a "bar",
    i.e., secondly, minutely, 5-min, 30-min, 60 min or EOD.
    """

    @abstractmethod
    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the portfolio logic.
        """
        raise NotImplementedError("Should implement update_signal()")

    @abstractmethod
    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings
        from a FillEvent.
        """
        raise NotImplementedError("Should implement update_fill()")


class NaivePortfolio(Portfolio):
    """
    The NaivePortfolio object is designed to send orders to
    a brokerage object with a constant quantity size blindly,
    i.e., without any risk management or position sizing.
    It is used to test simpler strategies.
    """

    def __init__(self, bars, events, start_date, initial_capital=100000.0):
        """
        Initialize the portfolio with starting cash.
        
        Parameters:
        -----------
        bars : DataHandler
            The DataHandler object with current market data
        events : Queue
            The Event Queue object
        start_date : datetime
            The start date of the portfolio
        initial_capital : float
            The starting capital in USD
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self._construct_all_positions()
        self.current_positions = {s: 0 for s in self.symbol_list}

        self.all_holdings = self._construct_all_holdings()
        self.current_holdings = self._construct_current_holdings()

    def _construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = {s: 0 for s in self.symbol_list}
        d['datetime'] = self.start_date
        return [d]

    def _construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = {s: 0.0 for s in self.symbol_list}
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return [d]

    def _construct_current_holdings(self):
        """
        Constructs the dictionary which will hold the instantaneous
        value of the portfolio across all symbols.
        """
        d = {s: 0.0 for s in self.symbol_list}
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d

    def update_timeindex(self, event):
        """
        Adds a new record to the positions matrix for the current
        market data bar. This reflects the PREVIOUS bar, i.e., all
        current market data at this stage is known (OHLCV).
        
        Makes use of a MarketEvent from the events queue.
        """
        latest_datetime = self.bars.get_latest_bar_datetime(
            self.symbol_list[0]
        )

        # Update positions
        dp = {s: self.current_positions[s] for s in self.symbol_list}
        dp['datetime'] = latest_datetime
        self.all_positions.append(dp)

        # Update holdings
        dh = {s: 0.0 for s in self.symbol_list}
        dh['datetime'] = latest_datetime
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for s in self.symbol_list:
            # Approximation to the real value
            market_value = self.current_positions[s] * \
                          self.bars.get_latest_bar_value(s, "close")
            dh[s] = market_value
            dh['total'] += market_value

        self.all_holdings.append(dh)

    def update_positions_from_fill(self, fill):
        """
        Takes a Fill object and updates the position matrix to
        reflect the new position.
        
        Parameters:
        -----------
        fill : FillEvent
            The FillEvent object to update the positions with
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update positions list with new quantities
        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_holdings_from_fill(self, fill):
        """
        Takes a Fill object and updates the holdings matrix to
        reflect the holdings value.
        
        Parameters:
        -----------
        fill : FillEvent
            The FillEvent object to update the holdings with
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update holdings list with new quantities
        fill_cost = self.bars.get_latest_bar_value(
            fill.symbol, "close"
        )
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)

    def update_fill(self, event):
        """
        Updates the portfolio current positions and holdings
        from a FillEvent.
        """
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)

    def generate_naive_order(self, signal):
        """
        Simply files an Order object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.
        
        Parameters:
        -----------
        signal : SignalEvent
            The SignalEvent signal information
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        mkt_quantity = 100  # Fixed quantity for simplicity
        cur_quantity = self.current_positions[symbol]
        order_type = 'MKT'

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, 'BUY')
        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), 'SELL')

        return order

    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the portfolio logic.
        """
        if event.type == 'SIGNAL':
            order_event = self.generate_naive_order(event)
            if order_event is not None:
                self.events.put(order_event)

    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        return curve

    def output_summary_stats(self):
        """
        Creates a list of summary statistics for the portfolio.
        """
        equity_curve = self.create_equity_curve_dataframe()
        
        total_return = equity_curve['equity_curve'][-1]
        returns = equity_curve['returns']
        pnl = equity_curve['equity_curve']
        
        sharpe_ratio = self._calculate_sharpe_ratio(returns)
        max_dd, dd_duration = self._calculate_max_drawdown(pnl)
        
        stats = [
            ("Total Return", f"{(total_return - 1.0) * 100.0:.2f}%"),
            ("Sharpe Ratio", f"{sharpe_ratio:.2f}"),
            ("Max Drawdown", f"{max_dd * 100.0:.2f}%"),
            ("Drawdown Duration", f"{dd_duration}")
        ]
        
        return stats

    def _calculate_sharpe_ratio(self, returns, periods=252):
        """
        Calculate the Sharpe Ratio for a strategy.
        
        Parameters:
        -----------
        returns : pd.Series
            A pandas Series representing period percentage returns
        periods : int
            Daily (252), Hourly (252*6.5), Minutely (252*6.5*60)
        """
        return np.sqrt(periods) * (returns.mean() / returns.std())

    def _calculate_max_drawdown(self, pnl):
        """
        Calculate the maximum peak-to-trough drawdown of the PnL curve.
        
        Parameters:
        -----------
        pnl : pd.Series
            A pandas Series representing the equity curve
            
        Returns:
        --------
        max_dd : float
            Maximum drawdown
        duration : int
            Duration of the drawdown
        """
        # Calculate the cumulative returns
        hwm = [0]
        idx = pnl.index
        drawdown = pd.Series(index=idx)
        duration = pd.Series(index=idx)
        
        # Loop over the index range
        for t in range(1, len(idx)):
            hwm.append(max(hwm[t-1], pnl.iloc[t]))
            drawdown.iloc[t] = (hwm[t] - pnl.iloc[t]) / hwm[t]
            duration.iloc[t] = 0 if drawdown.iloc[t] == 0 else duration.iloc[t-1] + 1
            
        return drawdown.max(), duration.max()
