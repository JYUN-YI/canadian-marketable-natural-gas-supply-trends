# 🛢️ Canadian Marketable Natural Gas Supply Trends

## 📌 Project Objective

## 🏗️ Project Structure
```bash
📦 ca_gas_supply_trends/
│
├── data/
│   ├── raw/                  
│   │   └── canadian-marketable-natural-gas-productions.XLSX
│   └── processed/           
│       ├── canadian_marketable_gas_2000_25_mmcfd.csv
│       ├── canadian_marketable_gas_2000_25_103m3d.csv
│       ├── canadian_marketable_gas_2023_25_mmcfd.csv
│       ├── canadian_marketable_gas_2023_25_103m3d.csv
│       │
│       └── app_data/   
│           ├── forecast_results.csv
│           ├── forecast_prophet.csv
│           ├── forecast_sarima.csv
│           ├── lng_supply_demand.csv
│           ├── production_master.csv
│           └── structural_breaks.csv
│
├── notebooks/             
│   ├── 01_data_prep.ipynb    
│   ├── 02_EDA.ipynb                # Descriptive analysis, trends, CAGR
│   ├── 03_structural_change.ipynb  # Rolling, change-point analysis
│   ├── 04_unit_conversion.ipynb    # e3m3/d to mtpa
│   ├── 05_forecasting.ipynb        # SARIMA / Prophet forecasting
│   └── 06_build_app_dataset.csv
│
├── src/  
│   ├── __init__.py            
│   ├── data_loader.py                     
│   ├── data_processor.py     # Cleaning, calculating CAGR, and rolling logic
│   ├── unit_converter.py     # Unit conversion functions
│   └── plot_helpers.py       # Reusable plotting functions
│
├── app/
│   └── streamlit_app.py
│
├── outputs/                 
│   ├── Canadian_Natural_Gas_Production_Trends_Upstream_Capacity_LNG_Canada_Phase1.pptx
│   └── Canadian_Natural_Gas_Production_Trends_Upstream_Capacity_LNG_Canada_Phase1.pdf
│
├── requirements.txt
├── README.md            
└── .gitignore
```
## 🔍 Exploratory Data Analysis (EDA)

## ⏳ Time Series Models

## 🔑 Feature Importance Analysis

## 🚀 Interactive Application

## ⚙️ Technologies Used
- Programming Language: Python
- Data Processing: Pandas, NumPy
- Data Visualization: Matplotlib, Seaborn
- Time Series Models: 
- Deployment: Streamlit, Docker, Hugging Face Spaces
- Version Control: Git, GitHub
- Development Environment: Databricks Free Edition

## 📎 Dataset


## 🎨 Portfolio Showcase
Please view the full report (PDF) and interact with the live application here: 
- [Canadian Natural Gas Production Trends and Upstream Capacity to Support LNG Canada Phase 1](outputs/Canadian_Natural_Gas_Production_Trends_Upstream_Capacity_LNG_Canada_Phase1.pdf)
- [Streamlit App on Hugging Face Spaces](https://huggingface.co/spaces/jyunyilin/canadian_marketable_natural_gas_supply_trends)

## ✨ Future Improvements

