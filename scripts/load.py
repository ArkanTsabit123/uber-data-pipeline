# scripts/load.py
# Load transformed data to DuckDB

"""
Load transformed Star Schema data into DuckDB database.
Creates 4 tables and 1 analytics view.
"""

import duckdb
import pandas as pd
import os

def load_data(**context):
    """
    Load transformed data to DuckDB
    
    Args:
        context: Airflow context dictionary
        
    Returns:
        dict: Dictionary with load status
    """
    # ============================================
    # READ TRANSFORMED DATA
    # ============================================
    datetime_dim = pd.read_csv('/tmp/datetime_dim.csv')
    rate_code_dim = pd.read_csv('/tmp/rate_code_dim.csv')
    location_dim = pd.read_csv('/tmp/location_dim.csv')
    fact_table = pd.read_csv('/tmp/fact_table.csv')
    
    # ============================================
    # CONNECT TO DUCKDB
    # ============================================
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'warehouse',
        'uber.duckdb'
    )
    
    conn = duckdb.connect(db_path)
    print("✅ Connected to DuckDB")
    
    # ============================================
    # CREATE TABLES
    # ============================================
    # datetime_dim
    conn.execute("DROP TABLE IF EXISTS datetime_dim")
    conn.execute("CREATE TABLE datetime_dim AS SELECT * FROM datetime_dim")
    print(f"✅ Loaded datetime_dim: {len(datetime_dim):,} rows")
    
    # rate_code_dim
    conn.execute("DROP TABLE IF EXISTS rate_code_dim")
    conn.execute("CREATE TABLE rate_code_dim AS SELECT * FROM rate_code_dim")
    print(f"✅ Loaded rate_code_dim: {len(rate_code_dim):,} rows")
    
    # location_dim
    conn.execute("DROP TABLE IF EXISTS location_dim")
    conn.execute("CREATE TABLE location_dim AS SELECT * FROM location_dim")
    print(f"✅ Loaded location_dim: {len(location_dim):,} rows")
    
    # fact_table
    conn.execute("DROP TABLE IF EXISTS fact_table")
    conn.execute("CREATE TABLE fact_table AS SELECT * FROM fact_table")
    print(f"✅ Loaded fact_table: {len(fact_table):,} rows")
    
    # ============================================
    # CREATE ANALYTICS VIEW
    # ============================================
    conn.execute("""
    CREATE OR REPLACE VIEW trip_analytics AS
    SELECT 
        f.trip_id,
        f.trip_distance,
        f.fare_amount,
        f.total_amount,
        f.passenger_count,
        d.pickup_datetime,
        d.pick_hour,
        d.pick_weekday,
        d.pick_month,
        d.pick_year,
        r.rate_code_name,
        pl.location_name AS pickup_location,
        dl.location_name AS dropoff_location
    FROM fact_table f
    LEFT JOIN datetime_dim d ON f.datetime_id = d.datetime_id
    LEFT JOIN rate_code_dim r ON f.rate_code_id = r.rate_code_id
    LEFT JOIN location_dim pl ON f.pickup_location_id = pl.location_id
    LEFT JOIN location_dim dl ON f.dropoff_location_id = dl.location_id
    """)
    print("✅ Created trip_analytics view")
    
    # ============================================
    # SHOW TABLES
    # ============================================
    tables = conn.execute("SHOW TABLES").fetchall()
    print("\n📋 Tables in DuckDB:")
    for table in tables:
        print(f"   • {table[0]}")
    
    # ============================================
    # CLOSE CONNECTION
    # ============================================
    conn.close()
    print("✅ Data loaded successfully!")
    
    return {'status': 'success'}