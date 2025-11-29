setwd("C:/Users/antes/OneDrive/Escritorio/ESG Barcos Noruega/Base de datos/ESG/Social")

library(janitor)   # for clean_names()
library(dplyr)     # for mutate, rename, etc.


csv_files <- list.files(pattern = "(?i)\\.csv$", full.names = TRUE)
csv_files



# 2. Read raw CSVs
gender_discr   <- read.csv2("Gender discrimination cases upheld.csv",
                            stringsAsFactors = FALSE)
sick_days      <- read.csv2("Number of days of absence per full-time employee per year, by age group and sex.csv",
                            stringsAsFactors = FALSE)
palma          <- read.csv2("Palma ratio.csv",
                            stringsAsFactors = FALSE)
low_income     <- read.csv2("Proportion of persons in the low-income group.csv",
                            stringsAsFactors = FALSE)
soc_benefits   <- read.csv2("Proportion of the working-age population on social security benefits.csv",
                            stringsAsFactors = FALSE)
edu_completed  <- read.csv2("who have completed lower secondary school.csv",
                            stringsAsFactors = FALSE)

# 3. Clean column names
gender_discr   <- clean_names(gender_discr)
sick_days      <- clean_names(sick_days)
palma          <- clean_names(palma)
low_income     <- clean_names(low_income)
soc_benefits   <- clean_names(soc_benefits)
edu_completed  <- clean_names(edu_completed)



## 4. Standardise each dataset 

## 4.1) Gender discrimination cases upheld
gender_discr_std <- gender_discr %>%
  rename(
    case_type = type,
    year_raw  = tid,
    value_raw = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "gender_discr_upheld_cases"
  ) %>%
  select(indicator, year, case_type, value)

head(gender_discr_std)


## 4.2) Days of absence per full-time employee

sick_days_std <- sick_days %>%
  rename(
    absence_desc = fravaer1,
    absence_type = fravaer,
    sector       = sektor,
    sex          = kon,
    age_group    = alder,
    year_raw     = tid,
    value_raw    = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "sick_days_per_employee"
  ) %>%
  select(indicator, year, absence_type, sector, sex, age_group, value)

head(sick_days_std)


## 4.3) Palma ratio (inequality)
palma_std <- palma %>%
  rename(
    palma_type = decilgen,
    year_raw   = tid,
    value_raw  = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "palma_ratio"
  ) %>%
  select(indicator, year, palma_type, value)

head(palma_std)


## 4.4) Proportion of persons in the low-income group (poverty)
low_income_std <- low_income %>%
  rename(
    income_status = antar,   # <- THIS is the correct column name
    year_raw      = tid,
    value_raw     = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "low_income_share"
  ) %>%
  select(indicator, year, income_status, value)

head(low_income_std)


## 4.5) Working-age population on social security benefits
soc_benefits_std <- soc_benefits %>%
  rename(
    benefit_type = ydelsestype,
    year_raw     = tid,
    value_raw    = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "social_benefits_share"
  ) %>%
  select(indicator, year, benefit_type, value)

head(soc_benefits_std)


## 4.6) Completed lower secondary school
edu_completed_std <- edu_completed %>%
  rename(
    education_group = uddannelse,
    year_raw        = tid,
    value_raw       = indhold
  ) %>%
  mutate(
    year   = as.integer(year_raw),
    value  = as.numeric(gsub(",", ".", value_raw)),
    indicator = "completed_lower_secondary_share"
  ) %>%
  select(indicator, year, education_group, value)

head(edu_completed_std)


## 5) Combine all Social indicators into one long table

soc_all <- bind_rows(
  gender_discr_std,
  sick_days_std,
  palma_std,
  low_income_std,
  soc_benefits_std,
  edu_completed_std
)

head(soc_all)
unique(soc_all$indicator)
str(soc_all)

## 6) Save Social clean table
write.csv2(soc_all, "Social_clean_all.csv", row.names = FALSE)

