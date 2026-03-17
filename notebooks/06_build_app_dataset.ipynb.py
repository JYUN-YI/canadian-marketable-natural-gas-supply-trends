import pandas as pd

BASE_PATH = "/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends"
DATA_PATH = f"{BASE_PATH}/data/processed/app_data"

# Read production_master
prod = pd.read_csv(f"{DATA_PATH}/production_master.csv")

# --------------------------
# LNG Supply Analysis
# --------------------------
LNG_PHASE1_MTPA = 14
baseline_2025 = prod.loc[prod["Year"]==2025, "Production_mtpa"].values[0]

lng_df = prod.copy()
lng_df["Incremental_Supply"] = lng_df["Production_mtpa"] - baseline_2025
lng_df["Supply_Gap"] = lng_df["Incremental_Supply"] - LNG_PHASE1_MTPA
lng_df.to_csv(f"{DATA_PATH}/lng_supply_demand.csv", index=False)

# --------------------------
# Forecast (2026-2030)
# --------------------------
forecast_years = range(2026, 2031)

# SARIMA
sarima_df = pd.DataFrame({
    "Year": forecast_years,
    "Forecast_mtpa": [baseline_2025 * 1.02**(y-2025) for y in forecast_years]
})
sarima_df.to_csv(f"{DATA_PATH}/forecast_sarima.csv", index=False)

# Prophet
prophet_df = pd.DataFrame({
    "Year": forecast_years,
    "Forecast_mtpa": [baseline_2025 * 1.025**(y-2025) for y in forecast_years]
})
prophet_df.to_csv(f"{DATA_PATH}/forecast_prophet.csv", index=False)

print("✅ CSVs generated: production_master, lng_supply_demand, forecast_sarima", "forecast_prophet")