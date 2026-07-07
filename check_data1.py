#check_data1.py
# Load dataset for shorted output check

import pandas as pd

# Load dataset
df = pd.read_csv('data/uber_data.csv')

print("=" * 50)
print("📊 DATASET INFORMATION")
print("=" * 50)
print(f"📁 File location: data/uber_data.csv")
print(f"📊 Total rows: {len(df):,}")
print(f"📋 Total columns: {len(df.columns)}")
print(f"📋 Columns: {', '.join(df.columns.tolist())}")
print(f"💾 Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
print("\n📄 Preview (first 5 rows):")
print(df.head())
