"""
Main backtesting engine that orchestrates the event-driven simulation.
"""

import queue
import time
from .events import MarketEvent


class Backtest:
    """
    Encapsulates the settings and components for carrying out
    an event-driven backtest.
    """

    def __init__(
        self, 
        csv_dir, 
        symbol_list, 
        initial_capital,
        heartbeat, 
        start_date, 
        data_handler_cls,
        execution_handler_cls, 
        portfolio_cls, 
        strategy_cls,
        **strategy_params
    ):
        """
        Initialize the backtest.
        
        Parameters:
        -----------
        csv_dir : str
            The hard root to the CSV data directory
        symbol_list : list
            The list of symbol strings
        initial_capital : float
            The starting capital for the portfolio
        heartbeat : float
            The heartbeat in seconds for the backtest
        start_date : datetime
            The start datetime of the strategy
        data_handler_cls : class
            The DataHandler class to use
        execution_handler_cls : class
            The ExecutionHandler class to use
        portfolio_cls : class
            The Portfolio class to use
        strategy_cls : class
            The Strategy class to use
        **strategy_params : dict
            Additional parameters for the strategy
        """
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat
        self.start_date = start_date
        
        self.data_handler_cls = data_handler_cls
        self.execution_handler_cls = execution_handler_cls
        self.portfolio_cls = portfolio_cls
        self.strategy_cls = strategy_cls
        self.strategy_params = strategy_params
        
        self.events = queue.Queue()
        
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1
        
        self._generate_trading_instances()

    def _generate_trading_instances(self):
        """
        Generates the trading instance objects from their class types.
        """
        print("Creating DataHandler, Strategy, Portfolio and ExecutionHandler")
        
        self.data_handler = self.data_handler_cls(
            self.events, self.csv_dir, self.symbol_list
        )
        
        self.strategy = self.strategy_cls(
            self.data_handler, self.events, **self.strategy_params
        )
        
        self.portfolio = self.portfolio_cls(
            self.data_handler, self.events, 
            self.start_date, self.initial_capital
        )
        
        self.execution_handler = self.execution_handler_cls(
            self.events
        )

    def _run_backtest(self):
        """
        Executes the backtest by processing events in the queue.
        """
        i = 0
        while True:
            i += 1
            print(f"Processing bar {i}...", end='\r')
            
            # Update the market bars
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break
            
            # Handle the events
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(event)
                            self.portfolio.update_timeindex(event)
                            
                        elif event.type == 'SIGNAL':
                            self.signals += 1
                            self.portfolio.update_signal(event)
                            
                        elif event.type == 'ORDER':
                            self.orders += 1
                            self.execution_handler.execute_order(event)
                            
                        elif event.type == 'FILL':
                            self.fills += 1
                            self.portfolio.update_fill(event)
            
            time.sleep(self.heartbeat)

    def _output_performance(self):
        """
        Outputs the strategy performance from the backtest.
        """
        print("\n" + "="*60)
        print("Backtest Complete!")
        print("="*60)
        print(f"Signals: {self.signals}")
        print(f"Orders: {self.orders}")
        print(f"Fills: {self.fills}")
        print("="*60)
        
        stats = self.portfolio.output_summary_stats()
        print("\nPerformance Summary:")
        print("-"*60)
        for stat in stats:
            print(f"{stat[0]:<25} {stat[1]:>15}")
        print("="*60)

    def simulate_trading(self):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        self._output_performance()
        return self.portfolio.create_equity_curve_dataframe()
