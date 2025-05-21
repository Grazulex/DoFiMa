from pathlib import Path

def create_file(path: Path):
    path.touch()

def link_file(origin: Path, destination: Path):
    destination.symlink_to(origin, target_is_directory=True)

def unlink_file(path: Path):
    path.unlink()
