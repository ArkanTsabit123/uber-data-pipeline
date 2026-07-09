# verify-phase-5.py

"""
Phase 5: Dashboard Development Verification

This script verifies that the Streamlit dashboard is properly set up,
contains all required components, and is accessible.

Checks performed:
    1. Dashboard File - Verifies dashboard/app.py exists
    2. Dashboard Imports - Checks required imports (streamlit, duckdb, pandas, plotly)
    3. Streamlit Installation - Verifies Streamlit is installed
    4. Dashboard Features - Checks for KPI cards, charts, filters, data table
    5. Dashboard Running - Verifies dashboard is accessible at http://localhost:8501
    6. DuckDB Connection - Checks if dashboard connects to database
"""

import os
import sys
import json
import importlib.util
import subprocess
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


class Phase5Verifier:
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
    
    def verify_dashboard_file(self):
        """Check if dashboard file exists"""
        self.print_section("Check 1: Dashboard File")
        dashboard_path = self.project_root / 'dashboard' / 'app.py'
        self.total_checks += 1
        
        if dashboard_path.exists():
            self.checks_passed += 1
            self.print_check("dashboard/app.py exists", True)
            
            try:
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                
                self.print_check(f"File size: {lines} lines", True)
                self.add_check_result(
                    'dashboard_file',
                    True,
                    f'dashboard/app.py exists ({lines} lines)',
                    {'lines': lines}
                )
                return True
            except Exception as e:
                self.checks_failed += 1
                self.print_check("dashboard/app.py exists but cannot be read", False, str(e))
                self.add_check_result(
                    'dashboard_file',
                    False,
                    f'Cannot read dashboard/app.py: {str(e)}'
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check("dashboard/app.py NOT found", False, "Create dashboard/app.py")
            self.add_check_result(
                'dashboard_file',
                False,
                'dashboard/app.py not found',
                {'expected_path': 'dashboard/app.py'}
            )
            return False
    
    def verify_dashboard_imports(self):
        """Check if all required imports are present"""
        self.print_section("Check 2: Dashboard Imports")
        dashboard_path = self.project_root / 'dashboard' / 'app.py'
        self.total_checks += 1
        
        if not dashboard_path.exists():
            self.checks_failed += 1
            self.print_check("dashboard/app.py not found", False)
            return False
        
        try:
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_imports = ['streamlit', 'duckdb', 'pandas', 'plotly']
            found_imports = []
            missing_imports = []
            
            for imp in required_imports:
                if f'import {imp}' in content or f'from {imp}' in content:
                    found_imports.append(imp)
                else:
                    missing_imports.append(imp)
            
            if not missing_imports:
                self.checks_passed += 1
                self.print_check("All imports found", True, f"{', '.join(found_imports)}")
                self.add_check_result(
                    'dashboard_imports',
                    True,
                    'All required imports present',
                    {'imports': found_imports}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("Missing imports", False, f"Missing: {', '.join(missing_imports)}")
                self.add_check_result(
                    'dashboard_imports',
                    False,
                    'Some imports missing',
                    {'found': found_imports, 'missing': missing_imports}
                )
                return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Cannot read dashboard file", False, str(e))
            return False
    
    def verify_streamlit_installed(self):
        """Check if Streamlit is installed"""
        self.print_section("Check 3: Streamlit Installation")
        self.total_checks += 1
        
        try:
            import streamlit
            import pkg_resources
            version = pkg_resources.get_distribution('streamlit').version
            
            self.checks_passed += 1
            self.print_check(f"Streamlit installed", True, f"v{version}")
            self.add_check_result(
                'streamlit_installed',
                True,
                f'Streamlit v{version} installed',
                {'version': version}
            )
            return True
            
        except ImportError:
            self.checks_failed += 1
            self.print_check("Streamlit NOT installed", False, "💡 Run: pip install streamlit")
            self.add_check_result(
                'streamlit_installed',
                False,
                'Streamlit not installed'
            )
            return False
    
    def verify_dashboard_features(self):
        """Check for dashboard features"""
        self.print_section("Check 4: Dashboard Features")
        dashboard_path = self.project_root / 'dashboard' / 'app.py'
        self.total_checks += 1
        
        if not dashboard_path.exists():
            self.checks_failed += 1
            self.print_check("dashboard/app.py not found", False)
            return False
        
        try:
            with open(dashboard_path, 'r', encoding='utf-8') as f:
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
            
            found_features = []
            missing_features = []
            
            for key, desc in features.items():
                if key in content:
                    found_features.append(desc)
                else:
                    missing_features.append(desc)
            
            if len(found_features) >= 5:
                self.checks_passed += 1
                self.print_check(f"Dashboard features found", True, f"{len(found_features)}/7 features")
                for feature in found_features:
                    self.print_check(f"  ✅ {feature}", True)
                self.add_check_result(
                    'dashboard_features',
                    True,
                    f'{len(found_features)}/7 features found',
                    {'found': found_features, 'missing': missing_features}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check(f"Missing dashboard features", False, f"Only {len(found_features)}/7 features")
                for feature in missing_features:
                    self.print_check(f"  ❌ {feature}", False)
                self.add_check_result(
                    'dashboard_features',
                    False,
                    f'{len(found_features)}/7 features found',
                    {'found': found_features, 'missing': missing_features}
                )
                return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Cannot read dashboard file", False, str(e))
            return False
    
    def verify_dashboard_running(self):
        """Check if dashboard is running"""
        self.print_section("Check 5: Dashboard Running")
        self.total_checks += 1
        
        try:
            import urllib.request
            import urllib.error
            
            url = 'http://localhost:8501'
            req = urllib.request.Request(url, method='HEAD')
            
            try:
                response = urllib.request.urlopen(req, timeout=3)
                if response.getcode() == 200:
                    self.checks_passed += 1
                    self.print_check("Dashboard is running", True, "http://localhost:8501")
                    self.add_check_result(
                        'dashboard_running',
                        True,
                        'Dashboard is accessible',
                        {'url': url}
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("Dashboard returned error", False, f"Status: {response.getcode()}")
                    return False
            except urllib.error.URLError:
                self.checks_failed += 1
                self.print_check("Dashboard NOT running", False, "💡 Run: streamlit run dashboard/app.py")
                self.add_check_result(
                    'dashboard_running',
                    False,
                    'Dashboard not accessible'
                )
                return False
                
        except Exception:
            self.checks_failed += 1
            self.print_check("Cannot check dashboard", False, "💡 Run: streamlit run dashboard/app.py")
            self.add_check_result(
                'dashboard_running',
                False,
                'Cannot check dashboard'
            )
            return False
    
    def verify_duckdb_connection_in_dashboard(self):
        """Check if dashboard connects to DuckDB"""
        self.print_section("Check 6: DuckDB Connection")
        dashboard_path = self.project_root / 'dashboard' / 'app.py'
        self.total_checks += 1
        
        if not dashboard_path.exists():
            self.checks_failed += 1
            self.print_check("dashboard/app.py not found", False)
            return False
        
        try:
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'duckdb.connect' in content:
                self.checks_passed += 1
                self.print_check("DuckDB connection configured", True)
                self.add_check_result(
                    'duckdb_connection_dashboard',
                    True,
                    'DuckDB connection configured in dashboard'
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check("DuckDB connection NOT found", False)
                self.add_check_result(
                    'duckdb_connection_dashboard',
                    False,
                    'DuckDB connection not found in dashboard'
                )
                return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Cannot read dashboard file", False, str(e))
            return False
    
    def save_json_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 5,
            'phase_name': 'Dashboard Development',
            'summary': {
                'total_checks': total,
                'passed': self.checks_passed,
                'failed': self.checks_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase5_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 JSON report saved to: {json_file}")
        return report
    
    def save_text_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase5_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 5 VERIFICATION REPORT\n")
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
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 5 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ You are ready to proceed to Phase 6 (Deployment){Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before proceeding to Phase 6{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        self.print_header("🔍 PHASE 5 VERIFICATION - DASHBOARD DEVELOPMENT")
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_dashboard_file()
        self.verify_dashboard_imports()
        self.verify_streamlit_installed()
        self.verify_dashboard_features()
        self.verify_dashboard_running()
        self.verify_duckdb_connection_in_dashboard()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    try:
        verifier = Phase5Verifier()
        success = verifier.run_all_checks()
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase5_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase5_verification_report.txt{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()