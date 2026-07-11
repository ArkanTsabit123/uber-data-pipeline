# check_data1.py
"""
Quick data overview script for Uber ETL Pipeline.

Shows basic information about the dataset including:
- Row and column counts
- Column data types and null values
- Data quality metrics
"""

import pandas as pd
from pathlib import Path


def main() -> None:
    """Display basic dataset overview."""
    print("=" * 60)
    print("DATA OVERVIEW")
    print("=" * 60)

    data_path = Path('data/uber_data.csv')

    if not data_path.exists():
        print("Dataset not found: data/uber_data.csv")
        print("Hint: Download dataset first")
        return

    print("\nLoading dataset...")
    df = pd.read_csv(data_path)

    print(f"\nDataset: {data_path.name}")
    print("-" * 40)
    print(f"   Rows: {len(df):,}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Size: {data_path.stat().st_size / (1024 * 1024):.2f} MB")

    print("\nColumns:")
    print("-" * 40)
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"   {col}: {dtype}, nulls={nulls}, unique={unique}")

    print("\nFirst 5 rows:")
    print("-" * 40)
    print(df.head())

    print("\nData Quality:")
    print("-" * 40)
    duplicate_rows = df.duplicated().sum()
    null_cells = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = (1 - null_cells / total_cells) * 100

    print(f"   Duplicate rows: {duplicate_rows:,}")
    print(f"   Null cells: {null_cells:,}")
    print(f"   Completeness: {completeness:.2f}%")

    print("\n" + "=" * 60)
    print("Overview complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()