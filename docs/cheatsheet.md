# Uber ETL Pipeline - Cheat Sheet (Apache Airflow with Docker)

## Quick Commands

### Virtual Environment

```bash
# One Command Start (Windows PowerShell on root files)
venv\Scripts\activate; docker-compose up -d; docker-compose ps; start http://localhost:8080

# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# Activate venv (Mac/Linux)
source venv/bin/activate

# Deactivate venv
deactivate

# Delete venv (Windows)
rmdir /s venv

# Delete venv (Mac/Linux)
rm -rf venv
```

---

## Docker Commands (Airflow)

### Start Airflow with Docker

```bash
# Start all services
docker-compose up -d

# Start with logs
docker-compose up

# Start specific service
docker-compose up -d airflow-webserver

# Stop all services
docker-compose down

# Stop and remove volumes (clean reset)
docker-compose down -v

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart airflow-webserver

# Check container status
docker-compose ps

# View all logs
docker-compose logs -f

# View specific container logs
docker-compose logs airflow-webserver -f
docker-compose logs airflow-scheduler -f

# Check resource usage
docker stats

# Clean up unused images/containers
docker system prune -f
```

### Airflow Docker URLs

```bash
# Airflow UI
http://localhost:8080

# Flower (Celery monitoring)
http://localhost:5555

# PostgreSQL (metadata database)
localhost:5432
```

### Airflow Docker Default Credentials

```bash
Username: admin
Password: admin
```

### Port Mapping Summary

| Service | Port |
|---------|------|
| Airflow UI | 8080 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Streamlit Dashboard | 8501 |

---

## Airflow Commands (Inside Container / Linux Only)

**Note:** Airflow does not run natively on Windows. Use Docker!

### DAG Management (From host)

```bash
# Trigger a DAG
airflow dags trigger uber_etl_pipeline

# Trigger with config
airflow dags trigger -c '{"key":"value"}' uber_etl_pipeline

# Pause a DAG
airflow dags pause uber_etl_pipeline

# Unpause a DAG
airflow dags unpause uber_etl_pipeline

# List DAG runs
airflow dags list-runs --dag-id uber_etl_pipeline

# List all DAGs
airflow dags list
```

### Task Management

```bash
# List tasks in a DAG
airflow tasks list uber_etl_pipeline

# Test a single task
airflow tasks test uber_etl_pipeline extract_data 2026-01-01

# Clear task instances
airflow tasks clear -d uber_etl_pipeline

# Show task state
airflow tasks state uber_etl_pipeline extract_data 2026-01-01
```

---

## Package Management

### Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Install Airflow only
pip install apache-airflow==2.7.3

# Install with extras
pip install apache-airflow[celery,postgres,docker]==2.7.3

# Upgrade pip
python -m pip install --upgrade pip

# List installed packages
pip list

# Freeze requirements
pip freeze > requirements.txt

# Uninstall package
pip uninstall package_name
```

---

## Python Commands

### Verify Installation

```bash
# Check Python version
python --version

# Check Airflow version
airflow version

# Test imports
python -c "import airflow; print('Airflow OK')"
python -c "import duckdb; print('DuckDB OK')"
python -c "import pandas; print('Pandas OK')"
python -c "import streamlit; print('Streamlit OK')"
python -c "import plotly; print('Plotly OK')"
```

### Run Verification Scripts

```bash
# Phase 1: Setup
python verify-phase-1.py

# Phase 2: DAG
python verify-phase-2.py

# Phase 3: Transform
python verify-phase-3.py

# Phase 4: Load
python verify-phase-4.py

# Phase 5: Dashboard
python verify-phase-5.py

# Phase 6: Deployment
python verify-phase-6.py

# Run all verifications (PowerShell)
1..6 | ForEach-Object { python verify-phase-$_.py }

# Run all verifications (Windows CMD)
for %i in (1 2 3 4 5 6) do python verify-phase-%i.py

# Run all verifications (Mac/Linux)
for i in {1..6}; do python verify-phase-$i.py; done
```

---

## Running the Pipeline

### Start Everything

```bash
# 1. Start Airflow with Docker
docker-compose up -d

# 2. Check if all containers are running
docker-compose ps

# 3. Open Airflow UI
start http://localhost:8080   # Windows
open http://localhost:8080    # Mac

# 4. Trigger DAG (via UI or CLI)
airflow dags trigger uber_etl_pipeline

# 5. Run Dashboard
streamlit run dashboard/app.py
```

### Check Pipeline Status

```bash
# Check DAG run status
airflow dags list-runs --dag-id uber_etl_pipeline

# View logs
docker-compose logs airflow-scheduler -f
```

---

## DuckDB Commands

```bash
# Connect to DuckDB
python -c "import duckdb; conn = duckdb.connect('warehouse/uber.duckdb')"

# List tables
python -c "import duckdb; conn = duckdb.connect('warehouse/uber.duckdb'); print(conn.execute('SHOW TABLES').fetchall())"

# Query data
python -c "import duckdb; conn = duckdb.connect('warehouse/uber.duckdb'); print(conn.execute('SELECT * FROM trip_analytics LIMIT 5').fetchdf())"

# Count rows
python -c "import duckdb; conn = duckdb.connect('warehouse/uber.duckdb'); print(conn.execute('SELECT COUNT(*) FROM fact_table').fetchone())"
```

---

## Project Structure Quick Reference

| Folder | Content |
|--------|---------|
| `dags/` | Airflow DAG files |
| `scripts/` | ETL Python scripts (extract, transform, load) |
| `data/` | Raw dataset (uber_data.csv) |
| `warehouse/` | DuckDB database |
| `dashboard/` | Streamlit app |
| `screenshots/` | Documentation screenshots |
| `docs/` | Documentation files |

---

## Star Schema Tables

### Tables

```sql
-- 1. datetime_dim
datetime_id (PK)
pickup_datetime
pick_hour, pick_day, pick_month, pick_year
pick_weekday

-- 2. rate_code_dim
rate_code_id (PK)
RatecodeID
rate_code_name

-- 3. location_dim
location_id (PK)
location_name
borough

-- 4. fact_table
trip_id (PK)
datetime_id (FK)
rate_code_id (FK)
pickup_location_id (FK)
dropoff_location_id (FK)
trip_distance
trip_duration
fare_amount
total_amount
passenger_count
payment_type
```

### Sample Queries

```sql
-- Daily revenue
SELECT pick_weekday, SUM(total_amount) as revenue
FROM fact_table f
JOIN datetime_dim d ON f.datetime_id = d.datetime_id
GROUP BY pick_weekday;

-- Rate code distribution
SELECT rate_code_name, COUNT(*) as count
FROM fact_table f
JOIN rate_code_dim r ON f.rate_code_id = r.rate_code_id
GROUP BY rate_code_name;

-- Hourly demand
SELECT pick_hour, COUNT(*) as trips
FROM fact_table f
JOIN datetime_dim d ON f.datetime_id = d.datetime_id
GROUP BY pick_hour
ORDER BY pick_hour;
```

---

## One-Liner Setup

```bash
# Complete project setup
python setup_project.py && python setup_pipeline.py

# Reset everything (venv + docker)
docker-compose down -v && rmdir /s venv && python -m venv venv

# Full reset + reinstall
docker-compose down -v && rmdir /s venv && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

---

## Troubleshooting

### Docker Issues

| Issue | Solution |
|-------|----------|
| Docker not running | Start Docker Desktop first |
| Port already in use | Change port in docker-compose.yml |
| Container not starting | `docker-compose logs` to see errors |
| Permission denied | Run terminal as admin |
| Volume conflicts | `docker-compose down -v` |

### Airflow Issues

| Issue | Solution |
|-------|----------|
| Webserver not running | `docker-compose up -d airflow-webserver` |
| DAG not showing | Check `dags/` folder, restart scheduler |
| Task failed | Check logs in UI or `docker-compose logs` |
| Database connection error | Check Postgres container is running |
| Authentication failed | Use default: admin/admin |

### Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt --upgrade` |
| `No module named 'pwd'` | **Use Docker** (Airflow doesn't run natively on Windows) |
| `ERR_CONNECTION_REFUSED` | Start webserver: `docker-compose up -d airflow-webserver` |
| `DAG not found in UI` | Wait 30 seconds, restart scheduler |
| `Port 8080 already in use` | Change port: `"8081:8080"` |

### Quick Troubleshooting Flow

```bash
# 1. Check status of all containers
docker-compose ps

# 2. Check latest errors
docker-compose logs --tail=50

# 3. Restart webserver (if UI is not accessible)
docker-compose restart airflow-webserver

# 4. Restart scheduler (if DAG does not appear)
docker-compose restart airflow-scheduler

# 5. Full restart (if still having issues)
docker-compose down && docker-compose up -d
```

---

## DAG Structure Template

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_name',
    default_args=default_args,
    description='Your DAG description',
    schedule_interval='@daily',
    catchup=False,
)

def task_function(**context):
    print("Task executed!")
    return "Success"

task = PythonOperator(
    task_id='task_name',
    python_callable=task_function,
    dag=dag,
)
```

---

## Important URLs

| Service | URL |
|---------|-----|
| Airflow UI | http://localhost:8080 |
| Flower (Celery) | http://localhost:5555 |
| Streamlit Dashboard | http://localhost:8501 |
| GitHub Repository | https://github.com/ArkanTsabit123/uber-data-pipeline |

---

## Documentation Links

| Resource | URL |
|----------|-----|
| Airflow Docs | https://airflow.apache.org/docs/ |
| DuckDB Docs | https://duckdb.org/docs/ |
| Streamlit Docs | https://docs.streamlit.io/ |
| Plotly Docs | https://plotly.com/python/ |
| Pandas Docs | https://pandas.pydata.org/docs/ |
| Docker Docs | https://docs.docker.com/ |

---

## Quick Tips for Windows Users

1. Always use Docker for Airflow on Windows
2. Always activate venv before working with Python
3. Check `docker-compose ps` to ensure all services are running
4. Use `docker-compose logs -f` to monitor in real-time
5. DAGs are in `./dags` folder (mounted to `/opt/airflow/dags`)
6. Scripts are in `./scripts` folder (mounted to `/opt/airflow/scripts`)
7. Restart services after adding new DAGs
8. Check ports if services won't start (8080, 5432, 6379, 8501)

---

**Save this cheat sheet for quick reference!**