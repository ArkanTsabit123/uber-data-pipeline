# verify-phase-4.py

"""
Phase 4: Data Loading Verification

This script verifies that data has been successfully loaded into DuckDB
and all tables are properly populated with data.

Checks performed:
    1. Load Script - Verifies load.py exists and contains required functions
    2. Database File - Checks if uber.duckdb exists and has size > 0
    3. Tables Populated - Verifies all tables have row counts > 0
    4. View Data - Checks trip_analytics view has data
    5. Foreign Key Relationships - Validates referential integrity
"""

import os
import sys
import json
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


class Phase4Verifier:
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
    
    def verify_load_script(self):
        """Check if load script exists and is valid"""
        self.print_section("Check 1: Load Script")
        load_path = self.project_root / 'scripts' / 'load.py'
        self.total_checks += 1
        
        if load_path.exists():
            self.checks_passed += 1
            self.print_check("load.py exists", True, "scripts/load.py")
            
            with open(load_path, 'r') as f:
                content = f.read()
            
            required_elements = {
                'duckdb': 'duckdb imported',
                'DROP TABLE IF EXISTS': 'drop table statement',
                'CREATE TABLE': 'create table statement',
                'trip_analytics': 'trip_analytics view'
            }
            
            all_found = True
            for key, desc in required_elements.items():
                if key in content:
                    self.print_check(f"  ✅ {desc}", True)
                else:
                    all_found = False
                    self.print_check(f"  ❌ {desc}", False)
            
            if all_found:
                self.checks_passed += 1
                self.add_check_result(
                    'load_script',
                    True,
                    'load.py exists and is valid',
                    {'elements': list(required_elements.keys())}
                )
            else:
                self.checks_failed += 1
                self.add_check_result(
                    'load_script',
                    False,
                    'load.py exists but missing elements',
                    {'missing': [k for k, v in required_elements.items() if k not in content]}
                )
            return True
        else:
            self.checks_failed += 1
            self.print_check("load.py NOT found", False, "scripts/load.py")
            self.add_check_result(
                'load_script',
                False,
                'load.py not found',
                {'expected_path': 'scripts/load.py'}
            )
            return False
    
    def verify_database_file(self):
        """Check if database file exists and has data"""
        self.print_section("Check 2: Database File")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if db_path.exists():
            size = db_path.stat().st_size
            size_mb = size / (1024 * 1024)
            
            if size > 0:
                self.checks_passed += 1
                self.print_check("Database file exists", True, f"{size_mb:.2f} MB")
                self.add_check_result(
                    'database_file',
                    True,
                    f'Database file exists ({size_mb:.2f} MB)',
                    {'size_mb': round(size_mb, 2)}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("Database file is empty", False)
                self.add_check_result(
                    'database_file',
                    False,
                    'Database file is empty',
                    {'size_bytes': size}
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check("Database file NOT found", False, "warehouse/uber.duckdb")
            self.add_check_result(
                'database_file',
                False,
                'Database file not found',
                {'expected_path': 'warehouse/uber.duckdb'}
            )
            return False
    
    def verify_tables_populated(self):
        """Check if all tables have data"""
        self.print_section("Check 3: Tables Populated")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if not db_path.exists():
            self.checks_failed += 1
            self.print_check("Database not found", False)
            return False
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            
            tables = conn.execute("SHOW TABLES").fetchall()
            table_names = [t[0] for t in tables]
            
            if not table_names:
                self.checks_failed += 1
                self.print_check("No tables found", False)
                return False
            
            all_populated = True
            for table in table_names:
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                if count > 0:
                    self.print_check(f"✅ {table}: {count:,} rows", True)
                    self.checks_passed += 1
                else:
                    self.checks_failed += 1
                    all_populated = False
                    self.print_check(f"❌ {table}: EMPTY", False)
            
            conn.close()
            
            self.add_check_result(
                'tables_populated',
                all_populated,
                'All tables have data' if all_populated else 'Some tables are empty',
                {'tables': table_names}
            )
            return all_populated
            
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking tables", False, str(e))
            self.add_check_result(
                'tables_populated',
                False,
                f'Error: {str(e)}',
                {'error': str(e)}
            )
            return False
    
    def verify_view_data(self):
        """Check if trip_analytics view has data"""
        self.print_section("Check 4: View Data")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if not db_path.exists():
            self.checks_failed += 1
            self.print_check("Database not found", False)
            return False
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            
            # Check if view exists (compatible with DuckDB 1.5.4)
            view_exists = False
            try:
                conn.execute("SELECT * FROM trip_analytics LIMIT 1")
                view_exists = True
            except:
                try:
                    result = conn.execute("SELECT table_name FROM information_schema.views WHERE table_name = 'trip_analytics'").fetchall()
                    view_exists = len(result) > 0
                except:
                    pass
            
            if not view_exists:
                self.checks_failed += 1
                self.print_check("trip_analytics view NOT found", False)
                self.add_check_result(
                    'view_data',
                    False,
                    'trip_analytics view not found'
                )
                conn.close()
                return False
            
            count = conn.execute("SELECT COUNT(*) FROM trip_analytics").fetchone()[0]
            if count > 0:
                self.checks_passed += 1
                self.print_check("trip_analytics view has data", True, f"{count:,} rows")
                self.add_check_result(
                    'view_data',
                    True,
                    f'trip_analytics view has {count:,} rows',
                    {'rows': count}
                )
                conn.close()
                return True
            else:
                self.checks_failed += 1
                self.print_check("trip_analytics view is empty", False)
                self.add_check_result(
                    'view_data',
                    False,
                    'trip_analytics view is empty',
                    {'rows': 0}
                )
                conn.close()
                return False
            
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking view", False, str(e))
            self.add_check_result(
                'view_data',
                False,
                f'Error: {str(e)}',
                {'error': str(e)}
            )
            return False
    
    def verify_foreign_keys(self):
        """Check foreign key relationships"""
        self.print_section("Check 5: Foreign Key Relationships")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if not db_path.exists():
            self.checks_failed += 1
            self.print_check("Database not found", False)
            return False
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            
            tables = conn.execute("SHOW TABLES").fetchall()
            table_names = [t[0] for t in tables]
            
            if 'fact_table' not in table_names:
                self.checks_failed += 1
                self.print_check("fact_table not found", False)
                conn.close()
                return False
            
            fk_checks = [
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN datetime_dim d ON f.datetime_id = d.datetime_id WHERE d.datetime_id IS NULL", "datetime_dim references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN rate_code_dim r ON f.rate_code_id = r.rate_code_id WHERE r.rate_code_id IS NULL", "rate_code_dim references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN location_dim pl ON f.pickup_location_id = pl.location_id WHERE pl.location_id IS NULL", "pickup location references"),
                ("SELECT COUNT(*) FROM fact_table f LEFT JOIN location_dim dl ON f.dropoff_location_id = dl.location_id WHERE dl.location_id IS NULL", "dropoff location references")
            ]
            
            all_valid = True
            for query, desc in fk_checks:
                result = conn.execute(query).fetchone()[0]
                if result == 0:
                    self.print_check(f"✅ {desc}: valid", True)
                    self.checks_passed += 1
                else:
                    self.checks_failed += 1
                    all_valid = False
                    self.print_check(f"❌ {desc}: {result} orphan records", False)
            
            conn.close()
            
            self.add_check_result(
                'foreign_keys',
                all_valid,
                'Foreign key relationships are valid' if all_valid else 'Some foreign keys have issues',
                {'valid': all_valid}
            )
            return all_valid
            
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking foreign keys", False, str(e))
            self.add_check_result(
                'foreign_keys',
                False,
                f'Error: {str(e)}',
                {'error': str(e)}
            )
            return False
    
    def save_json_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 4,
            'phase_name': 'Data Loading',
            'summary': {
                'total_checks': total,
                'passed': self.checks_passed,
                'failed': self.checks_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase4_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 JSON report saved to: {json_file}")
        return report
    
    def save_text_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase4_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 4 VERIFICATION REPORT\n")
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
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 4 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ You are ready to proceed to Phase 5 (Dashboard){Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before proceeding to Phase 5{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        self.print_header("🔍 PHASE 4 VERIFICATION - DATA LOADING")
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_load_script()
        self.verify_database_file()
        self.verify_tables_populated()
        self.verify_view_data()
        self.verify_foreign_keys()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    try:
        verifier = Phase4Verifier()
        success = verifier.run_all_checks()
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase4_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase4_verification_report.txt{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()