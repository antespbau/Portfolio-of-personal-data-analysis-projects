# Danish Power Market Analytics: Forecasting and PnL Analysis

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices in the two bidding zones, DK1 (West Denmark) and DK2 (East Denmark). The workflow covers data ingestion, exploratory analysis, feature engineering, model development and evaluation, and extends into directional trading and PnL analysis.

The objective of the project is not only to generate accurate forecasts, but to assess whether those forecasts can be transformed into consistent and profitable trading decisions.

---

# FIRST PART OF THE PROJECT

# Project Overview

Electricity prices in Denmark are influenced by a combination of demand patterns, seasonal effects, renewable generation, fuel costs and cross-border market interactions. These dynamics create a complex environment where prices are both highly volatile and structurally driven.

To progressively capture this behaviour, the project is developed through three modelling stages. The first model relies exclusively on historical price information and temporal features. The second model introduces key market fundamentals such as wind generation, temperature and gas prices. The third model expands the feature set further by including system load and cross-border flows.

All models are evaluated using standard forecasting metrics, specifically MAE and RMSE, in order to compare their predictive performance.

---

# 1. Baseline Forecasting Model

## Exploratory visualisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/dk1_dk2_price_evolution.png" width="900"/>
</p>

The historical price series shows strong volatility, with frequent spikes and abrupt changes. DK1 and DK2 generally follow similar patterns, reflecting the integration of the Danish electricity market, although noticeable divergences appear during specific periods. Clear intraday cycles and short-term repetition can also be observed, suggesting that past prices contain useful predictive information.

---

## Training window optimisation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/window_results_plot.png" width="900"/>
</p>

The training window is selected using the script:

➡️ [`test_best_window.py`](Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/Scripts/Basic%20model/basic%20model/test_best_window.py)

The results show that intermediate windows, around 12 months, provide the best performance. Short windows lead to unstable models that overreact to recent fluctuations, while long windows include outdated market conditions and reduce predictive accuracy.

---

## Forecast generation

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_next_week_hourly.png" width="900"/>
</p>

The baseline model captures the general trend and seasonal structure of electricity prices. However, predictions are noticeably smoother than actual prices and fail to capture extreme spikes. This reflects the limitation of relying exclusively on historical price behaviour without incorporating market drivers.

---

# 2. Market Drivers Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

The introduction of market fundamentals reveals clear relationships between prices and underlying drivers. Lagged prices remain dominant, confirming strong short-term persistence. Wind generation shows a clear negative relationship with prices, reflecting its role as a supply-side driver. Temperature is also negatively correlated, acting as a proxy for demand, while gas prices display a weaker but consistent positive relationship, representing marginal production costs.

---

## Actual vs Predicted Prices

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK1.png" width="750"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/actual_vs_predicted_market_drivers_DK2.png" width="750"/>
</p>

Compared to the baseline model, predictions align more closely with actual price movements. The model reacts better to changes in market conditions and improves the timing of price variations. Although extreme spikes are still underestimated, the overall structure of the series is more accurately represented.

---

# 3. Extended Structural Model

## Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

The addition of structural variables such as load and cross-border flows introduces new relationships, but these variables do not dominate the model. Core drivers such as lagged prices and wind generation remain the most relevant, while some additional variables appear noisy or inconsistent.

---

## Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

The extended model does not provide a clear improvement over the Market Drivers model. Predictions become slightly noisier and the ability to capture extreme movements does not improve. This indicates that increasing complexity does not necessarily enhance predictive performance.

---

# 4. Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

The comparison highlights clear differences between models. The baseline model produces overly smooth forecasts and fails to capture volatility. The extended model introduces instability and noise. The Market Drivers model provides the best balance between stability and responsiveness, making it the most reliable approach.

---

# SECOND PART OF THE PROJECT — TRADING

# 5. Directional Trading and PnL Analysis

## Motivation

Forecasting price levels alone is not sufficient for trading purposes. A model can achieve good accuracy metrics while still failing to generate profitable signals. For this reason, the problem is reformulated as a directional prediction task, focusing on whether prices will move up or down in the next period.

---

## Strategy Results

| Market | Total PnL | Win Rate | Avg Trade PnL | Sharpe-like | Max Drawdown |
|--------|----------:|---------:|--------------:|------------:|-------------:|
| DK1 | 33129 | 64.1% | 7.13 | 0.40 | -114 |
| DK2 | 41550 | 66.1% | 8.78 | 0.42 | -91 |

The strategy produces consistent positive performance across both bidding zones. Win rates above 60% and positive average returns indicate that the model captures a meaningful directional signal. Drawdowns remain controlled relative to total profitability.

---

## Cumulative PnL

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/daily_cumulative_pnl.png" width="900"/>
</p>

The cumulative PnL evolves steadily over time, indicating that performance is not driven by isolated events but by consistent signal generation. DK2 shows slightly stronger results than DK1.

---

## Drawdown Analysis

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/PNG/PNG/drawdown.png" width="900"/>
</p>

Drawdowns are present but remain limited and short-lived. The absence of prolonged negative periods suggests that the strategy maintains a stable risk profile.

---

# 6. Final Summary

This project develops a complete analytical pipeline to study Danish day-ahead electricity prices, moving from a purely statistical time-series approach to models that incorporate market fundamentals and, finally, evaluating their usefulness in a trading context.

The baseline model confirms that electricity prices exhibit strong short-term persistence and recurring temporal patterns, but it also highlights the limitations of relying exclusively on historical data. By introducing market fundamentals such as wind generation, temperature and gas prices, the model becomes more aligned with the economic mechanisms that drive price formation, resulting in improved predictive performance.

Extending the model further with additional structural variables does not lead to better results, showing that increasing complexity can introduce noise rather than useful information. The most effective model is therefore the one that balances simplicity with economically meaningful variables.

The trading analysis demonstrates that forecasting accuracy alone is not sufficient to generate profitable strategies. By reframing the problem as a directional prediction task, the model becomes better aligned with trading objectives and is able to produce consistent positive PnL, stable win rates and controlled drawdowns.

Overall, the project shows that the value of a model in energy markets lies not only in its predictive power, but in its ability to support real decision-making.

---

# Author

Antonio Espino Bautista  

Economics & Business Intelligence  
Energy Market Analytics | Forecasting | Trading  

GitHub:  
https://github.com/antespbau
