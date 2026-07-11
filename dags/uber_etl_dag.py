# dags/uber_etl_dag.py
"""
Airflow DAG for Uber ETL Pipeline.

Orchestrates the Extract, Transform, Load process for NYC Uber/Taxi data.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta
import sys
import os


# ============================================
# Add scripts folder to Python path
# ============================================

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))


# ============================================
# Import ETL functions
# ============================================

from extract import extract_data
from transform import transform_data
from load import load_data


# ============================================
# DAG Default Arguments
# ============================================

default_args = {
    'owner': 'Arkan Tsabit',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


# ============================================
# DAG Definition
# ============================================

dag = DAG(
    'uber_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for NYC Uber/Taxi data using Apache Airflow',
    schedule_interval='@daily',
    catchup=False,
    tags=['uber', 'etl', 'nyc', 'airflow'],
)


# ============================================
# Tasks
# ============================================

start = DummyOperator(
    task_id='start',
    dag=dag,
)

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

end = DummyOperator(
    task_id='end',
    dag=dag,
)


# ============================================
# Task Dependencies
# ============================================

start >> extract_task >> transform_task >> load_task >> end