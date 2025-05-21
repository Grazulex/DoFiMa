from pathlib import Path

def create_file(path: Path):
    """
    Create a file at the specified path. If the file already exists, it will be ignored.
    """
    path.touch()

def link_file(origin: Path, destination: Path):
    """
    Link a file or directory to the destination via symlink.
    """
    destination.symlink_to(origin, target_is_directory=True)

def unlink_file(path: Path):
    """
    Unlink a file or directory from the destination.
    """
    path.unlink()
