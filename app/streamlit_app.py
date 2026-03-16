import sys
from pathlib import Path

# --------------------------
# Project Root for src imports
# --------------------------
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from src.plot_helpers import plot_production, plot_yoy, plot_lng_supply_gap, plot_production_with_breaks, plot_incremental_vs_demand, plot_supply_gap, plot_cumulative_supply, plot_forecast_comparison, plot_forecast_with_history, plot_forecast_supply_gap  # type: ignore

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# Paths
# --------------------------
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data/processed/app_data"

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="Canada Gas Supply Dashboard",
    page_icon="🛢️",
    layout="wide"
)

st.title("Canada Marketable Natural Gas Supply Dashboard")

# --------------------------
# Load CSVs
# --------------------------
production_df = pd.read_csv(DATA_PATH / "production_master.csv")
lng_df = pd.read_csv(DATA_PATH / "lng_supply_demand.csv")
sarima_df = pd.read_csv(DATA_PATH / "forecast_sarima.csv")
prophet_df = pd.read_csv(DATA_PATH / "forecast_prophet.csv")
forecast_results = pd.read_csv(DATA_PATH / "forecast_results.csv")

# --------------------------
# Sidebar Navigation
# --------------------------
st.sidebar.title("Streamlit App")
page = st.sidebar.radio(
    "Choose a page",
    ["Executive Overview", "Historical & Structural", "LNG Supply", "Forecasting", "Limitations & Assumptions"]
)

# Define regime table
regime_table = pd.DataFrame({
    "Regime": ["Growth", "Decline", "Stagnation"],
    "Condition": ["YoY > 3%", "YoY < -3%", "-3% ≤ YoY ≤ 3%"]
})

# =========================
# Page Routing
# =========================
if page == "Executive Overview":
    st.header("Executive Overview")
    st.plotly_chart(plot_production(production_df))
    st.plotly_chart(plot_yoy(production_df))

elif page == "Historical & Structural":
    st.header("Historical Production & Structural Regimes")

    # ---------- Row 1: Production Table ----------
    st.subheader("Historical Production (mtpa)")
    st.dataframe(
        production_df[["Year", "Production_mtpa", "Rolling_3yr"]].style.format("{:,.1f}")
    )

    # ---------- Row 2: YoY + Rolling Trends ----------
    st.subheader("YoY & Rolling Trends")
    fig_yoy = px.line(
        production_df,
        x="Year",
        y=["YoY_pct", "Rolling_3yr"],
        labels={"value":"mtpa / %", "variable":"Metric"},
        title="YoY and Rolling 3-year Average"
    )
    st.plotly_chart(fig_yoy)

    # ---------- Row 3: Regime Changes ----------
    st.subheader("Structural Regimes (Colored by Regime)")
    fig_regime = px.bar(
        production_df,
        x="Year",
        y="YoY_pct",
        color="Regime",
        color_discrete_map={"Growth":"green","Decline":"red","Stagnation":"gray"},
        labels={"YoY_pct":"YoY %"},
        title="Regime Changes"
    )
    st.plotly_chart(fig_regime)

    breaks_df = pd.read_csv(DATA_PATH / "structural_breaks.csv")
    st.subheader("Structural Break Analysis")
    
    st.plotly_chart(
        plot_production_with_breaks(production_df, breaks_df),
        use_container_width=True
        )

elif page == "LNG Supply":
    st.header("LNG Canada Supply Adequacy")

    # Incremental vs Demand
    st.subheader("Incremental Supply vs LNG Phase 1 Demand")
    st.plotly_chart(plot_incremental_vs_demand(lng_df), use_container_width=True)

    # Supply Gap
    st.subheader("Supply Gap (Surplus / Deficit)")
    st.plotly_chart(plot_supply_gap(lng_df), use_container_width=True)

    # Long-term supply capacity
    st.subheader("Cumulative Incremental Supply")
    st.plotly_chart(plot_cumulative_supply(lng_df), use_container_width=True)

elif page == "Forecasting":
    st.header("Forecasting Canada Marketable Gas Production")

    # ---------- Section A: Model Comparison ----------
    st.subheader("Model Comparison: SARIMA vs Prophet")
    fig_forecast = plot_forecast_comparison(sarima_df, prophet_df)
    st.plotly_chart(fig_forecast)

    # ---------- Section B: Historical + Forecast ----------
    st.subheader("Historical Production + Forecast")
    fig_hist_forecast = plot_forecast_with_history(production_df, sarima_df, prophet_df)
    st.plotly_chart(fig_hist_forecast)
    
    # ---------- Section C: Supply Gap Projection ----------
    st.subheader("Supply Gap Projection")
    fig_gap = plot_forecast_supply_gap(forecast_results)  # 這裡用 forecast_results.csv
    st.plotly_chart(fig_gap)

elif page == "Limitations & Assumptions":
    st.title("Limitations & Assumptions")
    st.info("""
            This dashboard is designed for exploratory analysis and educational purposes.
            It should not be used as the sole basis for investment or operational decisions.
            """)
    
    with st.expander("Data Limitations", expanded=True):
        st.markdown("""
                    The analysis is based on monthly marketable natural gas production data reported by the Canada Energy Regulator (CER), spanning 2000 to 2025. Data is available in both million cubic feet per day (mmcfd) and thousand cubic meters per day (10³ m³/d).
                    - Production data is annual and may mask short-term volatility
                    - Historical revisions by statistical agencies are not incorporated
                    - Data represents marketable production only
                    - Unit conversions (10³ m³/d ↔ mtpa) introduce minor approximation errors
                    """)

    with st.expander("Methodological Assumptions"):
        st.markdown("""
                    Based on **a ±3% threshold** of Year-over-Year (YoY) growth:
                    """)
        st.table(regime_table)
        st.markdown("""
                    Note: This threshold is arbitrary and may not capture subtle trends.
                    """)
        st.markdown("""
                    - Rolling averages smooth short-term fluctuations
                    - Structural breaks are identified based on major market events
                    - Change-point detection was performed using the PELT algorithm (rpt.Pelt(model="rbf")). Sensitivity of detection was controlled via the penalty parameter (pen=1). Full formal statistical validation across all periods was not performed.
                    """)

    with st.expander("Forecasting Uncertainty"):
        st.markdown("""
                    - Forecasts assume continuation of historical production dynamics
                    - No explicit modeling of future project sanctions
                    - Price-driven supply responses are not incorporated
                    """)

    with st.expander("LNG Supply Analysis Constraints"):
        st.markdown("""
                    - LNG Canada Phase 1 demand treated as fixed capacity
                    - Pipeline constraints are not considered
                    - Domestic consumption and export competition are excluded
                    - Supply adequacy does not imply deliverability at specific hubs
                    """)

    with st.expander("External Risk Factors"):
        st.markdown("""
                    - Commodity price volatility
                    - Policy and regulatory changes
                    - Technological developments
                    - Global LNG market dynamics
                    - Geopolitical disruptions
                    """)