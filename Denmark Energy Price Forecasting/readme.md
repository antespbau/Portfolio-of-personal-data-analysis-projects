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

After building the baseline model, I extended the project by adding **market fundamentals** to give the forecasting model more economic significance.

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

_Add your feature importance figure or coefficient chart here._

**Suggested place for image:**

```markdown
![Feature importance](PATH_TO_YOUR_IMAGE)
