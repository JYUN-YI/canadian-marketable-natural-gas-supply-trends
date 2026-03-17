# Databricks notebook source
# MAGIC %pip install streamlit

# COMMAND ----------

# MAGIC %pip install openpyxl
# MAGIC
# MAGIC %pip install ruptures

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

import sys
from pathlib import Path
import pandas as pd

BASE_PATH = Path("/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends")
sys.path.append(str(BASE_PATH))

from src.data_processor import (
    read_mmcfd_2023_25,
    read_mmcfd_2000_25,
    read_e3m3d_2023_25,
    read_e3m3d_2000_25
)

# =========================
# 1. Setup paths
# =========================
BASE_PATH = "/Workspace/Users/kimjylin@gmail.com/ca_gas_supply_trends"
RAW_FILE = f"{BASE_PATH}/data/raw/canadian-marketable-natural-gas-productions.XLSX"

OUTPUT_23_25_mmcfd = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2023_25_mmcfd.csv"
OUTPUT_2000_25_mmcfd = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2000_25_mmcfd.csv"
OUTPUT_23_25_e3m3d = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2023_25_103m3d.csv"
OUTPUT_2000_25_e3m3d = f"{BASE_PATH}/data/processed/canadian_marketable_gas_2000_25_103m3d.csv"

# =========================
# 2. Read and tidy
# =========================
df_23_25_mmcfd = read_mmcfd_2023_25(RAW_FILE)
df_2000_25_mmcfd = read_mmcfd_2000_25(RAW_FILE)
df_23_25_e3m3d = read_e3m3d_2023_25(RAW_FILE)
df_2000_25_e3m3d = read_e3m3d_2000_25(RAW_FILE)

# =========================
# 3. Save to CSV
# =========================
df_23_25_mmcfd.to_csv(OUTPUT_23_25_mmcfd, index=False, encoding="utf-8-sig")
df_2000_25_mmcfd.to_csv(OUTPUT_2000_25_mmcfd, index=False, encoding="utf-8-sig")
df_23_25_e3m3d.to_csv(OUTPUT_23_25_e3m3d, index=False, encoding="utf-8-sig")
df_2000_25_e3m3d.to_csv(OUTPUT_2000_25_e3m3d, index=False, encoding="utf-8-sig")

print(f"Saved 2000–25-mmcfd data: {OUTPUT_2000_25_mmcfd}")
print(f"Saved 2023–25-mmcfd data: {OUTPUT_23_25_mmcfd}")
print(f"Saved 2000–25-e3m3d data: {OUTPUT_2000_25_e3m3d}")
print(f"Saved 2023–25-e3m3d data: {OUTPUT_23_25_e3m3d}")