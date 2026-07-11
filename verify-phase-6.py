# verify-phase-6.py
"""
Phase 6: Deployment & Documentation Verification

This script verifies all components related to Phase 6 of the
Uber ETL Pipeline project.

Checks performed:
    - README.md exists with required sections
    - LICENSE exists and is valid
    - .gitignore exists with required entries
    - docker-compose.yml exists with Airflow services
    - Screenshots folder exists with images
    - Git repository is initialized
    - GitHub remote is configured
"""

import os
import sys
import json
import subprocess
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
# Phase 6: Deployment & Documentation
# ============================================

class Phase6Verifier(PhaseVerifier):
    """Verifier for Phase 6: Deployment & Documentation."""

    def __init__(self):
        super().__init__(6, "Deployment & Documentation")

    def check_readme(self) -> bool:
        """Check if README.md exists with required sections."""
        self.print_section("README.md")

        readme_path = self.project_root / 'README.md'
        exists = readme_path.exists()

        if not exists:
            self.print_check("README.md NOT found", False)
            self.add_result('readme', False, 'README.md not found')
            return False

        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = ['Project Overview', 'Architecture', 'Tech Stack', 'Quick Start']
        found = [s for s in required_sections if s in content]

        has_enough = len(found) >= 3
        self.print_check("README.md exists", True, f"{len(found)}/{len(required_sections)} sections found")

        for section in found:
            self.print_check(f"  {section}", True)

        self.add_result('readme', has_enough, f'README.md has {len(found)}/{len(required_sections)} sections')
        return has_enough

    def check_license(self) -> bool:
        """Check if LICENSE exists and is valid."""
        self.print_section("LICENSE")

        license_path = self.project_root / 'LICENSE'
        exists = license_path.exists()

        if not exists:
            self.print_check("LICENSE NOT found", False)
            self.add_result('license', False, 'LICENSE not found')
            return False

        with open(license_path, 'r', encoding='utf-8') as f:
            content = f.read()

        valid = 'MIT License' in content or 'Copyright' in content
        self.print_check("LICENSE exists", valid)

        self.add_result('license', valid, 'LICENSE valid' if valid else 'LICENSE may be invalid')
        return valid

    def check_gitignore(self) -> bool:
        """Check if .gitignore exists with required entries."""
        self.print_section(".gitignore")

        gitignore_path = self.project_root / '.gitignore'
        exists = gitignore_path.exists()

        if not exists:
            self.print_check(".gitignore NOT found", False)
            self.add_result('gitignore', False, '.gitignore not found')
            return False

        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required = ['venv', '__pycache__', '.env']
        found = [e for e in required if e in content]

        has_enough = len(found) >= 2
        self.print_check(".gitignore exists", has_enough, f"{len(found)}/{len(required)} entries found")

        for entry in found:
            self.print_check(f"  {entry}", True)

        self.add_result('gitignore', has_enough, f'.gitignore has {len(found)}/{len(required)} entries')
        return has_enough

    def check_docker_compose(self) -> bool:
        """Check if docker-compose.yml exists with Airflow services."""
        self.print_section("docker-compose.yml")

        compose_path = self.project_root / 'docker-compose.yml'
        exists = compose_path.exists()

        if not exists:
            self.print_check("docker-compose.yml NOT found", False)
            self.add_result('docker_compose', False, 'docker-compose.yml not found')
            return False

        with open(compose_path, 'r', encoding='utf-8') as f:
            content = f.read()

        has_airflow = 'airflow' in content
        self.print_check("docker-compose.yml exists", has_airflow, "Airflow services found" if has_airflow else "No Airflow services")

        self.add_result('docker_compose', has_airflow, 'docker-compose.yml valid' if has_airflow else 'docker-compose.yml missing Airflow')
        return has_airflow

    def check_screenshots(self) -> bool:
        """Check if screenshots exist."""
        self.print_section("Screenshots")

        screenshots_dir = self.project_root / 'screenshots'

        if not screenshots_dir.exists():
            self.print_check("screenshots/ folder NOT found", False)
            self.add_result('screenshots', False, 'screenshots/ folder not found')
            return False

        screenshots = list(screenshots_dir.glob('*.png')) + list(screenshots_dir.glob('*.jpg'))
        count = len(screenshots)
        expected = 32

        has_enough = count >= 15
        self.print_check(f"Screenshots count", has_enough, f"{count}/{expected}")

        self.add_result('screenshots', has_enough, f'{count}/{expected} screenshots found')
        return has_enough

    def check_git_repo(self) -> bool:
        """Check if Git repository is initialized."""
        self.print_section("Git Repository")

        git_dir = self.project_root / '.git'
        exists = git_dir.exists()

        if not exists:
            self.print_check("Git repository NOT found", False, "Run: git init")
            self.add_result('git_repo', False, 'Git repository not initialized')
            return False

        self.print_check("Git repository initialized", True)

        try:
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True, timeout=5)
            has_remote = 'origin' in result.stdout
            self.print_check("Remote origin configured", has_remote)
            self.add_result('git_repo', has_remote, 'Git repo ready' if has_remote else 'No remote origin')
            return has_remote
        except:
            self.print_check("Could not check remote", False)
            self.add_result('git_repo', False, 'Could not check git remote')
            return False

    def check_github(self) -> bool:
        """Check GitHub connection."""
        self.print_section("GitHub Repository")

        try:
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                url = result.stdout.strip()
                is_github = 'github.com' in url
                self.print_check("GitHub repository connected", is_github, url if is_github else "Not GitHub")
                self.add_result('github', is_github, f'GitHub repo: {url}' if is_github else 'Not a GitHub repo')
                return is_github
            else:
                self.print_check("No remote origin set", False)
                self.add_result('github', False, 'No remote origin')
                return False
        except:
            self.print_check("Could not check GitHub", False)
            self.add_result('github', False, 'Could not check GitHub')
            return False

    def run(self) -> bool:
        """Run all Phase 6 checks."""
        self.check_readme()
        self.check_license()
        self.check_gitignore()
        self.check_docker_compose()
        self.check_screenshots()
        self.check_git_repo()
        self.check_github()

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
        verifier = Phase6Verifier()
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