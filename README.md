# ILO Wage Statistics Dataset

## Overview

This repository contains wage statistics data from the International Labour Organization (ILO), specifically focusing on average monthly earnings of employees disaggregated by sex and urban/rural areas.

## Dataset Description

The dataset contains wage statistics from various countries processed from ILO Statistics data:

- **Raw data**: `data-raw/EAR_4MTH_SEX_GEO_CUR_NB_A-filtered-2025-06-01.csv`
- **Cleaned data**: `ilostat_wage.csv`

Dataset characteristics:

- **Source**: ILO Statistics Database
- **Indicator**: Average monthly earnings of employees
- **Currency**: 2021 PPP $ (Purchasing Power Parity adjusted US Dollars)
- **Disaggregation**: By sex (Total, Male, Female) and area type (National, Rural, Urban)
- **Time Coverage**: Various years depending on country data availability
- **Filter Date**: 2025-06-01

## Data Structure

The cleaned dataset (`ilostat_wage.csv`) contains the following columns:

1. `country` - Country name
2. `source` - Data source (e.g., Labour Force Survey, Household Survey)
3. `indicator` - Indicator description
4. `sex` - Sex category (Total, Male, Female)
5. `area_type` - Geographic area type (National, Rural, Urban)
6. `currency_info` - Currency information
7. `year` - Year of observation
8. `earnings_ppp` - Average monthly earnings in 2021 PPP dollars
9. `obs_status` - Observation status (e.g., "Break in series")
10. `note_indicator` - Additional notes about the indicator
11. `note_source` - Notes about the data source

A data dictionary is available at `dictionary.csv`.

## Usage

This data can be used for:
- Analyzing wage gaps between sexes
- Comparing urban vs rural wage disparities
- Cross-country wage comparisons
- Temporal analysis of wage trends

## Data Source

Original data retrieved from the ILO Statistics Database (ILOSTAT).

## License

[License information to be added]

## Citation

When using this data, please cite:
International Labour Organization. ILOSTAT database. Available from https://ilostat.ilo.org/data/.