import sys
from pathlib import Path

# --------------------------
# Project Root for src imports
# --------------------------
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from src.data_loader import load_monthly
from src.unit_converter import convert_units
from src.plot_helpers import add_structural_breaks, classify_regime


import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

# =========================
# Utility Functions
# =========================
def convert_lng_demand(lng_mtpa, unit):
    if unit == "mtpa":
        return lng_mtpa
    elif unit == "mmcfd":
        return lng_mtpa * 1e6 / 365 / 0.0283168
    elif unit == "bcm/year":
        return lng_mtpa / 0.73
    elif unit == "e3m3d":
        return lng_mtpa * 1e6 / 365 / 0.73

# --------------------------
# Load CSVs
# --------------------------
@st.cache_data
def load_data():
    base = ROOT / "data/processed/app_data"
    return {
        "monthly": load_monthly(),
        "forecast": pd.read_csv(DATA_PATH / "forecast_results.csv"),
        "breaks": pd.read_csv(DATA_PATH / "structural_breaks.csv"),
    }

data = load_data()


# --------------------------
# Sidebar Navigation
# --------------------------
page = st.sidebar.radio(
    "Page",
    ["Historical Production Overview", "Forecasting Analysis", "Limitations & Assumptions"]
)

# =========================
# Page Routing
# =========================
if page == "Historical Production Overview":

    st.header("Historical Production Overview")

    df_m = data["monthly"].copy()
    df_m["ds"] = pd.to_datetime(df_m["ds"])

    # =========================
    # Layout
    # =========================
    left, right = st.columns([1, 3])

    # =========================
    # LEFT: Scenario Control
    # =========================
    with left:
        st.subheader("Scenario Control")
        st.divider()
        
        mode = st.selectbox(
            "Perspective",
            ["Business (mtpa)", "Engineering (e3m3d)", "Market/Policy (bcm/year)"]
        )
        
        # =========================
        # # Mode config (single source of truth)
        # # =========================
        if mode == "Business (mtpa)":
            unit = "mtpa"
            lng_demand = st.slider("LNG Demand (mtpa)", 0.0, 40.0, 14.0)
        
        elif mode == "Engineering (e3m3d)":
            unit = "e3m3d"
            lng_demand = st.slider("LNG Demand (e3m3d)", 0.0, 20000.0, 8000.0)
        
        elif mode == "Market/Policy (bcm/year)":
            unit = "bcm/year"
            lng_demand = st.slider("LNG Demand (bcm/year)", 0.0, 200.0, 50.0)

        with st.expander("Historical Context"):
            st.markdown("""
                        - 2005: Early shale development  
                        - 2010: US shale boom  
                        - 2015: Oil price crash  
                        - 2020: COVID-19 demand shock  
                        """)

    # =========================
    # DATA PREP
    # =========================
    df_m["value"] = convert_units(df_m["Production_e3m3d"], unit)

    # annual from monthly
    df_a = (
        df_m
        .groupby(df_m["ds"].dt.year)["value"]
        .mean()
        .reset_index()
    )
    df_a.columns = ["Year", "value"]
    df_a["ds"] = pd.to_datetime(df_a["Year"].astype(str) + "-01-01")

    # KPI 計算
    max_prod = df_a["value"].max()
    worst_gap = (df_a["value"] - lng_demand).min()

    # =========================
    # RIGHT: KPI + Chart
    # =========================
    with right:

        # -------- KPI ROW --------
        k1, k2, k3 = st.columns(3)

        k1.metric("LNG Demand", f"{lng_demand:.1f} {unit}")
        k2.metric("Max Production", f"{max_prod:.1f} {unit}")
        k3.metric("Worst Gap", f"{worst_gap:.1f} {unit}")

        # -------- MAIN CHART --------
        fig = go.Figure()

        # Monthly
        fig.add_trace(go.Scatter(
            x=df_m["ds"],
            y=df_m["value"],
            name="Monthly",
            opacity=0.4
        ))

        # Annual
        fig.add_trace(go.Scatter(
            x=df_a["ds"],
            y=df_a["value"],
            name="Annual",
            line=dict(width=3)
        ))

        # Change-points
        break_years = data["breaks"]["Year"].dropna().astype(int).tolist()
        
        first = True
        
        for y in break_years:
            fig.add_trace(go.Scatter(
                x=[pd.to_datetime(f"{int(y)}-01-01")] * 2,
                y=[df_m["value"].min(), df_m["value"].max()],
                mode="lines",
                line=dict(color="purple", dash="dash"),
                name="Change-point" if first else None,
                showlegend=first,
                legendgroup="cp",
                hoverinfo="skip"
            ))
            first = False

        # LNG Demand line
        fig.add_trace(go.Scatter(
            x=df_a["ds"],
            y=[lng_demand] * len(df_a),
            name="LNG Demand",
            line=dict(color="red", dash="dash")
        ))

        fig.update_layout(
            legend=dict(
                orientation="v",
                x=1.02,
                y=0,
                xanchor="left",
                yanchor="bottom"
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        

    # =====================
    # YoY
    # =====================
    st.subheader("Year-over-Year Growth Regime")

    left, right = st.columns([3, 1])
    
    with right:
        st.subheader("Scenario Control")
        st.divider()
        threshold = st.slider("YoY Threshold (%)", 0, 10, 3)
    
    with left:
        df_regime = df_a.sort_values("ds").copy()
        df_regime["YoY_pct"] = df_regime["value"].pct_change() * 100
        
        df_regime = classify_regime(
            df_regime,
            value_col="value",
            threshold=threshold
            )
        
        color_map = {
            "Growth": "green",
            "Decline": "red",
            "Stagnation": "gray",
            "NA": "lightgray"
            }
        
        fig2 = go.Figure()
        
        fig2.add_bar(
            x=df_regime["ds"],
            y=df_regime["YoY_pct"],
            marker_color=df_regime["Regime"].map(color_map)
        )
        
        st.plotly_chart(fig2, use_container_width=True)


elif page == "Forecasting Analysis":

    st.header("Forecasting Analysis")

    df = data["forecast"].copy()
    df["ds"] = pd.to_datetime(df["ds"])

    # =========================
    # Sidebar Controls
    # =========================
    left, right = st.columns([1, 3])

    with left:
        st.subheader("Scenario Control")
        st.divider()

        model_select = st.multiselect(
            "Select Models",
            ["Historical", "Prophet", "SARIMA"],
            default=["Historical", "Prophet"]
        )

        show_ci = st.checkbox("Show Confidence Interval", True)

        view_mode = st.radio(
            "View Mode",
            ["Total Production", "Incremental Supply"]
        )

        lng_demand = st.slider(
            "LNG Canada Phase 1 Demand (mtpa)",
            0.0, 40.0, 14.0
        )

    # =========================
    # Baseline (AUTO)
    # =========================
    baseline_2025 = (
        df[(df["ds"].dt.year == 2025) & (df["model"] == "Historical")]
        ["yhat"]
        .mean()
    )

    # =========================
    # Plot
    # =========================
    with right:
        fig = go.Figure()
        
        for m in model_select:
            sub = df[df["model"] == m].copy()
            
            # Incremental mode
            if view_mode == "Incremental Supply":
                sub["yhat"] = sub["yhat"] - baseline_2025
                
                if "yhat_upper" in sub.columns:
                    sub["yhat_upper"] = sub["yhat_upper"] - baseline_2025
                    sub["yhat_lower"] = sub["yhat_lower"] - baseline_2025

            # Main line
            fig.add_trace(go.Scatter(
                x=sub["ds"],
                y=sub["yhat"],
                mode="lines",
                name=m
            ))

            # Confidence Interval
            if show_ci and m != "Historical":

                if "yhat_upper" in sub.columns:

                    fig.add_trace(go.Scatter(
                        x=sub["ds"],
                        y=sub["yhat_upper"],
                        line=dict(width=0),
                        showlegend=False,
                        hoverinfo='skip'
                 ))

                    fig.add_trace(go.Scatter(
                        x=sub["ds"],
                        y=sub["yhat_lower"],
                        fill="tonexty",
                        opacity=0.2,
                        name=f"{m} CI"
                    ))

        # =========================
        # LNG Demand Line
        # =========================
        if view_mode == "Total Production":
            fig.add_hline(
                y=lng_demand,
                line_dash="dash",
                line_color="red",
                annotation_text="LNG Demand"
            )

        elif view_mode == "Incremental Supply":
            fig.add_hline(
                y=lng_demand,
                line_dash="dash",
                line_color="red",
                annotation_text="Required Increment"
                )
            
            fig.add_hline(
                y=0,
                line_color="black"
                )

        # =========================
        # Layout
        # =========================
        fig.update_layout(
            title="Forecast Comparison (Prophet vs SARIMA)",
            xaxis_title="Year",
            yaxis_title="Production (mtpa)", 
            legend=dict(
                orientation="v",
                x=1.02,
                y=1
                )
            )
        
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # Insight Box）
    # =========================
    st.markdown("### Key Insight")

    if view_mode == "Incremental Supply":
        st.info("""
        Incremental view isolates **new supply growth beyond 2025 baseline**.
        
        This reveals whether future production expansion alone can meet LNG demand,
        rather than being masked by large historical production levels.
        """)

    else:
        st.info("""
        Total production view shows overall supply trajectory,
        but may overstate supply adequacy due to large existing baseline.
        """)

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
        regime_table = pd.DataFrame({
            "Regime": ["Growth", "Stagnation", "Decline"],
            "Definition": [
                "YoY > +threshold",
                "-threshold ≤ YoY ≤ +threshold",
                "YoY < -threshold"
                ]
                })
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
