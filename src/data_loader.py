import pandas as pd
from pathlib import Path

# --------------------------
# Paths
# --------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed" / "app_data"

# --------------------------
# Load Functions
# --------------------------
def load_production_data() -> pd.DataFrame:
    """
    Load historical production data
    """
    return pd.read_csv(DATA_DIR / "production_master.csv")


def load_lng_data() -> pd.DataFrame:
    """
    Load LNG supply analysis
    """
    return pd.read_csv(DATA_DIR / "lng_supply_demand.csv")

def load_structural_breaks() -> pd.DataFrame:
    """
    Load structural break / change point data
    """
    return pd.read_csv(DATA_DIR / "structural_breaks.csv")

def load_forecast_sarima() -> pd.DataFrame:
    """
    Load SARIMA forecast results
    """
    return pd.read_csv(DATA_DIR / "forecast_sarima.csv")

def load_forecast_prophet() -> pd.DataFrame:
    """
    Load Prophet forecast results
    """
    return pd.read_csv(DATA_DIR / "forecast_prophet.csv")

def load_forecast_results() -> pd.DataFrame:
    """
    Load forecast results
    """
    return pd.read_csv(DATA_DIR / "forecast_results.csv")