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

This was the original model developed in the project.

The baseline model uses only historical prices and time-based features, treating price itself as the main source of information. Economically, this reflects the idea that electricity prices contain persistence, recurring hourly effects and short-term volatility patterns. It is a useful benchmark because it captures market memory, although it does not explicitly model the underlying drivers of price formation.

---

## Data ingestion

`ingest.py`

Downloads electricity price data from the Danish Energy Data Service API.

The script combines: historical prices from **Elspotprices** and recent prices from **DayAheadPrices**

The data is stored locally in a **DuckDB database**.

---

## Exploratory visualisation

`plot.py`

Creates historical electricity price charts for DK1 and DK2.

These plots allow quick inspection of: **long-term trends, seasonal behaviour and volatility patterns**  

**DK1 vs DK2 electricity prices — historical price evolution**

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>
The historical series shows no stable or simple pattern, but rather high volatility, sharp spikes and changing regimes over time. Over the last 36 months, DK1 and DK2 broadly follow similar trends, which reflects their integration in the wider power system. Still, visible differences between both zones suggest that regional conditions and transmission constraints continue to influence price formation.

---

## Feature engineering

`features.py`

Creates time-series features used for forecasting.

**Calendar features:** hour of day, day of week, month and weekend indicator  

**Lag features:** price lag 1 hour, price lag 24 hours and price lag 168 hours  

**Rolling statistics:** 24 hour rolling mean, 24 hour rolling standard deviation, 168 hour rolling mean and 168 hour rolling standard deviation  

---

## Training window optimisation

`test_best_window.py`

Tests multiple historical training windows to determine the optimal amount of historical information.

**Models are evaluated using:** MAE and RMSE  

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png" width="900"/>
</p>

Selecting the training window is important because too little history can make the model unstable, while too much can introduce outdated market conditions. The results indicate that a **12-month window** performs best for this model. This suggests that the most recent full annual cycle captures enough seasonal structure while remaining close to current market dynamics.

---

## Forecast generation

`forecast.py`

Trains the final baseline model and generates hourly electricity price forecasts for the next week.

**Outputs include:** forecast CSV file, forecast visualisation and forecast summary table 

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png" width="900"/>
</p>

---

# 2. Market Drivers Model

After building the baseline model, the project was extended by incorporating **market fundamentals** to give the forecasting model more economic significance.

The idea was to move from a purely autoregressive approach to a model that reflects **real drivers of electricity price formation**.

---

## Added variables

The model incorporates:**wind_generation**, **temperature** and **gas_price**

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

The addition of wind generation, temperature and gas prices clearly improves the forecasts in both DK1 and DK2. This shows that electricity prices are better explained when the model includes real supply, demand and cost signals rather than relying only on past prices. Economically, it confirms that short-term power prices respond strongly to current market fundamentals.

---

# Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

Lagged prices remain highly relevant, confirming the importance of short-term persistence in electricity markets. The market drivers add extra explanatory power by capturing part of the variation missed by the baseline model. In economic terms, wind generation, temperature and gas prices help connect the forecast to the physical and cost structure of the market.

---

# Actual vs Predicted Prices

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png" width="750"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png" width="750"/>
</p>

---

# 3. Extended Structural Model (Improve Market Drivers)

The final stage tested additional structural variables.

Added variables:

- Electricity **load**
- Cross-border electricity **flows**
- Neighbouring markets: **Germany, Sweden, Norway and Netherlands**  

These variables attempt to represent **physical grid conditions and international electricity trading dynamics**. They are economically relevant because Danish prices are shaped not only by domestic conditions, but also by regional interconnection and power exchange with neighbouring markets. In theory, this should make the model more realistic by reflecting broader structural influences on price formation.

---
# Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

The added structural variables are economically meaningful, but their effect appears less clear and stable than the core market drivers. Load, flows and neighbouring market conditions may interact strongly with one another, making interpretation more difficult. This suggests that greater structural richness can also increase redundancy and reduce model robustness.

---

# Improved Model Results

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

Although the model remained strong, these variables introduced additional noise and slightly worsened performance.

The extended model still performs better than the baseline, but slightly worse than the Market Drivers model in both bidding zones. This suggests that adding more variables does not automatically improve forecasting accuracy. In this case, the extra structural information seems to introduce more noise or overlapping signals than useful predictive power.

---

# Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

---

# 4. Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

The comparison shows a clear trade-off between simplicity, economic realism and predictive performance. The baseline model captures temporal structure, but the Market Drivers model delivers the best overall forecasts by adding a focused set of meaningful fundamentals. The extended structural model adds complexity, but not enough extra value to outperform the more parsimonious specification.

---

---

# 5. Directional Trading and PnL Analysis

After developing the forecasting models, the project was extended to analyse whether price predictions could be translated into **trading decisions**.

The objective of this stage is to evaluate the practical usefulness of the forecasts by measuring their impact on **profit and loss (PnL)** under a simple trading framework.

---

## Initial trading approach

The first strategy generated trading signals by comparing forecasted prices with a benchmark level.

- Buy signal if forecast is significantly above the benchmark  
- Sell signal if forecast is significantly below the benchmark  

Although this approach produced very high win rates, the results were misleading. Profits were calculated relative to the benchmark instead of real price movements, making the strategy artificially profitable.

---

## Corrected backtesting framework

To obtain realistic results, the trading logic was redesigned.

- PnL is calculated using **actual price changes**  
- Signals are evaluated based on **real market movement**  
- Transaction costs are included  

---

## Directional modelling approach

To improve performance, the modelling problem was redefined.

Instead of predicting price levels, the model predicts **direction of price movement**.

Key changes:

- Target variable defined as **next-hour price change**  
- Model outputs **probability of upward movement**  
- Trading signals generated only when confidence is sufficiently high  

---

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

Extending the analysis to trading revealed an important limitation: accurate price forecasts do not necessarily translate into profitable trading strategies. The initial approach based on price levels produced misleading results due to an incorrect PnL definition.

By reformulating the problem as a directional prediction task, the model becomes better aligned with trading objectives. This adjustment leads to consistent positive PnL, improved win rates and controlled drawdowns across both Danish price areas.

Overall, the project highlights a key insight for applied energy analytics: the most effective models are not the most complex ones, but those that combine relevant market signals with a structure aligned to the final decision-making objective.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy market analytics | Data analysis | Forecasting  

GitHub  
https://github.com/antespbau

