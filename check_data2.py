# check_data2.py
"""
Detailed data inspection script for Uber ETL Pipeline.

Provides comprehensive analysis including:
- Column statistics and distributions
- Date/time patterns
- Payment type and rate code distributions
- Outlier detection
- Summary report
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


def main() -> None:
    """Run detailed data inspection."""
    print("=" * 60)
    print("DETAILED DATA INSPECTION")
    print("=" * 60)

    data_path = Path('data/uber_data.csv')

    if not data_path.exists():
        print("Dataset not found: data/uber_data.csv")
        print("Hint: Download dataset first")
        return

    print("\nLoading dataset...")
    df = pd.read_csv(data_path)

    # 1. Basic Information
    print("\n" + "=" * 60)
    print("1. BASIC INFORMATION")
    print("=" * 60)

    print(f"\nDataset: {data_path.name}")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Size: {data_path.stat().st_size / (1024 * 1024):.2f} MB")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # 2. Column Analysis
    print("\n" + "=" * 60)
    print("2. COLUMN ANALYSIS")
    print("=" * 60)

    print("\nColumn Details:")
    print("-" * 60)
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        null_pct = (nulls / len(df)) * 100
        unique = df[col].nunique()

        if pd.api.types.is_numeric_dtype(df[col]):
            min_val = df[col].min()
            max_val = df[col].max()
            mean_val = df[col].mean()
            print(f"\n   {col}:")
            print(f"      Type: {dtype}")
            print(f"      Nulls: {nulls:,} ({null_pct:.1f}%)")
            print(f"      Unique: {unique:,}")
            print(f"      Range: {min_val:.2f} - {max_val:.2f}")
            print(f"      Mean: {mean_val:.2f}")
        else:
            print(f"\n   {col}:")
            print(f"      Type: {dtype}")
            print(f"      Nulls: {nulls:,} ({null_pct:.1f}%)")
            print(f"      Unique: {unique:,}")
            if unique <= 10:
                print(f"      Values: {df[col].value_counts().to_dict()}")

    # 3. Statistical Summary
    print("\n" + "=" * 60)
    print("3. STATISTICAL SUMMARY")
    print("=" * 60)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print("\nNumeric Columns Statistics:")
    print("-" * 60)
    print(df[numeric_cols].describe())

    # 4. Date/Time Analysis
    print("\n" + "=" * 60)
    print("4. DATE/TIME ANALYSIS")
    print("=" * 60)

    if 'tpep_pickup_datetime' in df.columns:
        df['pickup_dt'] = pd.to_datetime(df['tpep_pickup_datetime'])
        print("\nPickup Date Range:")
        print(f"   Earliest: {df['pickup_dt'].min()}")
        print(f"   Latest: {df['pickup_dt'].max()}")
        print(f"   Duration: {(df['pickup_dt'].max() - df['pickup_dt'].min()).days} days")

        print("\nTrips by Hour:")
        hour_counts = df['pickup_dt'].dt.hour.value_counts().sort_index()
        max_count = max(hour_counts)
        for hour, count in hour_counts.items():
            bar = "█" * int(count / max_count * 30)
            print(f"   {hour:02d}:00  {bar} ({count:,})")

    # 5. Payment Type Analysis
    print("\n" + "=" * 60)
    print("5. PAYMENT TYPE DISTRIBUTION")
    print("=" * 60)

    if 'payment_type' in df.columns:
        payment_counts = df['payment_type'].value_counts()
        payment_pct = df['payment_type'].value_counts(normalize=True) * 100
        payment_map = {1: 'Credit Card', 2: 'Cash', 3: 'No Charge', 4: 'Dispute', 5: 'Unknown'}

        print("\nPayment Types:")
        for ptype, count in payment_counts.items():
            pct = payment_pct[ptype]
            pname = payment_map.get(ptype, f'Type {ptype}')
            bar = "█" * int(pct / 2)
            print(f"   {pname}: {bar} {count:,} ({pct:.1f}%)")

    # 6. Rate Code Analysis
    print("\n" + "=" * 60)
    print("6. RATE CODE DISTRIBUTION")
    print("=" * 60)

    if 'RatecodeID' in df.columns:
        rate_counts = df['RatecodeID'].value_counts()
        rate_pct = df['RatecodeID'].value_counts(normalize=True) * 100
        rate_map = {1: 'Standard', 2: 'JFK', 3: 'Newark',
                    4: 'Nassau/Westchester', 5: 'Negotiated', 6: 'Group Ride'}

        print("\nRate Codes:")
        for rate, count in rate_counts.items():
            pct = rate_pct[rate]
            rname = rate_map.get(rate, f'Code {rate}')
            bar = "█" * int(pct / 2)
            print(f"   {rname}: {bar} {count:,} ({pct:.1f}%)")

    # 7. Data Quality Report
    print("\n" + "=" * 60)
    print("7. DATA QUALITY REPORT")
    print("=" * 60)

    duplicate_rows = df.duplicated().sum()
    null_cells = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = (1 - null_cells / total_cells) * 100

    print(f"\n   Duplicate rows: {duplicate_rows:,}")
    print(f"   Null cells: {null_cells:,}")
    print(f"   Completeness: {completeness:.2f}%")

    print("\nOutlier Detection (Z-Score > 3):")
    print("-" * 40)
    for col in numeric_cols:
        if df[col].std() > 0:
            z_score = (df[col] - df[col].mean()) / df[col].std()
            outliers = len(z_score[abs(z_score) > 3])
            if outliers > 0:
                print(f"   {col}: {outliers:,} outliers ({outliers / len(df) * 100:.2f}%)")

    # 8. SUMMARY REPORT
    print("\n" + "=" * 60)
    print("8. SUMMARY REPORT")
    print("=" * 60)

    print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Dataset: {data_path.name}")
    print(f"Total Records: {len(df):,}")
    print(f"Total Columns: {len(df.columns)}")

    print("\nData Quality Summary:")
    print(f"   Completeness: {completeness:.2f}%")
    print(f"   Duplicate Rows: {duplicate_rows:,}")
    print(f"   Null Cells: {null_cells:,}")

    print("\nKey Metrics:")
    if 'trip_distance' in df.columns:
        print(f"   Average Trip Distance: {df['trip_distance'].mean():.2f} miles")
        print(f"   Max Trip Distance: {df['trip_distance'].max():.2f} miles")
    if 'fare_amount' in df.columns:
        print(f"   Average Fare: ${df['fare_amount'].mean():.2f}")
        print(f"   Max Fare: ${df['fare_amount'].max():.2f}")
    if 'total_amount' in df.columns:
        print(f"   Average Total Amount: ${df['total_amount'].mean():.2f}")
        print(f"   Total Revenue: ${df['total_amount'].sum():,.2f}")

    if 'passenger_count' in df.columns:
        print(f"   Average Passengers: {df['passenger_count'].mean():.2f}")

    print("\nTop Insights:")
    if 'pickup_dt' in df.columns:
        peak_hour = df['pickup_dt'].dt.hour.mode()[0]
        print(f"   Peak Hour: {peak_hour}:00")

    if 'payment_type' in df.columns:
        top_payment = df['payment_type'].mode()[0]
        payment_names = {1: 'Credit Card', 2: 'Cash', 3: 'No Charge', 4: 'Dispute', 5: 'Unknown'}
        print(f"   Most Common Payment: {payment_names.get(top_payment, 'Unknown')}")

    if 'RatecodeID' in df.columns:
        top_rate = df['RatecodeID'].mode()[0]
        rate_names = {1: 'Standard', 2: 'JFK', 3: 'Newark', 4: 'Nassau/Westchester', 5: 'Negotiated', 6: 'Group Ride'}
        print(f"   Most Common Rate Code: {rate_names.get(top_rate, 'Unknown')}")

    print("\nDataset Shape:")
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    print("\nColumns List:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col} ({df[col].dtype})")

    print("\n" + "=" * 60)
    print("Detailed inspection complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()