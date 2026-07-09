# check_data1.py
# Quick data overview

"""
Quick data overview script for Uber ETL Pipeline.
Shows basic information about the dataset.
"""

import pandas as pd
from pathlib import Path

def main():
    print("=" * 60)
    print("📊 QUICK DATA OVERVIEW")
    print("=" * 60)
    
    # Check if data file exists
    data_path = Path('data/uber_data.csv')
    if not data_path.exists():
        print("❌ Dataset not found: data/uber_data.csv")
        print("   💡 Download dataset first")
        return
    
    # Load data
    print("\n📂 Loading dataset...")
    df = pd.read_csv(data_path)
    
    # Basic info
    print(f"\n📊 Dataset: {data_path.name}")
    print("-" * 40)
    print(f"   • Rows: {len(df):,}")
    print(f"   • Columns: {len(df.columns)}")
    print(f"   • Size: {data_path.stat().st_size / (1024*1024):.2f} MB")
    
    # Column info
    print("\n📋 Columns:")
    print("-" * 40)
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"   • {col}: {dtype}, nulls={nulls}, unique={unique}")
    
    # Sample data
    print("\n🔍 First 5 rows:")
    print("-" * 40)
    print(df.head())
    
    # Data quality
    print("\n✅ Data Quality:")
    print("-" * 40)
    duplicate_rows = df.duplicated().sum()
    null_cells = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = (1 - null_cells / total_cells) * 100
    
    print(f"   • Duplicate rows: {duplicate_rows:,}")
    print(f"   • Null cells: {null_cells:,}")
    print(f"   • Completeness: {completeness:.2f}%")
    
    print("\n" + "=" * 60)
    print("✅ Quick overview complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()