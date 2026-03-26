# Danish Power Market Analytics: Forecasting and PnL Analysis

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

**Technologies Used:** Python, pandas, numpy, matplotlib, scikit-learn, xgboost, duckdb, requests  

---

# 1. Baseline Forecasting Model

## Exploratory visualisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>

---

## Training window optimisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/window_results_plot.png" width="900"/>
</p>

---

## Forecast generation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/forecast_next_week_hourly.png" width="900"/>
</p>

---

# 2. Market Drivers Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

---

## Actual vs Predicted Prices

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png" width="750"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png" width="750"/>
</p>

---

# 3. Extended Structural Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

---

## Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

---

# 4. Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

---

# 5. Directional Trading and PnL Analysis

## Strategy results

| Market | Total PnL | Win Rate | Avg Trade PnL | Sharpe-like | Max Drawdown |
|--------|----------:|---------:|--------------:|------------:|-------------:|
| DK1 | 33129 | 64.1% | 7.13 | 0.40 | -114 |
| DK2 | 41550 | 66.1% | 8.78 | 0.42 | -91 |

---

## Cumulative PnL

<p align="center">
  <img src="outputs/plots/daily_cumulative_pnl.png" width="900"/>
</p>

---

## Drawdown analysis

<p align="center">
  <img src="outputs/plots/daily_drawdown.png" width="900"/>
</p>

---

# 6. Final Summary

This project analyses Danish day-ahead electricity prices through multiple modelling stages, moving from a pure time-series baseline to models that incorporate market fundamentals and broader structural variables.

The results show that price history alone contains useful information, but forecast accuracy improves significantly when the model includes economically meaningful drivers such as wind generation, temperature and gas prices.

The Market Drivers model achieved the best balance between predictive performance and economic interpretability. Adding further structural variables increased complexity, but introduced additional noise without improving results.

Extending the analysis to trading revealed an important limitation: accurate price forecasts do not necessarily translate into profitable trading strategies.

By reformulating the problem as a directional prediction task, the model becomes better aligned with trading objectives, resulting in consistent positive PnL, improved win rates and controlled drawdowns.

Overall, the project highlights a key insight for applied energy analytics: the most effective models are those that combine relevant market signals with a structure aligned to the final decision-making objective.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy market analytics | Data analysis | Forecasting  

GitHub  
https://github.com/antespbau
