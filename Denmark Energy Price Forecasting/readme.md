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

## Project Structure

```bash
Denmark Energy Price Forecasting/
│
├── Scripts/
│   ├── ingest.py
│   ├── plot.py
│   ├── plot_spread.py
│   ├── features.py
│   ├── test_best_window.py
│   ├── forecast.py
│   └── runpipeline.py
│
├── PNG/
│   ├── price_plot.png
│   ├── spread_plot.png
│   ├── feature_analysis.png
│   ├── window_test_results.png
│   └── forecast_next_week.png
│
├── energy.duckdb
├── window_results.csv
├── forecast_next_week_hourly.csv
└── readme.md
