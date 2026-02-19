"""
Excel Upgrade
"""

import pandas as pd
import os
import re

def get_latest_sheet_name(xls_file):
    """
    Returns the sheet name representing the most recent year.
    """
    sheets = xls_file.sheet_names
    try:
        sorted_sheets = sorted(sheets, key=lambda x: int(x), reverse=True)
        return sorted_sheets[0]
    except ValueError:
        return sheets[-1]

def find_column(df, keywords):
    """
    Helper function to find a column that matches one of the keywords.
    Case-insensitive partial match.
    """
    clean_cols = [str(c).strip().lower() for c in df.columns]
    
    for keyword in keywords:
        for i, col in enumerate(clean_cols):
            if col == keyword or (len(keyword) > 2 and keyword in col):
                return df.columns[i]
    return None

def get_forecast_data(sku, location, filename="Sales_Excel.xlsx"):
    """
    Reads the Excel file, finds the latest year, handles duplicates 
    by picking the row with the HIGHEST TOTAL SALES.
    """
    if not os.path.exists(filename):
        csv_name = filename + " - 2025.csv"
        if os.path.exists(csv_name):
            filename = csv_name
            is_csv = True
        else:
            print(f"Error: File '{filename}' not found.")
            return None
    else:
        is_csv = False

    try:
        if is_csv:
            print(f"Loading data from CSV: {filename}...")
            df = pd.read_csv(filename)
            latest_sheet = "CSV"
        else:
            xls = pd.ExcelFile(filename)
            latest_sheet = get_latest_sheet_name(xls)
            print(f"Loading forecast from sheet: {latest_sheet}...")
            df = pd.read_excel(xls, sheet_name=latest_sheet)

        # Minimize NaN error by filling in blanks as 0's
        df = df.fillna(0)
        
        # 1. Identify Key Columns dynamically
        col_sku = find_column(df, ['sku', 'item', 'item sku'])
        col_loc = find_column(df, ['location', 'loc', 'warehouse'])
        
        if not col_sku or not col_loc:
            print("Error: Could not identify 'SKU' or 'Location' columns in the file.")
            return None

        # 2. Identify Month Columns dynamically
        month_map = {}
        target_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                         'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        
        for m in target_months:
            # Look for 'jan', 'january', 'jan.', etc.
            found_col = find_column(df, [m, m + '.', m + 'uary', m + 'ruary', m + 'ch', m + 'il', m + 'e', m + 'y', m + 'ust', m + 'ember', m + 'ober'])
            if found_col:
                month_map[m] = found_col

        # 3. Filter for the specific SKU and Location
        # Clean the input and the dataframe columns for comparison
        target_sku = str(sku).strip().lower()
        target_loc = str(location).strip().lower()
        
        mask = (df[col_sku].astype(str).str.strip().str.lower() == target_sku) & \
               (df[col_loc].astype(str).str.strip().str.lower() == target_loc)
        
        matches = df[mask].copy()
        
        if matches.empty:
            print(f"Error: SKU '{sku}' at '{location}' not found in '{latest_sheet}'.")
            return None
            
        # 4. Handle Duplicates: Calculate Total Sales based on FOUND columns
        valid_month_cols = list(month_map.values())
        
        # Sum the month columns row-by-row
        matches['calculated_total'] = matches[valid_month_cols].sum(axis=1, numeric_only=True)
        
        # Sort by highest sales
        matches = matches.sort_values(by='calculated_total', ascending=False)
        
        # Pick the winner
        best_match_row = matches.iloc[0]
        
        # 5. Build the result dictionary using the standard keys your other scripts expect
        result = {}
        for std_key, excel_col in month_map.items():
            result[std_key] = best_match_row[excel_col]
        
        # Handle SRV separately
        col_srv = find_column(df, ['srv', 'service', 'van'])
        if col_srv:
            result['srv'] = best_match_row[col_srv]
        else:
            result['srv'] = 0

        # Handle 'oct' vs 'octo' mismatch for your specific code
        if 'oct' in result:
            result['octo'] = result['oct']

        print(f"Selected entry with Calculated Total Sales: {best_match_row['calculated_total']}")
        return result

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

