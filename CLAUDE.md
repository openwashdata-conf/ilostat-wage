# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a data repository containing ILO (International Labour Organization) wage statistics following the openwashdata publishing guidelines. The repository processes raw ILO wage data into a tidy format suitable for analysis and publication.

## Data Architecture

The repository follows the openwashdata data package structure:

- **Raw data**: `data-raw/` contains the original ILO data file and processing scripts
- **Cleaned data**: `ilostat_wage.csv` is the main tidy dataset in the repository root
- **Data dictionary**: `data-raw/dictionary.csv` defines all variables in the cleaned dataset
- **Processing script**: `data-raw/data_processing.py` handles the raw-to-clean data transformation

## Key Data Processing Commands

To regenerate the cleaned dataset from raw data:
```bash
cd data-raw
python3 data_processing.py
```

This script:
1. Reads the raw CSV file with ILO column names (e.g., `ref_area.label`, `obs_value`)
2. Maps to clean column names (e.g., `country`, `earnings_ppp`)
3. Cleans area type values by removing "Area type: " prefix
4. Converts data types (year to int, earnings to float)
5. Outputs the tidy dataset to `../ilostat_wage.csv`

## Data Structure

The cleaned dataset contains wage statistics with these key variables:
- `country`: Country/territory name
- `sex`: Total, Male, Female
- `area_type`: National, Rural, Urban
- `year`: Year of observation
- `earnings_ppp`: Average monthly earnings in 2021 PPP dollars
- `obs_status`: Data quality notes (e.g., "Break in series")

## Publishing Guidelines

This repository follows the openwashdata/washr data publishing workflow:
- All raw data and processing scripts must be in `data-raw/`
- The data dictionary must be in `data-raw/dictionary.csv` with columns: variable_name, variable_type, description
- The final cleaned dataset should be in the repository root as a CSV file
- Documentation should follow FAIR principles (Findable, Accessible, Interoperable, Reproducible)