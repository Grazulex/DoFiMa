from pathlib import Path
from dofima.tools.output import print_warning, print_success

def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print_success(f"📦 Created directory: {path}")

def remove_directory(path: Path):
    path.rmdir()
    print_warning(f"🗑️  Removed existing directory: {path}")