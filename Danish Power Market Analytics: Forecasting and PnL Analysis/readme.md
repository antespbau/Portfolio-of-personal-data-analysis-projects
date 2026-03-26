# Danish Power Market Analytics: Forecasting and PnL Analysis

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
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>

---

## Training window optimisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/window_results_plot.png" width="900"/>
</p>

---

## Forecast generation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_next_week_hourly.png" width="900"/>
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

After evaluating the forecasting models, the project was extended to analyse whether the information contained in the predictions could be translated into **directional trading signals**.

The purpose of this stage is not simply to forecast the level of electricity prices, but to assess whether the model can correctly anticipate **the next short-term movement of the market** and convert this into a trading decision.

---

## Why a directional model was needed

The initial trading tests used forecasted price levels to create trading signals. However, this produced misleading results because forecasting a price level well does not necessarily mean forecasting whether the next movement will be upward or downward.

This is a key distinction in trading applications:

- **Price forecasting** asks: what price level is likely?
- **Directional trading** asks: will the price move up or down next?

Because of this, the trading framework was redesigned as a **directional prediction problem**.

---

## Step 1. Build the directional dataset

A new dataset was created using the original forecasting variables together with additional features designed to capture short-term changes.

Examples include:

- lagged prices  
- rolling statistics  
- temperature, wind generation and gas prices  
- changes in those variables over time  
- spread features between DK1 and DK2  

The target variable was redefined as the **next-hour price movement**, allowing the model to learn whether the price is more likely to move upward or downward.

---

## Step 2. Train a directional model

A new model was trained to predict the **probability of upward movement** rather than the exact future price level.

This makes the model output directly relevant for trading, because it provides a measure of confidence about direction.

In practice, the model estimates:

- high probability of upward movement → bullish signal  
- low probability of upward movement → bearish signal  

---

## Step 3. Generate trading signals

The next step is to convert probabilities into actual trading decisions.

The logic is:

- **Long signal** when the probability of upward movement is sufficiently high  
- **Short signal** when the probability of upward movement is sufficiently low  
- **No trade** when the probability is close to neutral  

This confidence filter is important because it avoids forcing a trade at every hour and keeps only the signals with stronger conviction.

---

## Step 4. Backtest the strategy

Once the signals are created, they are applied to the realised next-hour price movement.

The backtest evaluates what would have happened historically if the strategy had followed the model’s signals.

For each trade:

- long position profits if price increases  
- short position profits if price decreases  
- transaction costs are subtracted  

This produces the key trading outputs:

- trade-by-trade PnL  
- cumulative PnL  
- win rate  
- drawdown  
- Sharpe-like performance measure  

---

## Step 5. Evaluate strategy performance

The final directional strategy is assessed using a set of practical trading metrics.

| Market | Total PnL | Win Rate | Avg Trade PnL | Sharpe-like | Max Drawdown |
|--------|----------:|---------:|--------------:|------------:|-------------:|
| DK1 | 33129 | 64.1% | 7.13 | 0.40 | -114 |
| DK2 | 41550 | 66.1% | 8.78 | 0.42 | -91 |

These results show that the directional framework produces:

- positive cumulative profitability in both bidding zones  
- win rates above 60%  
- positive average trade PnL  
- limited drawdowns relative to total gains  

---

## Cumulative PnL

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/daily_cumulative_pnl.png" width="900"/>
</p>

The cumulative PnL chart shows that profitability increases steadily through time in both DK1 and DK2. This indicates that the performance does not depend on a single isolated period, but is built progressively across the backtest.

---

## Drawdown analysis

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/drawdown.png" width="900"/>
</p>

The drawdown chart measures temporary losses from previous PnL peaks. In this case, drawdowns remain relatively limited and short-lived compared with the overall profitability of the strategy, suggesting a controlled risk profile.

---

## Key trading insight

This stage shows that **forecasting price levels and building profitable trading strategies are not the same problem**.

The original level-based approach was not well aligned with directional trading. By reformulating the task as a probability-based directional model, the strategy becomes more consistent with the underlying trading objective and produces stronger practical results.

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
