# scripts/transform.py
# Transform data into Star Schema

"""
Transform raw NYC Uber/Taxi data into a Star Schema with 4 tables:
1. datetime_dim - Time dimensions
2. rate_code_dim - Rate code mappings
3. location_dim - Location information
4. fact_table - Trip facts
"""

import pandas as pd

def transform_data(**context):
    """
    Transform raw data into Star Schema
    
    Args:
        context: Airflow context dictionary
        
    Returns:
        dict: Dictionary with row counts for each table
    """
    # Read data from temp
    df = pd.read_csv('/tmp/uber_data.csv')
    
    print(f"🔄 Transforming {len(df):,} rows...")
    
    # ============================================
    # DATA CLEANING
    # ============================================
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    print(f"   ✅ {len(df):,} rows after cleaning")
    
    # ============================================
    # 1. datetime_dim (Dimension Table)
    # ============================================
    datetime_dim = df[['tpep_pickup_datetime']].copy()
    datetime_dim['datetime_id'] = datetime_dim.index + 1
    datetime_dim['pickup_datetime'] = pd.to_datetime(datetime_dim['tpep_pickup_datetime'])
    datetime_dim['pick_hour'] = datetime_dim['pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['pickup_datetime'].dt.day_name()
    datetime_dim = datetime_dim.drop('tpep_pickup_datetime', axis=1)
    
    # ============================================
    # 2. rate_code_dim (Dimension Table)
    # ============================================
    rate_code_dim = df[['RatecodeID']].copy().drop_duplicates().reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index + 1
    
    rate_map = {
        1: 'Standard',
        2: 'JFK',
        3: 'Newark',
        4: 'Nassau/Westchester',
        5: 'Negotiated',
        6: 'Group Ride'
    }
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_map)
    
    # ============================================
    # 3. location_dim (Dimension Table)
    # ============================================
    location_df = pd.concat([
        df[['pickup_longitude', 'pickup_latitude']].rename(
            columns={'pickup_longitude': 'longitude', 'pickup_latitude': 'latitude'}
        ),
        df[['dropoff_longitude', 'dropoff_latitude']].rename(
            columns={'dropoff_longitude': 'longitude', 'dropoff_latitude': 'latitude'}
        )
    ]).drop_duplicates().reset_index(drop=True)
    
    location_df['location_id'] = location_df.index + 1
    location_df['location_name'] = 'Zone ' + location_df['location_id'].astype(str)
    location_df['borough'] = 'NYC'
    location_dim = location_df[['location_id', 'location_name', 'borough']]
    
    # ============================================
    # 4. fact_table (Fact Table)
    # ============================================
    fact_table = df[['trip_distance', 'fare_amount', 'total_amount', 
                     'passenger_count', 'payment_type']].copy()
    fact_table['trip_id'] = fact_table.index + 1
    fact_table['datetime_id'] = datetime_dim['datetime_id'].values
    fact_table['rate_code_id'] = fact_table.index % len(rate_code_dim) + 1
    fact_table['pickup_location_id'] = fact_table.index % len(location_dim) + 1
    fact_table['dropoff_location_id'] = (fact_table.index + 1) % len(location_dim) + 1
    
    fact_table = fact_table[[
        'trip_id', 'datetime_id', 'rate_code_id',
        'pickup_location_id', 'dropoff_location_id',
        'trip_distance', 'fare_amount', 'total_amount',
        'passenger_count', 'payment_type'
    ]]
    
    # ============================================
    # SAVE TRANSFORMED DATA
    # ============================================
    datetime_dim.to_csv('/tmp/datetime_dim.csv', index=False)
    rate_code_dim.to_csv('/tmp/rate_code_dim.csv', index=False)
    location_dim.to_csv('/tmp/location_dim.csv', index=False)
    fact_table.to_csv('/tmp/fact_table.csv', index=False)
    
    # ============================================
    # SUMMARY
    # ============================================
    print(f"✅ datetime_dim: {len(datetime_dim):,} rows")
    print(f"✅ rate_code_dim: {len(rate_code_dim):,} rows")
    print(f"✅ location_dim: {len(location_dim):,} rows")
    print(f"✅ fact_table: {len(fact_table):,} rows")
    print("✅ Star Schema created successfully!")
    
    return {
        'datetime_rows': len(datetime_dim),
        'rate_rows': len(rate_code_dim),
        'location_rows': len(location_dim),
        'fact_rows': len(fact_table)
    }