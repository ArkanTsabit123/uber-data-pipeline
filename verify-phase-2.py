# verify-phase-2.py
"""
Phase 2: Airflow DAG Creation Verification

This script verifies all components related to Phase 2 of the
Uber ETL Pipeline project.

Checks performed:
    - Airflow installation (Docker or local)
    - Docker status
    - Airflow containers
    - DAG file
    - Script files
    - Airflow UI accessibility
"""

import os
import sys
import json
import subprocess
import urllib.request
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

        raise NotImplementedError("Subclasses must implement run()")


# ============================================
# Phase 2: Airflow DAG Creation
# ============================================

class Phase2Verifier(PhaseVerifier):
    """Verifier for Phase 2: Airflow DAG Creation."""

    def __init__(self):
        super().__init__(2, "Airflow DAG Creation")

    def check_airflow_installed(self) -> bool:
        """Check if Airflow is installed or running."""
        self.print_section("Airflow Installation")

        # Check Docker
        try:
            result = subprocess.run(
                ['docker', 'ps', '--filter', 'name=airflow-webserver', '--format', '{{.Status}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if 'Up' in result.stdout:
                self.print_check("Apache Airflow running in Docker", True, "v2.7.3")
                self.add_result('airflow_installed', True, 'Airflow running in Docker')
                return True
        except:
            pass

        # Check local installation
        try:
            import airflow
            self.print_check("Apache Airflow installed locally", True)
            self.add_result('airflow_installed', True, 'Airflow installed locally')
            return True
        except:
            pass

        self.print_check("Apache Airflow NOT installed", False, "Run: docker-compose up -d")
        self.add_result('airflow_installed', False, 'Airflow not installed')
        return False

    def check_docker_running(self) -> bool:
        """Check if Docker is running."""
        self.print_section("Docker Status")

        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
            running = result.returncode == 0
            self.print_check("Docker is running", running)
            self.add_result('docker_running', running, 'Docker ready' if running else 'Docker not running')
            return running
        except:
            self.print_check("Docker is NOT running", False, "Start Docker Desktop first")
            self.add_result('docker_running', False, 'Docker not running')
            return False

    def check_airflow_containers(self) -> bool:
        """Check Airflow containers."""
        self.print_section("Airflow Containers")

        containers = ['airflow-webserver', 'airflow-scheduler', 'postgres', 'redis']
        found = []

        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                running = result.stdout.strip().split('\n')
                found = [c for c in containers if any(c in name for name in running)]

                for container in containers:
                    exists = container in found
                    self.print_check(f"{container}", exists)

                all_running = len(found) == len(containers)
                self.add_result('airflow_containers', all_running, f'Found {len(found)}/{len(containers)} containers')
                return all_running
        except:
            pass

        self.print_check("Airflow containers NOT running", False, "Run: docker-compose up -d")
        self.add_result('airflow_containers', False, 'Containers not running')
        return False

    def check_dag_file(self) -> bool:
        """Check DAG file."""
        self.print_section("DAG File")

        dag_path = self.project_root / 'dags' / 'uber_etl_dag.py'
        exists = dag_path.exists()

        if exists:
            self.print_check("uber_etl_dag.py exists", True)
            with open(dag_path, 'r') as f:
                content = f.read()
            has_dag_id = 'uber_etl_pipeline' in content
            self.print_check("DAG ID found", has_dag_id)
            self.add_result('dag_file', has_dag_id, 'DAG valid' if has_dag_id else 'DAG ID missing')
            return has_dag_id
        else:
            self.print_check("uber_etl_dag.py NOT found", False)
            self.add_result('dag_file', False, 'DAG file not found')
            return False

    def check_scripts(self) -> bool:
        """Check script files."""
        self.print_section("Script Files")

        scripts = ['extract.py', 'transform.py', 'load.py']
        all_exist = True

        for script in scripts:
            exists = (self.project_root / 'scripts' / script).exists()
            self.print_check(script, exists)
            if not exists:
                all_exist = False

        self.add_result('scripts', all_exist, 'All scripts exist' if all_exist else 'Some scripts missing')
        return all_exist

    def check_airflow_ui(self) -> bool:
        """Check Airflow UI."""
        self.print_section("Airflow UI")

        try:
            response = urllib.request.urlopen('http://localhost:8080', timeout=3)
            accessible = response.getcode() == 200
            self.print_check("Airflow UI accessible", accessible, "http://localhost:8080")
            self.add_result('airflow_ui', accessible, 'UI accessible' if accessible else 'UI not accessible')
            return accessible
        except:
            self.print_check("Airflow UI NOT accessible", False, "Run: docker-compose up -d")
            self.add_result('airflow_ui', False, 'UI not accessible')
            return False

    def run(self) -> bool:
        """Run all Phase 2 checks."""
        self.check_airflow_installed()
        self.check_docker_running()
        self.check_airflow_containers()
        self.check_dag_file()
        self.check_scripts()
        self.check_airflow_ui()

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
        verifier = Phase2Verifier()
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