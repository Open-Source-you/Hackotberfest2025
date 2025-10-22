"""
Event-Driven Backtesting Engine
A minimal event-driven backtesting framework for running strategies against historical OHLCV data.
"""

__version__ = "1.0.0"

from .events import Event, MarketEvent, SignalEvent, OrderEvent, FillEvent
from .data_handler import HistoricalCSVDataHandler
from .strategy import Strategy, MovingAverageCrossStrategy
from .portfolio import Portfolio
from .execution import SimulatedExecutionHandler
from .backtest import Backtest

__all__ = [
    'Event',
    'MarketEvent',
    'SignalEvent',
    'OrderEvent',
    'FillEvent',
    'HistoricalCSVDataHandler',
    'Strategy',
    'MovingAverageCrossStrategy',
    'Portfolio',
    'SimulatedExecutionHandler',
    'Backtest',
]
