# 📘 UBER ETL PIPELINE - TECHNICAL BLUEPRINT

## Document Information

| Property | Value |
|----------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2026-07-10 |
| **Status** | Production Ready |
| **Orchestration** | Apache Airflow 2.7.3 |
| **Database** | DuckDB 0.9.2 |
| **Dashboard** | Streamlit 1.29.0 |

---

## 🎯 Project Objectives

### Core Goals
1. Build **end-to-end data pipeline** for NYC Uber/Taxi trip data
2. Implement **Star Schema** in DuckDB for analytical queries
3. Create **interactive dashboard** with Streamlit + Plotly
4. Use **industry-standard tools** (Apache Airflow, Docker)
5. Provide **comprehensive verification** across 6 phases

### Success Metrics
- ✅ 52+ automated verification checks
- ✅ 100% data quality validation
- ✅ 32+ documentation screenshots
- ✅ < 5 minutes pipeline execution time (100,000 rows)

---

## 🏗️ System Architecture

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DOCKER CONTAINER ENVIRONMENT                    │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                    APACHE AIRFLOW (2.7.3)                    │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │ │
│  │  │   EXTRACT    │  │  TRANSFORM   │  │    LOAD      │      │ │
│  │  │              │  │              │  │              │      │ │
│  │  │ extract.py   │─▶│ transform.py │─▶│   load.py    │      │ │
│  │  │  (Python)    │  │  (Python)    │  │  (Python)    │      │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │ │
│  │         │                 │                 │                │ │
│  └─────────│─────────────────│─────────────────│────────────────┘ │
│            │                 │                 │                  │
│            ▼                 ▼                 ▼                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Raw CSV     │  │ Star Schema  │  │   DuckDB     │           │
│  │  Dataset     │  │  (4 Tables)  │  │  Warehouse   │           │
│  │  (100K rows) │  │              │  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                      │             │
│                                                      ▼             │
│                                             ┌──────────────┐       │
│                                             │  Streamlit   │       │
│                                             │  Dashboard   │       │
│                                             │  (Port 8501) │       │
│                                             └──────────────┘       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    POSTGRESQL (Metadata DB)                  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| **Orchestration** | Apache Airflow | 2.7.3 | Industry standard, widely adopted |
| **Containerization** | Docker | Latest | Reproducible environment |
| **Metadata DB** | PostgreSQL | 13 | Airflow's recommended backend |
| **Data Warehouse** | DuckDB | 0.9.2 | Lightweight OLAP, embedded |
| **Dashboard** | Streamlit | 1.29.0 | Python-native, rapid development |
| **Visualization** | Plotly | 5.18.0 | Interactive charts, Python-friendly |
| **Data Processing** | Pandas | 2.1.4 | Industry standard for data manipulation |

---

## 📊 Data Model Design

### Star Schema Diagram

```
┌─────────────────────┐          ┌─────────────────────────┐
│    datetime_dim     │          │     rate_code_dim       │
├─────────────────────┤          ├─────────────────────────┤
│ datetime_id (PK)    │◄─────┐   │ rate_code_id (PK)       │◄─────┐
│ pickup_datetime     │      │   │ RatecodeID              │      │
│ pick_hour           │      │   │ rate_code_name          │      │
│ pick_day            │      │   └─────────────────────────┘      │
│ pick_month          │      │                                     │
│ pick_year           │      │                                     │
│ pick_weekday        │      │                                     │
└─────────────────────┘      │                                     │
                              │    ┌──────────────────────────────┐│
                              └────┤        fact_table            ││
                                   ├──────────────────────────────┤│
                                   │ trip_id (PK)                 ││
                                   │ datetime_id (FK)             │─┘
                                   │ rate_code_id (FK)            │─┐
                                   │ pickup_location_id (FK)      │ │
                                   │ dropoff_location_id (FK)     │ │
                                   │ trip_distance                │ │
                                   │ trip_duration                │ │
                                   │ fare_amount                  │ │
                                   │ total_amount                 │ │
                                   │ passenger_count              │ │
                                   │ payment_type_id              │ │
                                   └──────────────────────────────┘ │
                              ┌─────────────────────────┐          │
                              │     location_dim        │          │
                              ├─────────────────────────┤          │
                              │ location_id (PK)        │◄─────────┘
                              │ location_name           │
                              │ borough                 │
                              └─────────────────────────┘
```

### Table Definitions

#### fact_table (Fact Table)
| Column | Type | Nullable | Description | Source |
|--------|------|----------|-------------|--------|
| trip_id | INTEGER | NOT NULL | Surrogate key | Auto-increment |
| datetime_id | INTEGER | NOT NULL | FK to datetime_dim | Join on pickup |
| rate_code_id | INTEGER | NOT NULL | FK to rate_code_dim | RatecodeID |
| pickup_location_id | INTEGER | NOT NULL | FK to location_dim | Coordinates |
| dropoff_location_id | INTEGER | NOT NULL | FK to location_dim | Coordinates |
| trip_distance | FLOAT | NULL | Distance in miles | trip_distance |
| trip_duration | FLOAT | NULL | Duration in minutes | Calculated |
| fare_amount | FLOAT | NULL | Fare amount | fare_amount |
| total_amount | FLOAT | NULL | Total with tips/tolls | total_amount |
| passenger_count | INTEGER | NULL | Number of passengers | passenger_count |
| payment_type_id | INTEGER | NULL | Payment type code | payment_type |

#### datetime_dim (Dimension)
| Column | Type | Description |
|--------|------|-------------|
| datetime_id | INTEGER | Surrogate key |
| pickup_datetime | TIMESTAMP | Original timestamp |
| pick_hour | INTEGER | 0-23 |
| pick_day | INTEGER | 1-31 |
| pick_month | INTEGER | 1-12 |
| pick_year | INTEGER | YYYY |
| pick_weekday | VARCHAR | Monday-Sunday |

#### rate_code_dim (Dimension)
| Column | Type | Description |
|--------|------|-------------|
| rate_code_id | INTEGER | Surrogate key |
| RatecodeID | INTEGER | Source code (1-6) |
| rate_code_name | VARCHAR | Human-readable name |

**Rate Code Mapping:**
| RatecodeID | Name |
|------------|------|
| 1 | Standard |
| 2 | JFK |
| 3 | Newark |
| 4 | Nassau/Westchester |
| 5 | Negotiated |
| 6 | Group Ride |

#### location_dim (Dimension)
| Column | Type | Description |
|--------|------|-------------|
| location_id | INTEGER | Surrogate key |
| location_name | VARCHAR | Display name |
| borough | VARCHAR | NYC borough |

---

## 📁 Project Structure

```
uber-data-pipeline/
│
├── 📁 dags/                              # Airflow DAGs
│   └── uber_etl_dag.py                   # Main DAG definition
│
├── 📁 scripts/                           # Python scripts
│   ├── extract.py                        # Extract data from CSV
│   ├── transform.py                      # Transform to Star Schema
│   └── load.py                           # Load to DuckDB
│
├── 📁 data/                              # Raw data
│   └── uber_data.csv                     # NYC Uber/Taxi dataset
│
├── 📁 warehouse/                         # Data warehouse
│   └── uber.duckdb                       # DuckDB database
│
├── 📁 dashboard/                         # Streamlit dashboard
│   └── app.py                            # Dashboard application
│
├── 📁 screenshots/                       # Documentation
│   └── (32+ screenshots)
│
├── 📄 docker-compose.yml                 # Docker Compose for Airflow
├── 📄 requirements.txt                   # Python dependencies
├── 📄 .gitignore                         # Git ignore file
├── 📄 LICENSE                            # MIT License
├── 📄 README.md                          # Project documentation
├── 📄 blueprint.md                       # This file
│
├── 📄 verify-phase-1.py                  # Phase 1: Setup
├── 📄 verify-phase-2.py                  # Phase 2: DAG Creation
├── 📄 verify-phase-3.py                  # Phase 3: Transform
├── 📄 verify-phase-4.py                  # Phase 4: Load
├── 📄 verify-phase-5.py                  # Phase 5: Dashboard
├── 📄 verify-phase-6.py                  # Phase 6: Deployment
│
├── 📄 setup_project.py                   # Project setup script
├── 📄 setup_pipeline.py                  # Pipeline setup script
└── 📄 structure.py                       # Display project structure
```

---

## 📋 Implementation Details

### DAG Configuration

```python
# dags/uber_etl_dag.py

DAG_ID = 'uber_etl_pipeline'
SCHEDULE_INTERVAL = '@daily'
START_DATE = datetime(2026, 1, 1)
CATCHUP = False
RETRIES = 1
RETRY_DELAY = timedelta(minutes=5)
```

### Task Dependencies

```python
start >> extract_data >> transform_data >> load_data >> end
```

### Docker Configuration

```yaml
# docker-compose.yml

Services:
  - postgres:13        # Metadata database
  - redis:latest       # Celery broker
  - airflow-webserver   # Airflow UI
  - airflow-scheduler   # Task scheduler

Ports:
  - 8080:8080          # Airflow UI
  - 5432:5432          # PostgreSQL
  - 6379:6379          # Redis

Volumes:
  - ./dags:/opt/airflow/dags
  - ./scripts:/opt/airflow/scripts
  - ./data:/opt/airflow/data
  - ./warehouse:/opt/airflow/warehouse
```

---

## ✅ Verification System

### Verification Summary

| Phase | Script | Checks | Focus |
|-------|--------|--------|-------|
| **1** | `verify-phase-1.py` | 20 | Setup & Environment |
| **2** | `verify-phase-2.py` | 9 | Airflow DAG Creation |
| **3** | `verify-phase-3.py` | 6 | Data Transformation |
| **4** | `verify-phase-4.py` | 4 | Data Loading |
| **5** | `verify-phase-5.py` | 6 | Dashboard Development |
| **6** | `verify-phase-6.py` | 7 | Deployment & Documentation |
| **TOTAL** | | **52** | **All Phases** |

### Verification Outputs
- `phaseX_verification.json` - Machine-readable results
- `phaseX_verification_report.txt` - Human-readable summary

---

## 🚀 Deployment Guide

### Prerequisites

| Item | Version | Check Command |
|------|---------|---------------|
| Python | 3.10+ | `python --version` |
| Docker | Latest | `docker --version` |
| Docker Compose | Latest | `docker-compose --version` |
| Git | Latest | `git --version` |

### Deployment Steps

```bash
# 1. Clone repository
git clone https://github.com/ArkanTsabit123/uber-data-pipeline.git
cd uber-data-pipeline

# 2. Setup virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup project structure
python setup_project.py
python setup_pipeline.py

# 5. Start Airflow
docker-compose up -d

# 6. Verify deployment
python verify-phase-1.py

# 7. Open Airflow UI
# http://localhost:8080 (admin/admin)

# 8. Trigger DAG
# Click "Trigger DAG" on uber_etl_pipeline

# 9. Launch Dashboard
streamlit run dashboard/app.py
```

---

## 📊 Performance Specifications

### Data Volume
| Metric | Value |
|--------|-------|
| Input Size | ~15 MB |
| Rows | 100,000 |
| Columns | 19 |
| Database Size | ~10 MB |

### Execution Time
| Task | Time |
|------|------|
| Extract | ~1 second |
| Transform | ~3 seconds |
| Load | ~1 second |
| **Total** | **~5 seconds** |

---

## 🔐 Security Considerations

### Default Credentials (Change for Production)

| Service | Username | Password |
|---------|----------|----------|
| Airflow UI | admin | admin |
| PostgreSQL | airflow | airflow |

### Network Ports
| Port | Service | Exposure |
|------|---------|----------|
| 8080 | Airflow UI | Localhost |
| 5432 | PostgreSQL | Localhost |
| 6379 | Redis | Localhost |
| 8501 | Dashboard | Localhost |

---

## 📝 Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-07-10 | Migrated from Mage AI to Airflow |
| 1.0.0 | 2026-07-08 | Initial release with Mage AI |

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| **Airflow UI** | http://localhost:8080 |
| **Dashboard** | http://localhost:8501 |
| **GitHub** | https://github.com/ArkanTsabit123/uber-data-pipeline |
| **Airflow Docs** | https://airflow.apache.org/docs/ |
| **DuckDB Docs** | https://duckdb.org/docs/ |
| **Streamlit Docs** | https://docs.streamlit.io/ |

---

**Built with ❤️ using industry-standard data engineering tools**