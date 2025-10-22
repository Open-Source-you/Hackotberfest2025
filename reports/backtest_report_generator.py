"""
Backtest report generator
Generates a standalone HTML performance report (single-file) with key metrics,
equity curve plots, drawdown plots, and comparison across multiple backtests.

Usage example at bottom: run the module as a script. It creates `example_report.html`.

Requirements: pandas, numpy, matplotlib

"""

import base64
import math
from io import BytesIO
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------- Metrics helpers ----------------------


def annualize_return(total_return: float, periods: int, periods_per_year: int) -> float:
    if periods <= 0:
        return np.nan
    return (1 + total_return) ** (periods_per_year / periods) - 1


def compute_cagr(equity: pd.Series, periods_per_year: int = 252) -> float:
    if equity.empty:
        return np.nan
    start_val = equity.iloc[0]
    end_val = equity.iloc[-1]
    total_return = end_val / start_val - 1
    periods = len(equity)
    return annualize_return(total_return, periods, periods_per_year)


def compute_annualized_vol(equity: pd.Series, periods_per_year: int = 252) -> float:
    # compute returns
    if len(equity) < 2:
        return np.nan
    returns = equity.pct_change().dropna()
    return returns.std() * math.sqrt(periods_per_year)


def compute_sharpe(
    equity: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252
) -> float:
    if len(equity) < 2:
        return np.nan
    returns = equity.pct_change().dropna()
    excess = returns - (risk_free_rate / periods_per_year)
    ann_excess = excess.mean() * periods_per_year
    ann_vol = returns.std() * math.sqrt(periods_per_year)
    if ann_vol == 0:
        return np.nan
    return ann_excess / ann_vol


def compute_sortino(
    equity: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252
) -> float:
    if len(equity) < 2:
        return np.nan
    returns = equity.pct_change().dropna()
    neg_returns = returns[returns < 0]
    downside_std = (
        neg_returns.std() * math.sqrt(periods_per_year)
        if not neg_returns.empty
        else 0.0
    )
    ann_excess = (
        returns.mean() - (risk_free_rate / periods_per_year)
    ) * periods_per_year
    if downside_std == 0:
        return np.nan
    return ann_excess / downside_std


def compute_max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return np.nan
    roll_max = equity.cummax()
    drawdown = (equity - roll_max) / roll_max
    return drawdown.min()


def compute_metrics(
    equity: pd.Series, periods_per_year: int = 252, risk_free_rate: float = 0.0
) -> Dict[str, float]:
    metrics = {}
    metrics["start_date"] = equity.index[0] if len(equity) else pd.NaT
    metrics["end_date"] = equity.index[-1] if len(equity) else pd.NaT
    metrics["periods"] = len(equity)
    metrics["total_return"] = (
        float(equity.iloc[-1] / equity.iloc[0] - 1) if len(equity) else np.nan
    )
    metrics["cagr"] = float(compute_cagr(equity, periods_per_year))
    metrics["annual_vol"] = float(compute_annualized_vol(equity, periods_per_year))
    metrics["sharpe"] = float(compute_sharpe(equity, risk_free_rate, periods_per_year))
    metrics["sortino"] = float(
        compute_sortino(equity, risk_free_rate, periods_per_year)
    )
    metrics["max_drawdown"] = float(compute_max_drawdown(equity))
    return metrics


# ---------------------- Plot helpers ----------------------


def fig_to_base64(fig: plt.Figure, fmt: str = "png") -> str:
    buf = BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format=fmt, bbox_inches="tight")
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("utf8")
    plt.close(fig)
    return img_b64


def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve") -> str:
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(equity.index, equity.values)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.grid(True)
    return fig_to_base64(fig)


def plot_drawdowns(equity: pd.Series, title: str = "Drawdown") -> str:
    roll_max = equity.cummax()
    drawdown = (equity - roll_max) / roll_max
    fig, ax = plt.subplots(figsize=(10, 3.5))
    ax.fill_between(drawdown.index, drawdown.values, 0)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True)
    return fig_to_base64(fig)


def plot_comparison(
    equities: Dict[str, pd.Series], title: str = "Equity Comparison"
) -> str:
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, series in equities.items():
        # normalize to 1.0 at start for visual comparison
        if series.empty:
            continue
        norm = series / series.iloc[0]
        ax.plot(norm.index, norm.values, label=name)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Equity (start=1.0)")
    ax.legend()
    ax.grid(True)
    return fig_to_base64(fig)


# ---------------------- HTML report builder ----------------------


def metrics_to_html_table(metrics: Dict[str, float]) -> str:
    rows = []
    mapping = [
        ("Start Date", "start_date"),
        ("End Date", "end_date"),
        ("Periods", "periods"),
        ("Total Return", "total_return"),
        ("CAGR", "cagr"),
        ("Annual Vol", "annual_vol"),
        ("Sharpe", "sharpe"),
        ("Sortino", "sortino"),
        ("Max Drawdown", "max_drawdown"),
    ]
    for label, key in mapping:
        val = metrics.get(key, "")
        if isinstance(val, float):
            if (
                abs(val) < 1
                and "return" in label.lower()
                or "cagr" in label.lower()
                or "drawdown" in label.lower()
            ):
                out = f"{val:.2%}"
            else:
                out = f"{val:.4f}"
        else:
            out = str(val)
        rows.append(
            f"<tr><th style='text-align:left;padding:6px'>{label}</th><td style='padding:6px'>{out}</td></tr>"
        )
    return '<table style="border-collapse:collapse">' + "\n".join(rows) + "</table>"


def build_report_html(
    backtests: Dict[str, pd.Series], output_path: str, title: str = "Backtest Report"
) -> None:
    # Compute metrics & plots
    metrics_map = {}
    equity_imgs = {}
    drawdown_imgs = {}

    for name, series in backtests.items():
        metrics_map[name] = compute_metrics(series)
        equity_imgs[name] = plot_equity_curve(series, title=f"{name} — Equity Curve")
        drawdown_imgs[name] = plot_drawdowns(series, title=f"{name} — Drawdown")

    comparison_img = plot_comparison(backtests, title="Strategy Comparison")

    # Build HTML
    html_parts = []
    html_parts.append(f"<html><head><meta charset='utf-8'><title>{title}</title>")
    html_parts.append(
        "<style>body{font-family:Arial, Helvetica, sans-serif;margin:20px} .card{box-shadow:0 1px 3px rgba(0,0,0,0.12);padding:12px;margin-bottom:18px;border-radius:6px} table{border:1px solid #eee}</style></head><body>"
    )
    html_parts.append(f"<h1>{title}</h1>")
    html_parts.append('<div class="card"><h2>Comparison</h2>')
    html_parts.append(
        f"<img src='data:image/png;base64,{comparison_img}' alt='comparison' style='max-width:100%'>"
    )
    # summary table comparing key metrics across backtests
    comp_rows = [
        "<tr><th style='text-align:left;padding:6px'>Metric</th>"
        + "".join([f"<th style='padding:6px'>{name}</th>" for name in backtests.keys()])
        + "</tr>"
    ]
    keys = ["total_return", "cagr", "annual_vol", "sharpe", "max_drawdown"]
    human = {
        "total_return": "Total Return",
        "cagr": "CAGR",
        "annual_vol": "Annual Vol",
        "sharpe": "Sharpe",
        "max_drawdown": "Max Drawdown",
    }
    for k in keys:
        row = f"<tr><th style='text-align:left;padding:6px'>{human[k]}</th>"
        for name in backtests.keys():
            val = metrics_map[name].get(k, "")
            if isinstance(val, float):
                if k in ("total_return", "cagr", "max_drawdown"):
                    cell = f"{val:.2%}"
                else:
                    cell = f"{val:.4f}"
            else:
                cell = str(val)
            row += f"<td style='padding:6px'>{cell}</td>"
        row += "</tr>"
        comp_rows.append(row)
    html_parts.append("<table>" + "\n".join(comp_rows) + "</table></div>")

    # Per-backtest sections
    for name in backtests.keys():
        html_parts.append(f"<div class='card'><h2>{name}</h2>")
        html_parts.append('<div style="display:flex;gap:12px;flex-wrap:wrap">')
        html_parts.append('<div style="flex:1 1 380px">')
        html_parts.append(metrics_to_html_table(metrics_map[name]))
        html_parts.append("</div>")
        html_parts.append('<div style="flex:1 1 380px">')
        html_parts.append(
            f"<h4>Equity Curve</h4><img src='data:image/png;base64,{equity_imgs[name]}' style='max-width:100%'>"
        )
        html_parts.append(
            f"<h4>Drawdown</h4><img src='data:image/png;base64,{drawdown_imgs[name]}' style='max-width:100%'>"
        )
        html_parts.append("</div></div></div>")

    html_parts.append("</body></html>")

    html = "\n".join(html_parts)
    with open(output_path, "w", encoding="utf8") as f:
        f.write(html)

    print(f"Report written to {output_path}")


# ---------------------- Example usage (creates an example report) ----------------------

if __name__ == "__main__":
    # Create example backtests: three simulated strategies
    np.random.seed(42)
    days = pd.date_range(
        start="2020-01-01", periods=750, freq="B"
    )  # business days ~3 years

    def make_strategy(drift=0.0002, vol=0.01):
        # geometric random walk on returns, cumulative equity starting at 10000
        rets = np.random.normal(loc=drift, scale=vol, size=len(days))
        prices = 10000 * np.cumprod(1 + rets)
        return pd.Series(data=prices, index=days)

    backtests = {
        "Strategy A": make_strategy(drift=0.0006, vol=0.012),
        "Strategy B": make_strategy(drift=0.0003, vol=0.01),
        "Strategy C": make_strategy(drift=0.0001, vol=0.02),
    }

    build_report_html(
        backtests, output_path="example_report.html", title="Example Backtest Report"
    )
