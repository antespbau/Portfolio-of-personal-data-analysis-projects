setwd("C:/Users/antes/OneDrive/Escritorio/ESG Barcos Noruega/Base de datos/ESG/Ecologic")
install.packages("janitor")

library(janitor)   
library(dplyr)    

csv_files <- list.files(pattern = "(?i)\\.csv$", full.names = TRUE)
csv_files

co2_kwh        <- read.csv2("CO2 emissions per kilowatt hour.csv",                                 stringsAsFactors = FALSE)
final_vs_gross <- read.csv2("Final energy consumption compared with gross energy consumption.csv", stringsAsFactors = FALSE)
gas_emiss      <- read.csv2("Gas Emissions.csv",                                                   stringsAsFactors = FALSE)
re_purpose     <- read.csv2("total energy consumption from renewable energy sources.csv",         stringsAsFactors = FALSE)
re_sector      <- read.csv2("total energy consumption of renewable energy, by sector.csv",        stringsAsFactors = FALSE)

co2_kwh        <- clean_names(co2_kwh)
final_vs_gross <- clean_names(final_vs_gross)
gas_emiss      <- clean_names(gas_emiss)
re_purpose     <- clean_names(re_purpose)
re_sector      <- clean_names(re_sector)

library(dplyr)

# 1. CO2 emissions per kWh
co2_kwh_std <- co2_kwh %>%
  rename(
    energy_type = energi1,
    year_raw    = tid,
    value_raw   = indhold
  ) %>%
  mutate(
    year  = as.integer(substr(year_raw, 1, 4)),             
    value = as.numeric(gsub(",", ".", value_raw)),           
    indicator = "co2_per_kwh"
  ) %>%
  select(indicator, year, energy_type, value)

# 2. Final energy consumption vs gross
final_vs_gross_std <- final_vs_gross %>%
  rename(
    area     = omrade,
    year_raw = tid,
    value_raw = indhold
  ) %>%
  mutate(
    year  = as.integer(substr(year_raw, 1, 4)),
    value = as.numeric(gsub(",", ".", value_raw)),
    indicator = "final_vs_gross_energy"
  ) %>%
  select(indicator, year, area, value)

# 3. Gas emissions (GHG)
gas_emiss_std <- gas_emiss %>%
  rename(
    emission_type = emtype8,
    year_raw      = tid,
    value_raw     = indhold
  ) %>%
  mutate(
    year  = as.integer(substr(year_raw, 1, 4)),
    value = as.numeric(gsub(",", ".", value_raw)),
    indicator = "total_ghg_emissions"
  ) %>%
  select(indicator, year, emission_type, value)

# 4. Renewable energy by purpose
re_purpose_std <- re_purpose %>%
  rename(
    purpose  = formal,
    year_raw = tid,
    value_raw = indhold
  ) %>%
  mutate(
    year  = as.integer(substr(year_raw, 1, 4)),
    value = as.numeric(gsub(",", ".", value_raw)),
    indicator = "re_share_by_purpose"
  ) %>%
  select(indicator, year, purpose, value)

# 5. Renewable energy by sector
re_sector_std <- re_sector %>%
  rename(
    sector   = branche,
    year_raw = tid,
    value_raw = indhold
  ) %>%
  mutate(
    year  = as.integer(substr(year_raw, 1, 4)),
    value = as.numeric(gsub(",", ".", value_raw)),
    indicator = "re_share_by_sector"
  ) %>%
  select(indicator, year, sector, value)

head(co2_kwh_std)
head(final_vs_gross_std)
head(gas_emiss_std)
head(re_purpose_std)
head(re_sector_std)

eco_all <- bind_rows(
  co2_kwh_std,
  final_vs_gross_std,
  gas_emiss_std,
  re_purpose_std,
  re_sector_std
)

head(eco_all)
unique(eco_all$indicator)

write.csv2(eco_all, "Ecology_clean_all.csv", row.names = FALSE)

