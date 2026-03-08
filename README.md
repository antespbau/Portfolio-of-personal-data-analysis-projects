# Portfolio of personal data analysis projects

Hi, I’m Antonio Espino Bautista. This repo is a small portfolio of personal data projects I’ve built to practice analytics end-to-end: cleaning data, building simple models, and presenting results in dashboards.

## Projects

### 1) Denmark electricity price forecasting (Python / Machine Learning)

**Goal:** analyse and forecast day-ahead electricity prices in Denmark (DK1 and DK2 bidding zones) using time-series features and machine learning models.

**What I did:**
- Extracted and cleaned Danish electricity price data from public energy market sources
- Built an end-to-end forecasting pipeline including ingestion, feature engineering, model training and forecast visualisation
- engineered time-series predictors such as lagged prices, rolling statistics and calendar variables
- tested different historical training windows to improve forecast performance
- trained **machine learning forecasting models with XGBoost** to predict next-week hourly electricity prices
- extended the baseline model with **market drivers** such as wind generation, temperature and gas prices to improve economic interpretability
- tested a more complex structural version including load and cross-border flows, and compared whether additional variables improved or worsened performance
- evaluated the models using **MAE** and **RMSE** across DK1 and DK2
- produced forecast comparison charts showing how the different modelling approaches behave in each price zone

➡️ Folder: [Denmark electricity price forecasting](Denmark%20Energy%20Price%20Forecasting/)

**Next week forecast comparison** — baseline vs market drivers vs extended model  

<p align="center">
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK1.png" width="650"/>
  <img src="https://raw.githubusercontent.com/antespbau/Portfolio-of-personal-data-analysis-projects/main/Denmark%20Energy%20Price%20Forecasting/PNG/PNG/forecast_comparison_models_DK2.png" width="650"/>
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
