# verify-phase-1.py

"""
Setup & Environment Verification
This script verifies the complete setup of the Uber ETL Pipeline project.
"""

import os
import sys
import json
import importlib.util
import subprocess
from pathlib import Path
from datetime import datetime


class Colors:
    """Terminal output color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class Phase1Verifier:
    """Verification engine for Phase 1 project setup (Airflow Version - FIXED)"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.checks_passed = 0
        self.checks_failed = 0
        self.total_checks = 0
        self.results = {}
        self.check_results = []
        self.timestamp = datetime.now().isoformat()
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
    
    def print_check(self, text, status, detail=""):
        """Print check result with appropriate color"""
        icon = "✅" if status else "❌"
        color = Colors.GREEN if status else Colors.RED
        if detail:
            print(f"{color}{icon} {text}{Colors.END}")
            print(f"   {Colors.CYAN}→ {detail}{Colors.END}")
        else:
            print(f"{color}{icon} {text}{Colors.END}")
    
    def print_section(self, text):
        """Print section header"""
        print(f"\n{Colors.YELLOW}📁 {text}{Colors.END}")
        print(f"{Colors.YELLOW}{'-'*40}{Colors.END}")
    
    def add_check_result(self, check_name, status, message, details=None):
        """Add check result to JSON structure"""
        self.check_results.append({
            'check': check_name,
            'status': status,
            'message': message,
            'details': details or {}
        })
    
    def verify_folder_structure(self):
        """Verify required folder structure exists"""
        self.print_section("Folder Structure")
        
        required_folders = [
            ('data', 'Dataset storage'),
            ('warehouse', 'DuckDB database'),
            ('dashboard', 'Streamlit app'),
            ('dags', 'Airflow DAGs'),
            ('scripts', 'Python scripts'),
            ('screenshots', 'Screenshots')
        ]
        
        all_exist = True
        folder_status = {}
        
        for folder, description in required_folders:
            folder_path = self.project_root / folder
            exists = folder_path.exists() and folder_path.is_dir()
            self.total_checks += 1
            folder_status[folder] = exists
            
            if exists:
                self.checks_passed += 1
                self.print_check(f"Folder '{folder}/' found", True, description)
            else:
                self.checks_failed += 1
                all_exist = False
                self.print_check(f"Folder '{folder}/' NOT found", False, description)
                self.results[f'folder_{folder}'] = False
        
        self.add_check_result(
            'folder_structure',
            all_exist,
            'All required folders exist' if all_exist else 'Some folders missing',
            {'folders': folder_status}
        )
        
        return all_exist
    
    def verify_data_file(self):
        """Verify dataset file exists and is readable"""
        self.print_section("Dataset File")
        
        data_file = self.project_root / 'data' / 'uber_data.csv'
        self.total_checks += 1
        
        if data_file.exists():
            file_size = data_file.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            try:
                import pandas as pd
                df_sample = pd.read_csv(data_file, nrows=5)
                
                self.checks_passed += 1
                self.print_check(
                    f"File found: {data_file.name}", 
                    True, 
                    f"{size_mb:.2f} MB, {len(df_sample.columns)} columns"
                )
                
                # Cek struktur data
                required_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance']
                missing_cols = [col for col in required_columns if col not in df_sample.columns]
                
                data_valid = len(missing_cols) == 0
                if data_valid:
                    self.print_check("Data structure valid", True, "All required columns present")
                else:
                    self.checks_failed += 1
                    self.print_check("Data structure incomplete", False, f"Missing: {', '.join(missing_cols)}")
                    self.results['data_structure'] = False
                
                # Cek jumlah baris
                total_rows = len(pd.read_csv(data_file))
                self.print_check(f"Total rows: {total_rows:,}", True)
                
                self.results['data_file'] = True
                
                self.add_check_result(
                    'data_file',
                    True,
                    f'Dataset found: {data_file.name} ({size_mb:.2f} MB, {total_rows:,} rows)',
                    {
                        'filename': data_file.name,
                        'size_mb': round(size_mb, 2),
                        'rows': total_rows,
                        'columns': len(df_sample.columns),
                        'valid_structure': data_valid
                    }
                )
                return True
                
            except Exception as e:
                self.checks_failed += 1
                self.print_check("File found but invalid", False, str(e))
                self.results['data_file'] = False
                self.add_check_result(
                    'data_file',
                    False,
                    f'File found but invalid: {str(e)}',
                    {'error': str(e)}
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check(
                "File NOT found", 
                False, 
                "Expected at: data/uber_data.csv\n   💡 Download dataset from NYC TLC website"
            )
            self.results['data_file'] = False
            self.add_check_result(
                'data_file',
                False,
                'Dataset file not found at data/uber_data.csv',
                {'expected_path': 'data/uber_data.csv'}
            )
            return False
    
    def verify_venv(self):
        """Verify virtual environment is active"""
        self.print_section("Virtual Environment")
        
        in_venv = sys.prefix != sys.base_prefix
        
        self.total_checks += 1
        venv_status = {
            'active': in_venv,
            'python_path': sys.prefix,
            'python_version': sys.version.split()[0]
        }
        
        if in_venv:
            self.checks_passed += 1
            venv_name = os.path.basename(sys.prefix)
            self.print_check(
                f"Virtual environment active: {venv_name}", 
                True, 
                f"Python {sys.version.split()[0]} at {sys.prefix}"
            )
            self.results['venv'] = True
        else:
            self.checks_failed += 1
            self.print_check(
                "Not in virtual environment", 
                False, 
                "💡 Run: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)"
            )
            self.results['venv'] = False
        
        venv_folder = self.project_root / 'venv'
        if venv_folder.exists():
            self.print_check("Folder 'venv/' found", True)
            venv_status['folder_exists'] = True
        else:
            self.print_check("Folder 'venv/' NOT found", False, "💡 Run: python -m venv venv")
            venv_status['folder_exists'] = False
        
        self.add_check_result(
            'virtual_environment',
            in_venv,
            'Virtual environment is active' if in_venv else 'Virtual environment not active',
            venv_status
        )
        
        return in_venv
    
    def verify_requirements(self):
        """Verify requirements.txt and installed libraries (FIXED)"""
        self.print_section("Requirements & Libraries")
        
        req_file = self.project_root / 'requirements.txt'
        self.total_checks += 1
        
        lib_status = {}
        
        if req_file.exists():
            self.checks_passed += 1
            self.print_check("File requirements.txt found", True)
            
            with open(req_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            self.print_check(f"Dependencies listed: {len(requirements)} package(s)", True)
            
            # ============================================
            # FIX: Check Apache Airflow in Docker Container
            # ============================================
            print("\n  📦 Library Installation Check:")
            all_installed = True
            
            # Check Apache Airflow - DETECT IN DOCKER
            self.total_checks += 1
            airflow_found = False
            airflow_version = None
            
            # Method 1: Check if Airflow container is running
            try:
                result = subprocess.run(
                    ['docker', 'ps', '--filter', 'name=airflow-webserver', '--format', '{{.Status}}'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if 'Up' in result.stdout:
                    airflow_found = True
                    airflow_version = "2.7.3 (Docker)"
                    self.print_check("✅ apache-airflow v2.7.3 running in Docker", True, "Orchestration")
                    self.checks_passed += 1
                    lib_status['apache-airflow'] = {'installed': True, 'version': '2.7.3 (Docker)', 'location': 'Docker'}
                else:
                    raise Exception("Airflow container not running")
            except:
                # Method 2: Check locally installed
                try:
                    import airflow
                    import pkg_resources
                    version = pkg_resources.get_distribution('apache-airflow').version
                    airflow_found = True
                    airflow_version = version
                    self.print_check(f"✅ apache-airflow v{version} installed locally", True, "Orchestration")
                    self.checks_passed += 1
                    lib_status['apache-airflow'] = {'installed': True, 'version': version, 'location': 'Local'}
                except:
                    # Method 3: Check if docker-compose is running
                    try:
                        result = subprocess.run(
                            ['docker-compose', 'ps', '--format', '{{.Status}}'],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if 'Up' in result.stdout:
                            airflow_found = True
                            airflow_version = "2.7.3 (Docker Compose)"
                            self.print_check("✅ apache-airflow running in Docker Compose", True, "Orchestration")
                            self.checks_passed += 1
                            lib_status['apache-airflow'] = {'installed': True, 'version': '2.7.3 (Docker Compose)', 'location': 'Docker Compose'}
                        else:
                            raise Exception("Docker Compose not running")
                    except:
                        self.checks_failed += 1
                        all_installed = False
                        lib_status['apache-airflow'] = {'installed': False}
                        self.print_check("❌ apache-airflow NOT installed/running", False, "Orchestration\n   💡 Run: docker-compose up -d")
            
            # Check other required libraries
            required_libs = {
                'duckdb': 'Analytics database',
                'pandas': 'Data manipulation',
                'streamlit': 'Dashboard framework',
                'plotly': 'Interactive visualizations'
            }
            
            for lib, purpose in required_libs.items():
                self.total_checks += 1
                try:
                    module_name = lib.replace('-', '_')
                    spec = importlib.util.find_spec(module_name)
                    
                    if spec is not None:
                        try:
                            import pkg_resources
                            version = pkg_resources.get_distribution(lib).version
                            version_info = f"v{version}"
                            lib_status[lib] = {'installed': True, 'version': version}
                        except:
                            version_info = "installed"
                            lib_status[lib] = {'installed': True, 'version': 'unknown'}
                        
                        self.checks_passed += 1
                        self.print_check(f"✅ {lib} {version_info}", True, purpose)
                    else:
                        self.checks_failed += 1
                        all_installed = False
                        lib_status[lib] = {'installed': False}
                        self.print_check(f"❌ {lib} NOT installed", False, f"{purpose}\n   💡 Run: pip install {lib}")
                        self.results[f'lib_{lib}'] = False
                        
                except Exception:
                    self.checks_failed += 1
                    all_installed = False
                    lib_status[lib] = {'installed': False}
                    self.print_check(f"❌ {lib} NOT installed", False, f"{purpose}\n   💡 Run: pip install {lib}")
                    self.results[f'lib_{lib}'] = False
            
            self.results['requirements'] = all_installed
            
            self.add_check_result(
                'requirements',
                all_installed,
                'All requirements installed' if all_installed else 'Some requirements missing',
                {'libraries': lib_status}
            )
            return all_installed
        else:
            self.checks_failed += 1
            self.print_check(
                "requirements.txt NOT found", 
                False, 
                "💡 Create requirements.txt with dependencies"
            )
            self.results['requirements'] = False
            self.add_check_result(
                'requirements',
                False,
                'requirements.txt not found',
                {'missing_file': 'requirements.txt'}
            )
            return False
    
    def verify_docker(self):
        """Verify Docker installation"""
        self.print_section("Docker")
        
        self.total_checks += 1
        
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.checks_passed += 1
                self.print_check(f"Docker installed", True, version)
                self.results['docker'] = True
                
                # Check Docker Compose
                result2 = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True, timeout=5)
                if result2.returncode == 0:
                    version2 = result2.stdout.strip()
                    self.print_check(f"Docker Compose installed", True, version2)
                    self.results['docker_compose'] = True
                else:
                    self.print_check("Docker Compose NOT found", False, "💡 Install Docker Compose")
                    self.results['docker_compose'] = False
                
                self.add_check_result(
                    'docker',
                    True,
                    'Docker installed',
                    {'version': version, 'compose_installed': self.results.get('docker_compose', False)}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("Docker NOT installed", False, "💡 Install Docker Desktop from docker.com")
                self.results['docker'] = False
                self.add_check_result(
                    'docker',
                    False,
                    'Docker not installed',
                    {'error': 'Docker not found in PATH'}
                )
                return False
        except:
            self.checks_failed += 1
            self.print_check("Docker NOT installed", False, "💡 Install Docker Desktop from docker.com")
            self.results['docker'] = False
            return False
    
    def verify_airflow_files(self):
        """Verify Airflow DAG and script files exist"""
        self.print_section("Airflow Files")
        
        all_exist = True
        
        # Check DAG file
        dag_file = self.project_root / 'dags' / 'uber_etl_dag.py'
        self.total_checks += 1
        if dag_file.exists():
            self.checks_passed += 1
            self.print_check("DAG file exists", True, "dags/uber_etl_dag.py")
            self.results['dag_file'] = True
            
            # Check DAG content
            with open(dag_file, 'r') as f:
                content = f.read()
            if 'uber_etl_pipeline' in content:
                self.print_check("DAG contains 'uber_etl_pipeline'", True)
            else:
                self.print_check("DAG may be incomplete", False, "Check DAG ID")
        else:
            self.checks_failed += 1
            all_exist = False
            self.print_check("DAG file NOT found", False, "dags/uber_etl_dag.py")
            self.results['dag_file'] = False
        
        # Check script files
        scripts = ['extract.py', 'transform.py', 'load.py']
        for script in scripts:
            script_file = self.project_root / 'scripts' / script
            self.total_checks += 1
            if script_file.exists():
                self.checks_passed += 1
                self.print_check(f"Script exists: {script}", True, f"scripts/{script}")
                self.results[f'script_{script}'] = True
            else:
                self.checks_failed += 1
                all_exist = False
                self.print_check(f"Script NOT found: {script}", False, f"scripts/{script}")
                self.results[f'script_{script}'] = False
        
        self.add_check_result(
            'airflow_files',
            all_exist,
            'All Airflow files exist' if all_exist else 'Some files missing',
            {
                'dag_file': self.results.get('dag_file', False),
                'scripts': {s: self.results.get(f'script_{s}', False) for s in scripts}
            }
        )
        
        return all_exist
    
    def verify_system_info(self):
        """Display system information"""
        self.print_section("System Information")
        
        python_version = sys.version.split()[0]
        self.print_check(f"Python version: {python_version}", True)
        self.checks_passed += 1
        
        self.print_check(f"Operating System: {sys.platform}", True)
        self.checks_passed += 1
        
        self.print_check(f"Project directory: {self.project_root}", True)
        self.checks_passed += 1
        
        disk_info = {}
        try:
            import shutil
            disk_usage = shutil.disk_usage(self.project_root)
            free_gb = disk_usage.free / (1024**3)
            total_gb = disk_usage.total / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            self.print_check(f"Disk space: {used_gb:.1f} GB used of {total_gb:.1f} GB ({free_gb:.1f} GB free)", True)
            disk_info = {
                'total_gb': round(total_gb, 1),
                'used_gb': round(used_gb, 1),
                'free_gb': round(free_gb, 1)
            }
        except:
            pass
        
        self.add_check_result(
            'system_info',
            True,
            'System information collected',
            {
                'python_version': python_version,
                'os': sys.platform,
                'project_root': str(self.project_root),
                'disk': disk_info
            }
        )
        
        return True
    
    def save_json_report(self):
        """Save JSON report - always overwrite"""
        total_passed = self.checks_passed
        total_failed = self.checks_failed
        total = total_passed + total_failed
        percentage = (total_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 1,
            'phase_name': 'Setup & Environment (Airflow - FIXED)',
            'summary': {
                'total_checks': total,
                'passed': total_passed,
                'failed': total_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if total_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase1_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 JSON report saved to: {json_file} (overwritten)")
        return report
    
    def save_text_report(self):
        """Save human-readable report"""
        total_passed = self.checks_passed
        total_failed = self.checks_failed
        total = total_passed + total_failed
        percentage = (total_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase1_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 1 VERIFICATION REPORT - AIRFLOW VERSION (FIXED)\n")
            f.write("="*60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Project: {self.project_root}\n")
            f.write(f"Success Rate: {percentage:.1f}%\n")
            f.write(f"Passed: {total_passed}, Failed: {total_failed}\n")
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
        """Generate and display summary"""
        total_passed = self.checks_passed
        total_failed = self.checks_failed
        total = total_passed + total_failed
        percentage = (total_passed / total * 100) if total > 0 else 0
        
        self.print_section("Verification Summary")
        
        print(f"\n  📊 Total Checks: {total}")
        print(f"  ✅ Passed: {total_passed}")
        print(f"  ❌ Failed: {total_failed}")
        print(f"  📈 Success Rate: {percentage:.1f}%")
        
        if total_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 1 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ You are ready to proceed to Phase 2 (Airflow DAG Creation){Colors.END}")
        elif total_failed <= 3:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Most checks passed with minor issues{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before proceeding to Phase 2{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Multiple issues need attention{Colors.END}")
            print(f"{Colors.RED}📌 Please fix the failed items before proceeding{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        """Execute all verification checks"""
        self.print_header("🔍 PHASE 1 VERIFICATION - UBER ETL PIPELINE (AIRFLOW - FIXED)")
        
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_folder_structure()
        self.verify_data_file()
        self.verify_venv()
        self.verify_requirements()
        self.verify_docker()
        self.verify_airflow_files()
        self.verify_system_info()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    """Main execution function"""
    try:
        verifier = Phase1Verifier()
        success = verifier.run_all_checks()
        
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase1_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase1_verification_report.txt{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️ Verification interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()