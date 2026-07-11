# verify-phase-4.py
"""
Phase 4: Data Loading Verification

This script verifies all components related to Phase 4 of the
Uber ETL Pipeline project.

Checks performed:
    - Load script exists and is valid
    - Database file exists and has data
    - Tables are populated with data
    - trip_analytics view has data
    - Foreign key relationships are valid
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
# Phase 4: Data Loading
# ============================================

class Phase4Verifier(PhaseVerifier):
    """Verifier for Phase 4: Data Loading."""

    def __init__(self):
        super().__init__(4, "Data Loading")

    def check_load_script(self) -> bool:
        """Check if load script exists."""
        self.print_section("Load Script")

        load_path = self.project_root / 'scripts' / 'load.py'
        exists = load_path.exists()

        if exists:
            self.print_check("load.py exists", True)
            self.add_result('load_script', True, 'Script exists')
        else:
            self.print_check("load.py NOT found", False)
            self.add_result('load_script', False, 'Script not found')

        return exists

    def check_database_file(self) -> bool:
        """Check if database file exists and has data."""
        self.print_section("Database File")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        exists = db_path.exists()

        if exists:
            size_mb = db_path.stat().st_size / (1024 * 1024)
            has_data = size_mb > 0
            self.print_check(f"Database exists", has_data, f"{size_mb:.2f} MB")
            self.add_result('database_file', has_data, f'Database exists ({size_mb:.2f} MB)')
            return has_data

        self.print_check("Database NOT found", False)
        self.add_result('database_file', False, 'Database not found')
        return False

    def check_tables_populated(self) -> bool:
        """Check if all tables have data."""
        self.print_section("Tables Populated")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'

        if not db_path.exists():
            self.print_check("Database not found", False)
            self.add_result('tables_populated', False, 'Database not found')
            return False

        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            tables = conn.execute("SHOW TABLES").fetchall()

            if not tables:
                self.print_check("No tables found", False)
                self.add_result('tables_populated', False, 'No tables found')
                conn.close()
                return False

            all_populated = True
            for table in tables:
                count = conn.execute(f"SELECT COUNT(*) FROM {table[0]}").fetchone()[0]
                has_data = count > 0
                self.print_check(f"{table[0]}: {count:,} rows", has_data)
                if not has_data:
                    all_populated = False

            conn.close()
            self.add_result('tables_populated', all_populated, 'All tables have data' if all_populated else 'Some tables empty')
            return all_populated

        except Exception as e:
            self.print_check("Error checking tables", False, str(e))
            self.add_result('tables_populated', False, str(e))
            return False

    def check_view_data(self) -> bool:
        """Check if trip_analytics view has data."""
        self.print_section("View Data")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'

        if not db_path.exists():
            self.print_check("Database not found", False)
            self.add_result('view_data', False, 'Database not found')
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

            if not view_exists:
                self.print_check("trip_analytics view NOT found", False)
                self.add_result('view_data', False, 'View not found')
                conn.close()
                return False

            count = conn.execute("SELECT COUNT(*) FROM trip_analytics").fetchone()[0]
            has_data = count > 0
            self.print_check(f"trip_analytics view has data", has_data, f"{count:,} rows")

            conn.close()
            self.add_result('view_data', has_data, f'View has {count:,} rows' if has_data else 'View is empty')
            return has_data

        except Exception as e:
            self.print_check("Error checking view", False, str(e))
            self.add_result('view_data', False, str(e))
            return False

    def check_foreign_keys(self) -> bool:
        """Check foreign key relationships."""
        self.print_section("Foreign Key Relationships")

        db_path = self.project_root / 'warehouse' / 'uber.duckdb'

        if not db_path.exists():
            self.print_check("Database not found", False)
            self.add_result('foreign_keys', False, 'Database not found')
            return False

        try:
            import duckdb
            conn = duckdb.connect(str(db_path))

            fk_checks = [
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN datetime_dim d ON f.datetime_id = d.datetime_id WHERE d.datetime_id IS NULL", "datetime_dim references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN rate_code_dim r ON f.rate_code_id = r.rate_code_id WHERE r.rate_code_id IS NULL", "rate_code_dim references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN location_dim pl ON f.pickup_location_id = pl.location_id WHERE pl.location_id IS NULL", "pickup location references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN location_dim dl ON f.dropoff_location_id = dl.location_id WHERE dl.location_id IS NULL", "dropoff location references")
            ]

            all_valid = True
            for query, desc in fk_checks:
                result = conn.execute(query).fetchone()[0]
                valid = result == 0
                self.print_check(f"{desc}", valid, f"{result} orphan records" if not valid else "")
                if not valid:
                    all_valid = False

            conn.close()
            self.add_result('foreign_keys', all_valid, 'All foreign keys valid' if all_valid else 'Some foreign keys have issues')
            return all_valid

        except Exception as e:
            self.print_check("Error checking foreign keys", False, str(e))
            self.add_result('foreign_keys', False, str(e))
            return False

    def run(self) -> bool:
        """Run all Phase 4 checks."""
        self.check_load_script()
        self.check_database_file()
        self.check_tables_populated()
        self.check_view_data()
        self.check_foreign_keys()

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
        verifier = Phase4Verifier()
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