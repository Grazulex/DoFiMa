from pathlib import Path
from dofima.tools.output import print_warning, print_success, print_error, print_info


def create_directory(path: Path, verbose: bool = False):
    path.mkdir(parents=True, exist_ok=True)
    print_info(f"📁 Created directory: {path}", verbose)

def remove_directory(path: Path, verbose: bool = False):
    path.rmdir()
    print_info(f"🗑️  Removed existing directory: {path}", verbose)

def init_directory(name: str, app_name: str = None, verbose: bool = False):
    from dofima.config import load_config
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    if not dotfiles_dir.exists():
        print_error("⚠ Dotfiles directory does not exist. Please initialize DoFiMa first.", True)
        return
    sub_dirs = config.get("sub_dirs", [])

    source_path = dotfiles_dir / name
    if source_path.exists():
        print_warning(f"⚠ {source_path} already exists. Skipped.", verbose)
    else:
        create_directory(source_path, verbose)

    for sub_dir in sub_dirs:
        if app_name:
            sub_dir = f"{sub_dir}/{app_name}"
        else:
            sub_dir = f"{sub_dir}/{name}"
        sub_path = source_path / sub_dir
        if not sub_path.exists():
            create_directory(sub_path, verbose)
        else:
            print_warning(f"⚠ {sub_path} already exists. Skipped.", verbose)