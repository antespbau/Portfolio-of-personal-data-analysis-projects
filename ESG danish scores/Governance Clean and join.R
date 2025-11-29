

setwd("C:/Users/antes/OneDrive/Escritorio/ESG Barcos Noruega/Base de datos/ESG/Governance")
+
library(dplyr)
library(tidyr)

gov_all <- read.csv2("Governance_clean_all.csv", stringsAsFactors = FALSE)

gov_all <- gov_all %>%
  mutate(
    value = as.numeric(gsub(",", ".", value))
  )

cpi_year <- gov_all %>%
  filter(indicator == "cpi_score") %>%
  group_by(year) %>%
  summarise(
    cpi_value = mean(value, na.rm = TRUE),
    .groups = "drop"
  )

trust_rows <- gov_all %>%
  filter(indicator == "trust_in_institutions")

trust_good_years <- trust_rows %>%
  filter(year %in% c(2016, 2018, 2021, 2023))

dim_cols <- setdiff(
  names(trust_good_years),
  c("indicator", "year", "value", "year_raw", "value_raw")
)

if (length(dim_cols) == 0) {
  
  trust_year <- trust_good_years %>%
    group_by(year) %>%
    summarise(
      trust_value = mean(value, na.rm = TRUE),
      .groups = "drop"
    )
  
} else {
  
  inst_by_year <- trust_good_years %>%
    group_by(year, across(all_of(dim_cols))) %>%
    summarise(n = n(), .groups = "drop")
  
  common_combos <- inst_by_year %>%
    group_by(across(all_of(dim_cols))) %>%
    summarise(
      years_present = n_distinct(year),
      .groups = "drop"
    ) %>%
    filter(years_present == 4) %>%
    select(-years_present)
  

  trust_clean <- trust_good_years %>%
    inner_join(common_combos, by = dim_cols)
  
  
  trust_year <- trust_clean %>%
    group_by(year) %>%
    summarise(
      trust_value = mean(value, na.rm = TRUE),
      .groups = "drop"
    )
}

head(trust_year)

gov_year <- cpi_year %>%
  inner_join(trust_year, by = "year") %>% 
  pivot_longer(
    cols = c(cpi_value, trust_value),
    names_to = "indicator",
    values_to = "value"
  )

head(gov_year)

gov_scaled <- gov_year %>%
  group_by(indicator) %>%
  mutate(
    v_min    = min(value, na.rm = TRUE),
    v_max    = max(value, na.rm = TRUE),
    value_01 = ifelse(
      v_max == v_min,
      0.5,  
      (value - v_min) / (v_max - v_min)
    ),
    score_01  = value_01,        
    score_100 = score_01 * 100
  ) %>%
  ungroup()

head(gov_scaled)

G_scores <- gov_scaled %>%
  group_by(year) %>%
  summarise(
    G_index = mean(score_100, na.rm = TRUE),
    .groups = "drop"
  )

head(G_scores)

write.csv2(G_scores, "G_scores.csv", row.names = FALSE)
