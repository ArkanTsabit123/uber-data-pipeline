import os
from pathlib import Path

def show_tree(path=".", prefix="", exclude=None):
    if exclude is None:
        exclude = ['venv', '.git', '__pycache__', '.pytest_cache', '.vscode', '.idea', 'node_modules']
    
    path = Path(path)
    items = [p for p in path.iterdir() if p.name not in exclude]
    
    folders = [p for p in items if p.is_dir()]
    files = [p for p in items if p.is_file()]
    
    # Sort
    folders.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    
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