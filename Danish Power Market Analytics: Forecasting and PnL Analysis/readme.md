# Danish Power Market Analytics: Forecasting and PnL Analysis

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices. It is composed of two main parts:

1. **Price Forecasting**  
   Development and evaluation of three models to predict day-ahead electricity prices, covering:
   - data ingestion  
   - exploratory analysis  
   - feature engineering  
   - model training and evaluation  
   - next-week forecasting  

2. **Directional Trading & PnL Analysis**  
   Transformation of model outputs into trading signals and evaluation of profitability.

The analysis focuses on the two Danish bidding zones:

- **DK1 — West Denmark**
- **DK2 — East Denmark**

**Objective:**  
To convert forecasting outputs into **consistent and profitable trading decisions**.

---

# FIRST PART OF THE PROJECT

# Project Overview

Electricity prices in Denmark are driven by:

- demand patterns  
- seasonality  
- renewable generation (especially wind)  
- fuel prices  
- cross-border flows  
- system load  

To progressively improve performance, three modelling approaches are implemented:

| Stage | Description |
|------|-------------|
| **1. Baseline forecasting model** | Uses only historical prices and temporal patterns |
| **2. Market Drivers model** | Adds wind generation, temperature and gas prices |
| **3. Extended structural model** | Adds load and cross-border flows |

Models are evaluated using:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**

**Technologies:** Python, pandas, numpy, matplotlib, scikit-learn, xgboost, duckdb, requests  

---

# 1. Baseline Forecasting Model

## Exploratory visualisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>

**Observations:**

- Electricity prices are highly volatile with frequent spikes  
- DK1 and DK2 follow similar patterns but diverge during stress periods  
- Strong intraday and weekly seasonality is visible  

---

## Training window optimisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/window_results_plot.png" width="900"/>
</p>

The optimal training window is selected using:

➡️ [`test_best_window.py`](Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/Scripts/Basic%20model/basic%20model/test_best_window.py)

**Observations:**

- Intermediate windows (~12 months) provide the best performance  
- Short windows → unstable and noisy predictions  
- Long windows → include outdated market dynamics  

---

## Forecast generation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_next_week_hourly.png" width="900"/>
</p>

**Observations:**

- The model captures the overall trend and seasonality  
- Predictions are smoother than real prices  
- Price spikes are consistently underestimated  

**Conclusion:**

The baseline model captures structure but lacks responsiveness to real market drivers.

---

# 2. Market Drivers Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

**Observations:**

- Lagged prices dominate → strong short-term persistence  
- Wind generation has a clear negative correlation with prices  
- Temperature is negatively related (demand effect)  
- Gas price shows a weaker but positive relationship  

**Interpretation:**

- Wind = supply shock → reduces prices  
- Temperature = demand proxy  
- Gas = marginal cost driver  

---

## Actual vs Predicted Prices

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png" width="750"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png" width="750"/>
</p>

**Observations:**

- Strong improvement vs baseline  
- Better timing of price movements  
- Spikes still underestimated but more aligned  

**Conclusion:**

Including market fundamentals significantly improves performance.

---

# 3. Extended Structural Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

**Observations:**

- Additional variables (flows, load) appear but are not dominant  
- Core drivers (lags, wind) still explain most of the behaviour  
- Some variables introduce noise  

---

## Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

**Observations:**

- No consistent improvement over Market Drivers  
- Slightly noisier predictions  
- No better capture of extreme movements  

**Conclusion:**

Additional structural variables increase complexity without improving accuracy.

---

# 4. Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

**Observations:**

- Baseline → too smooth, underestimates volatility  
- Extended → unstable and noisy  
- Market Drivers → best balance  

**Conclusion:**

The Market Drivers model is selected as the best-performing model.

---

# SECOND PART OF THE PROJECT — TRADING

# 5. Directional Trading and PnL Analysis

## Motivation

Forecasting price levels does not necessarily translate into trading performance.

The problem is reformulated as:

> predicting the **direction of the next price movement**

---

## Strategy Results

| Market | Total PnL | Win Rate | Avg Trade PnL | Sharpe-like | Max Drawdown |
|--------|----------:|---------:|--------------:|------------:|-------------:|
| DK1 | 33129 | 64.1% | 7.13 | 0.40 | -114 |
| DK2 | 41550 | 66.1% | 8.78 | 0.42 | -91 |

**Observations:**

- Positive PnL in both markets  
- Win rate consistently above 60%  
- Stable average returns  
- Controlled drawdowns  

---

## Cumulative PnL

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/daily_cumulative_pnl.png" width="900"/>
</p>

**Observations:**

- Smooth and consistent growth  
- DK2 outperforms DK1  
- No single period drives performance  

---

## Drawdown Analysis

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/drawdown.png" width="900"/>
</p>

**Observations:**

- Frequent but limited losses  
- No prolonged drawdowns  
- Risk remains controlled  

---

## Key Insight

> The model is not perfect at predicting price levels, but it is effective at predicting direction.

This is what makes the strategy profitable.

---

# 6. Final Summary

- Electricity prices show strong persistence  
- Wind is the most relevant external driver  
- Adding too many variables degrades performance  
- The Market Drivers model performs best  

**Final conclusion:**

> Forecasting accuracy alone is not enough — models must be aligned with the trading objective.

By reframing the problem as a directional task, the model generates **consistent and profitable trading results**.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy Market Analytics | Forecasting | Trading  

GitHub:  
https://github.com/antespbau
