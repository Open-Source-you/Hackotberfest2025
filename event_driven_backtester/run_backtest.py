"""
Example script demonstrating how to run the event-driven backtesting engine.
"""

import datetime
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from data_handler import HistoricalCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import NaivePortfolio
from strategy import MovingAverageCrossStrategy, BuyAndHoldStrategy, RSIStrategy
from backtest import Backtest


def run_backtest(strategy_name='ma_cross'):
    """
    Run a backtest with the specified strategy.
    
    Parameters:
    -----------
    strategy_name : str
        The strategy to use: 'ma_cross', 'buy_hold', or 'rsi'
    """
    # Set the paths and parameters
    csv_dir = os.path.join(os.path.dirname(__file__), 'data')
    symbol_list = ['AAPL']
    initial_capital = 100000.0
    heartbeat = 0.0  # Speed up backtest
    start_date = datetime.datetime(2020, 1, 1)
    
    # Select strategy and parameters
    if strategy_name == 'ma_cross':
        strategy_cls = MovingAverageCrossStrategy
        strategy_params = {
            'short_window': 50,
            'long_window': 200
        }
    elif strategy_name == 'buy_hold':
        strategy_cls = BuyAndHoldStrategy
        strategy_params = {}
    elif strategy_name == 'rsi':
        strategy_cls = RSIStrategy
        strategy_params = {
            'period': 14,
            'oversold': 30,
            'overbought': 70
        }
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    print("="*60)
    print(f"Running Backtest with {strategy_name} strategy")
    print("="*60)
    print(f"Symbol List: {symbol_list}")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
    print(f"Data Directory: {csv_dir}")
    print("="*60)
    
    # Create and run backtest
    backtest = Backtest(
        csv_dir=csv_dir,
        symbol_list=symbol_list,
        initial_capital=initial_capital,
        heartbeat=heartbeat,
        start_date=start_date,
        data_handler_cls=HistoricalCSVDataHandler,
        execution_handler_cls=SimulatedExecutionHandler,
        portfolio_cls=NaivePortfolio,
        strategy_cls=strategy_cls,
        **strategy_params
    )
    
    # Run the backtest and get results
    results = backtest.simulate_trading()
    
    # Save results
    output_file = f'backtest_results_{strategy_name}.csv'
    results.to_csv(output_file)
    print(f"\nResults saved to: {output_file}")
    
    return results


def main():
    """
    Main function to run backtests for different strategies.
    """
    print("\n" + "="*60)
    print("Event-Driven Backtesting Engine")
    print("="*60 + "\n")
    
    # Check if data exists
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(os.path.join(data_dir, 'AAPL.csv')):
        print("⚠️  Sample data not found!")
        print("Please run 'python generate_sample_data.py' first to create sample data.")
        return
    
    # Run backtests for different strategies
    strategies = ['buy_hold', 'ma_cross', 'rsi']
    
    for strategy in strategies:
        try:
            print(f"\n{'='*60}")
            print(f"Testing Strategy: {strategy.upper().replace('_', ' ')}")
            print(f"{'='*60}\n")
            run_backtest(strategy)
            print("\n")
        except Exception as e:
            print(f"Error running {strategy} strategy: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    # You can also run a specific strategy
    # run_backtest('ma_cross')
    
    # Or run all strategies
    main()
