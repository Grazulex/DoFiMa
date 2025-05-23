import os
from pathlib import Path
from dofima.config import load_config
from rich.table import Table
from rich.console import Console
from dofima.tools.output import print_error
from dofima.tools.files import link_file, unlink_file

def check_status(name: str):
    """
    Check the status of dotfiles for a given application.
    """
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    skip_dirs = config["skip_dirs"]
    source_path = dotfiles_dir / name
    if not source_path.exists():
        print_error(f"⚠ {source_path} does not exist. Please run command 'new' first.")
        return

    table = Table(title=f"DoFiMa Status of {name}")
    table.add_column("Source", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="bold")

    for entry in compute_symlink_instructions(source_path, skip_dirs):
        from_symlink = Path(entry['source'])
        to_symlink = Path(entry['destination'])
        if os.path.exists(to_symlink):
            if os.path.islink(to_symlink):
                table.add_row(str(from_symlink), "Symlink", str(to_symlink), "[green]Linked[/green]")
            else:
                table.add_row(str(from_symlink), "File", str(to_symlink), "[yellow]Exists but not a symlink[/yellow]")
        else:
            table.add_row(str(from_symlink), "File", str(to_symlink), "[red]Not linked[/red]")


    console = Console()
    console.print(table)

def link_dotfile(name: str):
    """
    Link a dotfile directory to the home directory via symlink.
    """
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    skip_dirs = config["skip_dirs"]
    source_path = dotfiles_dir / name
    if not source_path.exists():
        print_error(f"⚠ {source_path} does not exist. Please run command 'new' first.")
        return

    table = Table(title=f"Linking dotfiles for {name}")
    table.add_column("Source", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="bold")

    for entry in compute_symlink_instructions(source_path, skip_dirs):
        from_symlink = Path(entry['source'])
        to_symlink = Path(entry['destination'])
        if os.path.exists(to_symlink):
            if os.path.islink(to_symlink):
                table.add_row(str(from_symlink), str(to_symlink), "[yellow]Existing [/yellow]")
                continue
            else:
                table.add_row(str(from_symlink), str(to_symlink), "[red]Existing (but not a symlink)[/red]")
                continue
        link_file(from_symlink, to_symlink)
        table.add_row(str(from_symlink), str(to_symlink), "[green]Linked[/green]")

    console = Console()
    console.print(table)

def unlink_dotfile(name: str):
    """
    Unlink a dotfile directory from the home directory.
    """
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    skip_dirs = config["skip_dirs"]
    source_path = dotfiles_dir / name
    if not source_path.exists():
        print_error(f"⚠ {source_path} does not exist. Please run command 'new' first.")
        return

    table = Table(title=f"Unlinking dotfiles for {name}")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="bold")


    for entry in compute_symlink_instructions(source_path, skip_dirs):
        to_symlink = Path(entry['destination'])
        if os.path.exists(to_symlink):
            if os.path.islink(to_symlink):
                unlink_file(to_symlink)
                table.add_row(str(to_symlink), "[green]Unlinked[/green]")
            else:
                table.add_row(str(to_symlink), "[red]Exists but not a symlink[/red]")
                continue
        else:
            table.add_row(str(to_symlink), "[yellow]Not linked[/yellow]")
            continue

    console = Console()
    console.print(table)

def compute_symlink_instructions(source_dir, skip_dirs):
    """
    Generates a list of symlink instructions:
    - Symlinks the folder containing a file if it is under a skip_dir.
    - Directly symlinks files that are outside the skip_dirs.

    :param source_dir: Root directory of the dotfiles
    :param skip_dirs: Directories not to be symlinked themselves (e.g. ['.config', '.local/share'])
    :return: List of dicts {'source', 'destination', 'link_name'}
    """
    instructions = []
    skip_dirs_set = set(os.path.normpath(skip) for skip in skip_dirs)
    seen_targets = set()

    for root, dirs, files in os.walk(source_dir, topdown=True):
        rel_root = os.path.relpath(root, source_dir)
        if rel_root == ".":
            rel_root = ""

        norm_rel_root = os.path.normpath(rel_root)
        for skip in skip_dirs_set:
            if norm_rel_root.startswith(skip + os.sep):
                top = os.path.join(*norm_rel_root.split(os.sep)[:len(skip.split(os.sep)) + 1])
                if top not in seen_targets:
                    instructions.append({
                        "source": os.path.join(source_dir, top),
                        "destination": os.path.join(os.path.expanduser("~"), top),
                        "link_name": os.path.basename(top),
                    })
                    seen_targets.add(top)
                break
        else:
            for name in files:
                file_rel_path = os.path.normpath(os.path.join(norm_rel_root, name))
                if file_rel_path not in seen_targets:
                    instructions.append({
                        "source": os.path.join(source_dir, file_rel_path),
                        "destination": os.path.join(os.path.expanduser("~"), file_rel_path),
                        "link_name": name,
                    })
                    seen_targets.add(file_rel_path)

    return instructions

