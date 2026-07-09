# structure.py
# Display project folder structure

"""
Script to display project folder structure (excluding venv and temporary files)
Run: python structure.py
"""

import os
from pathlib import Path


def show_tree(path=".", prefix="", exclude=None):
    """
    Display folder structure as tree
    
    Args:
        path: Root path to display
        prefix: Prefix for tree formatting (used for recursion)
        exclude: List of folder/file names to exclude
    """
    if exclude is None:
        exclude = [
            'venv', '.git', '__pycache__', '.pytest_cache',
            '.vscode', '.idea', 'node_modules',
            '.ssh_tunnel',
            'phase1_verification.json', 'phase2_verification.json',
            'phase3_verification.json', 'phase4_verification.json',
            'phase5_verification.json', 'phase6_verification.json',
            'phase1_verification_report.txt', 'phase2_verification_report.txt',
            'phase3_verification_report.txt', 'phase4_verification_report.txt',
            'phase5_verification_report.txt', 'phase6_verification_report.txt'
        ]
    
    path = Path(path)
    items = [p for p in path.iterdir() if p.name not in exclude]
    
    folders = sorted([p for p in items if p.is_dir()], key=lambda x: x.name.lower())
    files = sorted([p for p in items if p.is_file()], key=lambda x: x.name.lower())
    
    all_items = folders + files
    
    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        
        if item.is_dir():
            print(f"{prefix}{connector}📁 {item.name}/")
            extension = "    " if is_last else "│   "
            show_tree(item, prefix + extension, exclude)
        else:
            print(f"{prefix}{connector}📄 {item.name}")


if __name__ == "__main__":
    print("📁 Project Structure:\n")
    show_tree(".")