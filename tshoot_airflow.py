# tshoot_airflow.py
"""
Troubleshooting script for Uber ETL Pipeline.

Helps diagnose common issues with:
    - Airflow installation and containers
    - DuckDB connection and data
    - Docker status
    - DAG and script files
"""

import subprocess
import sys
import urllib.request
from pathlib import Path


def run_command(cmd: str) -> bool:
    """Run shell command and print output."""
    print(f"\nRunning: {cmd}")
    print("-" * 50)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"Error: {result.stderr}")
    return result.returncode == 0


def check_python() -> None:
    """Check Python version."""
    print("\n1. Python Version:")
    run_command("python --version")


def check_venv() -> None:
    """Check virtual environment."""
    print("\n2. Virtual Environment:")
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f"Virtual environment active: {sys.prefix}")
    else:
        print("Virtual environment NOT active. Run: venv\\Scripts\\activate")


def check_packages() -> None:
    """Check required packages."""
    print("\n3. Required Packages:")
    packages = ['apache-airflow', 'duckdb', 'pandas', 'streamlit', 'plotly']
    for pkg in packages:
        try:
            __import__(pkg.replace('-', '_'))
            print(f"{pkg} - installed")
        except ImportError:
            print(f"{pkg} - NOT installed")
            print(f"   Run: pip install {pkg}")


def check_docker() -> None:
    """Check Docker status."""
    print("\n4. Docker Status:")
    success = run_command("docker ps")
    if success:
        print("Docker is running")
    else:
        print("Docker is NOT running")
        print("   Start Docker Desktop first")


def check_airflow_containers() -> None:
    """Check Airflow containers."""
    print("\n5. Airflow Containers:")
    containers = ['airflow-webserver', 'airflow-scheduler', 'postgres', 'redis']

    result = subprocess.run(
        ['docker', 'ps', '--format', '{{.Names}}'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        running = result.stdout.strip().split('\n')
        for container in containers:
            if any(container in name for name in running):
                print(f"{container} - running")
            else:
                print(f"{container} - NOT running")
                print(f"   Run: docker-compose up -d")
    else:
        print("Cannot check containers")
        print("   Run: docker-compose up -d")


def check_duckdb_file() -> None:
    """Check DuckDB database."""
    print("\n6. DuckDB Database:")
    db_path = Path('warehouse/uber.duckdb')

    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"Database exists: {size_mb:.2f} MB")

        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            tables = conn.execute("SHOW TABLES").fetchall()
            conn.close()

            if tables:
                print(f"Tables found: {len(tables)}")
                for table in tables:
                    print(f"   {table[0]}")
            else:
                print("No tables found. Run pipeline first.")
        except Exception as e:
            print(f"Cannot connect: {e}")
    else:
        print("Database NOT found")
        print("   Run pipeline first")


def check_duckdb_in_container() -> None:
    """Check DuckDB in container."""
    print("\n7. DuckDB in Airflow Container:")

    try:
        result = subprocess.run(
            'docker-compose exec airflow-scheduler python -c "import duckdb; print(\\"DuckDB imported\\")"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("DuckDB is available in container")
        else:
            print("DuckDB NOT available in container")
            print("   Run: docker-compose exec airflow-scheduler pip install --user duckdb")
    except Exception:
        print("Cannot check DuckDB in container")
        print("   Make sure Airflow is running")


def check_dag_files() -> None:
    """Check DAG files."""
    print("\n8. DAG Files:")

    dags_dir = Path('dags')
    if dags_dir.exists():
        dag_files = list(dags_dir.glob('*.py'))
        if dag_files:
            for f in dag_files:
                print(f"{f.name}")
                with open(f, 'r') as file:
                    content = file.read()
                if 'uber_etl_pipeline' in content:
                    print(f"   Contains 'uber_etl_pipeline'")
                else:
                    print(f"   May not be valid DAG")
        else:
            print("No DAG files found")
            print("   Run: python setup_pipeline.py")
    else:
        print("dags/ folder not found")
        print("   Run: python setup_project.py")


def check_script_files() -> None:
    """Check script files."""
    print("\n9. Script Files:")

    scripts = ['extract.py', 'transform.py', 'load.py']
    scripts_dir = Path('scripts')

    if scripts_dir.exists():
        for script in scripts:
            script_path = scripts_dir / script
            if script_path.exists():
                with open(script_path, 'r') as f:
                    content = f.read()
                if 'def' in content:
                    print(f"{script} - has function definition")
                else:
                    print(f"{script} - may be incomplete")
            else:
                print(f"{script} - NOT found")
                print(f"   Run: python setup_pipeline.py")
    else:
        print("scripts/ folder not found")
        print("   Run: python setup_project.py")


def check_airflow_ui() -> None:
    """Check Airflow UI."""
    print("\n10. Airflow UI:")
    try:
        response = urllib.request.urlopen('http://localhost:8080', timeout=3)
        if response.getcode() == 200:
            print("Airflow UI accessible: http://localhost:8080")
        else:
            print(f"Airflow UI returned: {response.getcode()}")
    except Exception:
        print("Airflow UI NOT accessible: http://localhost:8080")
        print("   Run: docker-compose up -d")


def fix_duckdb() -> None:
    """Fix DuckDB installation in container."""
    print("\n11. Fix DuckDB in Container:")
    print("Installing DuckDB in Airflow container...")
    result = subprocess.run(
        'docker-compose exec airflow-scheduler pip install --user duckdb==0.9.2',
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("DuckDB installed successfully!")
    else:
        print("Failed to install DuckDB")
        print("   Try manual: docker-compose exec airflow-scheduler /bin/bash")
        print("      Then: pip install --user duckdb==0.9.2")


def main() -> None:
    """Run all troubleshooting checks."""
    print("=" * 60)
    print("AIRFLOW TROUBLESHOOT")
    print("=" * 60)

    check_python()
    check_venv()
    check_packages()
    check_docker()
    check_airflow_containers()
    check_duckdb_file()
    check_duckdb_in_container()
    check_dag_files()
    check_script_files()
    check_airflow_ui()

    print("\n" + "=" * 60)
    print("Troubleshoot complete!")
    print("=" * 60)
    print("\nIf you still have issues:")
    print("1. Check logs: docker-compose logs -f")
    print("2. Restart: docker-compose restart")
    print("3. Full reset: docker-compose down && docker-compose up -d")


if __name__ == "__main__":
    main()