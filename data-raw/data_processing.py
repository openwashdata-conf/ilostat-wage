#!/usr/bin/env python3
"""
Data processing script for ILO wage statistics

This script reads the raw ILO wage data and processes it into a tidy format
suitable for analysis and publication.
"""

import csv
import os

def process_wage_data():
    """Process raw ILO wage data into tidy format"""
    
    # Input and output file paths
    input_file = 'EAR_4MTH_SEX_GEO_CUR_NB_A-filtered-2025-06-01.csv'
    output_file = '../ilostat_wage.csv'
    
    # Read the raw data
    with open(input_file, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
    
    # Clean column names mapping
    clean_columns = {
        'ref_area.label': 'country',
        'source.label': 'source',
        'indicator.label': 'indicator',
        'sex.label': 'sex',
        'classif1.label': 'area_type',
        'classif2.label': 'currency_info',
        'time': 'year',
        'obs_value': 'earnings_ppp',
        'obs_status.label': 'obs_status',
        'note_indicator.label': 'note_indicator',
        'note_source.label': 'note_source'
    }
    
    # Write cleaned data
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=list(clean_columns.values()))
        writer.writeheader()
        
        for row in rows:
            clean_row = {}
            for old_col, new_col in clean_columns.items():
                clean_row[new_col] = row[old_col]
            
            # Clean area type - remove "Area type: " prefix
            if clean_row['area_type'].startswith('Area type: '):
                clean_row['area_type'] = clean_row['area_type'].replace('Area type: ', '')
                
            # Convert year to integer
            clean_row['year'] = int(clean_row['year'])
            
            # Convert earnings to float
            clean_row['earnings_ppp'] = float(clean_row['earnings_ppp'])
            
            writer.writerow(clean_row)
    
    print(f'Data processed successfully. Output saved to {output_file}')
    print(f'Total records processed: {len(rows)}')

if __name__ == '__main__':
    process_wage_data()