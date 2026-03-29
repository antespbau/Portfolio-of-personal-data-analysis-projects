# Portfolio of personal data analysis projects

Hi, I’m Antonio Espino Bautista. This repo is a small portfolio of personal data projects I’ve built to practice analytics end-to-end: cleaning data, building simple models, and presenting results in dashboards.

## Projects

## 1) Danish Power Market Analytics: Forecasting & Trading (Python / Machine Learning)

**Goal:**  
Analyse and forecast Danish day-ahead electricity prices (DK1 and DK2), and evaluate whether those forecasts can be transformed into **profitable trading strategies**.

**Scope:**

This project is divided into two parts:

- **Forecasting:** development of machine learning models to predict electricity prices  
- **Trading:** conversion of model outputs into directional signals and PnL evaluation  

**What I did:**

- Built an end-to-end data pipeline using Danish energy market data (Energi Data Service)
- Engineered time-series features including lagged prices, rolling statistics and calendar variables
- Trained forecasting models using **XGBoost** and compared different modelling approaches:
  - Baseline (time-series only)
  - Market Drivers (wind, temperature, gas)
  - Extended Structural (load, cross-border flows)
- Evaluated performance using **MAE and RMSE**
- Analysed feature importance and economic interpretability of the models
- Designed a **directional trading strategy** based on predicted price movements
- Backtested trading performance including:
  - cumulative PnL  
  - win rate  
  - drawdown  
  - Sharpe-like metric  

**Key insight:**

The results show that while price forecasting alone has limitations, reframing the problem as a **directional prediction task** allows the model to generate **consistent and profitable trading signals**, capturing system-wide market dynamics.

➡️ Folder:  
[ Danish Power Market Analytics: Forecasting and PnL Analysis ](Danish%20Power%20Market%20Analytics%3A%20Forecasting%20and%20PnL%20Analysis/)


**Next week forecast comparison** — baseline vs market drivers vs extended model  

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK1.png" width="800"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK2.png" width="800"/>
</p>

### 2) ESG scoring dashboard (R / Power BI)
**Goal:** create a simple ESG scoring approach and compare entities.
**What I did:**
- cleaned and prepared the dataset
- built a composite ESG score (normalisation + weighting)
- visualised results in a Power BI dashboard

➡️ Folder: - [ESG scoring dashboard (R / Power BI)](ESG%20danish%20scores/)
🔗 **Live dashboard (Power BI):** [View report](https://app.powerbi.com/reportEmbed?reportId=dd0159d0-83fa-4255-8b75-bf1703bf680e&autoAuth=true&ctid=ffd8c5b5-7134-420b-90f6-18abe087e8f5)
<img width="1292" height="729" alt="Captura de pantalla (63)" src="https://github.com/user-attachments/assets/e893bf9a-f057-4c3e-a0f6-26accbd53a33" />


### 3) Norwegian fleet dashboard (Power BI)
**Goal:** explore fleet KPIs and present insights in a clear dashboard.
**What I did:**
- prepared the data and created the model in Power BI (relationships, measures)
- built KPI pages with filters and drill-downs
- focused on clear visual storytelling

➡️ Folder: - [Norwegian fleet dashboard (Power BI)](Overview%20of%20the%20norwegian%20fleets%20(dashboard)/)
🔗 **Live dashboard (Power BI):** [View report](https://app.powerbi.com/reportEmbed?reportId=aff4f1cb-a7d3-4532-9f94-02812ad566dc&autoAuth=true&ctid=ffd8c5b5-7134-420b-90f6-18abe087e8f5)
`<img width="1370" height="775" alt="Captura de pantalla (60)" src="https://github.com/user-attachments/assets/103fd460-2352-438f-a956-9fc47e289fbf" />


### 4) Master’s thesis — Immigration & employability in the EU (R / Econometrics)
**Goal:** study how immigration relates to native employability across EU countries using microdata.  
**What I did:**
- built a skill-cell panel (education × experience × country × year)
- estimated fixed-effects models with clustered standard errors
- analysed differences by country clusters and education level
- ran robustness/diagnostic tests (Hausman, Breusch–Pagan, Wooldridge, Breusch–Godfrey)

➡️ Folder: [Master’s thesis — code + documentation](Master%20thesis%20-%20EU%20immigration%20employability/)

*(Microdata not included due to licensing/access restrictions.)*

## Tools
Power BI (DAX, Power Query, data modelling), Excel, SQL, R, Python.

## Notes
- Some datasets are not included (source/licensing). Where that happens, I describe the structure and include the steps/code used.
- If you want a quick walkthrough, feel free to reach out.
