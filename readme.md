```markdown
# Uber ETL Pipeline Project

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7.3-blue.svg)](https://airflow.apache.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-0.9.2-yellow.svg)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-green.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Why This Project](#why-this-project)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Star Schema Design](#star-schema-design)
- [Pipeline Phases](#pipeline-phases)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Running the Pipeline](#running-the-pipeline)
- [Dashboard Preview](#dashboard-preview)
- [Business Questions Answered](#business-questions-answered)
- [Verification & Testing](#verification--testing)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

This project implements an **end-to-end data pipeline** for analyzing NYC Uber/Taxi trip data using **industry-standard open-source tools** that data engineers use in production environments.

### Key Features

- Orchestration with **Apache Airflow** (industry standard)
- **Star Schema Data Warehouse** in DuckDB (4 tables)
- **Interactive Dashboard** with Streamlit + Plotly
- **Containerized Setup** with Docker for easy deployment
- **Automated Scheduling** with Airflow DAGs
- **Comprehensive Documentation** with 33 screenshots

### Business Questions Addressed

- What are the peak hours for ride demand?
- How does revenue pattern vary by day of the week?
- Which rate codes are most frequently used?
- What are the average trip distance and revenue per trip?
- How do passenger counts affect fare amounts?
- What is the distribution of payment types?

---

## Why This Project

### The Problem This Project Solves

Many data engineering portfolios use niche tools that aren't widely adopted in the industry. This project is built with **tools that data engineers actually use** in production environments.

### Why Apache Airflow?

| Aspect | Airflow | Why It Matters |
|--------|---------|----------------|
| Industry Standard | 5/5 | Most used orchestration tool globally |
| Job Market | 5/5 | Required skill for 80%+ DE jobs |
| Community | 5/5 | Largest community, endless resources |
| Production Ready | 5/5 | Used by thousands of companies |
| Scalability | 5/5 | From small to enterprise scale |

### Tools Comparison

| Tool | Popularity | Used In Companies | Portfolio Value |
|------|------------|-------------------|-----------------|
| Apache Airflow | 5/5 | Most companies | 5/5 |
| Dagster | 4/5 | Growing | 4/5 |
| Prefect | 4/5 | Growing | 4/5 |
| Mage AI | 2/5 | Limited | 2/5 |

---

## Architecture

### Pipeline Flow Diagram

![Pipeline Flow Diagram](screenshots/32-pipeline-flow-diagram.png)

*Diagram showing the complete ETL pipeline flow from data extraction to dashboard visualization.*

### Data Flow Summary

1. **Extract**: Load CSV data from `data/uber_data.csv`
2. **Transform**: Build Star Schema with 4 dimension tables
3. **Load**: Store transformed data in DuckDB
4. **Visualize**: Display insights via Streamlit dashboard

---

## Tech Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Orchestration | Apache Airflow | 2.7.3 | Workflow scheduling & orchestration |
| Data Warehouse | DuckDB | 0.9.2 | In-process OLAP database |
| Dashboard | Streamlit | 1.29.0 | Interactive web application |
| Visualization | Plotly | 5.18.0 | Interactive charting |
| Data Processing | Pandas | 2.1.4 | Data manipulation |
| Container | Docker | Latest | Easy deployment |
| Language | Python | 3.10+ | Primary programming language |

---

## Star Schema Design

### Entity-Relationship Diagram

![ERD Diagram](screenshots/33-erd-diagram.png)

*Star Schema design showing fact_table and dimension tables (datetime_dim, rate_code_dim, location_dim).*

### Table Definitions

#### 1. datetime_dim (Dimension Table)

| Column | Type | Description |
|--------|------|-------------|
| `datetime_id` | INTEGER | Primary Key (auto-increment) |
| `pickup_datetime` | TIMESTAMP | Exact pickup timestamp |
| `pick_hour` | INTEGER | Hour of day (0-23) |
| `pick_day` | INTEGER | Day of month (1-31) |
| `pick_month` | INTEGER | Month (1-12) |
| `pick_year` | INTEGER | Year |
| `pick_weekday` | VARCHAR | Day name (Monday-Sunday) |

#### 2. rate_code_dim (Dimension Table)

| Column | Type | Description |
|--------|------|-------------|
| `rate_code_id` | INTEGER | Primary Key (auto-increment) |
| `RatecodeID` | INTEGER | Rate code ID from dataset |
| `rate_code_name` | VARCHAR | Human-readable rate name |

**Rate Code Mapping:**

| RatecodeID | Name |
|------------|------|
| 1 | Standard |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau/Westchester |
| 5 | Negotiated |
| 6 | Group Ride |

#### 3. location_dim (Dimension Table)

| Column | Type | Description |
|--------|------|-------------|
| `location_id` | INTEGER | Primary Key (auto-increment) |
| `location_name` | VARCHAR | NYC zone name |
| `borough` | VARCHAR | Borough (Manhattan, Brooklyn, etc.) |

#### 4. fact_table (Fact Table)

| Column | Type | Description |
|--------|------|-------------|
| `trip_id` | INTEGER | Primary Key (auto-increment) |
| `datetime_id` | INTEGER | FK → datetime_dim |
| `rate_code_id` | INTEGER | FK → rate_code_dim |
| `pickup_location_id` | INTEGER | FK → location_dim |
| `dropoff_location_id` | INTEGER | FK → location_dim |
| `trip_distance` | FLOAT | Trip distance (miles) |
| `trip_duration` | FLOAT | Trip duration (minutes) |
| `fare_amount` | FLOAT | Fare amount ($) |
| `total_amount` | FLOAT | Total amount with tips/tolls ($) |
| `passenger_count` | INTEGER | Number of passengers |
| `payment_type_id` | INTEGER | Payment type (1=Credit, 2=Cash, etc.) |

---

## Pipeline Phases

### Phase 1: Setup & Environment

Establish the foundation for the project.

| Task | Detail |
|------|--------|
| 1.1 | Folder structure: `dags/`, `scripts/`, `data/`, `warehouse/`, `dashboard/` |
| 1.2 | Virtual environment: `python -m venv venv` |
| 1.3 | Requirements: `apache-airflow`, `duckdb`, `pandas`, `streamlit`, `plotly` |
| 1.4 | Dataset: Download `uber_data.csv` to `data/` |
| 1.5 | Verification: `python verify-phase-1.py` |

### Phase 2: Airflow DAG Creation

Create the Airflow DAG for orchestration.

| Task | Detail |
|------|--------|
| 2.1 | Start Airflow: `docker-compose up -d` |
| 2.2 | Create DAG: `uber_etl_dag.py` in `dags/` folder |
| 2.3 | Create extract task: `scripts/extract.py` |
| 2.4 | Create transform task: `scripts/transform.py` |
| 2.5 | Create load task: `scripts/load.py` |
| 2.6 | Verification: `python verify-phase-2.py` |

### Phase 3: Data Transformation

Build the Star Schema.

| Task | Detail |
|------|--------|
| 3.1 | Data cleaning: `drop_duplicates()`, `dropna()`, `reset_index()` |
| 3.2 | Build `datetime_dim`: Extract temporal components |
| 3.3 | Build `rate_code_dim`: Map rate codes to names |
| 3.4 | Build `location_dim`: Create unique locations |
| 3.5 | Build `fact_table`: Combine all dimensions |
| 3.6 | Verification: `python verify-phase-3.py` |

### Phase 4: Data Loading to DuckDB

Store transformed data in DuckDB.

| Task | Detail |
|------|--------|
| 4.1 | Connect to DuckDB: `duckdb.connect('warehouse/uber.duckdb')` |
| 4.2 | Create tables: `DROP TABLE IF EXISTS`, `CREATE TABLE` |
| 4.3 | Insert data: Load transformed data |
| 4.4 | Create view: `trip_analytics` for dashboard |
| 4.5 | Verification: `python verify-phase-4.py` |

### Phase 5: Dashboard Development

Build an interactive visualization dashboard.

| Task | Detail |
|------|--------|
| 5.1 | Create `dashboard/app.py`: Streamlit application |
| 5.2 | KPI Cards: Total Trips, Revenue, Avg Distance, Avg Fare |
| 5.3 | Line Chart: Revenue per Hour |
| 5.4 | Bar Chart: Trips by Weekday |
| 5.5 | Pie Chart: Rate Code Distribution |
| 5.6 | Scatter Plot: Distance vs Fare |
| 5.7 | Sidebar filters: Year, Month, Weekday |
| 5.8 | Run dashboard: `streamlit run dashboard/app.py` |
| 5.9 | Verification: `python verify-phase-5.py` |

### Phase 6: Deployment & Documentation

Finalize the project.

| Task | Detail |
|------|--------|
| 6.1 | README.md: Comprehensive project documentation |
| 6.2 | Screenshots: 33 screenshots in `screenshots/` |
| 6.3 | Git init: `git init` |
| 6.4 | GitHub repo: Create public repository |
| 6.5 | Push: `git push origin main` |
| 6.6 | Verification: `python verify-phase-6.py` |

---

## Project Structure

```
uber-data-pipeline/
│
├── dags/
│   └── uber_etl_dag.py              # Airflow DAG definition
│
├── scripts/
│   ├── extract.py                   # Extract data from CSV
│   ├── transform.py                 # Transform to Star Schema
│   └── load.py                      # Load to DuckDB
│
├── data/
│   └── uber_data.csv                # Raw NYC Uber/Taxi dataset
│
├── warehouse/
│   └── uber.duckdb                  # DuckDB database file
│
├── dashboard/
│   └── app.py                       # Streamlit dashboard
│
├── screenshots/
│   └── (33 verification screenshots)
│
├── docker-compose.yml               # Airflow with Docker
├── verify-phase-1.py                # Phase 1: Setup Verification
├── verify-phase-2.py                # Phase 2: DAG Verification
├── verify-phase-3.py                # Phase 3: Transform Verification
├── verify-phase-4.py                # Phase 4: Load Verification
├── verify-phase-5.py                # Phase 5: Dashboard Verification
├── verify-phase-6.py                # Phase 6: Deployment Verification
│
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Git ignore file
├── LICENSE                          # MIT License
└── README.md                        # Documentation (this file)
```

---

## Prerequisites

Before you begin, ensure you have the following installed:

| Software | Version | Check Command | Download |
|----------|---------|---------------|----------|
| Python | 3.10+ | `python --version` | [python.org](https://python.org) |
| Docker | Latest | `docker --version` | [docker.com](https://docker.com) |
| Docker Compose | Latest | `docker-compose --version` | [docker.com](https://docker.com) |
| Git | Latest | `git --version` | [git-scm.com](https://git-scm.com) |

---

## Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/ArkanTsabit123/uber-data-pipeline.git
cd uber-data-pipeline

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # On Windows
source venv/bin/activate       # On Mac/Linux

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Start Airflow with Docker
docker-compose up -d

# 5. Wait for services to start (about 30 seconds)
# Access Airflow UI: http://localhost:8080
# Username: admin, Password: admin

# 6. Trigger the DAG
# In Airflow UI, find 'uber_etl_pipeline' and click 'Trigger DAG'

# 7. Run the dashboard
streamlit run dashboard/app.py
```

### Option 2: Local Installation (Without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/ArkanTsabit123/uber-data-pipeline.git
cd uber-data-pipeline

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Initialize Airflow database
airflow db init

# 5. Create admin user
airflow users create \
    --username admin \
    --password admin \
    --role Admin \
    --email admin@example.com

# 6. Start Airflow services
airflow scheduler &
airflow webserver -p 8080

# 7. Trigger the DAG
airflow dags trigger uber_etl_pipeline

# 8. Run the dashboard
streamlit run dashboard/app.py
```

---

## Running the Pipeline

### Trigger DAG from Airflow UI

1. Open Airflow UI: http://localhost:8080
2. Find DAG: `uber_etl_pipeline`
3. Click the play button to trigger
4. Monitor the DAG run status

### Trigger DAG from CLI

```bash
# Trigger manually
airflow dags trigger uber_etl_pipeline

# Check DAG status
airflow dags list-runs --dag-id uber_etl_pipeline
```

### Monitor DAG Run

1. In Airflow UI, click on DAG name
2. View the Grid View for task status
3. All tasks should show green (success)

---

## Dashboard Preview

The Streamlit dashboard provides the following visualizations:

### Key Performance Indicators (KPIs)

- **Total Trips**: Count of all trips
- **Total Revenue**: Sum of all fares
- **Average Distance**: Mean trip distance
- **Average Fare**: Mean fare amount

### Interactive Charts

| Chart | Type | Description |
|-------|------|-------------|
| Revenue by Hour | Line Chart | Shows hourly revenue patterns |
| Trips by Weekday | Bar Chart | Identifies peak days |
| Rate Code Distribution | Pie Chart | Most common rate codes |
| Distance vs Fare | Scatter Plot | Correlation analysis |

### Filters

- **Year**: Filter by year
- **Month**: Filter by month
- **Weekday**: Filter by day of week

---

## Business Questions Answered

### 1. When is demand highest?

```sql
SELECT pick_hour, COUNT(*) as trip_count
FROM fact_table f
JOIN datetime_dim d ON f.datetime_id = d.datetime_id
GROUP BY pick_hour
ORDER BY trip_count DESC;
```

### 2. How does revenue vary by day?

```sql
SELECT pick_weekday, SUM(total_amount) as revenue
FROM fact_table f
JOIN datetime_dim d ON f.datetime_id = d.datetime_id
GROUP BY pick_weekday
ORDER BY revenue DESC;
```

### 3. Which rate codes are most common?

```sql
SELECT rate_code_name, COUNT(*) as count
FROM fact_table f
JOIN rate_code_dim r ON f.rate_code_id = r.rate_code_id
GROUP BY rate_code_name
ORDER BY count DESC;
```

### 4. What are average trip metrics?

```sql
SELECT 
    AVG(trip_distance) as avg_distance,
    AVG(fare_amount) as avg_fare,
    AVG(total_amount) as avg_total
FROM fact_table;
```

---

## Verification & Testing

### Verification Summary

| Phase | Script | Focus |
|-------|--------|-------|
| 1 | `verify-phase-1.py` | Setup & Environment |
| 2 | `verify-phase-2.py` | Airflow DAG |
| 3 | `verify-phase-3.py` | Transform (Star Schema) |
| 4 | `verify-phase-4.py` | Load to DuckDB |
| 5 | `verify-phase-5.py` | Dashboard |
| 6 | `verify-phase-6.py` | Deployment |

### Run All Verifications

```bash
# Run all at once (Windows PowerShell)
1..6 | ForEach-Object { python verify-phase-$_.py }

# Run all at once (Mac/Linux)
for i in {1..6}; do python verify-phase-$i.py; done

# Using the runner script
python run_all_verifications.py
```

---

## Screenshots

### Architecture Diagrams

| Screenshot | Description |
|------------|-------------|
| ![Pipeline Flow Diagram](screenshots/32-pipeline-flow-diagram.png) | ETL Pipeline flow diagram showing the complete data flow from CSV to Dashboard |
| ![ERD Diagram](screenshots/33-erd-diagram.png) | Star Schema ERD diagram showing fact_table and dimension tables relationships |

### Phase 0: Repository & Setup

| Screenshot | Description |
|------------|-------------|
| ![GitHub Repository](screenshots/01-github-repo-created.png) | GitHub repository created |
| ![Terminal Setup](screenshots/02-terminal-setup.png) | Terminal with venv active |

### Phase 1: Environment Setup

| Screenshot | Description |
|------------|-------------|
| ![Folder Structure](screenshots/03-folder-structure.png) | Project folder structure |
| ![Dataset Downloaded](screenshots/04-dataset-downloaded.png) | Dataset in data/ folder |
| ![Phase 1 Verification](screenshots/05-verify-phase1-success.png) | Phase 1 verification passed (100%) |

### Phase 2: Airflow DAG

| Screenshot | Description |
|------------|-------------|
| ![Airflow UI](screenshots/06-airflow-ui.png) | Airflow UI dashboard |
| ![DAG List](screenshots/07-dag-list.png) | DAG list in Airflow |
| ![DAG Graph View](screenshots/08-dag-graph.png) | DAG graph view |
| ![DAG Success](screenshots/09-dag-success.png) | DAG run success |
| ![Phase 2 Verification](screenshots/10-verify-phase2-success.png) | Phase 2 verification passed |

### Phase 3: Data Transformation

| Screenshot | Description |
|------------|-------------|
| ![Transform Script](screenshots/11-transform-script.png) | Transform script code |
| ![Transform Logs](screenshots/12-transform-logs.png) | Transform execution logs |
| ![Phase 3 Verification](screenshots/13-verify-phase3-success.png) | Phase 3 verification passed |

### Phase 4: Data Loading

| Screenshot | Description |
|------------|-------------|
| ![Load Script](screenshots/14-load-script.png) | Load script code |
| ![DuckDB Tables](screenshots/15-duckdb-tables.png) | Tables created in DuckDB |
| ![DuckDB Data](screenshots/16-duckdb-data.png) | Sample data in DuckDB |
| ![Phase 4 Verification](screenshots/17-verify-phase4-success.png) | Phase 4 verification passed |

### Phase 5: Dashboard Development

| Screenshot | Description |
|------------|-------------|
| ![Dashboard Code](screenshots/18-dashboard-code.png) | Dashboard application code |
| ![Dashboard Overview](screenshots/19-dashboard-overview.png) | Dashboard overview |
| ![Dashboard Filters](screenshots/20-dashboard-filters.png) | Sidebar filters |
| ![Dashboard Charts](screenshots/21-dashboard-charts.png) | All interactive charts |
| ![Dashboard KPI](screenshots/22-dashboard-kpi.png) | KPI cards |
| ![Dashboard with Filter](screenshots/23-dashboard-with-filter.png) | Dashboard with filter applied |
| ![Phase 5 Verification](screenshots/24-verify-phase5-success.png) | Phase 5 verification passed |

### Phase 6: Deployment

| Screenshot | Description |
|------------|-------------|
| ![README Overview](screenshots/25-readme-overview.png) | README.md overview |
| ![Screenshots Folder](screenshots/26-screenshots-folder.png) | Screenshots folder |
| ![Phase 6 Verification](screenshots/27-verify-phase6-success.png) | Phase 6 verification passed |
| ![Git Commit](screenshots/28-git-commit.png) | Git commit |
| ![Git Push](screenshots/29-git-push.png) | Git push |
| ![GitHub Repo Final](screenshots/30-github-repo-final.png) | Final GitHub repository |
| ![README Rendered](screenshots/31-readme-rendered.png) | README.md rendered on GitHub |

---

## Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt --upgrade` |
| Database connection error | Verify `warehouse/uber.duckdb` exists and has data |
| Docker port already in use | Change ports in `docker-compose.yml` |
| Airflow UI not loading | Check `docker-compose ps` for container status |
| Dashboard not loading | Upgrade Streamlit: `pip install streamlit --upgrade` |
| DAG not showing in UI | Check DAG folder path in `airflow.cfg` |
| `No module named 'pwd'` | **Use Docker** (Airflow doesn't run natively on Windows) |

### Getting Help

- **Apache Airflow Documentation**: https://airflow.apache.org/docs/
- **DuckDB Documentation**: https://duckdb.org/docs/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Documentation**: https://plotly.com/python/

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 coding standards
- Add docstrings to all functions
- Update verification scripts for new features
- Include screenshots for UI changes

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Project Maintainer**: Arkan Tsabit
- **Email**: aarkantsabit@gmail.com
- **GitHub**: https://github.com/ArkanTsabit123/uber-data-pipeline

---

## Acknowledgments

- **Apache Airflow** for industry-standard orchestration
- **DuckDB** for lightweight OLAP database
- **Streamlit** for making data apps accessible
- **Plotly** for interactive visualizations

---

## Changelog

### v2.0.0 (2026-07-10)

- Migration: Mage AI to Apache Airflow
- Added: Docker Compose setup
- Added: DAG-based orchestration
- Updated: All documentation for Airflow
- Maintained: 6-phase verification system

### v1.0.0 (2026-07-08)

- Initial release with Mage AI
- Star schema in DuckDB
- Streamlit dashboard
- 115+ verification checks

---

## Star History

If you find this project useful, please give it a star on GitHub!

---

**Built with industry-standard data engineering tools**
```