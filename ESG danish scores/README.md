# ESG Danish scores (Power BI)

This project builds a simple ESG-style scoring view using Danish SDG indicators from Statistics Denmark:
https://www.dst.dk/en/Statistik/temaer/SDG/danske-maalepunkter

## Goal
Create a clear way to compare performance across indicators and summarise them into:
- Total score (all indicators)
- Environmental score
- Social score
- Governance score

## Data source
All indicators come from the SDG “danske målepunkter” pages on Statistics Denmark (DST).
I used the indicator time series and cleaned/standardised them so they can be combined in one model.

## What I did (high level)
- Collected the indicators from DST (SDG “danske målepunkter”)
- Cleaned and reshaped the data into a consistent table format
- Standardised indicators so they can be compared (handling direction / scale differences)
- Built a scoring model and created an interactive Power BI report

## Power BI report (4 pages)
1) **Total scores** — overview of the combined score<img width="1292" height="729" alt="Captura de pantalla (63)" src="https://github.com/user-attachments/assets/76088227-146b-4497-b266-0760f69f7b5c" />

2) **Environmental** — indicators grouped as environmental<img width="1290" height="732" alt="Captura de pantalla (64)" src="https://github.com/user-attachments/assets/f120e306-4a83-4d66-a165-3ab472ec84bf" />

3) **Social** — indicators grouped as social<img width="1299" height="732" alt="Captura de pantalla (65)" src="https://github.com/user-attachments/assets/2ec02f75-20b3-4c68-a8ac-335e2c05d684" />

4) **Governance** — indicators grouped as governance<img width="1294" height="732" alt="Captura de pantalla (66)" src="https://github.com/user-attachments/assets/828e2be8-9ec9-474d-a0bb-26f9c0ee6ffd" />

## Notes
This is a personal portfolio project. The goal is to show my workflow: sourcing indicators, cleaning them, and building a dashboard that is easy to explore.

