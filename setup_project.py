# setup_project.py
# Setup project structure and environment

"""
Setup script for Uber ETL Pipeline Project (Apache Airflow Version)
Run: python setup_project.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class ProjectSetup:
    """Setup class for project structure and environment"""
    
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
    
    def create_folders(self):
        """Create required folders"""
        self.print_header("📁 CREATING FOLDER STRUCTURE")
        
        folders = [
            'data',
            'warehouse',
            'dashboard',
            'dags',
            'scripts',
            'screenshots',
            'docs'
        ]
        
        for folder in folders:
            folder_path = self.root / folder
            if folder_path.exists():
                self.print_check(f"Folder '{folder}/' already exists", True)
            else:
                folder_path.mkdir(parents=True)
                self.print_check(f"Folder '{folder}/' created", True)
    
    def create_gitkeep(self):
        """Create .gitkeep files in empty folders"""
        self.print_header("📄 CREATING .GITKEEP FILES")
        
        folders = ['data', 'warehouse', 'screenshots']
        for folder in folders:
            file_path = self.root / folder / '.gitkeep'
            file_path.touch(exist_ok=True)
            self.print_check(f"{folder}/.gitkeep created", True)
    
    def create_requirements(self):
        """Create requirements.txt if not exists"""
        self.print_header("📦 CHECKING REQUIREMENTS")
        
        req_path = self.root / 'requirements.txt'
        if req_path.exists():
            self.print_check("requirements.txt already exists", True)
            return
        
        content = '''# ============================================
# UBER ETL PIPELINE - REQUIREMENTS
# Apache Airflow Version - Python 3.10+
# ============================================

# Orchestration
apache-airflow==2.7.3

# Airflow Providers
apache-airflow-providers-postgres==5.10.0
apache-airflow-providers-docker==3.8.0

# Core Dependencies
duckdb==0.9.2
pandas==2.1.4
numpy==1.24.3
streamlit==1.29.0
plotly==5.18.0

# Utilities
python-dotenv==1.0.0
pydantic==2.5.0
openpyxl==3.1.2
xlrd==2.0.1

# Data Processing
pyarrow==18.1.0
dask==2023.5.0
fastparquet==2023.10.1

# Visualization
matplotlib==3.8.2
seaborn==0.13.1

# Database
SQLAlchemy==2.0.23
psycopg2-binary==2.9.9

# Development
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.1
flake8==7.0.0
isort==5.13.2

# Docker Support
docker==6.1.3
'''
        
        with open(req_path, 'w') as f:
            f.write(content)
        self.print_check("requirements.txt created", True)
    
    def create_gitignore(self):
        """Create .gitignore if not exists"""
        self.print_header("📄 CHECKING .GITIGNORE")
        
        gitignore_path = self.root / '.gitignore'
        if gitignore_path.exists():
            self.print_check(".gitignore already exists", True)
            return
        
        content = '''# Virtual Environment
venv/
env/
ENV/
.env
.venv/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
*.whl

# Airflow
airflow.db
airflow.cfg
webserver_config.py
logs/
plugins/
*.pid

# Docker
.docker/
docker-compose.override.yml

# DuckDB
warehouse/*.duckdb
warehouse/*.db
warehouse/*.log

# Data Files
data/*.csv
!data/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# OS
Thumbs.db
desktop.ini

# Logs
logs/
*.log

# Streamlit
.streamlit/
.streamlit/config.toml

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Testing
.pytest_cache/
.coverage
htmlcov/

# Backup Files
*.bak
*.tmp

# Temporary files
/tmp/
*.tmp
'''
        
        with open(gitignore_path, 'w') as f:
            f.write(content)
        self.print_check(".gitignore created", True)
    
    def create_docker_compose(self):
        """Create docker-compose.yml if not exists"""
        self.print_header("🐳 CHECKING DOCKER COMPOSE")
        
        compose_path = self.root / 'docker-compose.yml'
        if compose_path.exists():
            self.print_check("docker-compose.yml already exists", True)
            return
        
        content = '''services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  airflow-webserver:
    image: apache/airflow:2.7.3
    depends_on:
      - postgres
      - redis
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
      AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
      AIRFLOW__WEBSERVER__SECRET_KEY: secret
      _AIRFLOW_WWW_USER_CREATE: "true"
      _AIRFLOW_WWW_USER_USERNAME: admin
      _AIRFLOW_WWW_USER_PASSWORD: admin
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./data:/opt/airflow/data
      - ./warehouse:/opt/airflow/warehouse
    ports:
      - "8080:8080"
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.7.3
    depends_on:
      - postgres
      - redis
    environment:
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CELERY__BROKER_URL: redis://redis:6379/0
      AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./scripts:/opt/airflow/scripts
      - ./data:/opt/airflow/data
      - ./warehouse:/opt/airflow/warehouse
    command: scheduler

volumes:
  postgres_data:
'''
        
        with open(compose_path, 'w') as f:
            f.write(content)
        self.print_check("docker-compose.yml created", True)
    
    def create_license(self):
        """Create LICENSE if not exists"""
        self.print_header("📄 CHECKING LICENSE")
        
        license_path = self.root / 'LICENSE'
        if license_path.exists():
            self.print_check("LICENSE already exists", True)
            return
        
        content = '''MIT License

Copyright (c) 2026 Arkan Tsabit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
        
        with open(license_path, 'w') as f:
            f.write(content)
        self.print_check("LICENSE created", True)
    
    def verify_venv(self):
        """Check if virtual environment is active"""
        self.print_header("🔧 VIRTUAL ENVIRONMENT")
        
        in_venv = sys.prefix != sys.base_prefix
        if in_venv:
            self.print_check("Virtual environment active", True, sys.prefix)
        else:
            self.print_check("Virtual environment NOT active", False, "Run: venv\\Scripts\\activate")
        
        venv_path = self.root / 'venv'
        if venv_path.exists():
            self.print_check("venv folder exists", True)
        else:
            self.print_check("venv folder NOT found", False, "Run: python -m venv venv")
    
    def run_all(self):
        """Run all setup steps"""
        self.print_header("🚀 UBER ETL PIPELINE - PROJECT SETUP")
        
        print(f"📂 Project Root: {self.root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        self.create_folders()
        self.create_gitkeep()
        self.create_requirements()
        self.create_gitignore()
        self.create_docker_compose()
        self.create_license()
        self.verify_venv()
        
        self.print_header("✅ SETUP COMPLETE!")
        print("\n📋 Next Steps:")
        print("  1. Activate venv: venv\\Scripts\\activate")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Start Docker Desktop")
        print("  4. Start Airflow: docker-compose up -d")
        print("  5. Open Airflow UI: http://localhost:8080")
        print("  6. Trigger DAG: uber_etl_pipeline")


if __name__ == "__main__":
    setup = ProjectSetup()
    setup.run_all()