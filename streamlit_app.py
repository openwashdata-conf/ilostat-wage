import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Set page config
st.set_page_config(
    page_title="Wage Disparity Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    """Load the ILO wage statistics data"""
    return pd.read_csv("ilostat_wage.csv")

# Load the data
df = load_data()

# Title and description
st.title("💰 Wage Disparity Dashboard")
st.markdown("""
This dashboard visualizes wage disparities from the International Labour Organization (ILO) dataset, 
focusing on gender and regional differences in earnings across countries and time periods.
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
tool_selection = st.sidebar.radio(
    "Select Tool:",
    ["Wage Disparity Tool", "Trends Tool", "Comparison Tool"]
)

# Tool 1: Wage Disparity Tool
if tool_selection == "Wage Disparity Tool":
    st.header("🔍 Wage Disparity Analysis")
    st.markdown("Select a country to analyze wage disparities by gender and region.")
    
    # Country selection
    countries = sorted(df['country'].unique())
    selected_country = st.selectbox("Select Country:", countries)
    
    # Filter data for selected country
    country_data = df[df['country'] == selected_country]
    
    if not country_data.empty:
        # Create two columns for the charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Gender Wage Disparity")
            
            # Gender disparity chart
            gender_data = country_data[
                (country_data['sex'].isin(['Male', 'Female'])) & 
                (country_data['area_type'] == 'National') &
                (country_data['earnings_ppp'].notna())
            ]
            
            if not gender_data.empty:
                # Get the latest year with data for both genders
                latest_year_data = gender_data.groupby('year').filter(lambda x: len(x) == 2).tail(2)
                
                if not latest_year_data.empty:
                    fig_gender = px.bar(
                        latest_year_data,
                        x='sex',
                        y='earnings_ppp',
                        title=f"Gender Wage Disparity - {selected_country}",
                        labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'sex': 'Gender'},
                        color='sex',
                        color_discrete_map={'Male': '#1f77b4', 'Female': '#ff7f0e'}
                    )
                    
                    # Calculate wage gap
                    male_earnings = latest_year_data[latest_year_data['sex'] == 'Male']['earnings_ppp'].iloc[0]
                    female_earnings = latest_year_data[latest_year_data['sex'] == 'Female']['earnings_ppp'].iloc[0]
                    wage_gap = ((male_earnings - female_earnings) / male_earnings) * 100
                    
                    st.plotly_chart(fig_gender, use_container_width=True)
                    st.metric("Gender Wage Gap", f"{wage_gap:.1f}%", 
                             help="Percentage difference between male and female earnings")
                else:
                    st.warning("No gender comparison data available for this country")
            else:
                st.warning("No gender data available for this country")
        
        with col2:
            st.subheader("🏙️ Regional Wage Disparity")
            
            # Regional disparity chart
            regional_data = country_data[
                (country_data['area_type'].isin(['Urban', 'Rural'])) & 
                (country_data['sex'] == 'Total') &
                (country_data['earnings_ppp'].notna())
            ]
            
            if not regional_data.empty:
                # Get the latest year with data for both regions
                latest_regional_data = regional_data.groupby('year').filter(lambda x: len(x) == 2).tail(2)
                
                if not latest_regional_data.empty:
                    fig_regional = px.bar(
                        latest_regional_data,
                        x='area_type',
                        y='earnings_ppp',
                        title=f"Regional Wage Disparity - {selected_country}",
                        labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'area_type': 'Area Type'},
                        color='area_type',
                        color_discrete_map={'Urban': '#2ca02c', 'Rural': '#d62728'}
                    )
                    
                    # Calculate regional gap
                    urban_earnings = latest_regional_data[latest_regional_data['area_type'] == 'Urban']['earnings_ppp'].iloc[0]
                    rural_earnings = latest_regional_data[latest_regional_data['area_type'] == 'Rural']['earnings_ppp'].iloc[0]
                    regional_gap = ((urban_earnings - rural_earnings) / urban_earnings) * 100
                    
                    st.plotly_chart(fig_regional, use_container_width=True)
                    st.metric("Urban-Rural Wage Gap", f"{regional_gap:.1f}%",
                             help="Percentage difference between urban and rural earnings")
                else:
                    st.warning("No regional comparison data available for this country")
            else:
                st.warning("No regional data available for this country")
        
        # Additional statistics
        st.subheader("📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_earnings = country_data[country_data['sex'] == 'Total']['earnings_ppp'].mean()
            st.metric("Average National Earnings", f"${avg_earnings:.0f}")
        
        with col2:
            years_available = country_data['year'].nunique()
            st.metric("Years of Data", years_available)
        
        with col3:
            latest_year = country_data['year'].max()
            st.metric("Latest Data Year", latest_year)
        
        with col4:
            data_points = len(country_data)
            st.metric("Total Data Points", data_points)
    
    else:
        st.error("No data available for the selected country")

# Tool 2: Trends Tool
elif tool_selection == "Trends Tool":
    st.header("📈 Wage Trends Analysis")
    st.markdown("Analyze wage disparity trends over time for a selected country.")
    
    # Country selection
    countries = sorted(df['country'].unique())
    selected_country = st.selectbox("Select Country:", countries)
    
    # Filter data for selected country
    country_data = df[df['country'] == selected_country]
    
    if not country_data.empty:
        # Year range selection
        min_year = int(country_data['year'].min())
        max_year = int(country_data['year'].max())
        
        year_range = st.slider(
            "Select Year Range:",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )
        
        # Filter by year range
        filtered_data = country_data[
            (country_data['year'] >= year_range[0]) & 
            (country_data['year'] <= year_range[1])
        ]
        
        # Create two columns for trend charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Gender Wage Trends")
            
            # Gender trends
            gender_trends = filtered_data[
                (filtered_data['sex'].isin(['Male', 'Female'])) & 
                (filtered_data['area_type'] == 'National') &
                (filtered_data['earnings_ppp'].notna())
            ]
            
            if not gender_trends.empty:
                fig_gender_trends = px.line(
                    gender_trends,
                    x='year',
                    y='earnings_ppp',
                    color='sex',
                    title=f"Gender Wage Trends - {selected_country}",
                    labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'year': 'Year'},
                    markers=True
                )
                st.plotly_chart(fig_gender_trends, use_container_width=True)
            else:
                st.warning("No gender trend data available for the selected period")
        
        with col2:
            st.subheader("🏙️ Regional Wage Trends")
            
            # Regional trends
            regional_trends = filtered_data[
                (filtered_data['area_type'].isin(['Urban', 'Rural'])) & 
                (filtered_data['sex'] == 'Total') &
                (filtered_data['earnings_ppp'].notna())
            ]
            
            if not regional_trends.empty:
                fig_regional_trends = px.line(
                    regional_trends,
                    x='year',
                    y='earnings_ppp',
                    color='area_type',
                    title=f"Regional Wage Trends - {selected_country}",
                    labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'year': 'Year'},
                    markers=True
                )
                st.plotly_chart(fig_regional_trends, use_container_width=True)
            else:
                st.warning("No regional trend data available for the selected period")
        
        # Wage gap trends
        st.subheader("📊 Wage Gap Trends")
        
        # Calculate gender wage gap over time
        gender_gap_data = []
        for year in filtered_data['year'].unique():
            year_data = filtered_data[
                (filtered_data['year'] == year) & 
                (filtered_data['area_type'] == 'National') &
                (filtered_data['sex'].isin(['Male', 'Female']))
            ]
            
            if len(year_data) == 2:
                male_earnings = year_data[year_data['sex'] == 'Male']['earnings_ppp'].iloc[0]
                female_earnings = year_data[year_data['sex'] == 'Female']['earnings_ppp'].iloc[0]
                wage_gap = ((male_earnings - female_earnings) / male_earnings) * 100
                gender_gap_data.append({'year': year, 'wage_gap': wage_gap, 'type': 'Gender Gap'})
        
        # Calculate regional wage gap over time
        regional_gap_data = []
        for year in filtered_data['year'].unique():
            year_data = filtered_data[
                (filtered_data['year'] == year) & 
                (filtered_data['sex'] == 'Total') &
                (filtered_data['area_type'].isin(['Urban', 'Rural']))
            ]
            
            if len(year_data) == 2:
                urban_earnings = year_data[year_data['area_type'] == 'Urban']['earnings_ppp'].iloc[0]
                rural_earnings = year_data[year_data['area_type'] == 'Rural']['earnings_ppp'].iloc[0]
                regional_gap = ((urban_earnings - rural_earnings) / urban_earnings) * 100
                regional_gap_data.append({'year': year, 'wage_gap': regional_gap, 'type': 'Regional Gap'})
        
        # Combine gap data
        all_gap_data = gender_gap_data + regional_gap_data
        
        if all_gap_data:
            gap_df = pd.DataFrame(all_gap_data)
            fig_gaps = px.line(
                gap_df,
                x='year',
                y='wage_gap',
                color='type',
                title=f"Wage Gap Trends - {selected_country}",
                labels={'wage_gap': 'Wage Gap (%)', 'year': 'Year'},
                markers=True
            )
            st.plotly_chart(fig_gaps, use_container_width=True)
        else:
            st.warning("No wage gap trend data available for the selected period")
    
    else:
        st.error("No data available for the selected country")

# Tool 3: Comparison Tool
elif tool_selection == "Comparison Tool":
    st.header("🔄 Country Comparison")
    st.markdown("Compare wage disparities between two countries over time.")
    
    # Country selection
    countries = sorted(df['country'].unique())
    
    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select First Country:", countries, key="country1")
    with col2:
        country2 = st.selectbox("Select Second Country:", countries, key="country2")
    
    if country1 != country2:
        # Filter data for both countries
        comparison_data = df[df['country'].isin([country1, country2])]
        
        if not comparison_data.empty:
            # Create comparison charts
            st.subheader("📊 Average Wage Comparison")
            
            # National average wages over time
            national_data = comparison_data[
                (comparison_data['sex'] == 'Total') & 
                (comparison_data['area_type'] == 'National') &
                (comparison_data['earnings_ppp'].notna())
            ]
            
            if not national_data.empty:
                fig_comparison = px.line(
                    national_data,
                    x='year',
                    y='earnings_ppp',
                    color='country',
                    title=f"National Average Wages: {country1} vs {country2}",
                    labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'year': 'Year'},
                    markers=True
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Gender comparison
            st.subheader("👥 Gender Wage Comparison")
            
            gender_comparison = comparison_data[
                (comparison_data['sex'].isin(['Male', 'Female'])) & 
                (comparison_data['area_type'] == 'National') &
                (comparison_data['earnings_ppp'].notna())
            ]
            
            if not gender_comparison.empty:
                fig_gender_comparison = px.line(
                    gender_comparison,
                    x='year',
                    y='earnings_ppp',
                    color='country',
                    facet_col='sex',
                    title=f"Gender Wage Comparison: {country1} vs {country2}",
                    labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'year': 'Year'},
                    markers=True
                )
                st.plotly_chart(fig_gender_comparison, use_container_width=True)
            
            # Regional comparison
            st.subheader("🏙️ Regional Wage Comparison")
            
            regional_comparison = comparison_data[
                (comparison_data['area_type'].isin(['Urban', 'Rural'])) & 
                (comparison_data['sex'] == 'Total') &
                (comparison_data['earnings_ppp'].notna())
            ]
            
            if not regional_comparison.empty:
                fig_regional_comparison = px.line(
                    regional_comparison,
                    x='year',
                    y='earnings_ppp',
                    color='country',
                    facet_col='area_type',
                    title=f"Regional Wage Comparison: {country1} vs {country2}",
                    labels={'earnings_ppp': 'Monthly Earnings (2021 PPP $)', 'year': 'Year'},
                    markers=True
                )
                st.plotly_chart(fig_regional_comparison, use_container_width=True)
            
            # Summary statistics comparison
            st.subheader("📈 Summary Statistics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**{country1}**")
                country1_data = comparison_data[comparison_data['country'] == country1]
                avg_earnings_1 = country1_data[country1_data['sex'] == 'Total']['earnings_ppp'].mean()
                years_1 = country1_data['year'].nunique()
                latest_year_1 = country1_data['year'].max()
                
                st.metric("Average Earnings", f"${avg_earnings_1:.0f}")
                st.metric("Years of Data", years_1)
                st.metric("Latest Data Year", latest_year_1)
            
            with col2:
                st.markdown(f"**{country2}**")
                country2_data = comparison_data[comparison_data['country'] == country2]
                avg_earnings_2 = country2_data[country2_data['sex'] == 'Total']['earnings_ppp'].mean()
                years_2 = country2_data['year'].nunique()
                latest_year_2 = country2_data['year'].max()
                
                st.metric("Average Earnings", f"${avg_earnings_2:.0f}")
                st.metric("Years of Data", years_2)
                st.metric("Latest Data Year", latest_year_2)
        
        else:
            st.error("No data available for the selected countries")
    
    else:
        st.warning("Please select two different countries for comparison")

# Footer
st.markdown("---")
st.markdown("""
**Data Source:** International Labour Organization (ILO) Statistics Database  
**Dataset:** Average monthly earnings of employees by sex and rural/urban areas  
**Currency:** 2021 PPP $ (Purchasing Power Parity adjusted US Dollars)
""")