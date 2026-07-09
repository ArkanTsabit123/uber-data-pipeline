# setup_pipeline.py
# Setup DAG and script files for Airflow pipeline

"""
Setup script for creating Airflow pipeline files
Run: python setup_pipeline.py
"""

import os
from pathlib import Path
from datetime import datetime


class PipelineSetup:
    """Setup class for creating pipeline files"""
    
    def __init__(self):
        self.root = Path.cwd()
        self.colors = {
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'RED': '\033[91m',
            'BLUE': '\033[94m',
            'CYAN': '\033[96m',
            'BOLD': '\033[1m',
            'END': '\033[0m'
        }
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{self.colors['CYAN']}{'='*60}{self.colors['END']}")
        print(f"{self.colors['BOLD']}{self.colors['BLUE']}{text}{self.colors['END']}")
        print(f"{self.colors['CYAN']}{'='*60}{self.colors['END']}\n")
    
    def print_check(self, text, status, detail=""):
        """Print check result with appropriate color"""
        icon = "✅" if status else "❌"
        color = self.colors['GREEN'] if status else self.colors['RED']
        if detail:
            print(f"{color}{icon} {text}{self.colors['END']}")
            print(f"   → {detail}")
        else:
            print(f"{color}{icon} {text}{self.colors['END']}")
    
    def create_dag(self):
        """Create DAG file"""
        self.print_header("📁 CREATING DAG FILE")
        
        dag_path = self.root / 'dags' / 'uber_etl_dag.py'
        if dag_path.exists():
            self.print_check("uber_etl_dag.py already exists", True)
            return
        
        content = '''from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from extract import extract_data
from transform import transform_data
from load import load_data

default_args = {
    'owner': 'Arkan Tsabit',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'uber_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for NYC Uber/Taxi data',
    schedule_interval='@daily',
    catchup=False,
    tags=['uber', 'etl', 'nyc'],
)

start = DummyOperator(task_id='start', dag=dag)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

start >> extract_task >> transform_task >> load_task >> end
'''
        
        dag_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dag_path, 'w') as f:
            f.write(content)
        self.print_check("uber_etl_dag.py created", True)
    
    def create_extract(self):
        """Create extract script"""
        self.print_header("📁 CREATING EXTRACT SCRIPT")
        
        extract_path = self.root / 'scripts' / 'extract.py'
        if extract_path.exists():
            self.print_check("extract.py already exists", True)
            return
        
        content = '''import pandas as pd
import os

def extract_data(**context):
    """Extract data from CSV file"""
    data_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'data',
        'uber_data.csv'
    )
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found: {data_path}")
    
    df = pd.read_csv(data_path)
    
    temp_path = '/tmp/uber_data.csv'
    df.to_csv(temp_path, index=False)
    
    print(f"✅ Extracted {len(df):,} rows")
    print(f"📊 Columns: {df.columns.tolist()}")
    
    return {'rows': len(df), 'columns': len(df.columns)}
'''
        
        extract_path.parent.mkdir(parents=True, exist_ok=True)
        with open(extract_path, 'w') as f:
            f.write(content)
        self.print_check("extract.py created", True)
    
    def create_transform(self):
        """Create transform script"""
        self.print_header("📁 CREATING TRANSFORM SCRIPT")
        
        transform_path = self.root / 'scripts' / 'transform.py'
        if transform_path.exists():
            self.print_check("transform.py already exists", True)
            return
        
        content = '''import pandas as pd

def transform_data(**context):
    """Transform data into Star Schema"""
    df = pd.read_csv('/tmp/uber_data.csv')
    
    print(f"🔄 Transforming {len(df):,} rows...")
    
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.dropna(subset=['tpep_pickup_datetime', 'tpep_dropoff_datetime'])
    print(f"   ✅ {len(df):,} rows after cleaning")
    
    datetime_dim = df[['tpep_pickup_datetime']].copy()
    datetime_dim['datetime_id'] = datetime_dim.index + 1
    datetime_dim['pickup_datetime'] = pd.to_datetime(datetime_dim['tpep_pickup_datetime'])
    datetime_dim['pick_hour'] = datetime_dim['pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['pickup_datetime'].dt.day_name()
    datetime_dim = datetime_dim.drop('tpep_pickup_datetime', axis=1)
    
    rate_code_dim = df[['RatecodeID']].copy().drop_duplicates().reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index + 1
    rate_map = {
        1: 'Standard', 2: 'JFK', 3: 'Newark',
        4: 'Nassau/Westchester', 5: 'Negotiated', 6: 'Group Ride'
    }
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_map)
    
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
    
    datetime_dim.to_csv('/tmp/datetime_dim.csv', index=False)
    rate_code_dim.to_csv('/tmp/rate_code_dim.csv', index=False)
    location_dim.to_csv('/tmp/location_dim.csv', index=False)
    fact_table.to_csv('/tmp/fact_table.csv', index=False)
    
    print(f"✅ datetime_dim: {len(datetime_dim):,} rows")
    print(f"✅ rate_code_dim: {len(rate_code_dim):,} rows")
    print(f"✅ location_dim: {len(location_dim):,} rows")
    print(f"✅ fact_table: {len(fact_table):,} rows")
    
    return {
        'datetime_rows': len(datetime_dim),
        'rate_rows': len(rate_code_dim),
        'location_rows': len(location_dim),
        'fact_rows': len(fact_table)
    }
'''
        
        transform_path.parent.mkdir(parents=True, exist_ok=True)
        with open(transform_path, 'w') as f:
            f.write(content)
        self.print_check("transform.py created", True)
    
    def create_load(self):
        """Create load script"""
        self.print_header("📁 CREATING LOAD SCRIPT")
        
        load_path = self.root / 'scripts' / 'load.py'
        if load_path.exists():
            self.print_check("load.py already exists", True)
            return
        
        content = '''import duckdb
import pandas as pd
import os

def load_data(**context):
    """Load transformed data to DuckDB"""
    datetime_dim = pd.read_csv('/tmp/datetime_dim.csv')
    rate_code_dim = pd.read_csv('/tmp/rate_code_dim.csv')
    location_dim = pd.read_csv('/tmp/location_dim.csv')
    fact_table = pd.read_csv('/tmp/fact_table.csv')
    
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'warehouse',
        'uber.duckdb'
    )
    
    conn = duckdb.connect(db_path)
    print("✅ Connected to DuckDB")
    
    conn.execute("DROP TABLE IF EXISTS datetime_dim")
    conn.execute("CREATE TABLE datetime_dim AS SELECT * FROM datetime_dim")
    print(f"✅ Loaded datetime_dim: {len(datetime_dim):,} rows")
    
    conn.execute("DROP TABLE IF EXISTS rate_code_dim")
    conn.execute("CREATE TABLE rate_code_dim AS SELECT * FROM rate_code_dim")
    print(f"✅ Loaded rate_code_dim: {len(rate_code_dim):,} rows")
    
    conn.execute("DROP TABLE IF EXISTS location_dim")
    conn.execute("CREATE TABLE location_dim AS SELECT * FROM location_dim")
    print(f"✅ Loaded location_dim: {len(location_dim):,} rows")
    
    conn.execute("DROP TABLE IF EXISTS fact_table")
    conn.execute("CREATE TABLE fact_table AS SELECT * FROM fact_table")
    print(f"✅ Loaded fact_table: {len(fact_table):,} rows")
    
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
    
    conn.close()
    print("✅ Data loaded successfully!")
    
    return {'status': 'success'}
'''
        
        load_path.parent.mkdir(parents=True, exist_ok=True)
        with open(load_path, 'w') as f:
            f.write(content)
        self.print_check("load.py created", True)
    
    def create_dashboard(self):
        """Create dashboard app"""
        self.print_header("📁 CREATING DASHBOARD APP")
        
        app_path = self.root / 'dashboard' / 'app.py'
        if app_path.exists():
            self.print_check("app.py already exists", True)
            return
        
        content = '''import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Uber NYC Dashboard",
    page_icon="🚖",
    layout="wide"
)

st.title("🚖 Uber NYC Trip Analytics Dashboard")
st.markdown("*End-to-End Data Pipeline with Apache Airflow*")

@st.cache_resource
def get_connection():
    return duckdb.connect('warehouse/uber.duckdb')

@st.cache_data
def load_data():
    conn = get_connection()
    try:
        df = conn.execute("SELECT * FROM trip_analytics").fetchdf()
    except:
        df = pd.DataFrame()
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ No data found. Please run the Airflow pipeline first!")
    st.info("1. Open Airflow UI: http://localhost:8080")
    st.info("2. Trigger DAG: uber_etl_pipeline")
    st.info("3. Refresh this dashboard")
else:
    st.sidebar.header("🔍 Filters")
    year = st.sidebar.selectbox("Year", sorted(df['pick_year'].unique()) if 'pick_year' in df.columns else [])
    month = st.sidebar.selectbox("Month", sorted(df['pick_month'].unique()) if 'pick_month' in df.columns else [])
    weekday = st.sidebar.multiselect("Weekday", df['pick_weekday'].unique() if 'pick_weekday' in df.columns else [])
    
    filtered_df = df.copy()
    if 'pick_year' in df.columns and year:
        filtered_df = filtered_df[filtered_df['pick_year'] == year]
    if 'pick_month' in df.columns and month:
        filtered_df = filtered_df[filtered_df['pick_month'] == month]
    if 'pick_weekday' in df.columns and weekday:
        filtered_df = filtered_df[filtered_df['pick_weekday'].isin(weekday)]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Trips", f"{len(filtered_df):,}")
    with col2:
        st.metric("Total Revenue", f"${filtered_df['total_amount'].sum():,.2f}")
    with col3:
        st.metric("Avg Distance", f"{filtered_df['trip_distance'].mean():.2f} miles")
    with col4:
        st.metric("Avg Fare", f"${filtered_df['fare_amount'].mean():.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        if 'pick_hour' in filtered_df.columns:
            hourly_revenue = filtered_df.groupby('pick_hour')['total_amount'].sum().reset_index()
            fig1 = px.line(hourly_revenue, x='pick_hour', y='total_amount', title='Revenue by Hour', markers=True)
            st.plotly_chart(fig1, use_container_width=True)
    with col2:
        if 'pick_weekday' in filtered_df.columns:
            weekday_trips = filtered_df['pick_weekday'].value_counts().reset_index()
            weekday_trips.columns = ['weekday', 'count']
            fig2 = px.bar(weekday_trips, x='weekday', y='count', title='Trips by Weekday')
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        if 'rate_code_name' in filtered_df.columns:
            rate_dist = filtered_df['rate_code_name'].value_counts().reset_index()
            rate_dist.columns = ['rate_code', 'count']
            fig3 = px.pie(rate_dist, values='count', names='rate_code', title='Rate Code Distribution')
            st.plotly_chart(fig3, use_container_width=True)
    with col4:
        if 'trip_distance' in filtered_df.columns and 'fare_amount' in filtered_df.columns:
            fig4 = px.scatter(filtered_df, x='trip_distance', y='fare_amount', title='Distance vs Fare', opacity=0.6)
            st.plotly_chart(fig4, use_container_width=True)
    
    with st.expander("📊 View Data Table"):
        st.dataframe(filtered_df)
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv, file_name="uber_trip_data.csv", mime="text/csv")

st.markdown("---")
st.markdown("Built with ❤️ using Apache Airflow, DuckDB, Streamlit, and Plotly")
'''
        
        app_path.parent.mkdir(parents=True, exist_ok=True)
        with open(app_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.print_check("app.py created", True)
    
    def run_all(self):
        """Run all setup steps"""
        self.print_header("🚀 UBER ETL PIPELINE - PIPELINE SETUP")
        
        print(f"📂 Project Root: {self.root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.create_dag()
        self.create_extract()
        self.create_transform()
        self.create_load()
        self.create_dashboard()
        
        self.print_header("✅ PIPELINE SETUP COMPLETE!")
        print("\n📋 Next Steps:")
        print("  1. Start Docker Desktop")
        print("  2. Start Airflow: docker-compose up -d")
        print("  3. Open Airflow UI: http://localhost:8080")
        print("  4. Trigger DAG: uber_etl_pipeline")
        print("  5. Check logs in Airflow UI")
        print("  6. Run: streamlit run dashboard/app.py")


if __name__ == "__main__":
    setup = PipelineSetup()
    setup.run_all()