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

The baseline model uses only historical electricity prices and time-based patterns to generate forecasts. In economic terms, this means that the model treats the electricity price itself as the main source of information, assuming that part of current price formation can be explained by persistence, recent volatility and recurring calendar effects such as hourly demand cycles, weekdays and seasonality. This is a useful starting point because electricity prices often display short-term autocorrelation and repeated behavioural patterns, even before introducing external market fundamentals. At the same time, the limitation of this approach is that it does not explicitly capture the underlying economic forces behind price formation, such as renewable output, fuel costs or weather-driven demand.

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

These plots allow quick inspection of: **long-term trends, seasonal behaviour and volatility patterns**  

**DK1 vs DK2 electricity prices — historical price evolution**

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png"/>

The historical series shows that Danish electricity prices do not follow a simple or stable pattern over time. Instead, prices display high volatility, frequent spikes and changing regimes, which is typical of electricity markets where supply-demand balance must be maintained in real time. Over the last 36 months, both DK1 and DK2 have moved broadly in the same direction, reflecting their integration within the Nordic and European power system, but differences between the two zones remain visible. These differences suggest that local market conditions, transmission constraints and regional supply dynamics still matter. The chart also shows that periods of relative stability can quickly be replaced by sharp fluctuations, which makes forecasting especially challenging and reinforces the importance of combining statistical techniques with economic interpretation.

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

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png"/>

Choosing the training window is an important modelling decision in electricity price forecasting. Using too little history can make the model unstable and too sensitive to short-term noise, while using too much history can reduce performance because market conditions change over time and older observations may no longer be representative of the current system. The results show that a **12-month window** provides the best balance for this baseline model. Economically, this suggests that the most relevant information comes from the most recent full annual cycle, which captures both seasonal effects and relatively current market behaviour without overloading the model with outdated regimes.

---

## Forecast generation

`forecast.py`

Trains the final baseline model and generates hourly electricity price forecasts for the next week.

**Outputs include:** forecast CSV file, forecast visualisation and forecast summary table  

<img width="1292" height="729" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png"/>

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

The results show a clear improvement over the baseline model in both Danish bidding zones. Adding wind generation, temperature and gas prices reduces forecast errors substantially, which indicates that electricity prices cannot be fully understood from past prices alone. From an economic perspective, this is an important result: the model performs better when it includes variables linked to supply conditions, weather-sensitive demand and marginal production costs. The stronger performance of the Market Drivers model suggests that these fundamentals capture a meaningful part of price formation in Denmark and provide a better balance between predictive accuracy and interpretability.

---

# Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_DK2.png" width="450"/>
</p>

The coefficient patterns are economically intuitive. Lagged price variables remain highly relevant, confirming that short-term persistence continues to matter in electricity markets. At the same time, the added market drivers help explain part of the variation that pure autoregressive features miss. Wind generation is expected to show a negative relationship with prices, since higher renewable output increases supply and tends to push prices down. Temperature helps proxy demand conditions, while gas prices reflect the cost pressure coming from thermal generation. The fact that these variables contribute alongside lagged prices reinforces the idea that Danish electricity prices are shaped by both market memory and contemporaneous fundamentals.

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

These variables attempt to represent **physical grid conditions and international electricity trading dynamics**. Electricity prices are not determined only by domestic supply and demand, but also by the broader interconnected power system. Load captures the direct pressure of consumption on the market, while cross-border flows reflect the role of imports, exports and transmission availability. Including neighbouring markets aims to account for the fact that Danish price zones are influenced by surrounding systems through interconnection and regional price coupling. In theory, these variables should improve the economic realism of the model by incorporating more of the structural mechanisms behind price formation.

---

# Improved Model Results

| Model | DK1 MAE | DK1 RMSE | DK2 MAE | DK2 RMSE |
|------|--------:|---------:|--------:|---------:|
| Baseline Model | 10.24 | 18.14 | 11.49 | 21.19 |
| **Market Drivers Model** | **7.55** | **13.36** | **8.68** | **15.79** |
| Improve Market Drivers | 8.10 | 13.83 | 8.88 | 16.58 |

Although the model remained strong, these variables introduced additional noise and slightly worsened performance.

The results suggest that adding more structural variables did not translate into better forecasts. Although the extended model still outperforms the baseline model, it performs slightly worse than the Market Drivers model in both DK1 and DK2. This indicates that more information does not automatically mean more predictive power. Some of the added variables may contain overlapping signals, measurement noise or effects that are harder to capture in a simple forecasting framework. Economically, this is also a useful finding: the most relevant drivers of short-term Danish electricity prices may already be captured by a relatively compact set of fundamentals, while further structural complexity can reduce model efficiency rather than improve it.

---

# Coefficients

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK1.png" width="450"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/price_correlation_improve_market_drivers_DK2.png" width="450"/>
</p>

The coefficient structure of the extended model shows that, while some additional variables contribute useful information, their overall effect is less clear and less stable than in the Market Drivers model. Variables related to load, flows and neighbouring markets are economically relevant, but they may interact in complex ways and can be strongly correlated with one another. This makes interpretation more difficult and may weaken the model’s ability to generalise. In practice, the results suggest that introducing broader structural factors increases conceptual richness, but also raises the risk of multicollinearity, redundant information and lower forecasting precision.

---

# Improved Model Actual vs Predicted

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK1.png" width="700"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/reduced_model_actual_vs_predicted_DK2.png" width="700"/>
</p>

---

# Forecast Comparison Across Models

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK1.png" width="900"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK2.png" width="900"/>
</p>

The forecast comparison across models highlights the trade-off between simplicity, economic realism and predictive accuracy. The baseline model captures general temporal dynamics but is less responsive to underlying market conditions. The Market Drivers model produces the best overall forecasts, suggesting that a focused set of economically meaningful variables is enough to improve performance significantly. The extended structural model remains informative, but the additional complexity does not produce further gains. This comparison shows that, in applied electricity price forecasting, the best model is not necessarily the most complex one, but the one that combines relevant economic signals with a parsimonious and robust structure.

---

# Final Summary

This project provides an applied economic and data-driven analysis of Danish day-ahead electricity prices in DK1 and DK2. Across the three modelling stages, the results show that electricity prices can be partially forecast using their own past behaviour, but that predictive performance improves significantly when the model incorporates market fundamentals linked to supply, demand and production costs. In particular, wind generation, temperature and gas prices add strong explanatory value because they reflect key mechanisms of price formation in power markets.

The main conclusion is that the **Market Drivers model** offers the best balance between forecasting accuracy and economic interpretability. It improves performance over the pure time-series baseline while remaining more robust than the broader structural specification. This suggests that, for short-term Danish electricity price forecasting, a focused set of economically meaningful variables can outperform a more complex model with a wider set of structural inputs.

Beyond forecasting, the project also illustrates a broader analytical point: electricity markets are influenced by recurring temporal patterns, but also by real physical and economic fundamentals. Combining both perspectives leads to stronger and more realistic models, which is especially relevant for energy market analysis, trading, system planning and business decision-making.

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
