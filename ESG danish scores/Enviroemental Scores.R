library(dplyr)

# 1. Un valor por indicador y año
eco_year <- eco_all %>%
  group_by(indicator, year) %>%
  summarise(
    value = mean(value, na.rm = TRUE),
    .groups = "drop"
  )

# 2. Normalizar 
bad_E <- c("co2_per_kwh", "total_ghg_emissions")

eco_scaled <- eco_year %>%
  group_by(indicator) %>%
  mutate(
    v_min    = min(value, na.rm = TRUE),
    v_max    = max(value, na.rm = TRUE),
    value_01 = (value - v_min) / (v_max - v_min)   
  ) %>%
  ungroup() %>%
  mutate(
    score_01 = if_else(indicator %in% bad_E,
                       1 - value_01,   
                       value_01),      
    score_100 = score_01 * 100
  )

# 3. Índice ambiental por año
E_scores <- eco_scaled %>%
  group_by(year) %>%
  summarise(
    E_index = mean(score_100, na.rm = TRUE),
    .groups = "drop"
  )

head(E_scores)

write.csv2(E_scores, "E_scores.csv", row.names = FALSE)



eco_scaled %>%
  select(indicator, year, value, score_100) %>%
  arrange(indicator, year)


