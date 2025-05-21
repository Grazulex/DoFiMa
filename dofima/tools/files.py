from pathlib import Path
from dofima.tools.output import print_warning, print_success

def create_file(path: Path, verbose: bool = False):
    path.touch()
    print_success(f"📄 Created file: {path}", verbose)

def link_file(origin: Path, destination: Path, verbose: bool = False):
    destination.symlink_to(origin, target_is_directory=True)
    print_success(f"🔗 Created symlink: {destination} -> {origin}", verbose)

def unlink_file(path: Path, verbose: bool = False):
    path.unlink()
    print_warning(f"🗑️  Removed existing symlink: {path}", verbose)