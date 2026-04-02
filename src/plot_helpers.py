import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# =========================
# Structural Breaks Helper
# =========================
def add_structural_breaks(fig, years, color="purple"):
    """
    Add vertical lines aligned to datetime axis.
    Ensures correct alignment with Plotly time axis.
    """

    for year in years:
        fig.add_vline(
            x=pd.to_datetime(f"{year}-01-01"),
            line_dash="dot",
            line_color=color,
            opacity=0.8
        )

    return fig

# =========================
# YoY regime helper
# =========================
def classify_regime(df, value_col="Production_mtpa", threshold=3):
    df = df.copy()

    df["YoY_pct"] = df[value_col].pct_change() * 100

    def rule(x):
        if pd.isna(x):
            return "NA"
        if x > threshold:
            return "Growth"
        elif x < -threshold:
            return "Decline"
        return "Stagnation"

    df["Regime"] = df["YoY_pct"].apply(rule)

    return df
