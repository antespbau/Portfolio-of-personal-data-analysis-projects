# Master’s thesis — Immigration & employability in the EU (2004–2013)

This folder contains my MSc thesis and the main R script used to run the analysis.
The thesis is written in Spanish, but it includes an English abstract.

## Topic
Impact of immigration on native employability across EU countries, with heterogeneity by country groups (clusters) and education level.

## Data
Eurostat Labour Force Survey microdata (LFS-PUF), 2004–2013.
Note: microdata is not included here due to access/licensing.

## Method (high level)
- Build skill-cells (education × potential experience × country × year)
- Panel model with fixed effects (cell-country + year) and clustered standard errors
- Heterogeneity analysis:
  - Immigration effect by country cluster
  - Immigration effect by education level
- Robustness/diagnostics: Hausman, Breusch–Pagan, Wooldridge, Breusch–Godfrey

## Files
- `Impacto_de_la_inmigracion_en_la_empleabilidad_de_la_UE.pdf`
- `Thesis_Script.R`

## How to run (if you have access to the data)
The script expects country folders inside a local `base_dir` path. You may need to change `base_dir` to your own structure before running.
