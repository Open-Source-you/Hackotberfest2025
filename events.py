# events.py


class Event:
    """Base class for all events."""

    pass


class MarketEvent(Event):
    def __init__(self):
        self.type = "MARKET"


class SignalEvent(Event):
    def __init__(self, symbol, datetime, signal_type, strength):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type  # 'BUY' or 'SELL'
        self.strength = strength


class OrderEvent(Event):
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type  # 'MKT' or 'LMT'
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'


class FillEvent(Event):
    def __init__(
        self,
        timeindex,
        symbol,
        exchange,
        quantity,
        direction,
        fill_cost,
        commission=None,
    ):
        self.type = "FILL"
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission
