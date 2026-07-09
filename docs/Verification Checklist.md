# ✅ Verification Checklist - Uber ETL Pipeline (Apache Airflow)

---

## 📋 Phase 1: Setup & Environment

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1.1 | Python 3.10+ installed | ⬜ | `python --version` |
| 1.2 | Virtual environment created | ⬜ | `python -m venv venv` |
| 1.3 | Virtual environment activated | ⬜ | `venv\Scripts\activate` |
| 1.4 | requirements.txt created | ⬜ | Airflow + DuckDB + Streamlit |
| 1.5 | All dependencies installed | ⬜ | `pip install -r requirements.txt` |
| 1.6 | Folder structure created | ⬜ | data/, warehouse/, dashboard/, dags/, scripts/, screenshots/ |
| 1.7 | Dataset downloaded | ⬜ | data/uber_data.csv (100,000 rows) |
| 1.8 | Docker installed | ⬜ | `docker --version` |
| 1.9 | Docker Compose installed | ⬜ | `docker-compose --version` |
| 1.10 | docker-compose.yml created | ⬜ | Airflow with Docker |
| 1.11 | DAG file created | ⬜ | dags/uber_etl_dag.py |
| 1.12 | Script files created | ⬜ | extract.py, transform.py, load.py |
| 1.13 | Dashboard file created | ⬜ | dashboard/app.py |
| 1.14 | Verification script passed | ⬜ | `python verify-phase-1.py` |

**Phase 1 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 14 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📋 Phase 2: Airflow DAG Creation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 2.1 | Airflow installed | ⬜ | `pip install apache-airflow==2.7.3` |
| 2.2 | Docker running | ⬜ | Docker Desktop must be active |
| 2.3 | Airflow containers running | ⬜ | `docker-compose up -d` |
| 2.4 | Airflow UI accessible | ⬜ | http://localhost:8080 |
| 2.5 | DAG file created | ⬜ | dags/uber_etl_dag.py |
| 2.6 | Extract task created | ⬜ | scripts/extract.py |
| 2.7 | Transform task created | ⬜ | scripts/transform.py |
| 2.8 | Load task created | ⬜ | scripts/load.py |
| 2.9 | DAG visible in UI | ⬜ | Airflow UI → DAGs list |
| 2.10 | DAG triggered successfully | ⬜ | Click "Trigger DAG" |
| 2.11 | All tasks green (success) | ⬜ | Check Grid View |
| 2.12 | Verification script passed | ⬜ | `python verify-phase-2.py` |

**Phase 2 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 12 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📋 Phase 3: Data Transformation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 3.1 | Data loaded successfully | ⬜ | Check DAG logs |
| 3.2 | Data cleaning applied | ⬜ | drop_duplicates, dropna |
| 3.3 | datetime_dim created | ⬜ | 7 columns |
| 3.4 | rate_code_dim created | ⬜ | 3 columns, rate mapping |
| 3.5 | location_dim created | ⬜ | 3 columns |
| 3.6 | fact_table created | ⬜ | 11 columns |
| 3.7 | All dimension tables populated | ⬜ | Check row counts |
| 3.8 | Fact table populated | ⬜ | Check row counts |
| 3.9 | Transform task successful | ⬜ | Check DAG logs |
| 3.10 | Verification script passed | ⬜ | `python verify-phase-3.py` |

**Phase 3 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 10 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📋 Phase 4: Data Loading to DuckDB

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | DuckDB connection established | ⬜ | `duckdb.connect()` |
| 4.2 | datetime_dim table created | ⬜ | warehouse/uber.duckdb |
| 4.3 | rate_code_dim table created | ⬜ | warehouse/uber.duckdb |
| 4.4 | location_dim table created | ⬜ | warehouse/uber.duckdb |
| 4.5 | fact_table table created | ⬜ | warehouse/uber.duckdb |
| 4.6 | Data inserted successfully | ⬜ | Check row counts |
| 4.7 | trip_analytics view created | ⬜ | For dashboard |
| 4.8 | DuckDB file exists | ⬜ | warehouse/uber.duckdb |
| 4.9 | Tables verified with SQL query | ⬜ | `SHOW TABLES` |
| 4.10 | Verification script passed | ⬜ | `python verify-phase-4.py` |

**Phase 4 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 10 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📋 Phase 5: Dashboard Development

| # | Task | Status | Notes |
|---|------|--------|-------|
| 5.1 | dashboard/app.py created | ⬜ | File exists |
| 5.2 | Imports added | ⬜ | streamlit, duckdb, pandas, plotly |
| 5.3 | Database connection | ⬜ | `@st.cache_resource` |
| 5.4 | Data loading | ⬜ | `@st.cache_data` |
| 5.5 | Title and header | ⬜ | `st.title()` |
| 5.6 | Sidebar filters | ⬜ | Year, Month, Weekday |
| 5.7 | KPI Cards | ⬜ | Total Trips, Revenue, Avg Distance, Avg Fare |
| 5.8 | Line Chart | ⬜ | Revenue by Hour |
| 5.9 | Bar Chart | ⬜ | Trips by Weekday |
| 5.10 | Pie Chart | ⬜ | Rate Code Distribution |
| 5.11 | Scatter Plot | ⬜ | Distance vs Fare |
| 5.12 | Data table | ⬜ | `st.dataframe()` |
| 5.13 | Download button | ⬜ | CSV export |
| 5.14 | Dashboard running | ⬜ | `streamlit run dashboard/app.py` |
| 5.15 | Dashboard accessible | ⬜ | http://localhost:8501 |
| 5.16 | Verification script passed | ⬜ | `python verify-phase-5.py` |

**Phase 5 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 16 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📋 Phase 6: Deployment & Documentation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1 | README.md complete | ⬜ | Full documentation |
| 6.2 | LICENSE added | ⬜ | MIT License |
| 6.3 | .gitignore configured | ⬜ | Python + Airflow + Docker |
| 6.4 | docker-compose.yml created | ⬜ | Airflow with Docker |
| 6.5 | Screenshot 01: GitHub repo | ⬜ | 01-github-repo-created.png |
| 6.6 | Screenshot 02: Terminal setup | ⬜ | 02-terminal-setup.png |
| 6.7 | Screenshot 03: Folder structure | ⬜ | 03-folder-structure.png |
| 6.8 | Screenshot 04: Dataset downloaded | ⬜ | 04-dataset-downloaded.png |
| 6.9 | Screenshot 05: Phase 1 verification | ⬜ | 05-verify-phase1-success.png |
| 6.10 | Screenshot 06-09: Phase 2 (Airflow) | ⬜ | Airflow UI, DAG list, Graph view, Success, Verification |
| 6.11 | Screenshot 10-12: Phase 3 | ⬜ | Transform, logs, verification |
| 6.12 | Screenshot 13-16: Phase 4 | ⬜ | DuckDB tables, data, verification |
| 6.13 | Screenshot 17-23: Phase 5 | ⬜ | Dashboard code, overview, filters, charts, KPI, filtered view, verification |
| 6.14 | Screenshot 24-30: Phase 6 | ⬜ | README, screenshots folder, git commit, git push, GitHub final, README rendered |
| 6.15 | Git initialized | ⬜ | `git init` |
| 6.16 | Git commit | ⬜ | `git commit -m "..."` |
| 6.17 | GitHub repository created | ⬜ | Public repo |
| 6.18 | Remote origin set | ⬜ | `git remote add origin` |
| 6.19 | Push to GitHub | ⬜ | `git push -u origin main` |
| 6.20 | Repository verified | ⬜ | Check GitHub |
| 6.21 | README rendered properly | ⬜ | Check on GitHub |
| 6.22 | Verification script passed | ⬜ | `python verify-phase-6.py` |

**Phase 6 Status:** ⬜ Pending / 🔄 In Progress / ✅ Complete

**Checks:** 22 | **Passed:** ___ | **Failed:** ___ | **Success Rate:** ___%

---

## 📊 Overall Summary

| Phase | Total Checks | Passed | Failed | Pending | Status |
|-------|--------------|--------|--------|---------|--------|
| Phase 1 | 14 | ___ | ___ | ___ | ⬜ |
| Phase 2 | 12 | ___ | ___ | ___ | ⬜ |
| Phase 3 | 10 | ___ | ___ | ___ | ⬜ |
| Phase 4 | 10 | ___ | ___ | ___ | ⬜ |
| Phase 5 | 16 | ___ | ___ | ___ | ⬜ |
| Phase 6 | 22 | ___ | ___ | ___ | ⬜ |
| **TOTAL** | **84** | **___** | **___** | **___** | **___% Complete** |

---

## 📋 Screenshots Status

| Phase | Total | Taken | Pending |
|-------|-------|-------|---------|
| Phase 0 | 2 | ___ | ___ |
| Phase 1 | 3 | ___ | ___ |
| Phase 2 | 4 | ___ | ___ |
| Phase 3 | 3 | ___ | ___ |
| Phase 4 | 4 | ___ | ___ |
| Phase 5 | 7 | ___ | ___ |
| Phase 6 | 7 | ___ | ___ |
| **TOTAL** | **30** | **___** | **___** |

---

## 🎯 Current Status

| Item | Status | Progress | Keterangan |
|------|--------|----------|------------|
| Phase 1 | ⬜ | 0% | Setup & Environment |
| Phase 2 | ⬜ | 0% | Airflow DAG Creation |
| Phase 3 | ⬜ | 0% | Data Transformation |
| Phase 4 | ⬜ | 0% | Load to DuckDB |
| Phase 5 | ⬜ | 0% | Dashboard Development |
| Phase 6 | ⬜ | 0% | Deployment & Documentation |

---

## 🚀 Next Steps

### **Immediate (Phase 1):**
1. Create virtual environment: `python -m venv venv`
2. Activate venv: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Download dataset to `data/uber_data.csv`
5. Run verification: `python verify-phase-1.py`

### **After Phase 1:**
1. **Phase 2**: Start Airflow with Docker → Create DAG
2. **Phase 3**: Run transform → Build Star Schema
3. **Phase 4**: Load data to DuckDB
4. **Phase 5**: Run Streamlit dashboard
5. **Phase 6**: Take screenshots → Finalize documentation

---

## 📝 Quick Commands

```bash
# Start Airflow
docker-compose up -d

# Trigger DAG
airflow dags trigger uber_etl_pipeline

# Run dashboard
streamlit run dashboard/app.py

# Verify current phase
python verify-phase-1.py
```

---

## 📌 Notes

- ✅ = Complete / Passed
- ⬜ = Pending / Not yet started
- 📌 = Important note
- 🔄 = In Progress

---

**Updated: 2026-07-10** 🚀