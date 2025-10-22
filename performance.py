# performance.py

import numpy as np
import pandas as pd


def create_drawdowns(equity_curve):
    hwm = [0]
    eq_idx = equity_curve.index
    drawdown = pd.Series(index=eq_idx)
    duration = pd.Series(index=eq_idx)

    for t in range(1, len(eq_idx)):
        hwm.append(max(hwm[t - 1], equity_curve[t]))
        drawdown[t] = hwm[t] - equity_curve[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t - 1] + 1

    return drawdown, drawdown.max(), duration.max()


def performance_metrics(equity_curve):
    returns = equity_curve.pct_change().dropna()
    total_return = equity_curve[-1] / equity_curve[0] - 1
    sharpe_ratio = np.sqrt(252) * returns.mean() / returns.std()
    drawdown, max_dd, dd_duration = create_drawdowns(equity_curve)

    return {
        "Total Return": round(total_return * 100, 2),
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Max Drawdown": round(max_dd * 100, 2),
    }
