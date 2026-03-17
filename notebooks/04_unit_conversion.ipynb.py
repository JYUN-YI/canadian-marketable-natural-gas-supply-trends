# Databricks notebook source
# MAGIC %md
# MAGIC ## 04. Unit Conversion

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

import sys
sys.path.append("/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends/src")
from unit_converter import e3m3d_to_mtpa, calculate_yoy_mtpa, add_yoy_regime, classify_growth
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# COMMAND ----------

BASE_PATH = "/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends"
CSV_FILE = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2000_25_103m3d.csv"

df = pd.read_csv(CSV_FILE)
df.head()

# COMMAND ----------

# MAGIC %md
# MAGIC We focus on Canada Total to analyze national-level structural trends rather than regional fluctuations.

# COMMAND ----------

# Keep Canada Total only
annual_df = df[df["Province"] == "Canada Total"].copy()

# If Month is string, convert to numeric
if annual_df["Month"].dtype == object:
    annual_df["Month"] = pd.to_datetime(annual_df["Month"], format='%B').dt.month

# Create datetime for monthly plotting if needed
annual_df["Date"] = pd.to_datetime(dict(year=annual_df["Year"], month=annual_df["Month"], day=1))
annual_df = annual_df.sort_values("Date").reset_index(drop=True)

annual_df.head()

# COMMAND ----------

# Annual aggregation
annual_df = annual_df.groupby("Year")["Production_e3m3d"].mean().reset_index()

annual_df.head()

# COMMAND ----------

annual_df = e3m3d_to_mtpa(annual_df)
annual_df = calculate_yoy_mtpa(annual_df)
annual_df = add_yoy_regime(annual_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Unit conversion: e3m³/d → mtpa
# MAGIC
# MAGIC To directly compare Canadian natural gas production with LNG export capacity (reported in mtpa), daily production volumes (e3m³/d) are converted into million tonnes per annum (mtpa) using an industry-standard LNG conversion factor.
# MAGIC
# MAGIC Original Data: Daily production in thousands of cubic meters of natural gas
# MAGIC
# MAGIC Conversion Steps:
# MAGIC - Step 1: Convert "thousands of cubic meters" (e3m³) to cubic meters (m³).
# MAGIC - Step 2: Convert daily production to annual production by multiplying by 365 days.
# MAGIC - Step 3: Convert annual production (m³/year) into LNG-equivalent million tonnes per annum (mtpa) using an industry benchmark of 1 mtpa ≈ 1.36 bcm/year.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Compare to LNG Canada Phase 1 demand

# COMMAND ----------

# MAGIC %md
# MAGIC LNG Canada's Phase 1 demand is approximately 14 million tonnes per annum.

# COMMAND ----------

LNG_PHASE1_MTPA = 14

# COMMAND ----------

# MAGIC %md
# MAGIC This is the annual gas volume required by LNG Canada Phase 1. Comparing production increments with this number shows whether Canada’s new production each year is enough to support the LNG project

# COMMAND ----------

# Check if production is enough to meet LNG demand
annual_df["Above_LNG_Demand"] = annual_df["Production_mtpa"] >= LNG_PHASE1_MTPA
print("Recent years production vs LNG Canada Phase 1 demand:")
print(annual_df[["Year", "Production_mtpa", "Above_LNG_Demand"]].tail(10))

# COMMAND ----------

colors = annual_df["Above_LNG_Demand"].map({True: "green", False: "red"})

plt.figure(figsize=(12,5))

# 1. Total production as bar (with color indicating above/below LNG demand)
plt.bar(
    annual_df["Year"],
    annual_df["Production_mtpa"],
    color=colors,
    alpha=0.6,
    label="Total Production"
)

# 2. Overlay line for production trend
plt.plot(
    annual_df["Year"],
    annual_df["Production_mtpa"],
    marker="o",
    color="black",
    linewidth=2,
    label="Production Trend"
)

# 3. Red dashed line for LNG Phase 1 demand
plt.axhline(
    LNG_PHASE1_MTPA,
    color="red",
    linestyle="--",
    label="LNG Canada Phase 1 (~14 million tonnes per annum)"
)

plt.title("Canada Natural Gas Production vs LNG Canada Phase 1 Demand")
plt.xlabel("Year")
plt.ylabel("Production (mtpa)")
plt.grid(True)

# Merge legends for bar, line, and reference
plt.legend()
plt.show()


# COMMAND ----------

# MAGIC %md
# MAGIC Each bar represents total annual marketable natural gas production in Canada. 
# MAGIC The red dashed line indicates the estimated LNG Canada Phase 1 feedgas requirement (~14 million tonnes per annum). 
# MAGIC Green bars highlight years in which production levels were above this benchmark. 
# MAGIC
# MAGIC While total production may exceed the LNG requirement in many years, actual LNG feasibility depends on the availability of incremental surplus relative to **domestic consumption** and **export commitments**.
# MAGIC

# COMMAND ----------

def classify_growth(x):
    if x > 3:
        return "Growth"
    elif x < -3:
        return "Decline"
    else:
        return "Stagnation"

annual_df["YoY_Regime"] = annual_df["YoY_mtpa"].apply(classify_growth)

color_map = {
    "Growth": "green",
    "Stagnation": "gray",
    "Decline": "red"
}
colors = annual_df["YoY_Regime"].map(color_map)

fig, ax1 = plt.subplots(figsize=(12,5))

# Total production (level)
ax1.plot(
    annual_df["Year"],
    annual_df["Production_mtpa"],
    color="black",
    marker="o",
    label="Total Production"
)
ax1.set_ylabel("Production (mtpa)")
ax1.set_xlabel("Year")

# YoY increment bars (growth)
ax2 = ax1.twinx()
ax2.bar(
    annual_df["Year"],
    annual_df["YoY_mtpa"],
    color=colors,
    alpha=0.7,
    # label="YoY Production Growth"
)
ax2.set_ylabel("Year-over-Year Production Growth (mtpa)")

# 🔴 LNG Canada Phase 1 demand line (increment benchmark)
ax2.axhline(
    LNG_PHASE1_MTPA,
    color="red",
    linestyle="--",
    linewidth=2,
    label="LNG Canada Phase 1 Demand"
)

# Legends
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

regime_patches = [
    Patch(facecolor="green", label="Growth"),
    Patch(facecolor="gray", label="Stagnation"),
    Patch(facecolor="red", label="Decline")
]

ax1.legend(
    handles=handles1 + handles2 + regime_patches,
    labels=labels1 + labels2 + [p.get_label() for p in regime_patches],
    loc="lower right"
)

plt.title("Canada Gas Production (mtpa) vs Annual Growth")
plt.grid(True)
plt.show()


# COMMAND ----------

# MAGIC %md
# MAGIC The black line shows total annual gas production in Canada, revealing the long-term trend. The bars show the year-over-year change, i.e., how production increased or decreased compared with the previous year Together, the chart helps us see both the overall scale of production and the year-to-year growth, and which years experienced strong growth, decline, or stagnation.

# COMMAND ----------

annual_df["YoY_mtpa"].std()