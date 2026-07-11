# verify-phase-3.py
"""
Phase 3: Data Transformation Verification

This script verifies all components related to Phase 3 of the
Uber ETL Pipeline project.

Checks performed:
    - Transform script exists and contains required functions
    - DuckDB tables exist (datetime_dim, rate_code_dim, location_dim, fact_table)
    - trip_analytics view exists
    - Transform logic is valid
"""

import os
import sys
import json
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

        raise NotImplementedError("Subclasses must implement run()")


# ============================================
# Phase 3: Data Transformation
# ============================================

class Phase3Verifier(PhaseVerifier):
    """Verifier for Phase 3: Data Transformation."""

    def __init__(self):
        super().__init__(3, "Data Transformation")

    def check_transform_script(self) -> bool:
        """Check if transform script exists and is valid."""
        self.print_section("Transform Script")

        transform_path = self.project_root / 'scripts' / 'transform.py'
        exists = transform_path.exists()

        if not exists:
            self.print_check("transform.py NOT found", False)
            self.add_result('transform_script', False, 'Script not found')
            return False

        self.print_check("transform.py exists", True)

        with open(transform_path, 'r') as f:
            content = f.read()

        required = ['datetime_dim', 'rate_code_dim', 'location_dim', 'fact_table']
        all_found = True

        for item in required:
            found = item in content
            self.print_check(f"Contains '{item}'", found)
            if not found:
                all_found = False

        self.add_result('transform_script', all_found, 'Script valid' if all_found else 'Missing components')
        return all_found

    def check_duckdb_tables(self) -> bool:
        """Check if Star Schema tables exist."""
        self.print_section("DuckDB Tables")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'

        if not db_path.exists():
            self.print_check("Database not found", False)
            self.add_result('duckdb_tables', False, 'Database not found')
            return False

        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            tables = [t[0] for t in conn.execute("SHOW TABLES").fetchall()]
            conn.close()

            required = ['datetime_dim', 'rate_code_dim', 'location_dim', 'fact_table']
            all_found = True

            for table in required:
                exists = table in tables
                self.print_check(f"{table}", exists)
                if not exists:
                    all_found = False

            self.add_result('duckdb_tables', all_found, 'All tables exist' if all_found else 'Some tables missing')
            return all_found

        except Exception as e:
            self.print_check("Error checking tables", False, str(e))
            self.add_result('duckdb_tables', False, str(e))
            return False

    def check_trip_analytics_view(self) -> bool:
        """Check if trip_analytics view exists."""
        self.print_section("trip_analytics View")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'

        if not db_path.exists():
            self.print_check("Database not found", False)
            self.add_result('trip_analytics_view', False, 'Database not found')
            return False

        try:
            import duckdb
            conn = duckdb.connect(str(db_path))

            view_exists = False
            try:
                conn.execute("SELECT * FROM trip_analytics LIMIT 1")
                view_exists = True
            except:
                pass

            self.print_check("trip_analytics view exists", view_exists)
            conn.close()

            self.add_result('trip_analytics_view', view_exists, 'View exists' if view_exists else 'View missing')
            return view_exists

        except Exception as e:
            self.print_check("Error checking view", False, str(e))
            self.add_result('trip_analytics_view', False, str(e))
            return False

    def check_transform_logic(self) -> bool:
        """Check for data cleaning and transformation functions."""
        self.print_section("Transform Logic")

        transform_path = self.project_root / 'scripts' / 'transform.py'

        if not transform_path.exists():
            self.print_check("transform.py not found", False)
            self.add_result('transform_logic', False, 'Script not found')
            return False

        with open(transform_path, 'r') as f:
            content = f.read()

        required_checks = [
            ('drop_duplicates', 'Data cleaning - drop_duplicates'),
            ('dropna', 'Data cleaning - dropna'),
            ('pd.to_datetime', 'datetime conversion'),
            ('rate_map', 'Rate code mapping')
        ]

        all_found = True
        for key, desc in required_checks:
            found = key in content
            self.print_check(f"{desc}", found)
            if not found:
                all_found = False

        self.add_result('transform_logic', all_found, 'All logic present' if all_found else 'Some logic missing')
        return all_found

    def run(self) -> bool:
        """Run all Phase 3 checks."""
        self.check_transform_script()
        self.check_duckdb_tables()
        self.check_trip_analytics_view()
        self.check_transform_logic()

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
        verifier = Phase3Verifier()
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