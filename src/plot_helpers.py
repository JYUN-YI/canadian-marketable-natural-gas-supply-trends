import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def plot_production(df):
    fig = px.line(df, x="Year", y="Production_mtpa",
                  title="Canada Gas Production Over Years")
    fig.update_traces(mode="lines+markers")
    return fig

def plot_yoy(df):
    fig = px.bar(df, x="Year", y="YoY_pct",
                 title="Year-over-Year % Change")
    return fig

def plot_production_with_breaks(
    prod_df: pd.DataFrame,
    breaks_df: pd.DataFrame
) -> go.Figure:
    """
    Plot production trend with structural break annotations
    """

    fig = go.Figure()

    # Production curve
    fig.add_trace(
        go.Scatter(
            x=prod_df["Year"],
            y=prod_df["Production_mtpa"],
            mode="lines+markers",
            name="Production",
            line=dict(width=3)
        )
    )

    # Add structural break lines
    for _, row in breaks_df.iterrows():
        fig.add_vline(
            x=row["Year"],
            line_dash="dot",
            line_color="red",
            line_width=2,
            annotation_text=f"{row['Year']} — {row['Event']}",
            annotation_position="top"
        )

    fig.update_layout(
        title="Production Trend with Structural Breaks",
        xaxis_title="Year",
        yaxis_title="Production (mtpa)",
        template="plotly_white"
    )

    return fig

def plot_lng_supply_gap(df):
    fig = px.line(df, x="Year", y="Supply_Gap",
                  title="LNG Supply Gap Over Time")
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    return fig

def plot_incremental_vs_demand(df):
    fig = px.line(
        df,
        x="Year",
        y="Incremental_Supply",
        markers=True,
        title="Incremental Supply vs LNG Phase 1 Demand"
    )

    fig.add_hline(
        y=14,
        line_dash="dash",
        line_color="red",
        annotation_text="LNG Phase 1 Demand (14 mtpa)"
    )

    fig.update_layout(
        yaxis_title="Incremental Supply (mtpa)",
        template="plotly_white"
    )
    return fig

def plot_supply_gap(df):
    fig = px.bar(
        df,
        x="Year",
        y="Supply_Gap",
        color="Supply_Gap",
        color_continuous_scale=["red", "yellow", "green"],
        title="Supply Gap vs LNG Phase 1"
    )

    fig.add_hline(y=0, line_dash="dash")

    fig.update_layout(
        yaxis_title="Supply Gap (mtpa)",
        template="plotly_white"
    )
    return fig

def plot_cumulative_supply(df):
    df = df.copy()
    df["Cumulative_Supply"] = df["Incremental_Supply"].cumsum()

    fig = px.area(
        df,
        x="Year",
        y="Cumulative_Supply",
        title="Cumulative Incremental Supply"
    )

    fig.update_layout(
        yaxis_title="Cumulative mtpa",
        template="plotly_white"
    )
    return fig

def plot_forecast(df):
    fig = px.line(df, x="Year", y="Forecast_mtpa", markers=True,
                  title="Forecasted Production 2026-2030")
    fig.add_scatter(x=df["Year"], y=df["Supply_Gap"], mode="lines+markers", name="Supply Gap")
    return fig

def plot_forecast_comparison(sarima_df: pd.DataFrame, prophet_df: pd.DataFrame) -> go.Figure:

    fig = go.Figure()

    # SARIMA
    fig.add_trace(
        go.Scatter(
            x=sarima_df["Year"],
            y=sarima_df["Forecast_mtpa"],
            mode="lines+markers",
            name="SARIMA",
            line=dict(color="blue"),
            marker=dict(symbol="circle", size=8)
        )
    )

    # Prophet
    fig.add_trace(
        go.Scatter(
            x=prophet_df["Year"],
            y=prophet_df["Forecast_mtpa"],
            mode="lines+markers",
            name="Prophet",
            line=dict(color="orange", dash="dash"),
            marker=dict(symbol="diamond", size=8)
        )
    )

    # Layout
    fig.update_layout(
        title="SARIMA vs Prophet Forecast Comparison",
        xaxis_title="Year",
        yaxis_title="Production (mtpa)",
        legend=dict(title="Model", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white",
        hovermode="x unified"
    )

    return fig

def plot_forecast_with_history(prod_df: pd.DataFrame, forecast_sarima: pd.DataFrame, forecast_prophet: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # Historical
    fig.add_trace(go.Scatter(
        x=prod_df["Year"],
        y=prod_df["Production_mtpa"],
        mode="lines+markers",
        name="Historical",
        line=dict(width=3)
    ))
    # SARIMA forecast
    fig.add_trace(go.Scatter(
        x=forecast_sarima["Year"],
        y=forecast_sarima["Forecast_mtpa"],
        mode="lines+markers",
        name="SARIMA Forecast",
        line=dict(color="blue")
    ))
    # Prophet forecast
    fig.add_trace(go.Scatter(
        x=forecast_prophet["Year"],
        y=forecast_prophet["Forecast_mtpa"],
        mode="lines+markers",
        name="Prophet Forecast",
        line=dict(color="orange", dash="dash")
    ))
    fig.update_layout(
        title="Historical + Forecasted Production",
        xaxis_title="Year",
        yaxis_title="Production (mtpa)",
        template="plotly_white"
    )
    return fig

def plot_forecast_supply_gap(forecast_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=forecast_df["Year"],
        y=forecast_df["Supply_Gap"],
        name="Supply Gap",
        marker_color=["red" if v < 0 else "green" for v in forecast_df["Supply_Gap"]]
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="black")
    fig.update_layout(
        title="Forecasted LNG Supply Gap vs Phase 1 Demand",
        xaxis_title="Year",
        yaxis_title="Supply Gap (mtpa)"
    )
    return fig