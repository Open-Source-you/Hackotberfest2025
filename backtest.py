# backtest.py

import queue

from events import FillEvent, MarketEvent, OrderEvent, SignalEvent


class Backtest:
    def __init__(self, data_handler, strategy, portfolio, execution_handler):
        self.events = queue.Queue()
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution_handler = execution_handler
        self.continue_backtest = True

    def run(self):
        while self.continue_backtest:
            # Update market data
            self.data_handler.update_bars()
            self.events.put(MarketEvent())

            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event.type == "MARKET":
                        self.strategy.calculate_signals(event)
                    elif event.type == "SIGNAL":
                        self.portfolio.update_signal(event)
                    elif event.type == "ORDER":
                        self.execution_handler.execute_order(event)
                    elif event.type == "FILL":
                        self.portfolio.update_fill(event)
