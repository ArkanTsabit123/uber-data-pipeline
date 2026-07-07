#check_data2.py
# Load dataset for detailed output check

import pandas as pd
import numpy as np
from datetime import datetime

# ============================================
# LOAD DATASET 
# ============================================
print("=" * 75)
print("📊 DATASET INFORMATION - NYC UBER TRIP DATA")
print("=" * 75)

# Load dataset
df = pd.read_csv('data/uber_data.csv')

# ============================================
# BASIC INFORMATION
# ============================================
print("\n📁 BASIC INFORMATION")
print("-" * 75)
print(f"📁 File location: data/uber_data.csv")
print(f"📊 Total rows: {len(df):,}")
print(f"📋 Total columns: {len(df.columns)}")
print(f"💾 Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")

# Date range (if datetime column exists)
if 'tpep_pickup_datetime' in df.columns:
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    print(f"📅 Date range: {df['tpep_pickup_datetime'].min()} to {df['tpep_pickup_datetime'].max()}")

# ============================================
# COLUMN LIST WITH DETAILS
# ============================================
print("\n" + "=" * 75)
print("📋 COLUMN LIST WITH DETAILS")
print("=" * 75)

for i, col in enumerate(df.columns, 1):
    dtype = df[col].dtype
    missing = df[col].isnull().sum()
    missing_pct = (missing / len(df)) * 100
    unique = df[col].nunique()
    
    # Count empty strings for object columns
    if dtype == 'object':
        empty = (df[col] == '').sum()
    else:
        empty = 0
    
    print(f"   {i:2}. {col:30} → {str(dtype):15} "
          f"| Missing: {missing:>6} ({missing_pct:>5.1f}%) "
          f"| Unique: {unique:>6} "
          f"| Empty: {empty:>6}")

# ============================================
# DATA TYPES SUMMARY
# ============================================
print("\n" + "=" * 75)
print("📋 DATA TYPES SUMMARY")
print("=" * 75)

dtype_counts = df.dtypes.value_counts()
for dtype, count in dtype_counts.items():
    print(f"   {str(dtype):15} → {count:>3} column(s)")

# ============================================
# DATA PREVIEW
# ============================================
print("\n" + "=" * 75)
print("📄 DATA PREVIEW (First 10 rows)")
print("=" * 75)
print(df.head(10))

# ============================================
# SAMPLE DATA (Last 5 rows)
# ============================================
print("\n" + "=" * 75)
print("📄 DATA PREVIEW (Last 5 rows)")
print("=" * 75)
print(df.tail(5))

# ============================================
# STATISTICAL SUMMARY (Numerical Columns)
# ============================================
print("\n" + "=" * 75)
print("📊 STATISTICAL SUMMARY (Numerical Columns)")
print("=" * 75)

numeric_cols = df.select_dtypes(include=[np.number]).columns
if len(numeric_cols) > 0:
    print(df[numeric_cols].describe())
else:
    print("   No numerical columns found.")

# ============================================
# MISSING VALUES SUMMARY
# ============================================
print("\n" + "=" * 75)
print("🔍 MISSING VALUES SUMMARY")
print("=" * 75)

missing_df = df.isnull().sum()
missing_df = missing_df[missing_df > 0]

if len(missing_df) > 0:
    print("   Columns with missing values:")
    for col, count in missing_df.items():
        pct = (count / len(df)) * 100
        print(f"   • {col:30} → {count:>6} rows ({pct:>5.1f}%)")
else:
    print("   ✅ No missing values found!")

# ============================================
# DUPLICATE ROWS
# ============================================
print("\n" + "=" * 75)
print("🔍 DUPLICATE ROWS CHECK")
print("=" * 75)

duplicates = df.duplicated().sum()
if duplicates > 0:
    print(f"   ⚠️  Found {duplicates:,} duplicate rows")
else:
    print("   ✅ No duplicate rows found!")

# ============================================
# UNIQUE VALUES ANALYSIS (Categorical Columns)
# ============================================
print("\n" + "=" * 75)
print("📋 UNIQUE VALUES ANALYSIS (Categorical Columns)")
print("=" * 75)

cat_cols = df.select_dtypes(include=['object', 'category']).columns
if len(cat_cols) > 0:
    for col in cat_cols[:5]:  # Show first 5 categorical columns
        unique_vals = df[col].nunique()
        if unique_vals <= 20:  # Only show if reasonable number of unique values
            print(f"\n   {col} (Unique values: {unique_vals}):")
            value_counts = df[col].value_counts().head(10)
            for val, count in value_counts.items():
                pct = (count / len(df)) * 100
                print(f"      • {str(val)[:30]:30} → {count:>6} ({pct:>5.1f}%)")
        else:
            print(f"\n   {col}: {unique_vals:,} unique values (showing first 10)")
            for val in df[col].dropna().unique()[:10]:
                print(f"      • {str(val)[:50]}")
else:
    print("   No categorical columns found.")

# ============================================
# CORRELATION MATRIX (Top correlations)
# ============================================
print("\n" + "=" * 75)
print("📊 TOP CORRELATIONS")
print("=" * 75)

if len(numeric_cols) > 1:
    try:
        corr_matrix = df[numeric_cols].corr()
        # Get top correlations (excluding diagonal)
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((
                    corr_matrix.columns[i],
                    corr_matrix.columns[j],
                    corr_matrix.iloc[i, j]
                ))
        
        # Sort by absolute correlation
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        print("   Top 5 highest correlations:")
        for i, (col1, col2, corr) in enumerate(corr_pairs[:5]):
            print(f"      {i+1}. {col1} ↔ {col2}: {corr:.3f}")
    except:
        print("   Unable to calculate correlations.")
else:
    print("   Not enough numerical columns for correlation.")

# ============================================
# SKEWNESS (Data distribution)
# ============================================
print("\n" + "=" * 75)
print("📊 SKEWNESS (Data Distribution)")
print("=" * 75)

if len(numeric_cols) > 0:
    skewed_cols = []
    for col in numeric_cols:
        skew = df[col].skew()
        if abs(skew) > 0.5:
            skewed_cols.append((col, skew))
    
    if skewed_cols:
        print("   Columns with high skewness:")
        for col, skew in sorted(skewed_cols, key=lambda x: abs(x[1]), reverse=True)[:5]:
            direction = "right" if skew > 0 else "left"
            print(f"      • {col:30} → {skew:>8.3f} ({direction} skewed)")
    else:
        print("   No highly skewed columns found.")
else:
    print("   No numerical columns found.")

# ============================================
# OUTLIER DETECTION (IQR Method)
# ============================================
print("\n" + "=" * 75)
print("📊 OUTLIER DETECTION (IQR Method)")
print("=" * 75)

if len(numeric_cols) > 0:
    outliers_found = False
    for col in numeric_cols[:5]:  # Check first 5 numerical columns
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].shape[0]
        if outliers > 0:
            pct = (outliers / len(df)) * 100
            print(f"      • {col:30} → {outliers:>6} outliers ({pct:>5.1f}%)")
            outliers_found = True
    if not outliers_found:
        print("   No significant outliers found.")
else:
    print("   No numerical columns found.")

# ============================================
# SUMMARY STATISTICS
# ============================================
print("\n" + "=" * 75)
print("📊 FINAL SUMMARY")
print("=" * 75)

print(f"""
   📁 Dataset:      uber_data.csv
   📊 Total Rows:   {len(df):,}
   📋 Total Cols:   {len(df.columns)}
   💾 Memory:       {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
   🔍 Missing:      {df.isnull().sum().sum():,} cells
   🔄 Duplicates:   {duplicates:,} rows
   📅 Date Range:   {df['tpep_pickup_datetime'].min()} to {df['tpep_pickup_datetime'].max()}
   📈 Numerical:    {len(numeric_cols)} columns
   📉 Categorical:  {len(cat_cols)} columns
""")

print("=" * 75)
print("✅ DATASET ANALYSIS COMPLETE!")
print("=" * 75)