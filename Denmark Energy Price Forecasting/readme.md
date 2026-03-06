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

---

### 3. Spread analysis

`plot_spread.py`

Calculates and visualises the price spread between DK2 and DK1.

This helps highlight structural differences between the two Danish price zones.

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

---

### 6. Forecast generation

`forecast.py`

Trains the final model and generates hourly electricity price forecasts for the next week.

Outputs include:

• forecast CSV file  
• forecast visualisation  
• forecast summary table

---

# Example Outputs

### Electricity price evolution

![Price plot](PNG/price_plot.png)

---

### Price spread DK2 – DK1

![Spread plot](PNG/spread_plot.png)

---

### Forecast for next week

![Forecast](PNG/forecast_next_week.png)

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

