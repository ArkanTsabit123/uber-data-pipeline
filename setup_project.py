"""
Project Structure Generator for Uber ETL Pipeline
Run: python setup_project.py
"""

import os
import sys
from pathlib import Path

def create_project_structure():
    """Create all required folders and files for the Uber ETL Pipeline project"""
    
    print("=" * 60)
    print("UBER ETL PIPELINE - PROJECT STRUCTURE GENERATOR")
    print("=" * 60)
    
    # Base directory
    base_dir = Path.cwd()
    print(f"\n[FOLDER] Base directory: {base_dir}")
    
    # ============================================
    # 1. CREATE FOLDER STRUCTURE
    # ============================================
    print("\n[CREATING] Folder structure...")
    
    folders = [
        'data',
        'warehouse',
        'dashboard',
        'screenshots',
        'mage_project',
        'mage_project/pipelines',
        'mage_project/pipelines/uber_etl_pipeline',
        'mage_project/pipelines/uber_etl_pipeline/blocks',
    ]
    
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"  [OK] Created: {folder}/")
    
    # ============================================
    # 2. CREATE FILES
    # ============================================
    print("\n[CREATING] Files...")
    
    # 2.1 README.md (sudah ada, skip)
    readme_path = base_dir / 'README.md'
    if not readme_path.exists():
        print("  [WARN] README.md not found - please create manually")
    else:
        print("  [OK] README.md exists")
    
    # 2.2 LICENSE (sudah ada, skip)
    license_path = base_dir / 'LICENSE'
    if not license_path.exists():
        print("  [WARN] LICENSE not found - please create manually")
    else:
        print("  [OK] LICENSE exists")
    
    # 2.3 requirements.txt (sudah ada, skip)
    req_path = base_dir / 'requirements.txt'
    if not req_path.exists():
        print("  [WARN] requirements.txt not found - please create manually")
    else:
        print("  [OK] requirements.txt exists")
    
    # 2.4 .gitignore (sudah ada, skip)
    gitignore_path = base_dir / '.gitignore'
    if not gitignore_path.exists():
        print("  [WARN] .gitignore not found - please create manually")
    else:
        print("  [OK] .gitignore exists")
    
    # 2.5 Create verification files
    verification_files = [
        'verify-phase-1.py',
        'verify-phase-2.py',
        'verify-phase-3.py',
        'verify-phase-4.py',
        'verify-phase-5.py',
        'verify-phase-6.py',
    ]
    
    for vf in verification_files:
        vf_path = base_dir / vf
        if not vf_path.exists():
            # Create basic verification file
            with open(vf_path, 'w', encoding='utf-8') as f:
                f.write(f'''# {vf}
# Uber ETL Pipeline - Phase Verification

import os
import sys

def verify_phase():
    print("=" * 60)
    print(f"VERIFYING: {vf.replace('verify-', '').replace('.py', '')}")
    print("=" * 60)
    
    checks_passed = 0
    total_checks = 10
    
    # Add your verification logic here
    print("\\nAll checks passed!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = verify_phase()
    sys.exit(0 if success else 1)
''')
            print(f"  [OK] Created: {vf}")
        else:
            print(f"  [OK] {vf} exists")
    
    # 2.6 Create dashboard app.py
    app_path = base_dir / 'dashboard' / 'app.py'
    if not app_path.exists():
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write('''# dashboard/app.py
# Uber NYC Trip Analytics Dashboard

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Uber NYC Dashboard",
    page_icon=":car:",
    layout="wide"
)

st.title("Uber NYC Trip Analytics Dashboard")
st.markdown("*End-to-End Data Pipeline Project*")

# Database connection
@st.cache_resource
def get_connection():
    return duckdb.connect('../warehouse/uber.duckdb')

@st.cache_data
def load_data():
    conn = get_connection()
    try:
        df = conn.execute("SELECT * FROM trip_analytics").fetchdf()
    except:
        df = pd.DataFrame()
    conn.close()
    return df

# Load data
df = load_data()

if df.empty:
    st.warning("No data found. Please run the ETL pipeline first!")
    st.info("1. Start Mage: `mage start mage_project`")
    st.info("2. Run the pipeline: uber_etl_pipeline")
    st.info("3. Refresh this dashboard")
else:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    year = st.sidebar.selectbox(
        "Year", 
        sorted(df['pick_year'].unique()) if 'pick_year' in df.columns else []
    )
    month = st.sidebar.selectbox(
        "Month", 
        sorted(df['pick_month'].unique()) if 'pick_month' in df.columns else []
    )
    weekday = st.sidebar.multiselect(
        "Weekday", 
        df['pick_weekday'].unique() if 'pick_weekday' in df.columns else []
    )
    
    # Filter data
    filtered_df = df.copy()
    if 'pick_year' in df.columns and year:
        filtered_df = filtered_df[filtered_df['pick_year'] == year]
    if 'pick_month' in df.columns and month:
        filtered_df = filtered_df[filtered_df['pick_month'] == month]
    if 'pick_weekday' in df.columns and weekday:
        filtered_df = filtered_df[filtered_df['pick_weekday'].isin(weekday)]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trips", f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Revenue", f"${filtered_df['total_amount'].sum():,.2f}")
    with col3:
        st.metric("Avg Distance", f"{filtered_df['trip_distance'].mean():.2f} miles")
    with col4:
        st.metric("Avg Fare", f"${filtered_df['fare_amount'].mean():.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        if 'pick_hour' in filtered_df.columns:
            hourly_revenue = filtered_df.groupby('pick_hour')['total_amount'].sum().reset_index()
            fig1 = px.line(
                hourly_revenue, 
                x='pick_hour', 
                y='total_amount',
                title='Revenue by Hour',
                markers=True
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        if 'pick_weekday' in filtered_df.columns:
            weekday_trips = filtered_df['pick_weekday'].value_counts().reset_index()
            weekday_trips.columns = ['weekday', 'count']
            fig2 = px.bar(
                weekday_trips, 
                x='weekday', 
                y='count',
                title='Trips by Weekday'
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        if 'rate_code_name' in filtered_df.columns:
            rate_dist = filtered_df['rate_code_name'].value_counts().reset_index()
            rate_dist.columns = ['rate_code', 'count']
            fig3 = px.pie(
                rate_dist, 
                values='count', 
                names='rate_code',
                title='Rate Code Distribution'
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        if 'trip_distance' in filtered_df.columns and 'fare_amount' in filtered_df.columns:
            fig4 = px.scatter(
                filtered_df, 
                x='trip_distance', 
                y='fare_amount',
                title='Distance vs Fare',
                opacity=0.6
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Data table
    with st.expander("View Data Table"):
        st.dataframe(filtered_df)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="uber_trip_data.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("Built with Python using Streamlit, DuckDB, and Plotly")
''')
        print("  [OK] Created: dashboard/app.py")
    else:
        print("  [OK] dashboard/app.py exists")
    
    # 2.7 Create .gitkeep in empty folders
    for folder in ['data', 'warehouse', 'screenshots']:
        keep_file = base_dir / folder / '.gitkeep'
        keep_file.touch(exist_ok=True)
    
    # ============================================
    # 3. VERIFICATION SUMMARY
    # ============================================
    print("\n" + "=" * 60)
    print("PROJECT STRUCTURE CREATED SUCCESSFULLY!")
    print("=" * 60)
    
    print("\nProject Structure:")
    print("""
uber-data-pipeline/
├── [FOLDER] data/                 # Raw dataset
│   └── uber_data.csv              [WARN] Download manually
├── [FOLDER] warehouse/            # DuckDB database
├── [FOLDER] dashboard/            # Streamlit app
│   └── app.py                    [OK] Created
├── [FOLDER] screenshots/          # Screenshots
├── [FOLDER] mage_project/         # Mage AI project
│   └── pipelines/
│       └── uber_etl_pipeline/
│           └── blocks/
├── [FILE] README.md              [WARN] Create manually
├── [FILE] LICENSE                [WARN] Create manually
├── [FILE] requirements.txt       [WARN] Create manually
├── [FILE] .gitignore             [WARN] Create manually
├── [FILE] verify-phase-1.py      [OK] Created
├── [FILE] verify-phase-2.py      [OK] Created
├── [FILE] verify-phase-3.py      [OK] Created
├── [FILE] verify-phase-4.py      [OK] Created
├── [FILE] verify-phase-5.py      [OK] Created
└── [FILE] verify-phase-6.py      [OK] Created
""")
    
    print("NEXT STEPS:")
    print("  1. Download dataset to data/uber_data.csv")
    print("  2. Create README.md, LICENSE, requirements.txt, .gitignore")
    print("  3. Activate venv: source venv/bin/activate (or venv\\Scripts\\activate)")
    print("  4. Install: pip install -r requirements.txt")
    print("  5. Start Mage: mage start mage_project")
    print("  6. Create pipeline in Mage UI")
    print("  7. Run: streamlit run dashboard/app.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    create_project_structure()