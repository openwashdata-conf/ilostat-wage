# 💰 Wage Disparity Dashboard

An interactive Streamlit dashboard for analyzing wage disparities from the International Labour Organization (ILO) dataset.

## Features

### 🔍 Wage Disparity Tool
- **Country Selection**: Choose any country from the dataset
- **Gender Analysis**: View wage disparities between male and female workers
- **Regional Analysis**: Compare urban vs rural wage differences
- **Metrics**: Calculate wage gap percentages and summary statistics

### 📈 Trends Tool
- **Time Period Selection**: Analyze trends over custom year ranges
- **Gender Trends**: Track how gender wage gaps change over time
- **Regional Trends**: Monitor urban-rural wage disparities over time
- **Gap Trends**: Visualize wage gap percentages as time series

### 🔄 Comparison Tool
- **Two-Country Comparison**: Compare wage patterns between any two countries
- **Multi-faceted Analysis**: View comparisons across gender and regional dimensions
- **Time Series**: Track comparative wage trends over time
- **Summary Statistics**: Side-by-side country statistics

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

Or if streamlit is not in your PATH:
```bash
python3 -m streamlit run streamlit_app.py
```

## Requirements

- Python 3.7+
- streamlit >= 1.28.0
- pandas >= 1.5.0
- plotly >= 5.15.0
- numpy >= 1.21.0

## Data Source

The dashboard uses the cleaned ILO wage statistics dataset (`ilostat_wage.csv`) which contains:
- 6,234 observations across 111 countries
- Years 2014-2024
- Gender categories: Total, Male, Female, Other
- Area types: National, Rural, Urban
- Earnings in 2021 PPP adjusted US Dollars

## Usage

1. **Select a Tool**: Use the sidebar to choose between the three analysis tools
2. **Configure Parameters**: Select countries, time periods, or comparison criteria
3. **Explore Visualizations**: Interactive charts update automatically based on your selections
4. **View Metrics**: Summary statistics and calculated wage gaps are displayed alongside charts

## Chart Types

- **Bar Charts**: For comparing wage levels between groups
- **Line Charts**: For tracking trends over time
- **Faceted Charts**: For multi-dimensional comparisons
- **Interactive Elements**: Hover for detailed information

## Testing

Run the test script to verify everything works correctly:
```bash
python3 test_streamlit.py
```

This will check:
- Data loading functionality
- Required package imports
- Data structure validity
- Available countries and years

## Features by Tool

### Wage Disparity Tool
- Side-by-side gender and regional wage charts
- Wage gap percentage calculations
- Summary statistics (average earnings, data availability)
- Latest year data prioritization

### Trends Tool
- Year range slider for custom time periods
- Separate trend lines for different categories
- Combined wage gap trend visualization
- Data availability warnings

### Comparison Tool
- Dual country selection interface
- Multiple comparison dimensions
- Faceted visualizations for detailed analysis
- Comparative summary statistics

## Limitations

- Data availability varies by country and year
- Some countries may have limited gender or regional data
- Wage gap calculations require data for both comparison groups
- Time series analysis depends on multi-year data availability