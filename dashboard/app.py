# dashboard/app.py
# Streamlit dashboard for Uber NYC Trip Analytics

"""
Uber NYC Trip Analytics Dashboard
Interactive dashboard for analyzing NYC Uber/Taxi trip data.
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Uber NYC Dashboard",
    page_icon="🚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================
# Title and Description
# ============================================
st.title("🚖 Uber NYC Trip Analytics Dashboard")
st.markdown("*End-to-End Data Pipeline with Apache Airflow*")
st.markdown("---")

# ============================================
# Database Connection
# ============================================
@st.cache_resource
def get_connection():
    """Get DuckDB connection"""
    try:
        return duckdb.connect('warehouse/uber.duckdb')
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

@st.cache_data
def load_data():
    """Load data from DuckDB"""
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        df = conn.execute("SELECT * FROM trip_analytics").fetchdf()
        conn.close()
        return df
    except Exception as e:
        conn.close()
        return pd.DataFrame()

# ============================================
# Load Data
# ============================================
df = load_data()

# ============================================
# Show Warning if No Data
# ============================================
if df.empty:
    st.warning("⚠️ No data found. Please run the Airflow pipeline first!")
    st.info("1. Open Airflow UI: http://localhost:8080")
    st.info("2. Trigger DAG: `uber_etl_pipeline`")
    st.info("3. Refresh this dashboard")
    st.stop()

# ============================================
# Sidebar Filters
# ============================================
st.sidebar.header("🔍 Filters")

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

# Apply filters
filtered_df = df.copy()

if 'pick_year' in df.columns and year:
    filtered_df = filtered_df[filtered_df['pick_year'] == year]

if 'pick_month' in df.columns and month:
    filtered_df = filtered_df[filtered_df['pick_month'] == month]

if 'pick_weekday' in df.columns and weekday:
    filtered_df = filtered_df[filtered_df['pick_weekday'].isin(weekday)]

# ============================================
# KPI Cards
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Trips",
        f"{len(filtered_df):,}",
        delta=None,
        help="Total number of trips"
    )

with col2:
    st.metric(
        "Total Revenue",
        f"${filtered_df['total_amount'].sum():,.2f}",
        delta=None,
        help="Total revenue from all trips"
    )

with col3:
    st.metric(
        "Avg Distance",
        f"{filtered_df['trip_distance'].mean():.2f} miles",
        delta=None,
        help="Average trip distance"
    )

with col4:
    st.metric(
        "Avg Fare",
        f"${filtered_df['fare_amount'].mean():.2f}",
        delta=None,
        help="Average fare per trip"
    )

st.markdown("---")

# ============================================
# Charts - Row 1
# ============================================
col1, col2 = st.columns(2)

# Chart 1: Revenue by Hour
with col1:
    if 'pick_hour' in filtered_df.columns:
        hourly_revenue = filtered_df.groupby('pick_hour')['total_amount'].sum().reset_index()
        fig1 = px.line(
            hourly_revenue,
            x='pick_hour',
            y='total_amount',
            title='💰 Revenue by Hour',
            markers=True,
            color_discrete_sequence=['#1f77b4']
        )
        fig1.update_layout(
            xaxis_title='Hour of Day',
            yaxis_title='Total Revenue ($)',
            hovermode='x unified'
        )
        st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Trips by Weekday
with col2:
    if 'pick_weekday' in filtered_df.columns:
        weekday_trips = filtered_df['pick_weekday'].value_counts().reset_index()
        weekday_trips.columns = ['weekday', 'count']
        
        # Order weekdays correctly
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_trips['weekday'] = pd.Categorical(weekday_trips['weekday'], categories=weekday_order, ordered=True)
        weekday_trips = weekday_trips.sort_values('weekday')
        
        fig2 = px.bar(
            weekday_trips,
            x='weekday',
            y='count',
            title='📊 Trips by Weekday',
            color='count',
            color_continuous_scale='Blues'
        )
        fig2.update_layout(
            xaxis_title='Weekday',
            yaxis_title='Number of Trips',
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

# ============================================
# Charts - Row 2
# ============================================
col3, col4 = st.columns(2)

# Chart 3: Rate Code Distribution
with col3:
    if 'rate_code_name' in filtered_df.columns:
        rate_dist = filtered_df['rate_code_name'].value_counts().reset_index()
        rate_dist.columns = ['rate_code', 'count']
        fig3 = px.pie(
            rate_dist,
            values='count',
            names='rate_code',
            title='🏷️ Rate Code Distribution',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)

# Chart 4: Distance vs Fare
with col4:
    if 'trip_distance' in filtered_df.columns and 'fare_amount' in filtered_df.columns:
        fig4 = px.scatter(
            filtered_df,
            x='trip_distance',
            y='fare_amount',
            title='📈 Distance vs Fare',
            opacity=0.5,
            color='passenger_count',
            color_continuous_scale='Viridis',
            labels={
                'trip_distance': 'Trip Distance (miles)',
                'fare_amount': 'Fare Amount ($)',
                'passenger_count': 'Passenger Count'
            }
        )
        fig4.update_layout(
            hovermode='closest'
        )
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ============================================
# Data Table
# ============================================
with st.expander("📊 View Data Table", expanded=False):
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'trip_id': 'Trip ID',
            'trip_distance': st.column_config.NumberColumn('Distance (miles)', format='%.2f'),
            'fare_amount': st.column_config.NumberColumn('Fare ($)', format='$%.2f'),
            'total_amount': st.column_config.NumberColumn('Total ($)', format='$%.2f'),
            'passenger_count': 'Passengers',
            'pickup_datetime': 'Pickup Time',
            'pick_hour': 'Hour',
            'pick_weekday': 'Weekday',
            'pick_month': 'Month',
            'pick_year': 'Year',
            'rate_code_name': 'Rate Code',
            'pickup_location': 'Pickup Location',
            'dropoff_location': 'Dropoff Location'
        }
    )
    
    # Download button
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="uber_trip_data.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================================
# Footer
# ============================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        Built with ❤️ using 
        <strong>Apache Airflow</strong>, 
        <strong>DuckDB</strong>, 
        <strong>Streamlit</strong>, and 
        <strong>Plotly</strong>
        <br>
        <small>© 2026 Arkan Tsabit</small>
    </div>
    """,
    unsafe_allow_html=True
)