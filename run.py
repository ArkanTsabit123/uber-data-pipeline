# run.py - Uber ETL Pipeline Runner
# Complete automation script for all project operations

"""
Uber ETL Pipeline - Complete Runner Script
Run: python run.py [command]

Commands:
  - setup        : Complete project setup (venv, dependencies, folders, pipeline files)
  - start        : Start Airflow with Docker
  - stop         : Stop Airflow
  - restart      : Restart Airflow
  - status       : Check Airflow container status
  - logs         : View Airflow logs
  - verify       : Run all verifications (Phase 1-6)
  - verify1-6    : Run specific phase verification
  - trigger      : Trigger Airflow DAG
  - dashboard    : Run Streamlit dashboard
  - structure    : Show project structure
  - clean        : Clean temporary files and reset
  - reset        : Full reset (venv + docker)
  - help         : Show this help message

Examples:
  python run.py setup        # Complete project setup
  python run.py start        # Start Airflow
  python run.py verify       # Run all verifications
  python run.py dashboard    # Run dashboard
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================

ROOT = Path(__file__).parent
VENV_PATH = ROOT / "venv"
PYTHON = VENV_PATH / "Scripts" / "python.exe"
PIP = VENV_PATH / "Scripts" / "pip.exe"
ACTIVATE = VENV_PATH / "Scripts" / "activate"

# ============================================
# COLORS
# ============================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

# ============================================
# UTILITY FUNCTIONS
# ============================================

def run_command(cmd, cwd=None):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd or ROOT, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def run_venv_command(cmd):
    """Run command in virtual environment"""
    full_cmd = f'"{PYTHON}" -c "{cmd}"' if not cmd.startswith("pip") else f'"{PIP}" {cmd}'
    return run_command(full_cmd)

def check_venv():
    """Check if venv exists and is active"""
    return VENV_PATH.exists()

def check_docker():
    """Check if Docker is running"""
    success, _, _ = run_command("docker ps")
    return success

def check_airflow():
    """Check if Airflow containers are running"""
    success, stdout, _ = run_command("docker-compose ps --format json")
    if success and "Up" in stdout:
        return True
    return False

# ============================================
# COMMANDS
# ============================================

def cmd_setup():
    """Complete project setup"""
    print_header("🚀 COMPLETE PROJECT SETUP")
    
    # 1. Create venv
    print_info("Creating virtual environment...")
    success, _, _ = run_command("python -m venv venv")
    if not success:
        print_error("Failed to create venv")
        return False
    print_success("Virtual environment created")
    
    # 2. Activate and install dependencies
    print_info("Installing dependencies...")
    success, _, _ = run_command(f'"{PIP}" install --upgrade pip')
    if not success:
        print_warning("Pip upgrade failed, continuing...")
    
    success, _, _ = run_command(f'"{PIP}" install -r requirements.txt')
    if not success:
        print_error("Failed to install dependencies")
        return False
    print_success("Dependencies installed")
    
    # 3. Run setup scripts
    print_info("Setting up project structure...")
    success, _, _ = run_command(f'"{PYTHON}" setup_project.py')
    if not success:
        print_warning("Setup_project.py failed, continuing...")
    
    print_info("Setting up pipeline files...")
    success, _, _ = run_command(f'"{PYTHON}" setup_pipeline.py')
    if not success:
        print_warning("Setup_pipeline.py failed, continuing...")
    
    print_success("Project setup complete!")
    print_info("Next steps:")
    print("  1. Start Docker Desktop")
    print("  2. Run: python run.py start")
    print("  3. Run: python run.py verify")
    return True

def cmd_start():
    """Start Airflow with Docker"""
    print_header("🐳 STARTING AIRFLOW")
    
    if not check_docker():
        print_error("Docker is not running. Please start Docker Desktop first.")
        return False
    
    print_info("Starting Airflow containers...")
    success, stdout, stderr = run_command("docker-compose up -d")
    
    if success:
        print_success("Airflow started successfully!")
        print_info("Airflow UI: http://localhost:8080")
        print_info("Username: admin, Password: admin")
        return True
    else:
        print_error(f"Failed to start Airflow: {stderr}")
        return False

def cmd_stop():
    """Stop Airflow"""
    print_header("🛑 STOPPING AIRFLOW")
    
    if not check_docker():
        print_warning("Docker is not running")
        return True
    
    print_info("Stopping Airflow containers...")
    success, _, stderr = run_command("docker-compose down")
    
    if success:
        print_success("Airflow stopped successfully!")
        return True
    else:
        print_error(f"Failed to stop Airflow: {stderr}")
        return False

def cmd_restart():
    """Restart Airflow"""
    print_header("🔄 RESTARTING AIRFLOW")
    
    if not cmd_stop():
        return False
    time.sleep(2)
    return cmd_start()

def cmd_status():
    """Check Airflow status"""
    print_header("📊 AIRFLOW STATUS")
    
    if not check_docker():
        print_error("Docker is not running")
        return False
    
    success, stdout, _ = run_command("docker-compose ps")
    if success:
        print(stdout)
        return True
    else:
        print_error("Failed to get status")
        return False

def cmd_logs():
    """View Airflow logs"""
    print_header("📋 AIRFLOW LOGS")
    
    if not check_docker():
        print_error("Docker is not running")
        return False
    
    print_info("Showing logs (Ctrl+C to exit)...")
    run_command("docker-compose logs -f")
    return True

def cmd_verify():
    """Run all verifications"""
    print_header("✅ RUNNING ALL VERIFICATIONS")
    
    phases = [1, 2, 3, 4, 5, 6]
    results = {}
    
    for phase in phases:
        print_info(f"Running Phase {phase}...")
        success, stdout, stderr = run_command(f'"{PYTHON}" verify-phase-{phase}.py')
        results[phase] = success
        
        if success:
            print_success(f"Phase {phase} PASSED")
        else:
            print_error(f"Phase {phase} FAILED")
            if stderr:
                print(f"  Error: {stderr}")
    
    # Summary
    print_header("📊 VERIFICATION SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for phase, success in results.items():
        icon = "✅" if success else "❌"
        color = Colors.GREEN if success else Colors.RED
        print(f"{color}{icon} Phase {phase}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} passed{Colors.END}")
    
    if passed == total:
        print_success("🎉 ALL VERIFICATIONS PASSED!")
        return True
    else:
        print_warning("⚠️ Some verifications failed. Fix them before proceeding.")
        return False

def cmd_verify_phase(phase):
    """Run specific phase verification"""
    print_header(f"✅ RUNNING PHASE {phase} VERIFICATION")
    
    success, stdout, stderr = run_command(f'"{PYTHON}" verify-phase-{phase}.py')
    
    if success:
        print_success(f"Phase {phase} PASSED")
        return True
    else:
        print_error(f"Phase {phase} FAILED")
        if stderr:
            print(f"  Error: {stderr}")
        return False

def cmd_trigger():
    """Trigger Airflow DAG"""
    print_header("🚀 TRIGGERING DAG")
    
    if not check_airflow():
        print_error("Airflow is not running. Run: python run.py start")
        return False
    
    print_info("Triggering DAG: uber_etl_pipeline...")
    success, stdout, stderr = run_command("airflow dags trigger uber_etl_pipeline")
    
    if success:
        print_success("DAG triggered successfully!")
        print_info("Check Airflow UI for progress: http://localhost:8080")
        return True
    else:
        print_error(f"Failed to trigger DAG: {stderr}")
        return False

def cmd_dashboard():
    """Run Streamlit dashboard"""
    print_header("📊 RUNNING DASHBOARD")
    
    print_info("Starting dashboard at http://localhost:8501")
    print_info("Press Ctrl+C to stop...")
    
    run_command(f'"{PYTHON}" -m streamlit run dashboard/app.py')
    return True

def cmd_structure():
    """Show project structure"""
    print_header("📁 PROJECT STRUCTURE")
    
    success, stdout, _ = run_command(f'"{PYTHON}" structure.py')
    if success:
        print(stdout)
        return True
    else:
        print_error("Failed to show structure")
        return False

def cmd_clean():
    """Clean temporary files"""
    print_header("🧹 CLEANING TEMPORARY FILES")
    
    print_info("Removing temporary files...")
    
    files_to_remove = [
        "phase*_verification.json",
        "phase*_verification_report.txt",
        "*.log",
        "*.tmp",
    ]
    
    for pattern in files_to_remove:
        for f in ROOT.glob(pattern):
            try:
                f.unlink()
                print_success(f"Removed: {f.name}")
            except:
                pass
    
    # Clean __pycache__
    for pycache in ROOT.glob("**/__pycache__"):
        try:
            import shutil
            shutil.rmtree(pycache)
            print_success(f"Removed: {pycache}")
        except:
            pass
    
    print_success("Clean complete!")
    return True

def cmd_reset():
    """Full reset"""
    print_header("🔄 FULL RESET")
    
    print_warning("This will delete venv and all Docker containers!")
    response = input("Are you sure? (y/N): ")
    
    if response.lower() != 'y':
        print_info("Reset cancelled.")
        return True
    
    # Stop docker
    print_info("Stopping Docker containers...")
    run_command("docker-compose down -v")
    
    # Delete venv
    print_info("Deleting virtual environment...")
    import shutil
    if VENV_PATH.exists():
        try:
            shutil.rmtree(VENV_PATH)
            print_success("Venv deleted")
        except:
            print_warning("Could not delete venv")
    
    print_success("Reset complete!")
    print_info("Run 'python run.py setup' to start fresh")
    return True

def cmd_help():
    """Show help"""
    print(__doc__)

# ============================================
# MAIN
# ============================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    commands = {
        'setup': cmd_setup,
        'start': cmd_start,
        'stop': cmd_stop,
        'restart': cmd_restart,
        'status': cmd_status,
        'logs': cmd_logs,
        'verify': cmd_verify,
        'verify1': lambda: cmd_verify_phase(1),
        'verify2': lambda: cmd_verify_phase(2),
        'verify3': lambda: cmd_verify_phase(3),
        'verify4': lambda: cmd_verify_phase(4),
        'verify5': lambda: cmd_verify_phase(5),
        'verify6': lambda: cmd_verify_phase(6),
        'trigger': cmd_trigger,
        'dashboard': cmd_dashboard,
        'structure': cmd_structure,
        'clean': cmd_clean,
        'reset': cmd_reset,
        'help': cmd_help,
    }
    
    if command in commands:
        success = commands[command]()
        sys.exit(0 if success else 1)
    else:
        print_error(f"Unknown command: {command}")
        print_info("Run 'python run.py help' for available commands")
        sys.exit(1)

if __name__ == "__main__":
    main()