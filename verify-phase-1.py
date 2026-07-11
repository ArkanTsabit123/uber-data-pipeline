# verify-phase-1.py
"""
Phase 1: Setup & Environment Verification

This script verifies all components related to Phase 1 of the
Uber ETL Pipeline project.

Checks performed:
    - Folder structure
    - Dataset file
    - Virtual environment
    - Requirements and libraries
    - Docker installation
    - Airflow files
    - System information
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple


class Colors:
    """Terminal color codes."""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class VerificationResult:
    """Result of a single verification check."""
    def __init__(self, name: str, status: bool, message: str, details: Optional[Dict] = None):
        self.name = name
        self.status = status
        self.message = message
        self.details = details or {}


class PhaseVerifier:
    """Base class for phase verification."""

    def __init__(self, phase: int, phase_name: str):
        self.phase = phase
        self.phase_name = phase_name
        self.project_root = Path.cwd()
        self.checks_passed = 0
        self.checks_failed = 0
        self.results: List[VerificationResult] = []
        self.timestamp = datetime.now().isoformat()

    def print_header(self, text: str) -> None:
        """Print formatted header."""
        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
        print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")

    def print_section(self, text: str) -> None:
        """Print section header."""
        print(f"\n{Colors.YELLOW}{text}{Colors.END}")
        print(f"{Colors.YELLOW}{'-' * 40}{Colors.END}")

    def print_check(self, text: str, status: bool, detail: str = "") -> None:
        """Print check result with appropriate color."""
        icon = "PASS" if status else "FAIL"
        color = Colors.GREEN if status else Colors.RED
        if detail:
            print(f"{color}{icon} {text}{Colors.END}")
            print(f"   {Colors.CYAN}-> {detail}{Colors.END}")
        else:
            print(f"{color}{icon} {text}{Colors.END}")

    def add_result(self, name: str, status: bool, message: str, details: Optional[Dict] = None) -> None:
        """Add a verification result."""
        self.results.append(VerificationResult(name, status, message, details))
        if status:
            self.checks_passed += 1
        else:
            self.checks_failed += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get verification summary."""
        total = self.checks_passed + self.checks_failed
        return {
            'phase': self.phase,
            'phase_name': self.phase_name,
            'total_checks': total,
            'passed': self.checks_passed,
            'failed': self.checks_failed,
            'success_rate': round((self.checks_passed / total * 100) if total > 0 else 0, 1)
        }

    def save_json_report(self) -> None:
        """Save JSON report."""
        summary = self.get_summary()
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': self.phase,
            'phase_name': self.phase_name,
            'summary': summary,
            'checks': [
                {'name': r.name, 'status': r.status, 'message': r.message, 'details': r.details}
                for r in self.results
            ],
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }

        json_file = self.project_root / f'phase{self.phase}_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nJSON report saved to: {json_file}")

    def save_text_report(self) -> None:
        """Save text report."""
        summary = self.get_summary()
        report_file = self.project_root / f'phase{self.phase}_verification_report.txt'

        with open(report_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write(f"PHASE {self.phase} VERIFICATION REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Success Rate: {summary['success_rate']:.1f}%\n")
            f.write(f"Passed: {self.checks_passed}, Failed: {self.checks_failed}\n")
            f.write("=" * 60 + "\n\n")

            failed = [r for r in self.results if not r.status]
            if failed:
                f.write("Failed Items:\n")
                for r in failed:
                    f.write(f"  - {r.name}: {r.message}\n")
            else:
                f.write("All checks passed successfully!\n")

        print(f"Text report saved to: {report_file}")

    def display_summary(self) -> None:
        """Display verification summary."""
        summary = self.get_summary()

        self.print_section("Verification Summary")
        print(f"\n  Total Checks: {summary['total_checks']}")
        print(f"  Passed: {self.checks_passed}")
        print(f"  Failed: {self.checks_failed}")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")

        if self.checks_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}All checks passed! Phase {self.phase} is complete!{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}Fix the failed items before proceeding{Colors.END}")

            failed = [r for r in self.results if not r.status]
            if failed:
                print(f"\n{Colors.RED}Items requiring attention:{Colors.END}")
                for r in failed:
                    print(f"  {r.name}: {r.message}")

        print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")

    def run(self) -> bool:
        """Run all verification checks."""
        self.print_header(f"PHASE {self.phase} VERIFICATION - {self.phase_name}")
        print(f"Project Root: {self.project_root}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Override this method in subclasses
        raise NotImplementedError("Subclasses must implement run()")


# ============================================
# Phase 1: Setup & Environment
# ============================================

class Phase1Verifier(PhaseVerifier):
    """Verifier for Phase 1: Setup & Environment."""

    def __init__(self):
        super().__init__(1, "Setup & Environment")

    def check_folder_structure(self) -> bool:
        """Verify required folders exist."""
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
        for folder, description in required_folders:
            exists = (self.project_root / folder).exists()
            self.print_check(f"Folder '{folder}/'", exists, description)
            if not exists:
                all_exist = False

        self.add_result('folder_structure', all_exist, 'All folders exist' if all_exist else 'Some folders missing')
        return all_exist

    def check_data_file(self) -> bool:
        """Verify dataset exists."""
        self.print_section("Dataset File")

        data_path = self.project_root / 'data' / 'uber_data.csv'
        exists = data_path.exists()

        if exists:
            size_mb = data_path.stat().st_size / (1024 * 1024)
            self.print_check(f"File found: {data_path.name}", True, f"{size_mb:.2f} MB")
            self.add_result('data_file', True, f'Dataset found ({size_mb:.2f} MB)')
        else:
            self.print_check("File NOT found", False, "Expected at: data/uber_data.csv")
            self.add_result('data_file', False, 'Dataset not found')

        return exists

    def check_venv(self) -> bool:
        """Verify virtual environment."""
        self.print_section("Virtual Environment")

        in_venv = sys.prefix != sys.base_prefix
        if in_venv:
            self.print_check("Virtual environment active", True, sys.prefix)
        else:
            self.print_check("Virtual environment NOT active", False, "Run: venv\\Scripts\\activate")

        venv_path = self.project_root / 'venv'
        exists = venv_path.exists()
        self.print_check("venv folder exists", exists)

        self.add_result('venv', in_venv and exists, 'Virtual environment ready' if in_venv and exists else 'Virtual environment issues')
        return in_venv and exists

    def check_requirements(self) -> bool:
        """Verify requirements and libraries."""
        self.print_section("Requirements & Libraries")

        req_file = self.project_root / 'requirements.txt'
        exists = req_file.exists()
        self.print_check("requirements.txt found", exists)

        if not exists:
            self.add_result('requirements', False, 'requirements.txt not found')
            return False

        all_installed = True
        required_libs = ['duckdb', 'pandas', 'streamlit', 'plotly']

        for lib in required_libs:
            try:
                spec = importlib.util.find_spec(lib)
                installed = spec is not None
                self.print_check(f"{lib}", installed)
                if not installed:
                    all_installed = False
            except Exception:
                self.print_check(f"{lib}", False)
                all_installed = False

        self.add_result('requirements', all_installed, 'All libraries installed' if all_installed else 'Some libraries missing')
        return all_installed

    def check_docker(self) -> bool:
        """Verify Docker installation."""
        self.print_section("Docker")

        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=5)
            installed = result.returncode == 0
            version = result.stdout.strip() if installed else "Not found"
            self.print_check("Docker installed", installed, version)

            if installed:
                result2 = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True, timeout=5)
                compose_installed = result2.returncode == 0
                self.print_check("Docker Compose installed", compose_installed)

            self.add_result('docker', installed, 'Docker ready' if installed else 'Docker not installed')
            return installed

        except Exception:
            self.print_check("Docker installed", False, "Install Docker Desktop from docker.com")
            self.add_result('docker', False, 'Docker not installed')
            return False

    def check_airflow_files(self) -> bool:
        """Verify Airflow files."""
        self.print_section("Airflow Files")

        dag_file = self.project_root / 'dags' / 'uber_etl_dag.py'
        dag_exists = dag_file.exists()
        self.print_check("DAG file exists", dag_exists)

        scripts = ['extract.py', 'transform.py', 'load.py']
        all_scripts_exist = True
        for script in scripts:
            exists = (self.project_root / 'scripts' / script).exists()
            self.print_check(f"Script: {script}", exists)
            if not exists:
                all_scripts_exist = False

        all_exist = dag_exists and all_scripts_exist
        self.add_result('airflow_files', all_exist, 'All Airflow files exist' if all_exist else 'Some files missing')
        return all_exist

    def run(self) -> bool:
        """Run all Phase 1 checks."""
        self.check_folder_structure()
        self.check_data_file()
        self.check_venv()
        self.check_requirements()
        self.check_docker()
        self.check_airflow_files()

        self.display_summary()
        self.save_json_report()
        self.save_text_report()

        return self.checks_failed == 0


# ============================================
# Main Entry Point
# ============================================

def main() -> None:
    """Main entry point."""
    try:
        verifier = Phase1Verifier()
        success = verifier.run()
        print(f"\n{Colors.CYAN}Verification complete!{Colors.END}")
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()