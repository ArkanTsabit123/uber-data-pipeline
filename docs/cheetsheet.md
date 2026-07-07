# 📚 Uber ETL Pipeline - Cheat Sheet

## 🚀 Quick Commands

### Virtual Environment
```bash
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

### Package Management
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install mage-ai==0.9.70
pip install duckdb==0.9.2
pip install pandas==2.1.4
pip install streamlit==1.29.0
pip install plotly==5.18.0

# List installed packages
pip list

# Uninstall package
pip uninstall package_name

# Check package version
pip show package_name
```

### Git Commands
```bash
# Initialize git
git init

# Check status
git status

# Add all files
git add .

# Add specific file
git add filename.py

# Commit with message
git commit -m "your message"

# Add remote
git remote add origin https://github.com/username/repo.git

# Check remote
git remote -v

# Push to GitHub
git push -u origin main

# Force push (if needed)
git push -u origin main --force

# Pull latest changes
git pull origin main

# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Create branch
git checkout -b feature-branch

# Switch branch
git checkout main

# Merge branch
git merge feature-branch
```

---

## 🏗️ Project Structure Commands

### Create Folders
```bash
# Windows
mkdir data warehouse dashboard screenshots mage_project
mkdir mage_project\pipelines
mkdir mage_project\pipelines\uber_etl_pipeline
mkdir mage_project\pipelines\uber_etl_pipeline\blocks

# Mac/Linux
mkdir -p data warehouse dashboard screenshots mage_project
mkdir -p mage_project/pipelines/uber_etl_pipeline/blocks
```

### Create Files
```bash
# Windows
type nul > data\.gitkeep
type nul > warehouse\.gitkeep
type nul > screenshots\.gitkeep

# Mac/Linux
touch data/.gitkeep
touch warehouse/.gitkeep
touch screenshots/.gitkeep
```

### Project Structure
```
uber-data-pipeline/
├── 📁 data/                 # Raw dataset
├── 📁 warehouse/            # DuckDB database
├── 📁 dashboard/            # Streamlit app
│   └── app.py
├── 📁 screenshots/          # Documentation screenshots
├── 📁 mage_project/         # Mage AI project
│   └── pipelines/
│       └── uber_etl_pipeline/
│           └── blocks/
│               ├── load_data.py
│               ├── create_star_schema.py
│               └── load_to_duckdb.py
├── 📄 verify-phase-1.py
├── 📄 verify-phase-2.py
├── 📄 verify-phase-3.py
├── 📄 verify-phase-4.py
├── 📄 verify-phase-5.py
├── 📄 verify-phase-6.py
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 LICENSE
└── 📄 README.md
```

---

## 🐍 Python Commands

### Verify Installation
```bash
# Check Python version
python --version

# Check pip version
pip --version

# Test imports
python -c "import mage_ai; print('✅ Mage AI OK')"
python -c "import duckdb; print('✅ DuckDB OK')"
python -c "import pandas; print('✅ Pandas OK')"
python -c "import streamlit; print('✅ Streamlit OK')"
python -c "import plotly; print('✅ Plotly OK')"
```

### Run Verification Scripts
```bash
# Phase 1: Setup
python verify-phase-1.py

# Phase 2: Extract
python verify-phase-2.py

# Phase 3: Transform
python verify-phase-3.py

# Phase 4: Load
python verify-phase-4.py

# Phase 5: Dashboard
python verify-phase-5.py

# Phase 6: Deployment
python verify-phase-6.py

# Run all verifications (Windows)
for %i in (1 2 3 4 5 6) do python verify-phase-%i.py

# Run all verifications (Mac/Linux)
for i in {1..6}; do python verify-phase-$i.py; done
```

---

## 🚀 Running the Pipeline

### Start Mage AI
```bash
# Start Mage
mage start mage_project

# Stop Mage (Ctrl+C in terminal)

# Access Mage UI
# http://localhost:6789
```

### Run Streamlit Dashboard
```bash
# Run dashboard
streamlit run dashboard/app.py

# Run with specific port
streamlit run dashboard/app.py --server.port 8501

# Access dashboard
# http://localhost:8501
```

---

## 🗄️ DuckDB Commands

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

## 📊 Star Schema Tables

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
fare_amount
total_amount
passenger_count
payment_type
```

---

## 🔧 Troubleshooting

### Common Errors & Solutions

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install package_name` |
| `'mage' not recognized` | Activate venv: `venv\Scripts\activate` |
| `Permission denied` | Run as admin or use `--user` flag |
| `Dependency conflict` | Use `--use-deprecated=legacy-resolver` |
| `Port already in use` | Change port or kill process |
| `UnicodeEncodeError` | Use `encoding='utf-8'` in open() |
| `venv not found` | `python -m venv venv` |
| `git push rejected` | `git pull origin main --allow-unrelated-histories` |

### Windows-Specific Issues
```bash
# PowerShell doesn't support &&
# Use ; instead
git pull; git push

# Or run separately
git pull
git push
```

---

## 📝 Requirements.txt Quick Reference

### Minimal Requirements
```txt
mage-ai==0.9.70
duckdb==0.9.2
pandas==2.1.4
streamlit==1.29.0
plotly==5.18.0
```

### Full Requirements
```txt
mage-ai==0.9.70
duckdb==0.9.2
pandas==2.1.4
numpy==1.24.3
streamlit==1.29.0
plotly==5.18.0
python-dotenv==1.0.0
pydantic==2.5.0
openpyxl==3.1.2
xlrd==2.0.1
pyarrow==14.0.1
matplotlib==3.8.2
seaborn==0.13.1
pytest==7.4.3
```

---

## 📋 Verification Summary

| Phase | Script | Checks | Status |
|-------|--------|--------|--------|
| 1 | `verify-phase-1.py` | 14 | Setup & Environment |
| 2 | `verify-phase-2.py` | 12 | Data Loading (Extract) |
| 3 | `verify-phase-3.py` | 32 | Transform (Star Schema) |
| 4 | `verify-phase-4.py` | 15 | Load to DuckDB |
| 5 | `verify-phase-5.py` | 23 | Dashboard |
| 6 | `verify-phase-6.py` | 19 | Deployment |
| **Total** | | **115** | **All Phases** |

---

## 🌐 Important URLs

| Service | URL |
|---------|-----|
| Mage AI | http://localhost:6789 |
| Streamlit Dashboard | http://localhost:8501 |
| GitHub Repository | https://github.com/ArkanTsabit123/uber-data-pipeline |

---

## 📚 Documentation Links

| Resource | URL |
|----------|-----|
| Mage AI Docs | https://docs.mage.ai/ |
| DuckDB Docs | https://duckdb.org/docs/ |
| Streamlit Docs | https://docs.streamlit.io/ |
| Plotly Docs | https://plotly.com/python/ |
| Pandas Docs | https://pandas.pydata.org/docs/ |

---

## 💡 Quick Tips

1. **Always activate venv** before working
2. **Run verification scripts** after each phase
3. **Commit often** with meaningful messages
4. **Use VS Code** for better development experience
5. **Check logs** for debugging
6. **Keep screenshots** for documentation

---

**📌 Save this cheat sheet for quick reference!** 🚀