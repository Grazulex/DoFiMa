from pathlib import Path
from dofima.tools.output import print_warning, print_success, print_error, print_info


def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print_info(f"📁 Created directory: {path}")

def remove_directory(path: Path):
    path.rmdir()
    print_info(f"🗑️  Removed existing directory: {path}")

def init_directory(name: str, app_name: str = None):
    from dofima.config import load_config
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    if not dotfiles_dir.exists():
        print_error("⚠ Dotfiles directory does not exist. Please initialize DoFiMa first.")
        return
    sub_dirs = config.get("sub_dirs", [])

    source_path = dotfiles_dir / name
    if source_path.exists():
        print_warning(f"⚠ {source_path} already exists. Skipped.")
    else:
        create_directory(source_path)

    for sub_dir in sub_dirs:
        if app_name:
            sub_dir = f"{sub_dir}/{app_name}"
        else:
            sub_dir = f"{sub_dir}/{name}"
        sub_path = source_path / sub_dir
        if not sub_path.exists():
            create_directory(sub_path)
        else:
            print_warning(f"⚠ {sub_path} already exists. Skipped.")