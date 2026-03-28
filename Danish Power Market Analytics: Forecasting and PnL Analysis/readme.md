# Danish Power Market Analytics: Forecasting and PnL Analysis

This project built an end-to-end data pipeline to analise and forecast Danish electricity. It is composed by two parts: the first part is the forecast of the price day ahead throught three different models, the workflow covers **data ingestion, exploratory analysis, feature engineering, model evaluation and next-week forecasting**. The second part extend into  **directional trading and PnL analysis**.

- **DK1 — West Denmark**
- **DK2 — East Denmark**

The aim objective is to convert the results into consistent and profitable tradint decisions. 

---

# FIRST PART OF THE PROJECT 

# Project Overview

Electricity prices in Denmark are driven by:

- demand patterns  
- seasonality  
- renewable generation (especially wind)  
- fuel prices  
- cross-border market interactions
- Energy Loads

To improve the results, there are gonna be three models: 

| Stage | Description |
|------|-------------|
| **1. Baseline forecasting model** | Uses only historical prices and temporal patterns |
| **2. Market Drivers model** | Adds wind generation, temperature and gas prices |
| **3. Extended structural model** | Adds load, cross-border flows |

Models are evaluated using:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**

**Technologies:** Python, pandas, numpy, matplotlib, scikit-learn, xgboost, duckdb, requests...  

---

# 1. Baseline Forecasting Model

## Exploratory visualisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>

**Observations:**

- Electricity prices are highly volatile with frequent spikes  
- DK1 and DK2 move similarly but diverge at specific periods  
- Strong intraday and short-term cyclical behaviour  

---

## Training window optimisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/window_results_plot.png" width="900"/>
</p>

**Observations:**

First of all, we trained the model trhought [test_best_window.py](Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/Scripts/Basic%20model/basic%20model/test_best_window.py) window Intermediate windows (around 12 months) perform best  
- Short windows: unstable models  
- Long windows: include outdated market conditions  

---

## Forecast generation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_next_week_hourly.png" width="900"/>
</p>

**Observations:**

- Forecasts follow the general trend  
- Predictions are smoother than real prices  
- Large spikes are underestimated  

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

- Lagged prices remain dominant (strong persistence)  
- Wind generation shows a clear negative relationship with price  
- Temperature is negatively correlated with price  
- Gas price has a weaker but positive relationship  

**Interpretation:**

- Wind acts as a supply shock → lowers prices  
- Temperature proxies demand → higher temperature reduces demand  
- Gas influences marginal cost but is less dominant short-term  

---

## Actual vs Predicted Prices

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png" width="750"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png" width="750"/>
</p>

**Observations:**

- Better alignment with actual prices than baseline  
- Improved reaction to market changes  
- Peaks still underestimated but better timed  

**Conclusion:**

Adding market fundamentals improves predictive quality and economic interpretability.

---

# 3. Extended Structural Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

**Observations:**

- Additional variables (flows, load) appear but are not dominant  
- Core drivers (lags, wind) remain the strongest  
- Some variables show weak or inconsistent relationships  

---

## Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

**Observations:**

- No clear improvement over Market Drivers model  
- Predictions become slightly noisier  
- Peaks still not well captured  

**Conclusion:**

Additional structural variables increase complexity without improving performance.

---

# 4. Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

**Observations:**

- Baseline → too smooth and underestimates volatility  
- Extended model → more unstable and overreacts  
- Market Drivers → best balance between stability and responsiveness  

**Conclusion:**

The Market Drivers model provides the most reliable forecasts.

---

# 5. Directional Trading and PnL Analysis

## Motivation

Forecasting price levels does not directly translate into trading performance.

The problem is reformulated as:

> predicting the **direction of the next price movement**

---

## Strategy Results

| Market | Total PnL | Win Rate | Avg Trade PnL | Sharpe-like | Max Drawdown |
|--------|----------:|---------:|--------------:|------------:|-------------:|
| DK1 | 33129 | 64.1% | 7.13 | 0.40 | -114 |
| DK2 | 41550 | 66.1% | 8.78 | 0.42 | -91 |

**Observations:**

- Positive cumulative PnL in both markets  
- Win rate above 60%  
- Positive average trade returns  
- Drawdowns are limited relative to gains  

---

## Cumulative PnL

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/daily_cumulative_pnl.png" width="900"/>
</p>

**Observations:**

- Steady upward growth over time  
- DK2 consistently outperforms DK1  
- Performance is not driven by a single period  

---

## Drawdown Analysis

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/drawdown.png" width="900"/>
</p>

**Observations:**

- Frequent but controlled drawdowns  
- Losses are short-lived  
- No prolonged negative periods  

---

## Key Insight

The model is not perfect at predicting price levels, but:

> it is effective at capturing **direction**, which is what drives trading performance

---

# 6. Final Summary

- Electricity prices show strong short-term persistence  
- Market fundamentals (especially wind) significantly improve forecasts  
- Adding more variables does not improve performance  
- The Market Drivers model provides the best balance  

**Final conclusion:**

> Forecasting accuracy alone is not sufficient — models must be aligned with the decision-making objective.

In this case, reformulating the problem as a directional prediction task enables the model to generate **consistent and profitable trading outcomes**.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy Market Analytics | Forecasting | Trading  

GitHub:  
https://github.com/antespbau
