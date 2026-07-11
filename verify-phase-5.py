# verify-phase-5.py
"""
Phase 5: Dashboard Development Verification

This script verifies all components related to Phase 5 of the
Uber ETL Pipeline project.

Checks performed:
    - Dashboard file exists (dashboard/app.py)
    - Required imports are present
    - Streamlit is installed
    - Dashboard features exist (KPI cards, charts, filters, data table)
    - Dashboard is running (optional)
    - DuckDB connection is configured
"""

import os
import sys
import json
import importlib.util
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
# Phase 5: Dashboard Development
# ============================================

class Phase5Verifier(PhaseVerifier):
    """Verifier for Phase 5: Dashboard Development."""

    def __init__(self):
        super().__init__(5, "Dashboard Development")

    def check_dashboard_file(self) -> bool:
        """Check if dashboard file exists."""
        self.print_section("Dashboard File")

        app_path = self.project_root / 'dashboard' / 'app.py'
        exists = app_path.exists()

        if exists:
            with open(app_path, 'r', encoding='utf-8') as f:
                lines = len(f.read().split('\n'))
            self.print_check("dashboard/app.py exists", True, f"{lines} lines")
            self.add_result('dashboard_file', True, f'Dashboard file exists ({lines} lines)')
        else:
            self.print_check("dashboard/app.py NOT found", False)
            self.add_result('dashboard_file', False, 'Dashboard file not found')

        return exists

    def check_dashboard_imports(self) -> bool:
        """Check if required imports are present."""
        self.print_section("Dashboard Imports")

        app_path = self.project_root / 'dashboard' / 'app.py'

        if not app_path.exists():
            self.print_check("Dashboard file not found", False)
            self.add_result('dashboard_imports', False, 'Dashboard file not found')
            return False

        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required = ['streamlit', 'duckdb', 'pandas', 'plotly']
        all_found = True

        for imp in required:
            found = f'import {imp}' in content or f'from {imp}' in content
            self.print_check(f"Import '{imp}'", found)
            if not found:
                all_found = False

        self.add_result('dashboard_imports', all_found, 'All imports present' if all_found else 'Some imports missing')
        return all_found

    def check_streamlit_installed(self) -> bool:
        """Check if Streamlit is installed."""
        self.print_section("Streamlit Installation")

        try:
            import streamlit
            import pkg_resources
            version = pkg_resources.get_distribution('streamlit').version
            self.print_check(f"Streamlit installed", True, f"v{version}")
            self.add_result('streamlit_installed', True, f'Streamlit v{version} installed')
            return True
        except:
            self.print_check("Streamlit NOT installed", False, "Run: pip install streamlit")
            self.add_result('streamlit_installed', False, 'Streamlit not installed')
            return False

    def check_dashboard_features(self) -> bool:
        """Check for dashboard features."""
        self.print_section("Dashboard Features")

        app_path = self.project_root / 'dashboard' / 'app.py'

        if not app_path.exists():
            self.print_check("Dashboard file not found", False)
            self.add_result('dashboard_features', False, 'Dashboard file not found')
            return False

        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()

        features = {
            'st.title': 'Page title',
            'st.metric': 'KPI metrics',
            'st.dataframe': 'Data table',
            'st.sidebar': 'Sidebar filters',
            'st.cache_resource': 'Caching',
            'plotly.express': 'Plotly charts',
            'st.download_button': 'Download button'
        }

        found = [desc for key, desc in features.items() if key in content]
        missing = [desc for key, desc in features.items() if key not in content]

        has_enough = len(found) >= 5
        self.print_check(f"Dashboard features found", has_enough, f"{len(found)}/{len(features)} features")

        for feature in found:
            self.print_check(f"  {feature}", True)

        self.add_result('dashboard_features', has_enough, f'{len(found)}/{len(features)} features found')
        return has_enough

    def check_dashboard_running(self) -> bool:
        """Check if dashboard is running."""
        self.print_section("Dashboard Running")

        try:
            response = urllib.request.urlopen('http://localhost:8501', timeout=3)
            running = response.getcode() == 200
            self.print_check("Dashboard is running", running, "http://localhost:8501")
            self.add_result('dashboard_running', running, 'Dashboard running' if running else 'Dashboard not running')
            return running
        except:
            self.print_check("Dashboard NOT running", False, "Run: streamlit run dashboard/app.py")
            self.add_result('dashboard_running', False, 'Dashboard not running')
            return False

    def check_duckdb_connection(self) -> bool:
        """Check if DuckDB connection is configured."""
        self.print_section("DuckDB Connection")

        app_path = self.project_root / 'dashboard' / 'app.py'

        if not app_path.exists():
            self.print_check("Dashboard file not found", False)
            self.add_result('duckdb_connection', False, 'Dashboard file not found')
            return False

        with open(app_path, 'r', encoding='utf-8') as f:
            content = f.read()

        configured = 'duckdb.connect' in content
        self.print_check("DuckDB connection configured", configured)
        self.add_result('duckdb_connection', configured, 'Connection configured' if configured else 'Connection not configured')
        return configured

    def run(self) -> bool:
        """Run all Phase 5 checks."""
        self.check_dashboard_file()
        self.check_dashboard_imports()
        self.check_streamlit_installed()
        self.check_dashboard_features()
        self.check_dashboard_running()
        self.check_duckdb_connection()

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
        verifier = Phase5Verifier()
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