# ilostat-wage

<!-- badges: start -->

[![License: CC BY
4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![R-CMD-check](https://github.com/openwashdata-conf/ilostat-wage/workflows/R-CMD-check/badge.svg)](https://github.com/openwashdata-conf/ilostat-wage/actions)

<!-- badges: end -->

This repository contains wage statistics data from the International Labour Organization (ILO), specifically focusing on average monthly earnings of employees disaggregated by sex and urban/rural areas. The data has been processed following the openwashdata publishing guidelines to provide a tidy dataset suitable for analysis.

## Installation

You can download the dataset as a CSV file from the table below.

| dataset      | CSV                                                                                                       |
|:-------------|:----------------------------------------------------------------------------------------------------------|
| ilostat_wage | [Download CSV](https://github.com/openwashdata-conf/ilostat-wage/raw/main/ilostat_wage.csv) |

## Data

The package provides access to ILO wage statistics data processed from the ILO Statistics Database.

``` r
library(readr)
library(dplyr)
library(gt)

# Read the dataset
ilostat_wage <- read_csv("ilostat_wage.csv")
```

### ilostat_wage

The dataset `ilostat_wage` contains wage statistics from various countries processed from ILO Statistics data.
It has 6235 observations and 11 variables.

``` r
ilostat_wage |> 
  head(3) |> 
  gt::gt() |>
  gt::as_raw_html()
```

For an overview of the variable names, see the following table.

| variable_name   | variable_type | description                                      |
|:----------------|:--------------|:-------------------------------------------------|
| country         | character     | Country or territory name                        |
| source          | character     | Data source survey type                          |
| indicator       | character     | Indicator description                            |
| sex             | character     | Sex category (Total/Male/Female)                 |
| area_type       | character     | Geographic area type (National/Rural/Urban)     |
| currency_info   | character     | Currency information                             |
| year            | numeric       | Year of observation                              |
| earnings_ppp    | numeric       | Average monthly earnings in 2021 PPP dollars    |
| obs_status      | character     | Observation status notes                         |
| note_indicator  | character     | Additional indicator notes                       |
| note_source     | character     | Data source notes                                |

## Dataset Description

Dataset characteristics:

- **Source**: ILO Statistics Database
- **Indicator**: Average monthly earnings of employees
- **Currency**: 2021 PPP $ (Purchasing Power Parity adjusted US Dollars)
- **Disaggregation**: By sex (Total, Male, Female) and area type (National, Rural, Urban)
- **Time Coverage**: Various years depending on country data availability
- **Filter Date**: 2025-06-01

## Example

``` r
library(ggplot2)
library(tidyverse)

# Distribution of earnings by sex
ilostat_wage |>
  filter(sex != "Total", !is.na(earnings_ppp)) |>
  ggplot(aes(x = earnings_ppp, fill = sex)) +
  geom_histogram(alpha = 0.7, position = "identity", bins = 30) +
  scale_x_log10() +
  labs(title = "Distribution of Monthly Earnings by Sex",
       x = "Monthly Earnings (2021 PPP $, log scale)",
       y = "Frequency",
       fill = "Sex") +
  theme_minimal()
```

### Which countries have the highest wage gaps?

``` r
# Calculate wage gaps by country
wage_gaps <- ilostat_wage |>
  filter(sex %in% c("Male", "Female"), 
         area_type == "National",
         !is.na(earnings_ppp)) |>
  group_by(country, year) |>
  filter(n() == 2) |>  # Only countries with both male and female data
  summarise(
    male_earnings = earnings_ppp[sex == "Male"],
    female_earnings = earnings_ppp[sex == "Female"],
    wage_gap = (male_earnings - female_earnings) / male_earnings * 100,
    .groups = "drop"
  ) |>
  arrange(desc(wage_gap))

wage_gaps |>
  head(10) |>
  gt::gt() |>
  gt::fmt_number(columns = c(male_earnings, female_earnings), decimals = 0) |>
  gt::fmt_number(columns = wage_gap, decimals = 1, suffix = "%") |>
  gt::as_raw_html()
```

### Urban vs Rural wage differences

``` r
# Compare urban vs rural wages
ilostat_wage |>
  filter(area_type %in% c("Urban", "Rural"),
         sex == "Total",
         !is.na(earnings_ppp)) |>
  ggplot(aes(x = area_type, y = earnings_ppp, fill = area_type)) +
  geom_boxplot() +
  scale_y_log10() +
  labs(title = "Urban vs Rural Monthly Earnings Distribution",
       x = "Area Type",
       y = "Monthly Earnings (2021 PPP $, log scale)",
       fill = "Area Type") +
  theme_minimal()
```

## License

Data are available as
[CC-BY](https://github.com/openwashdata-conf/ilostat-wage/blob/main/LICENSE).

## Citation

Please cite this dataset using:

International Labour Organization. ILOSTAT database. Available from https://ilostat.ilo.org/data/.

For this processed dataset, please also cite:
[Author]. (2025). ILO Wage Statistics Dataset. Retrieved from https://github.com/openwashdata-conf/ilostat-wage