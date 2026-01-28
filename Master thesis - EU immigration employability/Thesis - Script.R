packages <- c("dplyr", "stringr", "readr", "purrr", "fixest")
to_install <- setdiff(packages, rownames(installed.packages()))
if(length(to_install)) install.packages(to_install)
lapply(packages, library, character.only = TRUE)

# 1. Helper functions
# Read CSVs inside ZIP files
read_zip_csvs <- function(zip_path, country_hint = NULL) {
  files_in_zip <- unzip(zip_path, list = TRUE)$Name
  csvs <- files_in_zip[grepl("\\.csv$", files_in_zip, ignore.case = TRUE)]
  if (length(csvs) == 0) return(tibble())
  
  map_dfr(csvs, function(member) {
    con <- unz(zip_path, member)
    df <- tryCatch(
      readr::read_csv(con, col_types = cols(.default = col_character()), show_col_types = FALSE),
      error = function(e) readr::read_csv2(unz(zip_path, member), col_types = cols(.default = col_character()), show_col_types = FALSE)
    )
    df %>% mutate(
      source_file = member,
      source_zip  = basename(zip_path),
      country_from_folder = country_hint
    )
  })
}

# Read loose CSV files
read_dir_csvs <- function(dir_path, country_hint = NULL) {
  files <- list.files(dir_path, pattern = "\\.csv$", full.names = TRUE, recursive = TRUE)
  if (length(files) == 0) return(tibble())
  
  map_dfr(files, function(f) {
    df <- tryCatch(
      readr::read_csv(f, col_types = cols(.default = col_character()), show_col_types = FALSE),
      error = function(e) readr::read_csv2(f, col_types = cols(.default = col_character()), show_col_types = FALSE)
    )
    df %>% mutate(
      source_file = basename(f),
      source_zip  = NA_character_,
      country_from_folder = country_hint
    )
  })
}

# Read one country folder
read_country_folder <- function(dir_path, country_hint = NULL) {
  df_csv <- read_dir_csvs(dir_path, country_hint)
  zips <- list.files(dir_path, pattern = "\\.zip$", full.names = TRUE, recursive = TRUE)
  df_zip <- if (length(zips)) map_dfr(zips, read_zip_csvs, country_hint = country_hint) else tibble()
  bind_rows(df_csv, df_zip)
}

# 2. Automatic reading of all countries

# Root folder containing ALL countries
base_dir <- "C:/Users/antes/OneDrive/Escritorio/Paises"

# List all subfolders (each one is a country)
subcarpetas <- list.dirs(base_dir, recursive = FALSE)

# Read all country folders automatically
Paises <- map_dfr(subcarpetas, function(path) {
  country_code <- toupper(basename(path)) # Country code from folder name
  read_country_folder(path, country_hint = country_code)
})

# 3.Checks

glimpse(Paises)
table(Paises$country_from_folder)

library(dplyr)
library(fixest)
library(broom)

# 3.1 Robust cleaning

df <- Paises %>%
  rename_with(tolower) %>%
  mutate(
    year   = suppressWarnings(as.integer(coalesce(as.character(year), refyear))),
    age    = suppressWarnings(as.integer(age)),
    weight = suppressWarnings(as.numeric(coeff))
  ) %>%
  # Working-age population
  filter(!is.na(year), !is.na(age), age >= 15, age <= 64)

# EDUCATION (H/M/L)
df <- df %>%
  mutate(
    educ3 = case_when(
      hatlev1d == "L" ~ "low",
      hatlev1d == "M" ~ "mid",
      hatlev1d == "H" ~ "high",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(!is.na(educ3))

# EXPERIENCE (proxied by age)
df <- df %>%
  mutate(
    exp4 = cut(age, breaks = c(15,25,35,45,65), right = FALSE,
               labels = c("0-9","10-19","20-29","30-49")),
    cell = interaction(educ3, exp4, drop = TRUE)
  ) %>%
  filter(!is.na(exp4))


# 3.2 Properly coded key variables

# Employment (ILOSTAT: 1=employed, 2=unemployed, 3=inactive)
df <- df %>%
  mutate(
    employed = case_when(
      ilostat == "1" ~ 1L,
      ilostat %in% c("2","3") ~ 0L,
      TRUE ~ NA_integer_
    )
  )

# Immigrant status (prioritize country of birth; treat NO ANSWER as NA, not as immigrant)
df <- df %>%
  mutate(
    immigrant = case_when(
      !is.na(countryb) & countryb %in% c("000", "000-OWN COUNTRY") ~ 0L,  # native
      !is.na(countryb) & countryb %in% c("NO ANSWER","NOT STATED","UNKNOWN") ~ NA_integer_,
      !is.na(countryb) ~ 1L,                                              # immigrant
      TRUE ~ NA_integer_
    ),
    native = if_else(!is.na(immigrant), 1L - immigrant, NA_integer_)
  )

# Keep only valid observations to construct rates
df <- df %>%
  filter(!is.na(employed), !is.na(immigrant), !is.na(native), !is.na(weight))

# 3.3 Aggregation: country × year × cell

agg <- df %>%
  group_by(country, year, cell, educ3) %>%
  summarise(
    N      = sum(weight, na.rm = TRUE),
    N_inm  = sum(weight * immigrant, na.rm = TRUE),
    N_nat  = sum(weight * native,    na.rm = TRUE),
    emp_nat= sum(weight * native * employed, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  # Drop cells without natives or with very few natives
  filter(!is.na(N_nat), N_nat > 0) %>%
  mutate(
    ImmShare        = N_inm / N,
    emp_rate_native = emp_nat / N_nat
  ) %>%
  # Drop degenerate cases (rates outside [0,1] or NA)
  filter(is.finite(emp_rate_native), emp_rate_native >= 0, emp_rate_native <= 1)

# Diagnostics: is there variability?
cat("Unique emp_rate_native:", length(unique(round(agg$emp_rate_native, 4))), "\n")
print(summary(agg$emp_rate_native))
print(summary(agg$ImmShare))

# 3.4 Fixed effects model

agg <- agg %>% mutate(cell_country = interaction(country, cell, drop = TRUE))

# Estimate only if there is variability
if (length(unique(agg$emp_rate_native)) > 1) {
  m_base <- feols(
    emp_rate_native ~ ImmShare | cell_country + year,
    data = agg,
    cluster = ~cell_country
  )
  print(summary(m_base))
  coefs_base <- broom::tidy(m_base)
  print(coefs_base)
} else {
  cat("\n[WARNING] emp_rate_native has insufficient variability after cleaning.\n",
      "Check immigrant/employed coding or relax filters.\n")
}

# H3 and H4

#Ensure 'agg' and 'm_base' already exist

# 0. Quick checks
agg %>%
  summarise(
    rows = n(),
    cells = n_distinct(cell_country),
    years = paste0(min(year, na.rm=TRUE), "-", max(year, na.rm=TRUE)),
    var_emp = length(unique(round(emp_rate_native,4))),
    var_imm = length(unique(round(ImmShare,4)))
  ) %>% print()

# H3: Heterogeneity by country cluster
# 1. Create cluster variable 
if (!"cluster" %in% names(agg)) {
  agg <- agg %>%
    mutate(
      cluster = case_when(
        country %in% c("FR","NL","DK")        ~ "Consolidated",
        country %in% c("ES","IT","EL")        ~ "Mediterranean",
        country %in% c("IE","EE")             ~ "Nordic",
        country %in% c("BG","RO","SK")        ~ "Senders",
        TRUE                                  ~ "Other"
      )
    )
}

# 2. Factor and reference 
agg <- agg %>% mutate(cluster = factor(cluster,
                                       levels = c("Consolidated","Mediterranean","Nordic","Senders","Other")))

# 3. H3 model: immigration effect by cluster
m_H3 <- feols(
  emp_rate_native ~ i(cluster, ImmShare, ref = "Consolidated") | cell_country + year,
  data = agg, cluster = ~cell_country
)
cat("\n=== H3: Immigration × Cluster (ref = Consolidated) ===\n")
print(summary(m_H3))

# 4. Joint tests
wald(m_H3, "cluster::Mediterranean#ImmShare = 0") %>% print()
wald(m_H3, "cluster::Nordic#ImmShare = 0") %>% print()
wald(m_H3, "cluster::Senders#ImmShare = 0") %>% print()

# 5. Table of marginal effects by cluster
eff_H3 <- broom::tidy(m_H3) %>%
  mutate(term_clean = gsub("cluster::", "", term)) %>%
  filter(grepl("ImmShare", term_clean)) %>%
  select(cluster_effect = term_clean, estimate, std.error, statistic, p.value) %>%
  arrange(cluster_effect)
cat("\nMarginal effect of ImmShare by cluster (ref=Consolidated):\n")
print(eff_H3)

# H4: Heterogeneity by education level
agg <- agg %>% mutate(educ3 = factor(educ3, levels = c("high","mid","low")))

m_H4 <- feols(
  emp_rate_native ~ i(educ3, ImmShare, ref = "high") | cell_country + year,
  data = agg, cluster = ~cell_country
)
cat("\n=== H4: Immigration × Education (ref = high) ===\n")
print(summary(m_H4))

wald(m_H4, "educ3::mid#ImmShare = 0") %>% print()
wald(m_H4, "educ3::low#ImmShare = 0") %>% print()

eff_H4 <- broom::tidy(m_H4) %>%
  mutate(term_clean = gsub("educ3::", "", term)) %>%
  filter(grepl("ImmShare", term_clean)) %>%
  select(educ_effect = term_clean, estimate, std.error, statistic, p.value) %>%
  arrange(educ_effect)
cat("\nMarginal effect of ImmShare by education level (ref=high):\n")
print(eff_H4)


# Export results to CSV
readr::write_csv(eff_H3, "effects_H3_cluster.csv")
readr::write_csv(eff_H4, "effects_H4_education.csv")


# Combined model: cluster + education
m_H3H4 <- feols(
  emp_rate_native ~ i(cluster, ImmShare, ref="Consolidated") + i(educ3, ImmShare, ref="high") | cell_country + year,
  data = agg, cluster = ~cell_country
)
cat("\n=== Combined model (H3 + H4) ===\n")
print(summary(m_H3H4))


# Robustness tests (panel diagnostics)
library(plm)
library(lmtest)
library(tibble)

pdata <- pdata.frame(agg, index = c("cell_country","year"))

plm_fe <- plm(emp_rate_native ~ ImmShare, data = pdata, model = "within", effect = "twoways")
plm_re <- plm(emp_rate_native ~ ImmShare, data = pdata, model = "random", effect = "twoways")

# Hausman test
haus <- phtest(plm_fe, plm_re)
haus_tbl <- tibble(
  test = "Hausman (FE vs RE)",
  statistic = as.numeric(haus$statistic),
  df = as.numeric(haus$parameter),
  p_value = as.numeric(haus$p.value),
  decision = ifelse(p_value < 0.05, "Reject RE → use FE", "Do not reject RE (FE preferred due to bias)")
)

# Heteroskedasticity
bp <- bptest(plm_fe)
bp_tbl <- tibble(
  test = "Breusch–Pagan (heteroskedasticity)",
  statistic = as.numeric(bp$statistic),
  df = as.numeric(bp$parameter),
  p_value = as.numeric(bp$p.value),
  decision = ifelse(p_value < 0.05, "Heteroskedasticity → use robust/cluster SE", "No heteroskedasticity")
)

# Autocorrelation tests
wdg <- tryCatch(pwartest(plm_fe), error = function(e) e)
bgp <- tryCatch(pbgtest(plm_fe), error = function(e) e)

wdg_tbl <- if (inherits(wdg, "error")) {
  tibble(test="Wooldridge (panel autocorrelation)", statistic=NA, df=NA, p_value=NA,
         decision=paste("Unavailable:", wdg$message))
} else {
  tibble(test="Wooldridge (panel autocorrelation)",
         statistic=as.numeric(wdg$statistic),
         df=as.numeric(wdg$parameter),
         p_value=as.numeric(wdg$p.value),
         decision=ifelse(p_value < 0.05,"Autocorrelation → clustered SE required","No autocorrelation"))
}

bgp_tbl <- if (inherits(bgp, "error")) {
  tibble(test="Breusch–Godfrey (panel autocorrelation)", statistic=NA, df=NA, p_value=NA,
         decision=paste("Unavailable:", bgp$message))
} else {
  tibble(test="Breusch–Godfrey (panel autocorrelation)",
         statistic=as.numeric(bgp$statistic),
         df=as.numeric(bgp$parameter),
         p_value=as.numeric(bgp$p.value),
         decision=ifelse(p_value < 0.05,"Autocorrelation → clustered SE required","No autocorrelation"))
}

robustness_tbl <- dplyr::bind_rows(haus_tbl, bp_tbl, wdg_tbl, bgp_tbl)
print(robustness_tbl)

readr::write_csv(robustness_tbl, "robustness_tests_base_model_complete.csv")
