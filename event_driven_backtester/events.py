"""
Event classes for the event-driven backtesting engine.
"""


class Event:
    """Base class for all events in the system."""
    pass


class MarketEvent(Event):
    """
    Handles the event of receiving new market data update.
    """
    def __init__(self):
        self.type = 'MARKET'

    def __repr__(self):
        return f"MarketEvent()"


class SignalEvent(Event):
    """
    Handles the event of sending a signal from a Strategy object.
    This signal is received by a Portfolio object and acted upon.
    """
    def __init__(self, symbol, datetime, signal_type, strength):
        """
        Initialize SignalEvent.
        
        Parameters:
        -----------
        symbol : str
            The ticker symbol, e.g., 'AAPL'
        datetime : datetime
            The timestamp when the signal was generated
        signal_type : str
            'LONG' or 'SHORT'
        strength : float
            Signal strength/confidence (0.0 to 1.0)
        """
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength

    def __repr__(self):
        return f"SignalEvent(symbol={self.symbol}, datetime={self.datetime}, " \
               f"signal_type={self.signal_type}, strength={self.strength})"


class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol, order type (MKT or LMT), quantity, and direction.
    """
    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialize OrderEvent.
        
        Parameters:
        -----------
        symbol : str
            The ticker symbol, e.g., 'AAPL'
        order_type : str
            'MKT' for Market or 'LMT' for Limit
        quantity : int
            Non-negative integer for quantity
        direction : str
            'BUY' or 'SELL'
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def __repr__(self):
        return f"OrderEvent(symbol={self.symbol}, order_type={self.order_type}, " \
               f"quantity={self.quantity}, direction={self.direction})"


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage.
    Stores the quantity of an instrument actually filled and at what price.
    In addition, stores the commission of the trade from the brokerage.
    """
    def __init__(self, timeindex, symbol, exchange, quantity, 
                 direction, fill_cost, commission=None):
        """
        Initialize FillEvent.
        
        Parameters:
        -----------
        timeindex : datetime
            The timestamp when the order was filled
        symbol : str
            The ticker symbol, e.g., 'AAPL'
        exchange : str
            The exchange where the order was filled
        quantity : int
            The filled quantity
        direction : str
            'BUY' or 'SELL'
        fill_cost : float
            The total cost to fill the order including fees
        commission : float, optional
            The brokerage commission for the trade
        """
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        
        # Calculate commission if not provided
        if commission is None:
            self.commission = self._calculate_commission()
        else:
            self.commission = commission

    def _calculate_commission(self):
        """
        Calculate a realistic commission based on Interactive Brokers fees.
        For US stocks: $0.005 per share with $1 minimum.
        """
        commission = max(1.0, 0.005 * self.quantity)
        return commission

    def __repr__(self):
        return f"FillEvent(symbol={self.symbol}, exchange={self.exchange}, " \
               f"quantity={self.quantity}, direction={self.direction}, " \
               f"fill_cost={self.fill_cost:.2f}, commission={self.commission:.2f})"
