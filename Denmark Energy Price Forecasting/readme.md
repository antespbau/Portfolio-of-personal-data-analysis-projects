# Denmark Electricity Price Forecasting Pipeline

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices in the two bidding zones:

- **DK1 — West Denmark**
- **DK2 — East Denmark**

The workflow covers **data ingestion, exploratory analysis, feature engineering, model evaluation and next-week price forecasting** for the day-ahead electricity market.

The project started with a **pure time-series forecasting model**, and was later extended with **market fundamentals** and then with **additional structural variables** to test whether forecasting performance could be improved further.

The objective is to demonstrate practical data analytics and forecasting techniques applied to energy markets.

---

## Project Overview

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
| **3. Extended structural model** | Tests additional variables such as load and cross-border flows, which ultimately added noise and worsened the forecast metrics |

The models are evaluated using:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**

---

## Technologies Used

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

## Pipeline Workflow

The baseline model runs through the following steps:

### 1.1 Data ingestion

`ingest.py`

Downloads electricity price data from the Danish Energy Data Service API.

The script automatically combines:

- historical prices from the **Elspotprices** dataset
- recent prices from the **DayAheadPrices** dataset

The data is stored locally in a **DuckDB** database.

---

### 1.2 Exploratory visualisation

`plot.py`

Creates historical electricity price charts for DK1 and DK2.

These plots allow quick inspection of:

- long-term trends
- seasonal behaviour
- volatility patterns

**DK1 vs DK2 electricity prices** — historical price evolution in the Danish electricity market  

<img width="1292" height="729" alt="dk1_dk2_price_evolution" src="https://github.com/antespbau/Portfolio-of-personal-data-analysis-projects/blob/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png" />

---

### 1.3 Spread analysis

`plot_spread.py`

Calculates and visualises the price spread between DK2 and DK1.

This highlights structural differences between the two Danish price zones.

**DK1–DK2 price spread** — difference between West and East Denmark electricity prices  

<img width="1292" height="729" alt="dk_spread_evolution" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk_spread_evolution.png" />

---

### 1.4 Feature engineering

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

These features form the basis of the baseline model.

---

### 1.5 Training window optimisation

`test_best_window.py`

Tests multiple historical training windows and evaluates forecasting performance.

This step was used to identify the most appropriate amount of historical information for the baseline model.

Models were compared using:

- MAE
- RMSE

**Rolling window forecast results** — model performance across evaluation windows  

<img width="1292" height="729" alt="window_results_plot" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png" />

---

### 1.6 Forecast generation

`forecast.py`

Trains the final baseline model and generates hourly electricity price forecasts for the next week.

Outputs include:

- forecast CSV file
- forecast visualisation
- forecast summary table

**Next week hourly forecast** — projected electricity prices for the coming week  

<img width="1292" height="729" alt="forecast_next_week_hourly" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png" />

**Forecast summary table** — next week electricity price forecast by hour  

<img width="1292" height="729" alt="table_forecast_summary" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/table_forecast_summary.png" />

---

# 2. Market Drivers Model

After building the baseline model, the project was extended by incorporating **market fundamentals** to give the forecasting model more economic significance.

The idea was to move from a purely autoregressive approach to a model that also reflects key drivers of electricity price formation.

## Added variables

The new model incorporates:

- `wind_generation`
- `temperature_2m`
- `gas_price`

These variables were chosen because they represent:

- renewable supply conditions
- weather-related demand effects
- marginal fuel cost pressure

## Why this extension matters

Electricity prices are not driven only by their own past values. They are also influenced by the underlying structure of the market, especially in a system like Denmark with high renewable penetration.

Adding these variables made the model more economically meaningful and improved predictive accuracy.

## Market Drivers results

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |

This model produced the **best overall performance**.

---

## Feature importance / coefficients

To better understand the model behaviour, feature importance and coefficient analysis were performed.

This allows the model to be interpreted not only as a forecasting tool but also as a **market analysis framework**.

### Market Drivers — DK1
![Market Drivers DK1 coefficients](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/price_correlation_DK1.png)

### Market Drivers — DK2
![Market Drivers DK2 coefficients](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/price_correlation_DK2.png)

### Improve Market Drivers — Feature Importance
![Improve Market Drivers feature importance](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/feature_importance_improve_market_drivers.png)

These results help identify which variables contribute most to electricity price formation in each Danish bidding zone.

---

## Actual vs Predicted Prices

The model predictions were compared with real electricity prices for the most recent week.

This comparison helps verify whether the model captures:

- daily price cycles
- volatility spikes
- short-term trends

### Market Drivers — DK1
![Actual vs Predicted DK1](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/actual_vs_predicted_market_drivers_DK1.png)

### Market Drivers — DK2
![Actual vs Predicted DK2](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/actual_vs_predicted_market_drivers_DK2.png)
---

## Market Drivers Forecast

The trained Market Drivers model was used to generate **hourly electricity price forecasts for the next week**.

This stage shows how the pipeline can be used in a practical forecasting setting using both time-series structure and market fundamentals.

---

# 3. Extended Structural Model (Improve Market Drivers)

After obtaining strong results from the Market Drivers model, the project explored whether adding additional system-level variables could further improve the forecasts.

The aim of this stage was to test whether a richer structural representation of the power system would improve predictive performance.

## Additional variables tested

The extended model included:

- `load`
- `flow_DE`
- `flow_SE`
- `flow_NO`
- `flow_NL`

These variables were intended to represent:

- electricity demand
- imports and exports with neighbouring markets
- cross-border market coupling
- additional structural conditions in the Danish power system

## Why this extension was tested

The idea behind this model was that electricity prices are not only affected by generation and fuel costs, but also by the **physical and cross-border structure of the grid**.

This model therefore attempted to move closer to the real functioning of electricity markets by including:

- system load
- interconnection flows
- structural market interactions

## Improve Market Drivers results

Although this extended version remained a strong model, it introduced additional noise and slightly worsened the forecast metrics.

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

This suggests that, in this case, more variables did not necessarily provide more useful signal.

---

## Improve Model Feature Importance / Coefficients

As with the previous model, feature importance analysis was performed to understand how the additional variables influenced predictions.

### DK1
![Improve correlation DK1](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/price_correlation_improve_market_drivers_DK1.png)

### DK2
![Improve correlation DK2](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/price_correlation_improve_market_drivers_DK2.png)
---

## Improve Model Actual vs Predicted

### Improve Market Drivers — DK1
![Improve Model DK1](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/reduced_model_actual_vs_predicted_DK1.png)

### Improve Market Drivers — DK2
![Improve Model DK2](https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/reduced_model_actual_vs_predicted_DK2.png)
---

# Forecast Comparison Across Models

The forecasts produced by the three modelling approaches were compared visually:

- Baseline Model
- Market Drivers Model
- Improve Market Drivers Model

This comparison illustrates how increasing model complexity affects forecast behaviour in DK1 and DK2.

### DK1 Forecast Comparison

![Forecast comparison DK1](PATH_TO_IMAGE)

### DK2 Forecast Comparison

![Forecast comparison DK2](PATH_TO_IMAGE)

---

# Final Summary

This project demonstrates how electricity price forecasting models can be progressively improved by incorporating additional market information.

The modelling process evolved through three stages:

1. **Baseline autoregressive model**  
   Captures electricity price dynamics using lagged prices, calendar features and rolling statistics.

2. **Market Drivers model**  
   Introduces key economic variables such as wind generation, temperature and gas prices.

3. **Extended structural model**  
   Tests additional variables related to system demand and cross-border electricity flows.

## Main conclusion

The **Market Drivers model achieved the best balance between predictive accuracy and economic interpretability**.

This project shows that:

- a strong time-series baseline is essential
- adding relevant market fundamentals can significantly improve forecasts
- adding too many structural variables may introduce noise and reduce performance

In this case, the best results were obtained by combining:

- autoregressive price structure
- renewable generation
- weather
- fuel cost information

---

# Why This Project Matters

Electricity markets are highly dynamic systems influenced by:

- demand patterns
- renewable generation
- fuel prices
- interconnections
- market structure

This project demonstrates how **data pipelines, feature engineering and machine learning models** can be applied to electricity market analytics in a practical way.

It showcases skills relevant for roles such as:

- **Energy Market Analyst**
- **Data Analyst in energy companies**
- **Business Intelligence Analyst in utilities or trading firms**
- **Power Market / Forecasting Analyst**

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
