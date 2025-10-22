"""
Script to generate sample OHLCV data for backtesting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_ohlcv(symbol, start_date, end_date, initial_price=100.0):
    """
    Generate sample OHLCV data with random walk behavior.
    
    Parameters:
    -----------
    symbol : str
        The ticker symbol
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    initial_price : float
        Starting price for the security
    
    Returns:
    --------
    pd.DataFrame : DataFrame with OHLCV data
    """
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate random returns (daily percentage change)
    np.random.seed(42)  # For reproducibility
    returns = np.random.normal(0.0005, 0.02, len(dates))
    
    # Calculate prices using cumulative returns
    prices = initial_price * (1 + returns).cumprod()
    
    # Generate OHLC from close prices
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Add some randomness to OHLC
        daily_range = abs(np.random.normal(0, 0.015 * close))
        high = close + daily_range
        low = close - daily_range
        open_price = low + np.random.random() * (high - low)
        
        # Ensure OHLC relationships are valid
        high = max(high, open_price, close)
        low = min(low, open_price, close)
        
        # Generate volume
        volume = int(np.random.uniform(1000000, 5000000))
        
        data.append({
            'timestamp': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    return df


def main():
    """Generate sample data for multiple symbols."""
    symbols = ['AAPL', 'MSFT', 'GOOG']
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    
    initial_prices = {
        'AAPL': 75.0,
        'MSFT': 160.0,
        'GOOG': 1400.0
    }
    
    for symbol in symbols:
        print(f"Generating data for {symbol}...")
        df = generate_sample_ohlcv(
            symbol, 
            start_date, 
            end_date, 
            initial_prices[symbol]
        )
        
        # Save to CSV
        filename = f'data/{symbol}.csv'
        df.to_csv(filename, index=False)
        print(f"Saved {len(df)} rows to {filename}")
    
    print("\nSample data generation complete!")


if __name__ == '__main__':
    main()
