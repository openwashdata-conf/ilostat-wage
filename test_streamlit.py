#!/usr/bin/env python3
"""
Test script to verify the Streamlit dashboard works correctly
"""

import pandas as pd
import sys
import os

def test_data_loading():
    """Test if the CSV data loads correctly"""
    try:
        df = pd.read_csv("ilostat_wage.csv")
        print(f"✅ Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
        
        # Check required columns
        required_columns = ['country', 'sex', 'area_type', 'year', 'earnings_ppp']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing columns: {missing_columns}")
            return False
        else:
            print("✅ All required columns present")
        
        # Check data types
        print(f"✅ Countries available: {df['country'].nunique()}")
        print(f"✅ Years available: {df['year'].min()} - {df['year'].max()}")
        print(f"✅ Sex categories: {df['sex'].unique()}")
        print(f"✅ Area types: {df['area_type'].unique()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_streamlit_imports():
    """Test if all required packages can be imported"""
    try:
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import numpy as np
        print("✅ All required packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🧪 Testing Streamlit Dashboard Components")
    print("=" * 50)
    
    # Test imports
    if not test_streamlit_imports():
        sys.exit(1)
    
    # Test data loading
    if not test_data_loading():
        sys.exit(1)
    
    print("\n✅ All tests passed! The Streamlit dashboard should work correctly.")
    print("\nTo run the dashboard:")
    print("streamlit run streamlit_app.py")
    print("\nOr if streamlit is not in PATH:")
    print("python3 -m streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()