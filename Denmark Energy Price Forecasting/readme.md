# Denmark Electricity Price Forecasting Pipeline

This project builds an end-to-end data pipeline to analyse and forecast Danish electricity prices (DK1 and DK2) using Python.

The workflow covers data ingestion, exploratory analysis, feature engineering, model evaluation and price forecasting for the day-ahead electricity market.

The objective is to demonstrate practical data analytics and forecasting techniques applied to energy markets.

---

## Project Overview

Electricity prices in Denmark vary depending on demand patterns, seasonality, and differences between price zones.

This project:

- collects electricity price data
- stores and processes the data using DuckDB
- builds time-series features for forecasting
- tests different historical training windows
- generates forecasts for the next week

The project produces visual outputs and summary tables to support energy market analysis.

---

## Technologies Used

- Python
- pandas
- numpy
- matplotlib
- scikit-learn
- duckdb
- requests

---

# Pipeline Workflow

The project runs through the following steps:

### 1. Data ingestion

`ingest.py`

Downloads electricity price data from the Danish Energy Data Service API.

The script automatically combines:

• historical prices (Elspotprices dataset)  
• recent prices (DayAheadPrices dataset)

The data is stored locally in a DuckDB database.

---

### 2. Exploratory visualisation

`plot.py`

Creates historical electricity price charts for DK1 and DK2.

These plots allow quick inspection of:

• long-term trends  
• seasonal behaviour  
• volatility patterns
**DK1 vs DK2 electricity prices** — historical price evolution in the Danish electricity market  

<img width="1292" height="729" alt="dk1_dk2_price_evolution" src="https://github.com/antespbau/Portfolio-of-personal-data-analysis-projects/blob/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk1_dk2_price_evolution.png" />
---

### 3. Spread analysis

`plot_spread.py`

Calculates and visualises the price spread between DK2 and DK1.

This helps highlight structural differences between the two Danish price zones.
**DK1–DK2 price spread** — difference between West and East Denmark electricity prices  

<img width="1292" height="729" alt="dk_spread_evolution" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/dk_spread_evolution.png" />
---

### 4. Feature engineering

`features.py`

Creates time-series features used for forecasting, including:

• hour of day  
• day of week  
• month  
• weekend indicator  

Lag features:

• previous hour price  
• previous day price  
• previous week price  

Rolling statistics:

• 24-hour rolling mean and standard deviation  
• 168-hour rolling mean and standard deviation

---

### 5. Training window optimisation

`test_best_window.py`

Tests multiple historical training windows and evaluates forecasting performance.

Models are evaluated using:

• MAE (Mean Absolute Error)  
• RMSE (Root Mean Squared Error)

The best performing window is selected for the final model.
**Rolling window forecast results** — model performance across evaluation windows  

<img width="1292" height="729" alt="window_results_plot" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/window_results_plot.png" />
---

### 6. Forecast generation

`forecast.py`

Trains the final model and generates hourly electricity price forecasts for the next week.

Outputs include:

• forecast CSV file  
• forecast visualisation  
• forecast summary table

**Next week hourly forecast** — projected electricity prices for the coming week  

<img width="1292" height="729" alt="forecast_next_week_hourly" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/forecast_next_week_hourly.png" />

**Forecast summary table** — next week electricity price forecast by hour  

<img width="1292" height="729" alt="table_forecast_summary" src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/table_forecast_summary.png" />
---

# How to Run the Project

Run the complete pipeline:


The pipeline will automatically execute:


---

# Why This Project Matters

Electricity markets are highly dynamic systems influenced by demand patterns, renewable generation and market structure.

This project demonstrates how data pipelines and machine learning techniques can be applied to energy market analytics in a practical way.

It showcases skills relevant for roles such as:

• Energy Market Analyst  
• Data Analyst in energy companies  
• Business Intelligence analyst in utilities or trading firms  

---

# Author

Antonio Espino Bautista

Economics & Business Intelligence  
Energy market analytics | Data analysis | Forecasting

GitHub  
https://github.com/antespbau

