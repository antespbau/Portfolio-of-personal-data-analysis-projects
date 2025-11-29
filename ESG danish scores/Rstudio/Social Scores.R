
setwd("C:/Users/antes/OneDrive/Escritorio/ESG Barcos Noruega/Base de datos/ESG/Social")
library(dplyr)

soc_all <- read.csv2("Social_clean_all.csv", stringsAsFactors = FALSE)

soc_all <- soc_all %>%
  mutate(
    value = as.numeric(gsub(",", ".", value))
  )

soc_year <- soc_all %>%
  group_by(indicator, year) %>%
  summarise(
    value = mean(value, na.rm = TRUE),
    .groups = "drop"
  )

head(soc_year)

bad_S <- c(
  "low_income_share",
  "social_benefits_share",
  "sick_days_per_employee",
  "palma_ratio",
  "gender_discr_upheld_cases"
)

soc_scaled <- soc_year %>%
  group_by(indicator) %>%
  mutate(
    v_min    = min(value, na.rm = TRUE),
    v_max    = max(value, na.rm = TRUE),
    value_01 = ifelse(v_max == v_min,
                      0.5,  
                      (value - v_min) / (v_max - v_min))
  ) %>%
  ungroup() %>%
  mutate(
    score_01 = if_else(indicator %in% bad_S,
                       1 - value_01,     
                       value_01),         
    score_100 = score_01 * 100
  )

head(soc_scaled)

S_scores <- soc_scaled %>%
  group_by(year) %>%
  summarise(
    S_index = mean(score_100, na.rm = TRUE),
    .groups = "drop"
  )

head(S_scores)

# 5) Guardar para Power BI – formato europeo (coma decimal, ; separador)
write.csv2(S_scores, "S_scores.csv", row.names = FALSE)
