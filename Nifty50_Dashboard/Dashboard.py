from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import yfinance as yf
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import KMeans
from sklearn.manifold import MDS
from statsmodels.graphics.tsaplots import plot_acf

# Streamlit setup
st.set_page_config(page_title="Nifty 50 Financial Dashboard", layout="wide")

# Custom CSS to improve layout
st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .metric-card {
        border: 1px solid #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
        background-color: #f9f9f9;
    }
    .metric-card h4 {
        margin: 0;
        color: #1f77b4;
    }
    .metric-card p {
        margin: 5px 0 0 0;
        font-size: 1.2em;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Define stock tickers (removed ZEEL.NS as it's delisted)
tickers = [
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BHARTIARTL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HEROMOTOCO.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "IOC.NS",
    "INDUSINDBK.NS",
    "INFY.NS",
    "ITC.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "M&M.NS",
    "MARUTI.NS",
    "NESTLEIND.NS",
    "NTPC.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBIN.NS",
    "SUNPHARMA.NS",
    "TCS.NS",
    "TATACONSUM.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "TECHM.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "UPL.NS",
    "WIPRO.NS",
]


# Cache functions
@st.cache_data(ttl=86400)
def load_data(start_date, end_date):
    """Load stock price data"""
    try:
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=False,  # Explicitly set to avoid FutureWarning
        )

        # Handle both single and multiple ticker cases
        if "Adj Close" in data.columns:
            return data["Adj Close"]
        elif isinstance(data.columns, pd.MultiIndex):
            if "Adj Close" in data.columns.get_level_values(0):
                return data["Adj Close"]

        st.error("Adj Close data not found for selected tickers")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=86400)
def load_volume_and_ratios():
    """Load volume data, P/E ratios, and sector information"""
    volumes = {}
    pe_ratios = {}
    sectors = {}

    progress_bar = st.progress(0)
    for idx, ticker in enumerate(tickers):
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            volumes[ticker] = hist["Volume"] if not hist.empty else pd.Series()

            info = stock.info
            pe_ratios[ticker] = info.get("forwardPE", info.get("trailingPE", None))
            sectors[ticker] = info.get("sector", "Unknown")
        except Exception as e:
            st.warning(f"Data for {ticker} could not be fetched. Error: {e}")
            volumes[ticker] = pd.Series()
            pe_ratios[ticker] = None
            sectors[ticker] = "Unknown"

        progress_bar.progress((idx + 1) / len(tickers))

    progress_bar.empty()
    return volumes, pe_ratios, sectors


# Sidebar for date selection
with st.sidebar:
    st.title("📊 Configuration")

    # Date range selection
    st.subheader("Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now(),
        )
    with col2:
        end_date = st.date_input(
            "End Date", value=datetime.now(), max_value=datetime.now()
        )

# Load data
with st.spinner("Loading data..."):
    data = load_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    if data.empty:
        st.error(
            "Failed to load data. Please check your internet connection and try again."
        )
        st.stop()

    volumes, pe_ratios, sectors = load_volume_and_ratios()

# Header section
st.title("📈 Nifty 50 Financial Dashboard")
st.markdown(
    f"**Data Period:** {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
)

# Sidebar configuration (continued)
with st.sidebar:
    st.markdown("---")

    # Sector selection
    unique_sectors = sorted(list(set(s for s in sectors.values() if s != "Unknown")))
    selected_sector = st.selectbox("🏢 Choose Sector", ["All Sectors"] + unique_sectors)

    # Filter stocks based on sector
    if selected_sector == "All Sectors":
        sector_stocks = tickers
    else:
        sector_stocks = [
            ticker for ticker, sector in sectors.items() if sector == selected_sector
        ]

    # Stock selection
    num_default = min(10, len(sector_stocks))
    selected_stocks = st.multiselect(
        "📊 Select Stocks",
        options=sector_stocks,
        default=sector_stocks[:num_default],
        help="Select stocks to analyze (default: first 10)",
    )

    if not selected_stocks:
        st.warning("⚠️ Please select at least one stock")
        st.stop()

    # Advanced visualization options
    st.markdown("---")
    st.subheader("🔬 Advanced Analytics")
    show_correlation_matrix = st.checkbox("Correlation Matrix", value=True)
    show_distance_matrix = st.checkbox("Distance Matrix")
    show_mds = st.checkbox("MDS Visualization", value=True)
    show_kmeans = st.checkbox("KMeans Clustering")

    if show_kmeans:
        optimal_k = st.slider(
            "Number of Clusters",
            2,
            min(10, len(selected_stocks)),
            min(4, len(selected_stocks)),
        )

# Filter data based on selection
filtered_data = data[selected_stocks].dropna(how="all")
filtered_log_returns = np.log(filtered_data / filtered_data.shift(1)).dropna()

# Summary metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📊 Stocks Selected", len(selected_stocks))
with col2:
    avg_return = (filtered_log_returns.mean() * 252 * 100).mean()  # Annualized
    st.metric("📈 Avg Annual Return", f"{avg_return:.2f}%")
with col3:
    avg_volatility = (filtered_log_returns.std() * np.sqrt(252) * 100).mean()
    st.metric("📉 Avg Volatility", f"{avg_volatility:.2f}%")
with col4:
    correlation_avg = (
        filtered_log_returns.corr()
        .values[np.triu_indices_from(filtered_log_returns.corr().values, k=1)]
        .mean()
    )
    st.metric("🔗 Avg Correlation", f"{correlation_avg:.3f}")

st.markdown("---")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Price Analysis",
        "📊 Volume Analysis",
        "📉 Distribution Analysis",
        "🔬 Advanced Analytics",
        "💾 Download Center",
    ]
)

# Tab 1: Price Analysis
with tab1:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Price Trends")
        fig = go.Figure()
        for ticker in selected_stocks:
            fig.add_trace(
                go.Scatter(
                    x=filtered_data.index,
                    y=filtered_data[ticker],
                    mode="lines",
                    name=ticker.replace(".NS", ""),
                )
            )
        fig.update_layout(
            height=500,
            title="Time Series of Selected Stocks",
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Returns chart
        st.subheader("📊 Cumulative Returns")
        cumulative_returns = (1 + filtered_log_returns).cumprod()
        fig2 = go.Figure()
        for ticker in selected_stocks:
            fig2.add_trace(
                go.Scatter(
                    x=cumulative_returns.index,
                    y=cumulative_returns[ticker],
                    mode="lines",
                    name=ticker.replace(".NS", ""),
                )
            )
        fig2.update_layout(
            height=400,
            title="Cumulative Returns",
            xaxis_title="Date",
            yaxis_title="Cumulative Return",
            hovermode="x unified",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("💰 Latest Prices")
        closing_prices = filtered_data.iloc[-1].sort_values(ascending=False)
        for ticker, price in closing_prices.items():
            # Calculate return
            if len(filtered_data) > 1:
                prev_price = filtered_data[ticker].iloc[-2]
                change = ((price - prev_price) / prev_price) * 100
                color = "green" if change > 0 else "red"
                arrow = "↑" if change > 0 else "↓"
            else:
                change = 0
                color = "gray"
                arrow = ""

            st.markdown(
                f"""
            <div class="metric-card">
                <h4>{ticker.replace('.NS', '')}</h4>
                <p>₹{price:.2f}</p>
                <p style="color: {color}; font-size: 0.9em;">{arrow} {change:.2f}%</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

# Tab 2: Volume Analysis
with tab2:
    st.subheader("📊 Trading Volume Analysis")

    # Create volume dataframe
    volume_data = pd.DataFrame(
        {ticker: volumes.get(ticker, pd.Series()) for ticker in selected_stocks}
    ).dropna(how="all")

    if not volume_data.empty:
        fig = go.Figure()
        for ticker in selected_stocks:
            if ticker in volume_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=volume_data.index,
                        y=volume_data[ticker],
                        mode="lines",
                        name=ticker.replace(".NS", ""),
                    )
                )
        fig.update_layout(
            height=600,
            title="Volume Data of Selected Stocks",
            xaxis_title="Date",
            yaxis_title="Volume",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Average volume comparison
        st.subheader("📊 Average Volume Comparison")
        avg_volumes = volume_data.mean().sort_values(ascending=False)
        fig2 = go.Figure(
            go.Bar(
                x=[t.replace(".NS", "") for t in avg_volumes.index],
                y=avg_volumes.values,
                marker_color="lightblue",
            )
        )
        fig2.update_layout(
            height=400,
            title="Average Trading Volume",
            xaxis_title="Stock",
            yaxis_title="Average Volume",
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No volume data available for selected stocks")

# Tab 3: Distribution Analysis
with tab3:
    st.subheader("📉 Distribution Analysis of Log Returns")

    # Display in 2 columns
    cols = st.columns(2)
    for idx, ticker in enumerate(selected_stocks):
        with cols[idx % 2]:
            st.markdown(f"**{ticker.replace('.NS', '')}**")

            # Distribution plot
            fig, ax = plt.subplots(figsize=(8, 4))
            returns_data = filtered_log_returns[ticker].dropna()

            if len(returns_data) > 0:
                sns.histplot(
                    returns_data,
                    kde=True,
                    stat="density",
                    ax=ax,
                    label="Empirical",
                    alpha=0.6,
                )

                # Normal distribution overlay
                normal_data = np.random.normal(
                    loc=returns_data.mean(), scale=returns_data.std(), size=1000
                )
                sns.kdeplot(
                    normal_data,
                    ax=ax,
                    color="red",
                    linestyle="--",
                    label="Normal Dist",
                    linewidth=2,
                )

                ax.set_title("Distribution of Log Returns")
                ax.set_xlabel("Log Returns")
                ax.set_ylabel("Density")
                ax.legend()
                st.pyplot(fig)
                plt.close()

                # Statistics
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Mean", f"{returns_data.mean():.4f}")
                col_b.metric("Std Dev", f"{returns_data.std():.4f}")
                col_c.metric("Skewness", f"{returns_data.skew():.2f}")

                # Autocorrelation plot
                fig, ax = plt.subplots(figsize=(8, 4))
                plot_acf(filtered_data[ticker].dropna(), ax=ax, lags=20)
                ax.set_title("Autocorrelation")
                st.pyplot(fig)
                plt.close()
            else:
                st.warning(f"Insufficient data for {ticker}")

            st.markdown("---")

# Tab 4: Advanced Analytics
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        # P/E Ratios and Sectors
        st.subheader("📊 Fundamental Analysis")
        pe_sector_data = pd.DataFrame(
            {
                "Ticker": [t.replace(".NS", "") for t in selected_stocks],
                "P/E Ratio": [pe_ratios.get(ticker) for ticker in selected_stocks],
                "Sector": [
                    sectors.get(ticker, "Unknown") for ticker in selected_stocks
                ],
            }
        )

        # Add recommendation based on P/E ratio
        def get_recommendation(pe):
            if pe is None or pd.isna(pe):
                return "N/A"
            elif pe < 15:
                return "🟢 Undervalued"
            elif 15 <= pe <= 25:
                return "🟡 Fair Value"
            else:
                return "🔴 Overvalued"

        pe_sector_data["Recommendation"] = pe_sector_data["P/E Ratio"].apply(
            get_recommendation
        )
        pe_sector_data["P/E Ratio"] = pe_sector_data["P/E Ratio"].apply(
            lambda x: f"{x:.2f}" if x and not pd.isna(x) else "N/A"
        )

        st.dataframe(pe_sector_data, use_container_width=True, hide_index=True)

    with col2:
        # Risk-Return Profile
        st.subheader("📈 Risk-Return Profile")
        annual_returns = filtered_log_returns.mean() * 252 * 100
        annual_volatility = filtered_log_returns.std() * np.sqrt(252) * 100

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=annual_volatility,
                y=annual_returns,
                mode="markers+text",
                text=[t.replace(".NS", "") for t in selected_stocks],
                textposition="top center",
                marker=dict(
                    size=10, color=annual_returns, colorscale="RdYlGn", showscale=True
                ),
                hovertemplate="<b>%{text}</b><br>Return: %{y:.2f}%<br>Volatility: %{x:.2f}%<extra></extra>",
            )
        )
        fig.update_layout(
            height=400,
            title="Risk-Return Trade-off",
            xaxis_title="Annualized Volatility (%)",
            yaxis_title="Annualized Return (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Correlation Matrix
    if show_correlation_matrix and len(selected_stocks) > 1:
        st.subheader("🔗 Correlation Matrix")
        fig, ax = plt.subplots(figsize=(12, 10))
        corr_matrix = filtered_log_returns.corr()
        sns.heatmap(
            corr_matrix,
            cmap="coolwarm",
            annot=True,
            fmt=".2f",
            xticklabels=[t.replace(".NS", "") for t in selected_stocks],
            yticklabels=[t.replace(".NS", "") for t in selected_stocks],
            ax=ax,
            center=0,
            vmin=-1,
            vmax=1,
        )
        ax.set_title("Correlation Matrix of Log Returns")
        st.pyplot(fig)
        plt.close()

    # Distance Matrix and Clustering
    if (show_distance_matrix or show_mds or show_kmeans) and len(selected_stocks) > 1:
        st.subheader("🔬 Advanced Statistical Analysis")

        distance_matrix = squareform(pdist(filtered_log_returns.T, "euclidean"))

        if show_distance_matrix:
            st.markdown("**Distance Matrix**")
            fig, ax = plt.subplots(figsize=(12, 10))
            sns.heatmap(
                distance_matrix,
                cmap="viridis",
                xticklabels=[t.replace(".NS", "") for t in selected_stocks],
                yticklabels=[t.replace(".NS", "") for t in selected_stocks],
                ax=ax,
                annot=True,
                fmt=".2f",
            )
            ax.set_title("Euclidean Distance Matrix")
            st.pyplot(fig)
            plt.close()

        if len(selected_stocks) >= 2:
            mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42)
            mds_results = mds.fit_transform(distance_matrix)

            if show_mds:
                st.markdown("**Multidimensional Scaling (MDS)**")
                fig, ax = plt.subplots(figsize=(12, 10))
                scatter = ax.scatter(
                    mds_results[:, 0], mds_results[:, 1], c="orange", s=100, alpha=0.6
                )
                for i, ticker in enumerate(selected_stocks):
                    ax.text(
                        mds_results[i, 0],
                        mds_results[i, 1],
                        ticker.replace(".NS", ""),
                        fontsize=10,
                        ha="center",
                    )
                ax.set_title("MDS Visualization of Stock Relationships")
                ax.set_xlabel("MDS Dimension 1")
                ax.set_ylabel("MDS Dimension 2")
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()

            if show_kmeans:
                st.markdown("**KMeans Clustering**")
                kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(filtered_log_returns.T)

                fig, ax = plt.subplots(figsize=(12, 10))
                scatter = ax.scatter(
                    mds_results[:, 0],
                    mds_results[:, 1],
                    c=clusters,
                    cmap="viridis",
                    s=100,
                    alpha=0.6,
                )
                for i, ticker in enumerate(selected_stocks):
                    ax.text(
                        mds_results[i, 0],
                        mds_results[i, 1],
                        ticker.replace(".NS", ""),
                        fontsize=10,
                        ha="center",
                    )
                ax.set_title(f"KMeans Clustering (k={optimal_k})")
                ax.set_xlabel("MDS Dimension 1")
                ax.set_ylabel("MDS Dimension 2")
                legend1 = ax.legend(
                    *scatter.legend_elements(), title="Clusters", loc="upper right"
                )
                ax.add_artist(legend1)
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
                plt.close()

                # Show cluster assignments
                cluster_df = pd.DataFrame(
                    {
                        "Stock": [t.replace(".NS", "") for t in selected_stocks],
                        "Cluster": clusters,
                    }
                ).sort_values("Cluster")
                st.dataframe(cluster_df, use_container_width=True, hide_index=True)

# Tab 5: Download Center
with tab5:
    st.subheader("💾 Download Data")
    st.markdown("Download the analyzed data for further processing")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Closing Prices**")
        csv_data = filtered_data.to_csv().encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"closing_prices_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

    with col2:
        st.markdown("**Log Returns**")
        log_returns_csv = filtered_log_returns.to_csv().encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=log_returns_csv,
            file_name=f"log_returns_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

    with col3:
        st.markdown("**Volume Data**")
        if not volume_data.empty:
            volume_data_csv = volume_data.to_csv().encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=volume_data_csv,
                file_name=f"volume_data_{start_date}_{end_date}.csv",
                mime="text/csv",
            )
        else:
            st.info("No volume data available")

    # Additional downloads
    st.markdown("---")
    col4, col5 = st.columns(2)

    with col4:
        st.markdown("**Correlation Matrix**")
        if len(selected_stocks) > 1:
            corr_csv = filtered_log_returns.corr().to_csv().encode("utf-8")
            st.download_button(
                label="📥 Download CSV",
                data=corr_csv,
                file_name=f"correlation_matrix_{start_date}_{end_date}.csv",
                mime="text/csv",
            )

    with col5:
        st.markdown("**Summary Statistics**")
        summary_stats = filtered_log_returns.describe().T
        summary_stats["Annual Return %"] = filtered_log_returns.mean() * 252 * 100
        summary_stats["Annual Volatility %"] = (
            filtered_log_returns.std() * np.sqrt(252) * 100
        )
        summary_csv = summary_stats.to_csv().encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=summary_csv,
            file_name=f"summary_statistics_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>📊 Nifty 50 Financial Dashboard | Data powered by Yahoo Finance</p>
        <p style='font-size: 0.8em;'>⚠️ Disclaimer: This dashboard is for educational purposes only. Not financial advice.</p>
    </div>
""",
    unsafe_allow_html=True,
)
