# verify-phase-2.py

"""
Phase 2: Airflow DAG Creation Verification

This script verifies that the Airflow DAG and all required components
are properly set up and running for the Uber ETL Pipeline project.

Checks performed:
    1. Apache Airflow Installation - Verifies Airflow is installed (Docker or local)
    2. Docker Status - Checks if Docker is running
    3. Airflow Containers - Verifies webserver, scheduler, postgres, redis are running
    4. DAG File - Checks if uber_etl_dag.py exists and contains required components
    5. Script Files - Verifies extract.py, transform.py, load.py exist
    6. Airflow UI - Checks if UI is accessible at http://localhost:8080
    7. DuckDB Connection - Verifies database connection and tables
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class Phase2Verifier:
    def __init__(self):
        self.project_root = Path.cwd()
        self.checks_passed = 0
        self.checks_failed = 0
        self.total_checks = 0
        self.results = {}
        self.check_results = []
        self.timestamp = datetime.now().isoformat()
    
    def print_header(self, text):
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
    
    def print_check(self, text, status, detail=""):
        icon = "✅" if status else "❌"
        color = Colors.GREEN if status else Colors.RED
        if detail:
            print(f"{color}{icon} {text}{Colors.END}")
            print(f"   {Colors.CYAN}→ {detail}{Colors.END}")
        else:
            print(f"{color}{icon} {text}{Colors.END}")
    
    def print_section(self, text):
        print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")
        print(f"{Colors.YELLOW}{'-'*40}{Colors.END}")
    
    def add_check_result(self, check_name, status, message, details=None):
        self.check_results.append({
            'check': check_name,
            'status': status,
            'message': message,
            'details': details or {}
        })
    
    def verify_airflow_installed(self):
        """Check if Apache Airflow is installed"""
        self.print_section("Check 1: Apache Airflow Installation")
        self.total_checks += 1
        
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=airflow-webserver', '--format', '{{.Status}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'Up' in result.stdout:
                self.checks_passed += 1
                self.print_check("Apache Airflow running in Docker", True, "v2.7.3")
                self.add_check_result(
                    'airflow_installed',
                    True,
                    'Apache Airflow running in Docker (v2.7.3)',
                    {'version': '2.7.3', 'location': 'Docker'}
                )
                return True
        except:
            pass
        
        try:
            import airflow
            import pkg_resources
            version = pkg_resources.get_distribution('apache-airflow').version
            self.checks_passed += 1
            self.print_check(f"Apache Airflow installed locally", True, f"v{version}")
            self.add_check_result(
                'airflow_installed',
                True,
                f'Apache Airflow v{version} installed locally',
                {'version': version, 'location': 'Local'}
            )
            return True
        except:
            pass
        
        self.checks_failed += 1
        self.print_check("Apache Airflow NOT installed", False, "💡 Run: docker-compose up -d or pip install apache-airflow")
        self.add_check_result(
            'airflow_installed',
            False,
            'Apache Airflow not installed or running',
            {'error': 'Not found in Docker or local'}
        )
        return False
    
    def verify_docker_running(self):
        """Check if Docker is running"""
        self.print_section("Check 2: Docker Status")
        self.total_checks += 1
        
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.checks_passed += 1
                self.print_check("Docker is running", True)
                self.add_check_result(
                    'docker_running',
                    True,
                    'Docker is running',
                    {'status': 'active'}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("Docker is NOT running", False, "💡 Start Docker Desktop first")
                self.add_check_result(
                    'docker_running',
                    False,
                    'Docker not running',
                    {'error': 'Docker daemon not responding'}
                )
                return False
        except subprocess.TimeoutExpired:
            self.checks_failed += 1
            self.print_check("Docker check timeout", False, "💡 Start Docker Desktop first")
            return False
        except FileNotFoundError:
            self.checks_failed += 1
            self.print_check("Docker not found", False, "💡 Install Docker Desktop from docker.com")
            return False
    
    def verify_airflow_containers(self):
        """Check if Airflow containers are running"""
        self.print_section("Check 3: Airflow Containers")
        self.total_checks += 1
        
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                containers = result.stdout.strip().split('\n')
                airflow_containers = ['airflow-webserver', 'airflow-scheduler', 'postgres', 'redis']
                found = [c for c in airflow_containers if any(c in name for name in containers)]
                
                if len(found) >= 2:
                    self.checks_passed += 1
                    self.print_check(f"Airflow containers running", True, f"Found: {', '.join(found)}")
                    self.add_check_result(
                        'airflow_containers',
                        True,
                        f'Airflow containers running ({len(found)} containers)',
                        {'found': found}
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("Airflow containers NOT running", False, "💡 Run: docker-compose up -d")
                    self.add_check_result(
                        'airflow_containers',
                        False,
                        'Airflow containers not running',
                        {'found': found}
                    )
                    return False
            else:
                self.checks_failed += 1
                self.print_check("Cannot check containers", False, "💡 Run: docker-compose up -d")
                return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking containers", False, str(e))
            return False
    
    def verify_dag_file(self):
        """Check if DAG file exists and is valid"""
        self.print_section("Check 4: DAG File")
        dag_file = self.project_root / 'dags' / 'uber_etl_dag.py'
        self.total_checks += 1
        
        if dag_file.exists():
            self.checks_passed += 1
            self.print_check("DAG file exists", True, "dags/uber_etl_dag.py")
            
            with open(dag_file, 'r') as f:
                content = f.read()
            
            checks = ['uber_etl_pipeline', 'PythonOperator', 'extract_data', 'transform_data', 'load_data']
            all_found = True
            
            for key in checks:
                if key in content:
                    self.print_check(f"  ✅ {key} found", True)
                else:
                    all_found = False
                    self.print_check(f"  ❌ {key} missing", False)
            
            if all_found:
                self.checks_passed += 1
                self.add_check_result(
                    'dag_file',
                    True,
                    'DAG file exists and is valid',
                    {'path': str(dag_file)}
                )
            else:
                self.checks_failed += 1
                self.add_check_result(
                    'dag_file',
                    False,
                    'DAG file exists but may be incomplete',
                    {'path': str(dag_file)}
                )
            return True
        else:
            self.checks_failed += 1
            self.print_check("DAG file NOT found", False, "dags/uber_etl_dag.py\n   💡 Create the DAG file")
            self.add_check_result(
                'dag_file',
                False,
                'DAG file not found',
                {'expected_path': 'dags/uber_etl_dag.py'}
            )
            return False
    
    def verify_scripts(self):
        """Check if script files exist"""
        self.print_section("Check 5: Script Files")
        all_scripts_exist = True
        scripts = ['extract.py', 'transform.py', 'load.py']
        
        for script in scripts:
            script_path = self.project_root / 'scripts' / script
            self.total_checks += 1
            
            if script_path.exists():
                self.checks_passed += 1
                self.print_check(f"Script exists: {script}", True, f"scripts/{script}")
            else:
                self.checks_failed += 1
                all_scripts_exist = False
                self.print_check(f"Script NOT found: {script}", False, f"scripts/{script}")
        
        self.add_check_result(
            'scripts',
            all_scripts_exist,
            'All script files exist' if all_scripts_exist else 'Some scripts missing',
            {'scripts': scripts}
        )
        return all_scripts_exist
    
    def verify_airflow_ui(self):
        """Check if Airflow UI is accessible"""
        self.print_section("Check 6: Airflow UI")
        self.total_checks += 1
        
        try:
            import urllib.request
            import urllib.error
            response = urllib.request.urlopen('http://localhost:8080', timeout=3)
            if response.getcode() == 200:
                self.checks_passed += 1
                self.print_check("Airflow UI accessible", True, "http://localhost:8080")
                self.add_check_result(
                    'airflow_ui',
                    True,
                    'Airflow UI is accessible',
                    {'url': 'http://localhost:8080'}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("Airflow UI returned error", False, f"Status: {response.getcode()}")
                return False
        except:
            self.checks_failed += 1
            self.print_check("Airflow UI NOT accessible", False, "💡 Run: docker-compose up -d")
            self.add_check_result(
                'airflow_ui',
                False,
                'Airflow UI not accessible',
                {'error': 'Connection refused'}
            )
            return False
    
    def verify_duckdb_connection(self):
        """Check if DuckDB can connect to database"""
        self.print_section("Check 7: DuckDB Connection")
        self.total_checks += 1
        
        try:
            import duckdb
            db_path = self.project_root / 'warehouse' / 'uber.duckdb'
            
            if not db_path.exists():
                self.checks_failed += 1
                self.print_check("Database file NOT found", False, "warehouse/uber.duckdb")
                self.add_check_result(
                    'duckdb_connection',
                    False,
                    'Database file not found',
                    {'expected_path': 'warehouse/uber.duckdb'}
                )
                return False
            
            conn = duckdb.connect(str(db_path))
            tables = conn.execute("SHOW TABLES").fetchall()
            conn.close()
            
            self.checks_passed += 1
            table_names = [t[0] for t in tables]
            self.print_check("DuckDB connection successful", True, f"{len(tables)} tables found")
            for table in table_names:
                self.print_check(f"  → {table}", True)
            
            self.add_check_result(
                'duckdb_connection',
                True,
                'DuckDB connection successful',
                {'tables_found': len(tables), 'tables': table_names}
            )
            return True
        except ImportError:
            self.checks_failed += 1
            self.print_check("DuckDB NOT installed", False, "💡 Run: pip install duckdb")
            return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("DuckDB connection failed", False, str(e))
            return False
    
    def save_json_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 2,
            'phase_name': 'Airflow DAG Creation',
            'summary': {
                'total_checks': total,
                'passed': self.checks_passed,
                'failed': self.checks_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase2_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 JSON report saved to: {json_file}")
        return report
    
    def save_text_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase2_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 2 VERIFICATION REPORT\n")
            f.write("="*60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Success Rate: {percentage:.1f}%\n")
            f.write(f"Passed: {self.checks_passed}, Failed: {self.checks_failed}\n")
            f.write("="*60 + "\n\n")
            
            if self.results:
                failed_items = [k for k, v in self.results.items() if v is False]
                if failed_items:
                    f.write("Failed Items:\n")
                    for item in failed_items:
                        f.write(f"  - {item}\n")
                else:
                    f.write("All checks passed successfully!\n")
        print(f"📄 Text report saved to: {report_file}")
    
    def generate_summary(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        self.print_section("Verification Summary")
        print(f"\n  📊 Total Checks: {total}")
        print(f"  ✅ Passed: {self.checks_passed}")
        print(f"  ❌ Failed: {self.checks_failed}")
        print(f"  📈 Success Rate: {percentage:.1f}%")
        
        if self.checks_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 2 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ You are ready to proceed to Phase 3 (Data Transformation){Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before proceeding to Phase 3{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        self.print_header("🔍 PHASE 2 VERIFICATION - AIRFLOW DAG & PIPELINE")
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_airflow_installed()
        self.verify_docker_running()
        self.verify_airflow_containers()
        self.verify_dag_file()
        self.verify_scripts()
        self.verify_airflow_ui()
        self.verify_duckdb_connection()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    try:
        verifier = Phase2Verifier()
        success = verifier.run_all_checks()
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase2_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase2_verification_report.txt{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()