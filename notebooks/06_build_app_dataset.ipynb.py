import pandas as pd
import numpy as np

# =========================
# PATHS
# =========================
BASE_PATH = "/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends"
DATA_PATH = f"{BASE_PATH}/data/processed/app_data"

RAW_PATH = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2000_25_103m3d.csv"

# =========================
# LOAD RAW DATA
# =========================
df = pd.read_csv(RAW_PATH)
df = df[df["Province"] == "Canada Total"].copy()

# Month conversion
if df["Month"].dtype == object:
    df["Month"] = pd.to_datetime(df["Month"], format="%B").dt.month

# datetime index
df["ds"] = pd.to_datetime(dict(year=df["Year"], month=df["Month"], day=1))

# =========================
# BASE UNIT (mtpa)
# =========================
df["Production_mtpa"] = (
    df["Production_e3m3d"] * 365 / 1_000_000 * 0.73
)

# =========================
# SAVE MONTHLY
# =========================
df.to_csv(f"{DATA_PATH}/production_monthly.csv", index=False)
print("✅ production_monthly.csv saved")

# =========================
# ANNUAL (FIXED: sum not mean)
# =========================
annual_df = (
    df.groupby("Year", as_index=False)
    .agg({"Production_mtpa": "sum"})
)

# YoY
annual_df["YoY_pct"] = annual_df["Production_mtpa"].pct_change() * 100

# =========================
# LNG ANALYSIS
# =========================
LNG_PHASE1_MTPA = 14

baseline_2025 = annual_df.loc[
    annual_df["Year"] == 2025, "Production_mtpa"
].values[0]

annual_df["Incremental_Supply"] = (
    annual_df["Production_mtpa"] - baseline_2025
)

annual_df["Supply_Gap"] = (
    annual_df["Incremental_Supply"] - LNG_PHASE1_MTPA
)

annual_df.to_csv(f"{DATA_PATH}/production_master.csv", index=False)
print("✅ production_master.csv saved")

# =========================
# HISTORICAL (FOR OVERLAY)
# =========================
hist_df = df[["ds", "Production_mtpa"]].copy()
hist_df.rename(columns={"Production_mtpa": "yhat"}, inplace=True)

hist_df["yhat_lower"] = np.nan
hist_df["yhat_upper"] = np.nan
hist_df["model"] = "Historical"
hist_df["type"] = "historical"

hist_df.to_csv(f"{DATA_PATH}/historical.csv", index=False)
print("✅ historical.csv saved")

# =========================
# LOAD FORECASTS
# =========================

# -------------------------
# Prophet
# -------------------------
prophet_df = pd.read_csv(f"{DATA_PATH}/prophet_full.csv")

prophet_df = prophet_df[[
    "ds", "yhat", "yhat_lower", "yhat_upper"
]]

prophet_df["model"] = "Prophet"
prophet_df["type"] = "forecast"

prophet_df.to_csv(
    f"{DATA_PATH}/forecast_prophet_full.csv",
    index=False
)
print("✅ forecast_prophet_full.csv saved")

# -------------------------
# SARIMA
# -------------------------
sarima_df = pd.read_csv(f"{DATA_PATH}/sarima_full.csv")

sarima_df = sarima_df.rename(columns={
    "predicted_mean": "yhat"
})

# ensure CI exists
if "yhat_lower" not in sarima_df.columns:
    sarima_df["yhat_lower"] = np.nan
    sarima_df["yhat_upper"] = np.nan

sarima_df["model"] = "SARIMA"
sarima_df["type"] = "forecast"

sarima_df.to_csv(
    f"{DATA_PATH}/forecast_sarima_full.csv",
    index=False
)
print("✅ forecast_sarima_full.csv saved")

# =========================
# COMBINE FORECASTS
# =========================
combined = pd.concat([
    hist_df,
    prophet_df,
    sarima_df
], ignore_index=True)

combined["ds"] = pd.to_datetime(combined["ds"])
combined = combined.sort_values("ds")

combined.to_csv(
    f"{DATA_PATH}/forecast_results.csv",
    index=False
)

print("✅ forecast_results.csv saved (FINAL)")

# =========================
# STRUCTURAL BREAKS (FIXED & STABLE)
# =========================

# Use YoY volatility instead of hardcoding years
annual_df["YoY_abs"] = annual_df["YoY_pct"].abs()

threshold = annual_df["YoY_abs"].quantile(0.90)

breaks_df = annual_df[
    annual_df["YoY_abs"] >= threshold
][["Year"]].drop_duplicates()

breaks_df.to_csv(
    f"{DATA_PATH}/structural_breaks.csv",
    index=False
)

print("✅ structural_breaks.csv saved")
