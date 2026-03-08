# Denmark Electricity Price Forecasting Pipeline

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices in the two bidding zones:

- **DK1 — West Denmark**
- **DK2 — East Denmark**

The workflow covers **data ingestion, exploratory analysis, feature engineering, model evaluation and next-week price forecasting** for the day-ahead electricity market.

The project started with a **pure time-series forecasting model**, and was later extended with **market fundamentals** and then with **additional structural variables** to test whether forecasting performance could be improved further.

The objective is to demonstrate practical data analytics and forecasting techniques applied to energy markets.

---

# Project Overview

Electricity prices in Denmark vary depending on:

- demand patterns  
- seasonality  
- renewable generation  
- fuel prices  
- differences between price zones  

This project evolves through **three modelling stages**:

| Stage | Description |
|------|-------------|
| **1. Baseline forecasting model** | Pure time-series model using lagged prices, calendar effects and rolling statistics |
| **2. Market Drivers model** | Extends the baseline model with key market fundamentals such as wind generation, temperature and gas prices |
| **3. Extended structural model** | Tests additional variables such as load and cross-border flows |

Models are evaluated using:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**

---

# Technologies Used

- Python  
- pandas  
- numpy  
- matplotlib  
- scikit-learn  
- xgboost  
- duckdb  
- requests  

---

# 1. Baseline Forecasting Model

This was the original model developed in the project.

It focuses on **price dynamics only**, without adding exogenous market variables.

---

## Data ingestion

`ingest.py`

Downloads electricity price data from the Danish Energy Data Service API.

The script combines:

- historical prices from **Elspotprices**
- recent prices from **DayAheadPrices**

The data is stored locally in a **DuckDB database**.

---

## Exploratory visualisation

`plot.py`

Creates historical electricity price charts for DK1 and DK2.

These plots allow quick inspection of:

- long-term trends  
- seasonal behaviour  
- volatility patterns  

**DK1 vs DK2 electricity prices — historical price evolution**

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png"/>

---

## Spread analysis

`plot_spread.py`

Calculates and visualises the price spread between DK2 and DK1.

This highlights structural differences between the two Danish price zones.

**DK1–DK2 price spread**

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk_spread_evolution.png"/>

---

## Feature engineering

`features.py`

Creates time-series features used for forecasting.

### Calendar features

- hour of day  
- day of week  
- month  
- weekend indicator  

### Lag features

- price lag 1 hour  
- price lag 24 hours  
- price lag 168 hours  

### Rolling statistics

- 24 hour rolling mean  
- 24 hour rolling standard deviation  
- 168 hour rolling mean  
- 168 hour rolling standard deviation  

---

## Training window optimisation

`test_best_window.py`

Tests multiple historical training windows to determine the optimal amount of historical information.

Models are evaluated using:

- MAE  
- RMSE  

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png"/>

---

## Forecast generation

`forecast.py`

Trains the final baseline model and generates hourly electricity price forecasts for the next week.

Outputs include:

- forecast CSV file  
- forecast visualisation  
- forecast summary table  

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png"/>

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/table_forecast_summary.png"/>

---

# 2. Market Drivers Model

After building the baseline model, the project was extended by incorporating **market fundamentals** to give the forecasting model more economic significance.

The idea was to move from a purely autoregressive approach to a model that reflects **real drivers of electricity price formation**.

---

## Added variables

The model incorporates:

- **wind_generation**  
- **temperature**  
- **gas_price**

These variables represent three key forces in electricity markets.

| Variable | Interpretation |
|--------|---------------|
| Wind generation | Renewable electricity supply |
| Temperature | Weather-driven electricity demand |
| Gas price | Marginal generation cost |

Because Denmark has one of the highest wind penetrations in Europe, wind generation plays a major role in price volatility.

---

# Model Performance

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |

This model produced the **best forecasting performance**.

---

# Feature importance / coefficients

### Feature importance / coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

---

# Actual vs Predicted Prices

### DK1

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png"/>

### DK2

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png"/>

---

# 3. Extended Structural Model (Improve Market Drivers)

The final stage tested additional structural variables.

Added variables:

- electricity **load**
- cross-border electricity **flows**

with neighbouring markets:

- Germany  
- Sweden  
- Norway  
- Netherlands  

These variables attempt to represent **physical grid conditions and international electricity trading dynamics**.

---

# Improve Model Results

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

Although the model remained strong, these variables introduced additional noise and slightly worsened performance.

---

# Improve Model Feature Importance

### DK1

<img width="700" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK1.png"/>

### DK2

<img width="700" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK2.png"/>

---

# Improve Model Actual vs Predicted

### DK1

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png"/>

### DK2

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png"/>

---

# Forecast Comparison Across Models

### DK1

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK1.png"/>

### DK2

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK2.png"/>

---

# Final Summary

This project demonstrates how electricity price forecasting models can be progressively improved by incorporating additional market information.

The modelling process evolved through three stages:

1. **Baseline autoregressive model**  
2. **Market Drivers model**  
3. **Extended structural model**

The results show that the **Market Drivers model achieved the best balance between predictive accuracy and economic interpretability**.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy market analytics | Data analysis | Forecasting  

GitHub  
https://github.com/antespbau
