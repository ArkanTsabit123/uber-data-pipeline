# run_all_verifications.py
"""
Run All Verifications - Uber ETL Pipeline

This script runs all 6 phase verification scripts sequentially
and displays a summary of results.
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str) -> None:
    """Print formatted header."""
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}\n")


def print_check(text: str, status: bool, detail: str = "") -> None:
    """Print check result with appropriate color."""
    icon = "PASS" if status else "FAIL"
    color = Colors.GREEN if status else Colors.RED
    if detail:
        print(f"{color}{icon} {text}{Colors.END}")
        print(f"   {Colors.CYAN}-> {detail}{Colors.END}")
    else:
        print(f"{color}{icon} {text}{Colors.END}")


def run_verification(phase: int) -> bool:
    """Run a single phase verification script."""
    script = f"verify-phase-{phase}.py"

    if not os.path.exists(script):
        print_check(f"{script} not found", False, "File missing")
        return False

    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Running: {script}{Colors.END}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.END}")

    result = subprocess.run([sys.executable, script], capture_output=False)

    if result.returncode == 0:
        print_check(f"Phase {phase} PASSED", True)
        return True

    print_check(f"Phase {phase} FAILED", False)
    return False


def main() -> None:
    """Main execution function."""
    print_header("UBER ETL PIPELINE - ALL VERIFICATIONS")

    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project: {os.getcwd()}")

    results = {}

    for phase in range(1, 7):
        results[f"Phase {phase}"] = run_verification(phase)

    print_header("VERIFICATION SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for phase, status in results.items():
        icon = "PASS" if status else "FAIL"
        color = Colors.GREEN if status else Colors.RED
        print(f"{color}{icon} {phase}{Colors.END}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} passed{Colors.END}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}All verifications passed! Project is ready!{Colors.END}")
        sys.exit(0)

    print(f"\n{Colors.YELLOW}{Colors.BOLD}Some verifications failed.{Colors.END}")
    print(f"{Colors.YELLOW}Fix the failed items before proceeding{Colors.END}")
    sys.exit(1)


if __name__ == "__main__":
    main()