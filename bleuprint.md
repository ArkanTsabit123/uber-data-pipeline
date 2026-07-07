# 🚖 Uber ETL Pipeline Project

## 📘 Complete Blueprint

---

## 🎯 Project Overview

### Tujuan
Membangun **end-to-end data pipeline** untuk menganalisis data perjalanan Uber/Taxi NYC menggunakan **stack open-source** yang berjalan sepenuhnya di laptop Anda.

### Output Akhir
1. ✅ **Pipeline data** yang terstruktur dan dapat diaudit
2. ✅ **Star Schema** (tabel fakta + dimensi) di DuckDB
3. ✅ **Dashboard interaktif** dengan Streamlit + Plotly
4. ✅ **6 phase verification** dengan 115+ automated checks

### Business Questions yang Dijawab
- Jam berapa permintaan ride paling tinggi?
- Bagaimana pola revenue berdasarkan hari?
- Rate code apa yang paling sering digunakan?
- Berapa rata-rata jarak dan revenue per trip?

---

## 🏗️ Arsitektur

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       UBER ETL PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │   EXTRACT    │   │  TRANSFORM   │   │    LOAD      │       │
│  │              │   │              │   │              │       │
│  │  Data Loader │──▶│ Transformer  │──▶│ Data Exporter│       │
│  │  (Mage AI)   │   │  (Mage AI)   │   │  (Mage AI)   │       │
│  └──────────────┘   └──────────────┘   └──────────────┘       │
│         │                  │                  │                │
│         ▼                  ▼                  ▼                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │  Raw CSV     │   │ Star Schema  │   │   DuckDB     │       │
│  │  Dataset     │   │  (4 Tables)  │   │  Warehouse   │       │
│  └──────────────┘   └──────────────┘   └──────────────┘       │
│                                                  │             │
│                                                  ▼             │
│                                         ┌──────────────┐       │
│                                         │  Streamlit   │       │
│                                         │  Dashboard   │       │
│                                         └──────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Komponen | Teknologi | Versi | Fungsi |
|----------|-----------|-------|--------|
| **Orchestration** | Mage AI | 0.9.70 | Pipeline orchestrator dengan blok modular |
| **Data Warehouse** | DuckDB | 0.9.2 | In-process OLAP database |
| **Dashboard** | Streamlit | 1.29.0 | Interactive web app |
| **Visualization** | Plotly | 5.18.0 | Interactive charts |
| **Data Processing** | Pandas | 2.1.4 | Data manipulation |
| **Language** | Python | 3.10+ | Primary language |

---

## 🗂️ Project Structure

```
uber-data-pipeline/
│
├── 📁 dashboard/
│   └── app.py                         # Streamlit dashboard
│
├── 📁 data/
│   └── uber_data.csv                  # Raw dataset
│
├── 📁 warehouse/
│   └── uber.duckdb                    # DuckDB database
│
├── 📁 mage_project/
│   ├── metadata.yaml                  # Mage configuration
│   └── pipelines/
│       └── uber_etl_pipeline/
│           ├── pipeline.yaml
│           └── blocks/
│               ├── load_data.py       # Data Loader (Extract)
│               ├── create_star_schema.py  # Transformer
│               └── load_to_duckdb.py      # Data Exporter (Load)
│
├── 📁 screenshots/
│   └── (32+ screenshots)
│
├── 📄 verify-phase-1.py               # Phase 1: Setup
├── 📄 verify-phase-2.py               # Phase 2: Extract
├── 📄 verify-phase-3.py               # Phase 3: Transform
├── 📄 verify-phase-4.py               # Phase 4: Load
├── 📄 verify-phase-5.py               # Phase 5: Dashboard
├── 📄 verify-phase-6.py               # Phase 6: Deploy
│
├── 📄 requirements.txt                # Python dependencies
├── 📄 .gitignore                      # Git ignore
├── 📄 LICENSE                         # MIT License
└── 📄 README.md                       # Documentation
```

---

## 📊 Star Schema Design

### Diagram

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
                                   │ fare_amount                  │ │
                                   │ total_amount                 │ │
                                   └──────────────────────────────┘ │
                              ┌─────────────────────────┐          │
                              │     location_dim        │          │
                              ├─────────────────────────┤          │
                              │ location_id (PK)        │◄─────────┘
                              │ location_name           │
                              │ borough                 │
                              └─────────────────────────┘
```

### Tabel

#### 1. datetime_dim (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| `datetime_id` | INTEGER | Primary Key |
| `pickup_datetime` | TIMESTAMP | Waktu pickup |
| `pick_hour` | INTEGER | Jam (0-23) |
| `pick_day` | INTEGER | Tanggal (1-31) |
| `pick_month` | INTEGER | Bulan (1-12) |
| `pick_year` | INTEGER | Tahun |
| `pick_weekday` | VARCHAR | Nama hari (Monday-Sunday) |

#### 2. rate_code_dim (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| `rate_code_id` | INTEGER | Primary Key |
| `RatecodeID` | INTEGER | Rate code ID from dataset |
| `rate_code_name` | VARCHAR | Name mapping (Standard, JFK, Newark, etc.) |

#### 3. location_dim (Dimension Table)
| Column | Type | Description |
|--------|------|-------------|
| `location_id` | INTEGER | Primary Key |
| `location_name` | VARCHAR | Nama zona |
| `borough` | VARCHAR | Borough (NYC) |

#### 4. fact_table (Fact Table)
| Column | Type | Description |
|--------|------|-------------|
| `trip_id` | INTEGER | Primary Key |
| `datetime_id` | INTEGER | FK → datetime_dim |
| `rate_code_id` | INTEGER | FK → rate_code_dim |
| `pickup_location_id` | INTEGER | FK → location_dim |
| `dropoff_location_id` | INTEGER | FK → location_dim |
| `trip_distance` | FLOAT | Jarak perjalanan (miles) |
| `trip_duration` | FLOAT | Durasi perjalanan (minutes) |
| `fare_amount` | FLOAT | Biaya perjalanan |
| `total_amount` | FLOAT | Total biaya (with tips, tolls, etc.) |
| `passenger_count` | INTEGER | Jumlah penumpang |
| `payment_type_id` | INTEGER | Tipe pembayaran |

---

## 📋 6 Phases Implementasi

### Phase 1: Setup & Environment
**Tujuan:** Menyiapkan fondasi proyek

| # | Task | Detail |
|---|------|--------|
| 1.1 | Folder structure | `data/`, `warehouse/`, `dashboard/`, `mage_project/` |
| 1.2 | Virtual environment | `python -m venv venv` |
| 1.3 | Requirements | `mage-ai`, `duckdb`, `pandas`, `streamlit`, `plotly` |
| 1.4 | Dataset | Download `uber_data.csv` ke `data/` |
| 1.5 | Verification | `python verify-phase-1.py` |

**Verification Checks:** 14 checks

---

### Phase 2: Data Loading (Extract)
**Tujuan:** Load data CSV ke Mage

| # | Task | Detail |
|---|------|--------|
| 2.1 | Start Mage | `mage start mage_project` |
| 2.2 | Create pipeline | `uber_etl_pipeline` (Standard batch) |
| 2.3 | Data Loader block | Name: `load_data` |
| 2.4 | Code validation | `@data_loader`, pandas, `pd.read_csv()`, `return df` |
| 2.5 | Run block | Test execution |
| 2.6 | Verification | `python verify-phase-2.py` |

**Verification Checks:** 12 checks

---

### Phase 3: Data Transformation (Transform)
**Tujuan:** Membangun Star Schema

| # | Task | Detail |
|---|------|--------|
| 3.1 | Transformer block | Name: `create_star_schema` |
| 3.2 | Data cleaning | `drop_duplicates()`, `dropna()`, `reset_index()` |
| 3.3 | Build `datetime_dim` | `datetime_id`, `pick_hour`, `pick_day`, `pick_month`, `pick_year`, `pick_weekday` |
| 3.4 | Build `rate_code_dim` | `rate_code_id`, `RatecodeID`, `rate_code_name` |
| 3.5 | Build `location_dim` | `location_id`, `location_name`, `borough` |
| 3.6 | Build `fact_table` | `trip_id`, `datetime_id`, `rate_code_id`, `pickup_location_id`, `dropoff_location_id`, `trip_distance`, `fare_amount`, `total_amount` |
| 3.7 | Return dictionary | `{'datetime_dim': ..., 'rate_code_dim': ..., 'location_dim': ..., 'fact_table': ...}` |
| 3.8 | Verification | `python verify-phase-3.py` |

**Verification Checks:** 32 checks

---

### Phase 4: Data Loading to DuckDB (Load)
**Tujuan:** Simpan data ke DuckDB

| # | Task | Detail |
|---|------|--------|
| 4.1 | Data Exporter block | Name: `load_to_duckdb` |
| 4.2 | Import DuckDB | `import duckdb` |
| 4.3 | Connect to DB | `duckdb.connect('warehouse/uber.duckdb')` |
| 4.4 | Drop & Create tables | `DROP TABLE IF EXISTS`, `CREATE TABLE` |
| 4.5 | Loop tables | `for table_name, df in data.items()` |
| 4.6 | Create view | `trip_analytics` |
| 4.7 | Run pipeline | All 3 blocks |
| 4.8 | Verification | `python verify-phase-4.py` |

**Verification Checks:** 15 checks

---

### Phase 5: Dashboard Development
**Tujuan:** Visualisasi data interaktif

| # | Task | Detail |
|---|------|--------|
| 5.1 | Create `dashboard/app.py` | Streamlit application |
| 5.2 | Import libraries | `streamlit`, `duckdb`, `pandas`, `plotly` |
| 5.3 | Database connection | `@st.cache_resource` |
| 5.4 | Data loading | `@st.cache_data` |
| 5.5 | KPI Cards | Total Trips, Revenue, Avg Distance, Avg Fare |
| 5.6 | Line Chart | Revenue per Hour |
| 5.7 | Bar Chart | Trips by Weekday |
| 5.8 | Pie Chart | Rate Code Distribution |
| 5.9 | Scatter Plot | Distance vs Fare |
| 5.10 | Sidebar filters | Year, Month, Weekday |
| 5.11 | Data table | `st.dataframe()` |
| 5.12 | Run dashboard | `streamlit run dashboard/app.py` |
| 5.13 | Verification | `python verify-phase-5.py` |

**Verification Checks:** 23 checks

---

### Phase 6: Deployment & Documentation
**Tujuan:** Finalisasi proyek

| # | Task | Detail |
|---|------|--------|
| 6.1 | README.md | Project overview, tech stack, setup, pipeline, dashboard, screenshots |
| 6.2 | Screenshots | 32+ screenshots in `screenshots/` folder |
| 6.3 | Git init | `git init` |
| 6.4 | GitHub repo | Create public repository |
| 6.5 | Push | `git push origin main` |
| 6.6 | Verification | `python verify-phase-6.py` |

**Verification Checks:** 19 checks

---

## ✅ Verification Summary

| Phase | Script | Checks | Focus |
|-------|--------|--------|-------|
| **1** | `verify-phase-1.py` | 14 | Setup & Environment |
| **2** | `verify-phase-2.py` | 12 | Data Loading (Extract) |
| **3** | `verify-phase-3.py` | 32 | Data Transformation (Star Schema) |
| **4** | `verify-phase-4.py` | 15 | Data Loading to DuckDB |
| **5** | `verify-phase-5.py` | 23 | Dashboard Development |
| **6** | `verify-phase-6.py` | 19 | Deployment & Documentation |
| **TOTAL** | | **115** | **All Phases** |

---

## 🚀 Quick Start Commands

```bash
# 1. Clone
git clone https://github.com/yourusername/uber-data-pipeline.git
cd uber-data-pipeline

# 2. Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Start Mage
mage start mage_project

# 4. Create pipeline in Mage UI (http://localhost:6789)
# - Pipeline: uber_etl_pipeline
# - 3 blocks: Data Loader, Transformer, Data Exporter

# 5. Run verifications
python verify-phase-1.py
python verify-phase-2.py
python verify-phase-3.py
python verify-phase-4.py
python verify-phase-5.py
python verify-phase-6.py

# 6. Run dashboard
streamlit run dashboard/app.py

# 7. Push to GitHub
git add .
git commit -m "Complete Uber ETL Pipeline Project"
git push origin main
```

---

## 📸 Screenshots Checklist

| Phase | Screenshot | Description |
|-------|------------|-------------|
| 0 | `01-github-repo-created.png` | GitHub repository created |
| 0 | `02-terminal-setup.png` | Terminal with venv active |
| 1 | `03-folder-structure.png` | Folder structure |
| 1 | `04-dataset-downloaded.png` | Dataset in data/ folder |
| 1 | `05-verify-phase1-success.png` | Phase 1 verification passed |
| 2 | `06-mage-dashboard.png` | Mage UI dashboard |
| 2 | `07-mage-loader-block.png` | Data Loader block |
| 2 | `08-mage-loader-success.png` | Loader block success |
| 2 | `09-verify-phase2-success.png` | Phase 2 verification passed |
| 3 | `10-mage-transformer-block.png` | Transformer block |
| 3 | `11-mage-transformer-success.png` | Transformer block success |
| 3 | `12-verify-phase3-success.png` | Phase 3 verification passed |
| 4 | `13-mage-exporter-block.png` | Data Exporter block |
| 4 | `14-mage-exporter-success.png` | Exporter block success |
| 4 | `15-mage-pipeline-success.png` | Full pipeline success |
| 4 | `16-verify-phase4-success.png` | Phase 4 verification passed |
| 4 | `17-duckdb-tables.png` | DuckDB tables view |
| 4 | `18-duckdb-data.png` | DuckDB sample data |
| 5 | `19-dashboard-code.png` | Dashboard code |
| 5 | `20-dashboard-overview.png` | Dashboard overview |
| 5 | `21-dashboard-filters.png` | Sidebar filters |
| 5 | `22-dashboard-charts.png` | All charts |
| 5 | `23-dashboard-kpi.png` | KPI cards |
| 5 | `24-dashboard-with-filter.png` | Dashboard with filter |
| 5 | `25-verify-phase5-success.png` | Phase 5 verification passed |
| 6 | `26-readme-overview.png` | README.md overview |
| 6 | `27-screenshots-folder.png` | Screenshots folder |
| 6 | `28-verify-phase6-success.png` | Phase 6 verification passed |
| 7 | `29-git-commit.png` | Git commit |
| 7 | `30-git-push.png` | Git push |
| 7 | `31-github-repo-final.png` | Final GitHub repository |
| 7 | `32-readme-rendered.png` | README.md rendered |

---

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt --upgrade` |
| Database connection error | Check if `warehouse/uber.duckdb` exists |
| Mage server won't start | Check if port 6789 is available |
| Dashboard not loading | `pip install streamlit --upgrade` |
| Verification fails | Run setup script first |

---

## 📝 License

This project is licensed under the MIT License.

---