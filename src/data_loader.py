import pandas as pd
from pathlib import Path

# --------------------------
# Paths
# --------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed" / "app_data"

# --------------------------
# Load Functions
# --------------------------
def standardize_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip()

    if "Year" in df.columns:
        df["ds"] = pd.to_datetime(df["Year"].astype(str) + "-01-01")

    if "ds" in df.columns:
        df["ds"] = pd.to_datetime(df["ds"])

    return df

def load_monthly():
    df = pd.read_csv(DATA_DIR / "production_monthly.csv")
    return standardize_data(df)

def load_annual():
    df = pd.read_csv(DATA_DIR / "production_master.csv")
    return standardize_data(df)
