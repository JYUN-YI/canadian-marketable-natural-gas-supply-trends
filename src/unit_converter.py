# unit_converter.py

import pandas as pd

def e3m3d_to_mtpa(df, col="Production_e3m3d", new_col="Production_mtpa"):
    DAYS_PER_YEAR = 365
    M3_PER_E3M3 = 1000
    M3_PER_BCM = 1e9
    
    # LNG industry benchmark
    BCM_PER_MTPA = 1.36   # 1 mtpa ≈ 1.36 bcm/year

    bcm_per_year = df[col] * M3_PER_E3M3 * DAYS_PER_YEAR / M3_PER_BCM
    mtpa = bcm_per_year / BCM_PER_MTPA
    df[new_col] = mtpa
    return df

def calculate_yoy_mtpa(df, col="Production_mtpa"):
    """
    Calculate Year-over-Year increment in mtpa.
    """
    df = df.copy()
    df["YoY_mtpa"] = df[col].diff()
    return df
    return df

def classify_growth(x, threshold_growth=4):
    """
    Classify YoY growth into Growth, Decline, Stagnation
    """
    if x > threshold_growth:
        return "Growth"
    elif x < -threshold_growth:
        return "Decline"
    else:
        return "Stagnation"

def add_yoy_regime(df, col="YoY_mtpa", threshold=4):
    """
    Add a new column 'YoY_Regime' to classify growth.
    """
    df = df.copy()
    df["YoY_Regime"] = df[col].apply(lambda x: classify_growth(x, threshold))
    return df
