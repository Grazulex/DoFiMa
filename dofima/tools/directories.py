from pathlib import Path
from dofima.tools.output import print_error
from rich.table import Table
from rich.console import Console


def create_directory(path: Path):
    """
    Create a directory at the specified path. If the directory already exists, it will be ignored.
    """
    path.mkdir(parents=True, exist_ok=True)

def remove_directory(path: Path):
    """
    Remove a directory at the specified path. If the directory does not exist, it will be ignored.
    """
    path.rmdir()

def init_directory(name: str, app_name: str = None):
    """
    Initialize a directory for a given application. If the directory already exists, it will be ignored.
    """
    from dofima.config import load_config
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    if not dotfiles_dir.exists():
        print_error("⚠ Dotfiles directory does not exist. Please initialize DoFiMa first.")
        return
    sub_dirs = config.get("sub_dirs", [])

    table = Table(title=f"Initialization of directory {name}")
    table.add_column("Directory", style="cyan")
    table.add_column("Status", style="green")

    source_path = dotfiles_dir / name
    if source_path.exists():
        table.add_row(str(source_path), "⚠ Directory already exists (ignored)")
    else:
        create_directory(source_path)
        table.add_row(str(source_path), "✅ Created")

    for sub_dir in sub_dirs:
        if app_name:
            sub_dir = f"{sub_dir}/{app_name}"
        else:
            sub_dir = f"{sub_dir}/{name}"
        sub_path = source_path / sub_dir
        if not sub_path.exists():
            create_directory(sub_path)
            table.add_row(str(sub_path), "✅ Created")
        else:
            table.add_row(str(sub_path), "⚠ Directory already exists (ignored)")

    console = Console()
    console.print(table)
