# verify-phase-6.py

"""
Phase 6: Deployment & Documentation Verification

This script verifies that the project is properly documented,
deployed to GitHub, and ready for production.

Checks performed:
    1. README.md - Verifies README exists and contains required sections
    2. LICENSE - Checks if LICENSE file exists
    3. .gitignore - Verifies .gitignore exists and contains required entries
    4. docker-compose.yml - Checks if docker-compose.yml exists
    5. Screenshots - Verifies screenshots folder has images (32 expected)
    6. Git Repository - Checks if Git is initialized
    7. GitHub Remote - Verifies remote origin is configured
"""

import os
import sys
import json
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


class Phase6Verifier:
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
    
    def verify_readme(self):
        """Check if README.md exists and has required sections"""
        self.print_section("Check 1: README.md")
        readme_path = self.project_root / 'README.md'
        self.total_checks += 1
        
        if readme_path.exists():
            self.checks_passed += 1
            self.print_check("README.md exists", True)
            
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                
                required_sections = [
                    'Project Overview',
                    'Architecture',
                    'Tech Stack',
                    'Quick Start'
                ]
                
                found_sections = []
                missing_sections = []
                
                for section in required_sections:
                    if section in content:
                        found_sections.append(section)
                    else:
                        missing_sections.append(section)
                
                if len(found_sections) >= 3:
                    self.checks_passed += 1
                    self.print_check(f"README sections found", True, f"{len(found_sections)}/{len(required_sections)}")
                    self.add_check_result(
                        'readme',
                        True,
                        f'README.md exists ({lines} lines)',
                        {'lines': lines, 'sections_found': len(found_sections)}
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("README missing sections", False, f"Missing: {', '.join(missing_sections)}")
                    self.add_check_result(
                        'readme',
                        False,
                        'README.md missing sections',
                        {'missing': missing_sections}
                    )
                    return False
            except Exception as e:
                self.checks_failed += 1
                self.print_check("Cannot read README.md", False, str(e))
                self.add_check_result(
                    'readme',
                    False,
                    f'Cannot read README.md: {str(e)}'
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check("README.md NOT found", False)
            self.add_check_result(
                'readme',
                False,
                'README.md not found'
            )
            return False
    
    def verify_license(self):
        """Check if LICENSE exists"""
        self.print_section("Check 2: LICENSE")
        license_path = self.project_root / 'LICENSE'
        self.total_checks += 1
        
        if license_path.exists():
            self.checks_passed += 1
            self.print_check("LICENSE exists", True)
            
            try:
                with open(license_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'MIT License' in content or 'Copyright' in content:
                    self.print_check("License content valid", True)
                    self.add_check_result(
                        'license',
                        True,
                        'LICENSE exists and is valid'
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("License content may be invalid", False)
                    self.add_check_result(
                        'license',
                        False,
                        'LICENSE exists but content may be invalid'
                    )
                    return False
            except Exception as e:
                self.checks_failed += 1
                self.print_check("Cannot read LICENSE", False, str(e))
                return False
        else:
            self.checks_failed += 1
            self.print_check("LICENSE NOT found", False)
            self.add_check_result(
                'license',
                False,
                'LICENSE not found'
            )
            return False
    
    def verify_gitignore(self):
        """Check if .gitignore exists and has required entries"""
        self.print_section("Check 3: .gitignore")
        gitignore_path = self.project_root / '.gitignore'
        self.total_checks += 1
        
        if gitignore_path.exists():
            self.checks_passed += 1
            self.print_check(".gitignore exists", True)
            
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                required_entries = ['venv', '__pycache__', '.env']
                found_entries = [e for e in required_entries if e in content]
                
                if len(found_entries) >= 2:
                    self.checks_passed += 1
                    self.print_check("Good .gitignore entries found", True, f"{len(found_entries)} common entries")
                    self.add_check_result(
                        'gitignore',
                        True,
                        '.gitignore exists with required entries'
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("Few .gitignore entries", False, f"Only {len(found_entries)} common entries")
                    self.add_check_result(
                        'gitignore',
                        False,
                        '.gitignore missing required entries'
                    )
                    return False
            except Exception as e:
                self.checks_failed += 1
                self.print_check("Cannot read .gitignore", False, str(e))
                return False
        else:
            self.checks_failed += 1
            self.print_check(".gitignore NOT found", False)
            self.add_check_result(
                'gitignore',
                False,
                '.gitignore not found'
            )
            return False
    
    def verify_docker_compose(self):
        """Check if docker-compose.yml exists"""
        self.print_section("Check 4: docker-compose.yml")
        docker_path = self.project_root / 'docker-compose.yml'
        self.total_checks += 1
        
        if docker_path.exists():
            self.checks_passed += 1
            self.print_check("docker-compose.yml exists", True)
            
            try:
                with open(docker_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'airflow' in content:
                    self.print_check("Airflow services found", True)
                    self.add_check_result(
                        'docker_compose',
                        True,
                        'docker-compose.yml exists with Airflow services'
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("No Airflow services found", False)
                    self.add_check_result(
                        'docker_compose',
                        False,
                        'docker-compose.yml exists but no Airflow services'
                    )
                    return False
            except Exception as e:
                self.checks_failed += 1
                self.print_check("Cannot read docker-compose.yml", False, str(e))
                return False
        else:
            self.checks_failed += 1
            self.print_check("docker-compose.yml NOT found", False)
            self.add_check_result(
                'docker_compose',
                False,
                'docker-compose.yml not found'
            )
            return False
    
    def verify_screenshots(self):
        """Check if screenshots exist (expected 32)"""
        self.print_section("Check 5: Screenshots")
        screenshots_dir = self.project_root / 'screenshots'
        self.total_checks += 1
        
        if screenshots_dir.exists():
            self.checks_passed += 1
            self.print_check("screenshots/ folder exists", True)
            
            screenshots = list(screenshots_dir.glob('*.png')) + list(screenshots_dir.glob('*.jpg'))
            count = len(screenshots)
            expected_count = 32
            
            if count >= expected_count:
                self.checks_passed += 1
                self.print_check(f"Screenshots count: {count}/{expected_count}", True, "Complete!")
                self.add_check_result(
                    'screenshots',
                    True,
                    f'{count}/{expected_count} screenshots found',
                    {'count': count, 'expected': expected_count}
                )
                return True
            elif count >= 15:
                self.checks_passed += 1
                self.print_check(f"Screenshots count: {count}/{expected_count}", True, "Good progress")
                self.add_check_result(
                    'screenshots',
                    True,
                    f'{count}/{expected_count} screenshots found',
                    {'count': count, 'expected': expected_count}
                )
                return True
            elif count >= 5:
                self.checks_passed += 1
                self.print_check(f"Screenshots count: {count}/{expected_count}", True, "Getting there")
                self.add_check_result(
                    'screenshots',
                    True,
                    f'{count}/{expected_count} screenshots found',
                    {'count': count, 'expected': expected_count}
                )
                return True
            else:
                self.checks_failed += 1
                self.print_check(f"Screenshots count: {count}/{expected_count}", False, f"Need {expected_count} screenshots")
                self.add_check_result(
                    'screenshots',
                    False,
                    f'{count}/{expected_count} screenshots found (need {expected_count})',
                    {'count': count, 'expected': expected_count}
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check("screenshots/ folder NOT found", False)
            self.add_check_result(
                'screenshots',
                False,
                'screenshots/ folder not found'
            )
            return False
    
    def verify_git_repo(self):
        """Check if Git repository is initialized"""
        self.print_section("Check 6: Git Repository")
        git_dir = self.project_root / '.git'
        self.total_checks += 1
        
        if git_dir.exists():
            self.checks_passed += 1
            self.print_check("Git repository initialized", True)
            
            try:
                result = subprocess.run(
                    ['git', 'remote', '-v'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if 'origin' in result.stdout:
                    self.checks_passed += 1
                    self.print_check("Remote origin configured", True)
                    self.add_check_result(
                        'git_repo',
                        True,
                        'Git repository initialized with remote origin'
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("Remote origin NOT configured", False, "💡 git remote add origin ...")
                    self.add_check_result(
                        'git_repo',
                        False,
                        'Git repository initialized but no remote origin'
                    )
                    return False
            except Exception as e:
                self.checks_failed += 1
                self.print_check("Could not check git remote", False, str(e))
                self.add_check_result(
                    'git_repo',
                    False,
                    'Git repository issue'
                )
                return False
        else:
            self.checks_failed += 1
            self.print_check("Git repository NOT found", False, "💡 Run: git init")
            self.add_check_result(
                'git_repo',
                False,
                'Git repository not initialized'
            )
            return False
    
    def verify_github(self):
        """Check GitHub connection"""
        self.print_section("Check 7: GitHub Repository")
        self.total_checks += 1
        
        try:
            result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                url = result.stdout.strip()
                if 'github.com' in url:
                    self.checks_passed += 1
                    self.print_check("GitHub repository connected", True, url)
                    self.add_check_result(
                        'github',
                        True,
                        f'GitHub repository connected: {url}'
                    )
                    return True
                else:
                    self.checks_failed += 1
                    self.print_check("Not a GitHub repository", False, url)
                    self.add_check_result(
                        'github',
                        False,
                        'Remote URL is not GitHub'
                    )
                    return False
            else:
                self.checks_failed += 1
                self.print_check("No remote origin set", False, "💡 git remote add origin ...")
                self.add_check_result(
                    'github',
                    False,
                    'No remote origin configured'
                )
                return False
        except Exception as e:
            self.checks_failed += 1
            self.print_check("Could not check GitHub", False, str(e))
            self.add_check_result(
                'github',
                False,
                'Could not check GitHub connection'
            )
            return False
    
    def save_json_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report = {
            'timestamp': self.timestamp,
            'project_root': str(self.project_root),
            'phase': 6,
            'phase_name': 'Deployment & Documentation',
            'summary': {
                'total_checks': total,
                'passed': self.checks_passed,
                'failed': self.checks_failed,
                'success_rate': round(percentage, 1)
            },
            'checks': self.check_results,
            'overall_status': 'ready' if self.checks_failed == 0 else 'needs_fix'
        }
        
        json_file = self.project_root / 'phase6_verification.json'
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 JSON report saved to: {json_file}")
        return report
    
    def save_text_report(self):
        total = self.checks_passed + self.checks_failed
        percentage = (self.checks_passed / total * 100) if total > 0 else 0
        
        report_file = self.project_root / 'phase6_verification_report.txt'
        with open(report_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PHASE 6 VERIFICATION REPORT\n")
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
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED! Phase 6 is complete!{Colors.END}")
            print(f"{Colors.GREEN}✅ Project is ready for deployment!{Colors.END}")
        else:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}📌 Fix the failed items before final deployment{Colors.END}")
        
        if self.results:
            failed_items = [k for k, v in self.results.items() if v is False]
            if failed_items:
                print(f"\n{Colors.RED}📋 Items requiring attention:{Colors.END}")
                for item in failed_items:
                    print(f"  ❌ {item}")
        
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    
    def run_all_checks(self):
        self.print_header("🔍 PHASE 6 VERIFICATION - DEPLOYMENT & DOCUMENTATION")
        print(f"📂 Project Root: {self.project_root}")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.verify_readme()
        self.verify_license()
        self.verify_gitignore()
        self.verify_docker_compose()
        self.verify_screenshots()
        self.verify_git_repo()
        self.verify_github()
        
        self.generate_summary()
        self.save_json_report()
        self.save_text_report()
        
        return self.checks_failed == 0


def main():
    try:
        verifier = Phase6Verifier()
        success = verifier.run_all_checks()
        print(f"\n{Colors.CYAN}✅ Verification complete!{Colors.END}")
        print(f"{Colors.CYAN}📊 JSON report: phase6_verification.json{Colors.END}")
        print(f"{Colors.CYAN}📄 Text report: phase6_verification_report.txt{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error: {str(e)}{Colors.END}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()