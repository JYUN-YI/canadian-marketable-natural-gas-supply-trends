# 🛢️ Canadian Marketable Natural Gas Supply Trends
This project was developed as part of the **Data Science Mentorship Program** hosted by the Society of Petroleum Engineers (SPE) Calgary Section. Special thanks to my mentor **Ryan A. Mardani** for professional guidance and insights.

The project explores Canada’s marketable natural gas production, historical trends, structural changes, LNG demand-supply adequacy, and forecasting using SARIMA and Prophet models. It also includes an interactive Streamlit application for visualization and analysis.

## 📌 Project Objective
- Analyze historical marketable natural gas production (2000–2025)
- Identify structural changes by Year-over-Year (YoY) and Compound Annual Growth Rate (GAGR) Analyses
- Classified production regimes by using a ±3% threshol, with explanations linked to major global events
- Smoothed Structural Analysis for rolling trends
- Forecast production and assess LNG Canada Phase 1 supply adequacy and potential tightness
- Provide an interactive tool for trend exploration and scenario analysis

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
- Production trends (2000–2025)
- Year-over-Year (YoY) growth and Compound Annual Growth Rate (CAGR)
- Rolling averages and structural regime identification

## ⏳ Time Series Models
- SARIMA
- Prophet
### 🧠 Modeling Framework
| Component            | Period        | Description |
|----------------------|---------------|-------------|
| Training Period      | 2000–2022     | Models trained on historical production data |
| Validation Period    | 2023–2025     | Used for out-of-sample performance evaluation |
| Refitting Period     | 2000–2025     | Models retrained on full available dataset |
| Forecast Horizon     | 2026–2030     | Production projections for LNG adequacy analysis |

## 🚀 Interactive Application
The interactive dashboard is deployed using **Streamlit** on **Hugging Face Spaces**.

Users can navigate across multiple pages, including:
- Executive Overview
- Historical & Structural
- LNG Supply
- Forecasting
- Limitations & Assumptions

## ⚙️ Technologies Used
- Programming Language: Python
- Data Processing: Pandas, NumPy
- Data Visualization: Matplotlib, Seaborn
- Statistical & Time Series Modeling: statsmodels (SARIMA / SARIMAX), Prophet
- Structural Change Detection: ruptures (PELT algorithm)
- Model Evaluation: Scikit-Learn (MAE, RMSE)
- Deployment: Streamlit, Docker, Hugging Face Spaces
- Version Control: Git, GitHub
- Development Environment: Databricks Free Edition

## 📎 Dataset
### Raw Data
- Source: Canada Energy Regulator (CER)
- File: `canadian-marketable-natural-gas-productions.XLSX`
- Description: Monthly marketable natural gas production data for Canada, reported in mmcfd and 10³ m³/d.

### Processed Data
All processed datasets used in the analysis and application are stored in `data/processed/`.

#### Historical Production Data
- `canadian_marketable_gas_2000_25_mmcfd.csv`
- `canadian_marketable_gas_2000_25_103m3d.csv`
- `canadian_marketable_gas_2023_25_mmcfd.csv`
- `canadian_marketable_gas_2023_25_103m3d.csv`

#### Application Datasets (`data/processed/app_data/`)
- `production_master.csv` — Cleaned master dataset for analysis
- `structural_breaks.csv` — Identified structural change points and major events
- `lng_supply_demand.csv` — LNG Canada Phase 1 demand assumptions and supply data
- `forecast_sarima.csv` — SARIMA forecast results (2026–2030)
- `forecast_prophet.csv` — Prophet forecast results (2026–2030)
- `forecast_results.csv` — Combined forecast, incremental supply, and supply gap analysis

## 🎨 Portfolio Showcase
Please view the full report (PDF) and interact with the live application here: 
- [Canadian Natural Gas Production Trends and Upstream Capacity to Support LNG Canada Phase 1](outputs/Canadian_Natural_Gas_Production_Trends_Upstream_Capacity_LNG_Canada_Phase1.pdf)
- [Streamlit App on Hugging Face Spaces](https://huggingface.co/spaces/jyunyilin/canadian_marketable_natural_gas_supply_trends)

## ✨ Future Improvements
- Extend forecasts under alternative LNG demand scenarios (e.g., additional export terminals, policy changes)
- Incorporate external drivers such as natural gas prices, drilling activity, or macroeconomic indicators
- Apply additional change-point detection methods for robustness comparison
- Enhance the interactive application with scenario simulation tools
