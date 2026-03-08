# Denmark Electricity Price Forecasting Pipeline

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices in the two bidding zones:

- **DK1 — West Denmark**
- **DK2 — East Denmark**

The workflow covers **data ingestion, exploratory analysis, feature engineering, model evaluation and next-week price forecasting** for the day-ahead electricity market.

The main objective is to demonstrate how **data analytics, time-series modelling and market fundamentals** can be applied to energy market forecasting in a practical and reproducible way.

---

## Project Overview

Electricity prices in Denmark are highly dynamic and depend on:

- short-term price persistence
- daily and weekly demand patterns
- renewable generation
- weather conditions
- fuel costs
- structural differences between DK1 and DK2

This project develops and compares **three forecasting models** with increasing complexity:

| Model | Description |
|------|-------------|
| **1. Basic Model** | Autoregressive time-series model using only historical prices and calendar effects |
| **2. Market Drivers Model** | Adds key market fundamentals such as wind generation, temperature and gas prices |
| **3. Improve Market Drivers Model** | Extends the previous model with structural variables such as system load and cross-border flows |

The project produces **visual outputs, evaluation metrics and forecast files** to support electricity market analysis.

---

## Technologies Used

- **Python**
- **pandas**
- **numpy**
- **matplotlib**
- **scikit-learn**
- **xgboost**
- **duckdb**
- **requests**

---

# Pipeline Workflow

The project runs through the following steps:

### 1. Data ingestion

`ingest.py`

Downloads electricity price data from the Danish Energy Data Service API.

The script automatically combines:

- historical prices from the **Elspotprices** dataset
- recent prices from the **DayAheadPrices** dataset

The data is stored locally in a **DuckDB** database.

---

### 2. Exploratory visualisation

`plot.py`

Creates historical electricity price charts for DK1 and DK2.

These plots allow quick inspection of:

- long-term trends
- seasonal behaviour
- volatility patterns

**DK1 vs DK2 electricity prices** — historical price evolution in the Danish electricity market  

<img width="1292" height="729" alt="dk1_dk2_price_evolution" src="https://github.com/antespbau/Portfolio-of-personal-data-analysis-projects/blob/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png" />

---

### 3. Spread analysis

`plot_spread.py`

Calculates and visualises the price spread between DK2 and DK1.

This helps highlight structural differences between the two Danish price zones.

**DK1–DK2 price spread** — difference between West and East Denmark electricity prices  

<img width="1292" height="729" alt="dk_spread_evolution" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk_spread_evolution.png" />

---

### 4. Feature engineering

`features.py`

Creates time-series features used for forecasting, including:

**Calendar features**
- hour of day
- day of week
- month
- weekend indicator

**Lag features**
- previous hour price
- previous day price
- previous week price

**Rolling statistics**
- 24-hour rolling mean and standard deviation
- 168-hour rolling mean and standard deviation

These features provide the basis for the **Basic Model**.

---

## Forecasting Models

### Model 1 — Basic Model

The baseline model relies only on **historical electricity prices and calendar effects**.

Main features:

- `price_lag_1`
- `price_lag_24`
- `price_lag_168`
- `rolling_mean_24`
- `rolling_std_24`
- `hour`
- `day_of_week`
- `month`
- `is_weekend`

This model captures the strong autoregressive nature of electricity prices.

---

### Model 2 — Market Drivers Model

The second model introduces **fundamental market variables** in addition to the autoregressive structure.

Additional variables:

- `wind_generation`
- `temperature_2m`
- `gas_price`

This model is designed to capture:

- renewable supply shocks
- weather-related demand patterns
- fuel cost effects on electricity prices

The Market Drivers model delivered the **best overall forecasting performance**.

---

### Model 3 — Improve Market Drivers Model

The third model extends the previous specification with additional structural power-system variables such as:

- `load`
- `flow_DE`
- `flow_SE`
- `flow_NO`
- `flow_NL`

The purpose of this model is to test whether including **system load and cross-border flows** improves forecasting performance by better representing the physical and market structure of the Danish power system.

Although this extended version added useful economic interpretation, it did **not outperform** the simpler Market Drivers model in backtesting.

---

## Model Performance

Models were evaluated using:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Basic | 10.24 | 18.14 | 11.49 | 21.19 |
| Market Drivers | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

### Main takeaway

Adding **market fundamentals** significantly improved forecasting performance versus a purely autoregressive baseline.

The results suggest that, for short-term Danish electricity price forecasting, the best balance was achieved by combining:

- price dynamics
- wind generation
- temperature
- gas prices

while more complex structural variables added limited marginal improvement.

---

### 5. Training window optimisation

`test_best_window.py`

This step was originally applied to the **Basic Model** to test multiple historical training windows and evaluate forecasting performance.

Models were compared using:

- MAE
- RMSE

The best-performing historical window was then selected for the final baseline model.

**Rolling window forecast results** — model performance across evaluation windows  

<img width="1292" height="729" alt="window_results_plot" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png" />

---

### 6. Forecast generation

`forecast.py`  
`forecast_next_week_market_drivers.py`  
`forecast_next_week_improve_market_drivers.py`

These scripts train the final models and generate **hourly electricity price forecasts for the next week**.

Outputs include:

- forecast CSV files
- forecast visualisations
- forecast comparison plots

**Next week hourly forecast** — projected electricity prices for the coming week  

<img width="1292" height="729" alt="forecast_next_week_hourly" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png" />

**Forecast summary table** — next week electricity price forecast by hour  

<img width="1292" height="729" alt="table_forecast_summary" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/table_forecast_summary.png" />

---

## Forecast Comparison Across Models

The project also compares the forecast behaviour of the three models:

- Basic Model
- Market Drivers Model
- Improve Market Drivers Model

This allows visual comparison of how each specification responds to expected short-term price dynamics in DK1 and DK2.

---

# How to Run the Project

Run the complete pipeline in sequence:

```bash
python ingest.py
python plot.py
python plot_spread.py
python features.py
python test_best_window.py
python forecast.py
python wind.py
python temperature.py
python gas.py
python Build_market.py
python train_market_drivers_model.py
python forecast_next_week_market_drivers.py
python train_improve_market_drivers.py
python forecast_next_week_improve_market_drivers.py
python comparemodels.py
