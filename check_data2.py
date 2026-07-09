# check_data2.py
# Detailed data inspection

"""
Detailed data inspection script for Uber ETL Pipeline.
Shows comprehensive analysis of the dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def main():
    print("=" * 60)
    print("🔍 DETAILED DATA INSPECTION")
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
    
    # ============================================
    # 1. BASIC INFORMATION
    # ============================================
    print("\n" + "=" * 60)
    print("📊 1. BASIC INFORMATION")
    print("=" * 60)
    
    print(f"\nDataset: {data_path.name}")
    print(f"   • Rows: {len(df):,}")
    print(f"   • Columns: {len(df.columns)}")
    print(f"   • Size: {data_path.stat().st_size / (1024*1024):.2f} MB")
    print(f"   • Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    # ============================================
    # 2. COLUMN ANALYSIS
    # ============================================
    print("\n" + "=" * 60)
    print("📋 2. COLUMN ANALYSIS")
    print("=" * 60)
    
    print("\nColumn Details:")
    print("-" * 60)
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        null_pct = (nulls / len(df)) * 100
        unique = df[col].nunique()
        
        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            min_val = df[col].min()
            max_val = df[col].max()
            mean_val = df[col].mean()
            print(f"\n   📌 {col}:")
            print(f"      • Type: {dtype}")
            print(f"      • Nulls: {nulls:,} ({null_pct:.1f}%)")
            print(f"      • Unique: {unique:,}")
            print(f"      • Range: {min_val:.2f} - {max_val:.2f}")
            print(f"      • Mean: {mean_val:.2f}")
        else:
            print(f"\n   📌 {col}:")
            print(f"      • Type: {dtype}")
            print(f"      • Nulls: {nulls:,} ({null_pct:.1f}%)")
            print(f"      • Unique: {unique:,}")
            if unique <= 10:
                print(f"      • Values: {df[col].value_counts().to_dict()}")
    
    # ============================================
    # 3. STATISTICAL SUMMARY
    # ============================================
    print("\n" + "=" * 60)
    print("📊 3. STATISTICAL SUMMARY")
    print("=" * 60)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print("\nNumeric Columns Statistics:")
    print("-" * 60)
    print(df[numeric_cols].describe())
    
    # ============================================
    # 4. DATE/TIME ANALYSIS
    # ============================================
    print("\n" + "=" * 60)
    print("⏰ 4. DATE/TIME ANALYSIS")
    print("=" * 60)
    
    if 'tpep_pickup_datetime' in df.columns:
        df['pickup_dt'] = pd.to_datetime(df['tpep_pickup_datetime'])
        print("\nPickup Date Range:")
        print(f"   • Earliest: {df['pickup_dt'].min()}")
        print(f"   • Latest: {df['pickup_dt'].max()}")
        print(f"   • Duration: {(df['pickup_dt'].max() - df['pickup_dt'].min()).days} days")
        
        print("\nTrips by Hour:")
        hour_counts = df['pickup_dt'].dt.hour.value_counts().sort_index()
        for hour, count in hour_counts.items():
            bar = "█" * int(count / max(hour_counts) * 30)
            print(f"   {hour:02d}:00  {bar} ({count:,})")
    
    # ============================================
    # 5. PAYMENT TYPE ANALYSIS
    # ============================================
    print("\n" + "=" * 60)
    print("💳 5. PAYMENT TYPE DISTRIBUTION")
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
            print(f"   • {pname}: {bar} {count:,} ({pct:.1f}%)")
    
    # ============================================
    # 6. RATE CODE ANALYSIS
    # ============================================
    print("\n" + "=" * 60)
    print("🏷️ 6. RATE CODE DISTRIBUTION")
    print("=" * 60)
    
    if 'RatecodeID' in df.columns:
        rate_counts = df['RatecodeID'].value_counts()
        rate_pct = df['RatecodeID'].value_counts(normalize=True) * 100
        rate_map = {1: 'Standard', 2: 'JFK', 3: 'Newark', 4: 'Nassau/Westchester', 5: 'Negotiated', 6: 'Group Ride'}
        
        print("\nRate Codes:")
        for rate, count in rate_counts.items():
            pct = rate_pct[rate]
            rname = rate_map.get(rate, f'Code {rate}')
            bar = "█" * int(pct / 2)
            print(f"   • {rname}: {bar} {count:,} ({pct:.1f}%)")
    
    # ============================================
    # 7. DATA QUALITY REPORT
    # ============================================
    print("\n" + "=" * 60)
    print("✅ 7. DATA QUALITY REPORT")
    print("=" * 60)
    
    duplicate_rows = df.duplicated().sum()
    null_cells = df.isnull().sum().sum()
    total_cells = len(df) * len(df.columns)
    completeness = (1 - null_cells / total_cells) * 100
    
    print(f"\n   • Duplicate rows: {duplicate_rows:,}")
    print(f"   • Null cells: {null_cells:,}")
    print(f"   • Completeness: {completeness:.2f}%")
    
    # Check for outliers
    print("\nOutlier Detection (Z-Score > 3):")
    print("-" * 40)
    for col in numeric_cols:
        z_score = (df[col] - df[col].mean()) / df[col].std()
        outliers = len(z_score[abs(z_score) > 3])
        if outliers > 0:
            print(f"   • {col}: {outliers:,} outliers ({outliers/len(df)*100:.2f}%)")
    
    # ============================================
    # 8. RECOMMENDATIONS
    # ============================================
    print("\n" + "=" * 60)
    print("💡 8. RECOMMENDATIONS")
    print("=" * 60)
    
    print("\nData Cleaning Suggestions:")
    if duplicate_rows > 0:
        print(f"   • Remove {duplicate_rows:,} duplicate rows")
    if null_cells > 0:
        print(f"   • Handle {null_cells:,} null values")
    
    print("\nNext Steps:")
    print("   1. Run: python run.py verify")
    print("   2. Trigger DAG in Airflow UI")
    print("   3. Run: streamlit run dashboard/app.py")
    
    print("\n" + "=" * 60)
    print("✅ Detailed inspection complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()