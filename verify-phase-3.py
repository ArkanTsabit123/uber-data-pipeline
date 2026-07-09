# verify-phase-3.py

"""
Phase 3: Data Transformation Verification

This script verifies that the Star Schema transformation is working correctly
and all dimension tables are properly created in DuckDB.

Checks performed:
    1. Transform Script - Verifies transform.py exists and contains required functions
    2. DuckDB Tables - Checks if datetime_dim, rate_code_dim, location_dim, fact_table exist
    3. trip_analytics View - Verifies the analytics view is created
    4. Star Schema Structure - Validates column structure of each table
    5. Transform Logic - Checks for data cleaning and transformation functions
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


class Phase3Verifier:
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
    
    def verify_transform_script(self):
        """Check if transform script exists and is valid"""
        self.print_section("Check 1: Transform Script")
        transform_path = self.project_root / 'scripts' / 'transform.py'
        self.total_checks += 1
        
        if transform_path.exists():
            self.checks_passed += 1
            self.print_check("transform.py exists", True, "scripts/transform.py")
            
            with open(transform_path, 'r') as f:
                content = f.read()
            
            required_functions = [
                'datetime_dim',
                'rate_code_dim',
                'location_dim',
                'fact_table'
            ]
            
            all_found = True
            for func in required_functions:
                if func in content:
                    self.print_check(f"  ✅ {func} found", True)
                else:
                    all_found = False
                    self.print_check(f"  ❌ {func} missing", False)
            
            if all_found:
                self.checks_passed += 1
                self.add_check_result(
                    'transform_script',
                    True,
                    'transform.py exists and is valid',
                    {'functions': required_functions}
                )
            else:
                self.checks_failed += 1
                self.add_check_result(
                    'transform_script',
                    False,
                    'transform.py exists but missing functions',
                    {'functions': required_functions}
                )
            return True
        else:
            self.checks_failed += 1
            self.print_check("transform.py NOT found", False, "scripts/transform.py")
            self.add_check_result(
                'transform_script',
                False,
                'transform.py not found',
                {'expected_path': 'scripts/transform.py'}
            )
            return False
    
    def verify_duckdb_tables(self):
        """Check if all Star Schema tables exist"""
        self.print_section("Check 2: DuckDB Tables")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if not db_path.exists():
            self.checks_failed += 1
            self.print_check("Database not found", False, "Run pipeline first")
            self.add_check_result(
                'duckdb_tables',
                False,
                'Database not found',
                {'expected_path': 'warehouse/uber.duckdb'}
            )
            return False
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            tables = [t[0] for t in conn.execute("SHOW TABLES").fetchall()]
            conn.close()
            
            required_tables = ['datetime_dim', 'rate_code_dim', 'location_dim', 'fact_table']
            found = [t for t in required_tables if t in tables]
            missing = [t for t in required_tables if t not in tables]
            
            if not missing:
                self.checks_passed += 1
                self.print_check(f"All tables found", True, f"{len(found)}/{len(required_tables)}")
                for table in found:
                    self.print_check(f"  ✅ {table}", True)
                self.add_check_result(
                    'duckdb_tables',
                    True,
                    'All Star Schema tables exist',
                    {'found': found}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check(f"Missing tables", False, f"Missing: {', '.join(missing)}")
                for table in required_tables:
                    if table in found:
                        self.print_check(f"  ✅ {table}", True)
                    else:
                        self.print_check(f"  ❌ {table}", False)
                self.add_check_result(
                    'duckdb_tables',
                    False,
                    'Some tables missing',
                    {'found': found, 'missing': missing}
                )
                return False
                
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking tables", False, str(e))
            self.add_check_result(
                'duckdb_tables',
                False,
                f'Error: {str(e)}',
                {'error': str(e)}
            )
            return False
    
    def verify_trip_analytics_view(self):
        """Check if trip_analytics view exists"""
        self.print_section("Check 3: trip_analytics View")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        if not db_path.exists():
            self.checks_failed += 1
            self.print_check("Database not found", False)
            return False
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            views = conn.execute("SHOW VIEWS").fetchall()
            view_names = [v[0] for v in views]
            conn.close()
            
            if 'trip_analytics' in view_names:
                self.checks_passed += 1
                self.print_check("trip_analytics view exists", True)
                self.add_check_result(
                    'trip_analytics_view',
                    True,
                    'trip_analytics view exists',
                    {'view': 'trip_analytics'}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("trip_analytics view NOT found", False)
                self.add_check_result(
                    'trip_analytics_view',
                    False,
                    'trip_analytics view not found',
                    {'available_views': view_names}
                )
                return False
                
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking view", False, str(e))
            return False
    
    def verify_star_schema_structure(self):
        """Validate the structure of each Star Schema table"""
        self.print_section("Check 4: Star Schema Structure")
        db_path = self.project_root / 'warehouse' / 'uber.duckdb'
        self.total_checks += 1
        
        expected_columns = {
            'datetime_dim': ['datetime_id', 'pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday'],
            'rate_code_dim': ['rate_code_id', 'RatecodeID', 'rate_code_name'],
            'location_dim': ['location_id', 'location_name', 'borough'],
            'fact_table': ['trip_id', 'datetime_id', 'rate_code_id', 'pickup_location_id', 'dropoff_location_id', 'trip_distance', 'fare_amount', 'total_amount', 'passenger_count', 'payment_type']
        }
        
        try:
            import duckdb
            conn = duckdb.connect(str(db_path))
            all_valid = True
            
            for table, columns in expected_columns.items():
                try:
                    result = conn.execute(f"PRAGMA table_info({table})").fetchall()
                    actual_columns = [r[1] for r in result]
                    missing = [c for c in columns if c not in actual_columns]
                    
                    if not missing:
                        self.print_check(f"{table} structure valid", True, f"{len(actual_columns)} columns")
                        self.checks_passed += 1
                    else:
                        self.print_check(f"{table} missing columns", False, f"Missing: {', '.join(missing)}")
                        self.checks_failed += 1
                        all_valid = False
                except Exception:
                    self.print_check(f"{table} not found", False)
                    self.checks_failed += 1
                    all_valid = False
            
            conn.close()
            
            self.add_check_result(
                'star_schema_structure',
                all_valid,
                'Star Schema structure is valid' if all_valid else 'Some tables have issues',
                {'valid': all_valid}
            )
            return all_valid
            
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking schema", False, str(e))
            return False
    
    def verify_transform_logic(self):
        """Check for data cleaning and transformation functions"""
        self.print_section("Check 5: Transform Logic")
        transform_path = self.project_root / 'scripts' / 'transform.py'
        self.total_checks += 1
        
        if not transform_path.exists():
            self.checks_failed += 1
            self.print_check("transform.py not found", False)
            return False
        
        try:
            with open(transform_path, 'r') as f:
                content = f.read()
            
            required_checks = {
                'drop_duplicates': 'Data cleaning - drop_duplicates',
                'dropna': 'Data cleaning - dropna',
                'pd.to_datetime': 'datetime conversion',
                'rate_map': 'Rate code mapping'
            }
            
            all_found = True
            for key, desc in required_checks.items():
                if key in content:
                    self.print_check(f"✅ {desc}", True)
                    self.checks_passed += 1
                else:
                    self.checks_failed += 1
                    all_found = False
                    self.print_check(f"❌ {desc}", False)
            
            self.add_check_result(
                'transform_logic',
                all_found,
                'Transform logic is valid' if all_found else 'Some logic missing',
                {'checks': required_checks}
            )
            return all_found
            
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Error checking transform", False, str(e))
            return False
    
    def save_json_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 3,
            'phase_name': 'Data Transformation',
            'summary': {
                'total_checks': total,
                'passed': self.checks_passed,
                'failed': self.checks_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase3_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 JSON report saved to: {json_file}")
        return report
    
    def save_text_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase3_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 3 VERIFICATION REPORT\n")
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
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 3 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ You are ready to proceed to Phase 4 (Data Loading){Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before proceeding to Phase 4{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        self.print_header("🔍 PHASE 3 VERIFICATION - DATA TRANSFORMATION")
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_transform_script()
        self.verify_duckdb_tables()
        self.verify_trip_analytics_view()
        self.verify_star_schema_structure()
        self.verify_transform_logic()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    try:
        verifier = Phase3Verifier()
        success = verifier.run_all_checks()
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase3_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase3_verification_report.txt{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()