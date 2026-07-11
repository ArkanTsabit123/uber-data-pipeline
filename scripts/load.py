# scripts/load.py
"""
Load transformed Star Schema data into DuckDB database.

Creates four dimension tables and one analytics view:
1. datetime_dim - Temporal dimension
2. rate_code_dim - Rate code dimension
3. location_dim - Location dimension
4. fact_table - Fact table with foreign keys
5. trip_analytics - Analytics view for dashboard
"""

import duckdb
import pandas as pd
import os


def load_data(**context) -> dict:
    """
    Load transformed data to DuckDB.

    Args:
        context: Airflow context dictionary

    Returns:
        dict: Dictionary with load status
    """
    # Read transformed data from temporary files
    datetime_dim = pd.read_csv('/tmp/datetime_dim.csv')
    rate_code_dim = pd.read_csv('/tmp/rate_code_dim.csv')
    location_dim = pd.read_csv('/tmp/location_dim.csv')
    fact_table = pd.read_csv('/tmp/fact_table.csv')

    # Define database path
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'warehouse',
        'uber.duckdb'
    )

    # Connect to DuckDB
    conn = duckdb.connect(db_path)
    print("Connected to DuckDB")

    # 1. datetime_dim - Temporal dimension table
    conn.execute("DROP TABLE IF EXISTS datetime_dim")
    conn.execute("CREATE TABLE datetime_dim AS SELECT * FROM datetime_dim")
    print(f"Loaded datetime_dim: {len(datetime_dim):,} rows")

    # 2. rate_code_dim - Rate code dimension table
    conn.execute("DROP TABLE IF EXISTS rate_code_dim")
    conn.execute("CREATE TABLE rate_code_dim AS SELECT * FROM rate_code_dim")
    print(f"Loaded rate_code_dim: {len(rate_code_dim):,} rows")

    # 3. location_dim - Location dimension table
    conn.execute("DROP TABLE IF EXISTS location_dim")
    conn.execute("CREATE TABLE location_dim AS SELECT * FROM location_dim")
    print(f"Loaded location_dim: {len(location_dim):,} rows")

    # 4. fact_table - Fact table with foreign keys
    conn.execute("DROP TABLE IF EXISTS fact_table")
    conn.execute("CREATE TABLE fact_table AS SELECT * FROM fact_table")
    print(f"Loaded fact_table: {len(fact_table):,} rows")

    # Create analytics view for dashboard
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
    print("Created trip_analytics view")

    # Show created tables
    tables = conn.execute("SHOW TABLES").fetchall()
    print("\nTables in DuckDB:")
    for table in tables:
        print(f"   {table[0]}")

    conn.close()
    print("Data loaded successfully!")

    return {'status': 'success'}