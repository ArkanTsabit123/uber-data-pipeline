# scripts/extract.py
# Extract data from CSV file

"""
Extract data from NYC Uber/Taxi CSV file.
Reads the raw data and saves it to a temporary location for transformation.
"""

import pandas as pd
import os

def extract_data(**context):
    """
    Extract data from CSV file
    
    Args:
        context: Airflow context dictionary
        
    Returns:
        dict: Dictionary with rows and columns count
        
    Raises:
        FileNotFoundError: If the data file doesn't exist
    """
    # Define data path
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'uber_data.csv'
    )
    
    # Check if file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")
    
    # Read CSV file
    df = pd.read_csv(data_path)
    
    # Save to temporary file for next task
    temp_path = '/tmp/uber_data.csv'
    df.to_csv(temp_path, index=False)
    
    # Print summary
    print(f"✅ Extracted {len(df):,} rows")
    print(f"📊 Columns: {df.columns.tolist()}")
    print(f"📋 Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"💾 Data saved to: {temp_path}")
    
    return {'rows': len(df), 'columns': len(df.columns)}