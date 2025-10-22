"""
Visualization utilities for backtesting results.
Note: This requires matplotlib. Install with: pip install matplotlib
"""

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not installed. Install with: pip install matplotlib")

import pandas as pd
import os


def plot_equity_curve(results_df, title="Equity Curve", save_path=None):
    """
    Plot the equity curve from backtest results.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with equity curve data
    title : str
        Title for the plot
    save_path : str, optional
        Path to save the figure
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Cannot plot: matplotlib not installed")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    
    # Plot equity curve
    ax1.plot(results_df.index, results_df['equity_curve'], 
             linewidth=2, label='Strategy', color='blue')
    ax1.plot(results_df.index, [1.0] * len(results_df), 
             linestyle='--', linewidth=1, label='Buy & Hold', color='gray')
    ax1.set_ylabel('Equity Curve', fontsize=12)
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot drawdown
    running_max = results_df['equity_curve'].expanding().max()
    drawdown = (results_df['equity_curve'] - running_max) / running_max
    ax2.fill_between(results_df.index, drawdown * 100, 0, 
                     color='red', alpha=0.3, label='Drawdown')
    ax2.set_ylabel('Drawdown (%)', fontsize=12)
    ax2.set_xlabel('Date', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Format x-axis
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()


def plot_returns_distribution(results_df, save_path=None):
    """
    Plot the distribution of returns.
    
    Parameters:
    -----------
    results_df : pd.DataFrame
        DataFrame with returns data
    save_path : str, optional
        Path to save the figure
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Cannot plot: matplotlib not installed")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram
    returns = results_df['returns'].dropna() * 100  # Convert to percentage
    ax.hist(returns, bins=50, alpha=0.7, color='blue', edgecolor='black')
    ax.axvline(returns.mean(), color='red', linestyle='--', 
               linewidth=2, label=f'Mean: {returns.mean():.2f}%')
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    
    ax.set_xlabel('Daily Returns (%)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Daily Returns', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()


def create_performance_report(results_csv, output_dir='reports'):
    """
    Create a complete performance report with visualizations.
    
    Parameters:
    -----------
    results_csv : str
        Path to the results CSV file
    output_dir : str
        Directory to save the report files
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load results
    results = pd.read_csv(results_csv, index_col=0, parse_dates=True)
    
    # Extract strategy name from filename
    strategy_name = os.path.basename(results_csv).replace('backtest_results_', '').replace('.csv', '')
    
    print(f"\nGenerating performance report for: {strategy_name}")
    print("="*60)
    
    # Create plots
    equity_plot = os.path.join(output_dir, f'{strategy_name}_equity_curve.png')
    plot_equity_curve(results, 
                     title=f'Equity Curve - {strategy_name.upper()}',
                     save_path=equity_plot)
    
    returns_plot = os.path.join(output_dir, f'{strategy_name}_returns_dist.png')
    plot_returns_distribution(results, save_path=returns_plot)
    
    print(f"\nReport generated successfully in '{output_dir}/' directory")
    print("="*60)


def compare_strategies(results_files, save_path=None):
    """
    Compare multiple strategies on a single plot.
    
    Parameters:
    -----------
    results_files : list
        List of paths to results CSV files
    save_path : str, optional
        Path to save the figure
    """
    if not MATPLOTLIB_AVAILABLE:
        print("Cannot plot: matplotlib not installed")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    for i, results_file in enumerate(results_files):
        results = pd.read_csv(results_file, index_col=0, parse_dates=True)
        strategy_name = os.path.basename(results_file).replace('backtest_results_', '').replace('.csv', '')
        
        ax.plot(results.index, results['equity_curve'], 
               linewidth=2, label=strategy_name.upper(), 
               color=colors[i % len(colors)])
    
    ax.plot(results.index, [1.0] * len(results), 
           linestyle='--', linewidth=1, label='Baseline', color='gray')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Equity Curve', fontsize=12)
    ax.set_title('Strategy Comparison', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Comparison plot saved to: {save_path}")
    else:
        plt.show()


if __name__ == '__main__':
    # Example usage
    import glob
    
    # Find all result files
    result_files = glob.glob('backtest_results_*.csv')
    
    if not result_files:
        print("No backtest results found. Please run run_backtest.py first.")
    else:
        print(f"Found {len(result_files)} result file(s)")
        
        # Create individual reports
        for result_file in result_files:
            try:
                create_performance_report(result_file)
            except Exception as e:
                print(f"Error creating report for {result_file}: {e}")
        
        # Compare strategies if multiple results exist
        if len(result_files) > 1:
            try:
                compare_strategies(result_files, save_path='reports/strategy_comparison.png')
            except Exception as e:
                print(f"Error comparing strategies: {e}")
