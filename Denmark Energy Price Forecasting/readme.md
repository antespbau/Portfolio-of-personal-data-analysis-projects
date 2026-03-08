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

## Pipeline Workflow

### Data ingestion

Electricity price data is downloaded from the Danish Energy Data Service API and stored locally using DuckDB.

### Feature Engineering

The baseline model uses time-series derived variables:

**Calendar features**

- hour of day  
- day of week  
- month  
- weekend indicator  

**Lag features**

- price lag 1 hour  
- price lag 24 hours  
- price lag 168 hours  

**Rolling statistics**

- 24 hour rolling mean  
- 24 hour rolling standard deviation  
- 168 hour rolling mean  
- 168 hour rolling standard deviation  

### Training Window Optimisation

Different historical windows were tested to determine the most appropriate amount of historical data for the model.

The best window was selected using MAE and RMSE metrics.

---

# 2. Market Drivers Model

After building the baseline model, the project was extended by incorporating **market fundamentals** that influence electricity prices.

The goal of this stage was to move from a purely autoregressive model to one that reflects **economic drivers of electricity price formation**.

## Added Market Variables

The following variables were introduced:

- **Wind generation**
- **Temperature**
- **Gas price**

These variables represent three key forces in electricity markets.

| Variable | Interpretation |
|--------|---------------|
| Wind generation | Renewable electricity supply |
| Temperature | Weather-driven electricity demand |
| Gas price | Marginal generation cost in European power markets |

Because Denmark has one of the highest wind penetrations in Europe, wind generation plays a crucial role in price volatility.

Gas prices influence electricity prices through marginal generation costs in interconnected European markets.

---

# Model Performance

Adding these variables significantly improved the model accuracy.

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |

This model produced the **best forecasting performance**.

---

# Feature Importance / Coefficients

To better understand the model behaviour, feature importance analysis was performed.

## DK1 coefficients

![DK1 coefficients](PATH_TO_IMAGE)

## DK2 coefficients

![DK2 coefficients](PATH_TO_IMAGE)

These results help identify which variables contribute most to electricity price formation in each bidding zone.

---

# Actual vs Predicted Prices

The model predictions were compared with real electricity prices for the most recent week.

This comparison verifies whether the model captures:

- daily price cycles
- volatility spikes
- short-term trends

## DK1 — Actual vs Predicted

![Actual vs predicted DK1](PATH_TO_IMAGE)

## DK2 — Actual vs Predicted

![Actual vs predicted DK2](PATH_TO_IMAGE)

---

# 3. Extended Structural Model (Improve Market Drivers)

In the final stage of the project, additional structural variables were introduced to test whether forecasting accuracy could be improved further.

The additional variables included:

- **Electricity load**
- **Cross-border electricity flows**
    - Germany
    - Sweden
    - Norway
    - Netherlands

These variables represent **physical system conditions** in the electricity grid.

| Variable | Interpretation |
|--------|---------------|
| Load | Electricity demand level |
| Cross-border flows | Electricity imports and exports |
| Wind by zone | Renewable supply differences between DK1 and DK2 |

---

# Improve Model Results

Although the model remained strong, these additional variables introduced noise and slightly worsened performance.

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

---

# Improve Model Coefficients

## DK1 coefficients

![Improve DK1 coefficients](PATH_TO_IMAGE)

## DK2 coefficients

![Improve DK2 coefficients](PATH_TO_IMAGE)

---

# Improve Model Actual vs Predicted

## DK1

![Improve model DK1](PATH_TO_IMAGE)

## DK2

![Improve model DK2](PATH_TO_IMAGE)

---

# Forecast Comparison Across Models

The forecasts produced by the three models were compared visually.

## DK1 Forecast Comparison

![Forecast comparison DK1](PATH_TO_IMAGE)

## DK2 Forecast Comparison

![Forecast comparison DK2](PATH_TO_IMAGE)

---

# Final Conclusion

This project demonstrates how electricity price forecasting models can be progressively improved by incorporating additional market information.

The modelling process evolved through three stages:

1. **Baseline autoregressive model**  
   Uses only historical electricity prices and calendar features.

2. **Market Drivers model**  
   Introduces fundamental variables such as wind generation, temperature and gas prices.

3. **Extended structural model**  
   Tests additional variables related to system demand and cross-border electricity flows.

The results show that the **Market Drivers model achieved the best balance between predictive accuracy and economic interpretability**.

This highlights the importance of combining **time-series modelling with fundamental market drivers** when forecasting electricity prices.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy market analytics | Data analysis | Forecasting  

GitHub  
https://github.com/antespbau
