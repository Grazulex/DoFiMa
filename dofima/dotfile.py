import os
from pathlib import Path
from dofima.config import load_config
from rich.table import Table
from rich.console import Console
from dofima.tools.output import print_warning, print_error
from dofima.tools.files import create_file, link_file, unlink_file
from dofima.tools.directories import create_directory, remove_directory

def create_dotfile(name: str, is_directory: bool = False, force: bool = False):
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])

    source_path = dotfiles_dir / name

    if is_directory:
        print_warning(f"📦 Dotfile is a directory: {source_path}")
    else:
        print_warning(f"📄 Dotfile is a file: {source_path}")

    if source_path.exists() and not force:
        print_warning(f"⚠ {source_path} already exists. Use --force to overwrite.")
        return
    elif source_path.exists() and force:
        print_warning(f"⚠ {source_path} already exists. Overwriting...")
        #remove symlink (target_path) if it exists
        if is_directory:
            remove_directory(source_path)
            create_directory(source_path)
        else:
            unlink_file(source_path)
            create_file(source_path)
    else:
        if is_directory:
            create_directory(source_path)
        else:
            create_file(source_path)

    #if not is_directory, create a symlink to the ~/ directory
    target_path = Path.home() / f".{name}"
    if not is_directory:
        if target_path.exists():
            if target_path.is_symlink():
                unlink_file(target_path)
            else:
                print_error(f"⚠ {target_path} exists but is not a symlink. Skipped.")
                return
        link_file(source_path, target_path)
    else:
        print_error(f"📦 {source_path} is a directory. When content is done, use ""link"" command to create symlink")


def check_status():
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    home = Path.home()

    table = Table(title="DoFiMa Status")
    table.add_column("Source", style="cyan")
    table.add_column("Type", style="yellow")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="bold")

    # 1. Scan all items in dotfiles_dir (flat + containers)
    for item in dotfiles_dir.rglob("*"):
        if not item.is_file() and not item.is_dir():
            continue  # Skip weird entries
        rel_path = item.relative_to(dotfiles_dir)

        #check if dir
        if item.is_dir():
            is_dir = "[blue]📦 Directory"
        else:
            is_dir = "[yellow]📄 File"

        # Skip anything like README, .git, etc. unless nested under a container
        if rel_path.parts[0].startswith(".") and len(rel_path.parts) == 1 and item.is_file():
            continue

        # Only target entries in .config/, .local/, or top-level dotfiles
        if rel_path.parts[0].startswith("."):
            # Ex: vim/.config/nvim/init.lua → ~/.config/nvim/init.lua
            target_path = home / Path(*rel_path.parts)
        else:
            # Ex: zshrc → ~/.zshrc
            target_path = home / f".{rel_path}"

        source = item.resolve()



        if not target_path.exists():
            status = "[red]❌ Missing"
        elif not target_path.is_symlink():
            status = "[yellow]⚠ Not a symlink"
        elif os.path.realpath(target_path) != str(source):
            status = "[red]❌ Wrong target"
        else:
            status = "[green]✅ OK"

        table.add_row(str(rel_path), str(is_dir), str(target_path), status)

    Console().print(table)

def link_dotfile(name: str, verbose: bool = False):
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    skip_dirs = config["skip_dirs"]
    target_path = Path.home()
    source_path = dotfiles_dir / name
    if not source_path.exists():
        print_error(f"⚠ {source_path} does not exist. Please run command 'new' first.", True)
        return
    #link files in root source_path
    for (file_names) in os.listdir(source_path):
        if os.path.isfile(os.path.join(source_path, file_names)):
            from_file = source_path /f"{file_names}"
            to_file = target_path / f"{file_names}"
            if os.path.exists(to_file):
                if os.path.islink(to_file):
                    unlink_file(to_file, verbose)
                else:
                    print_error(f"⚠ {to_file} exists but is not a symlink. Skipped.", verbose)
                    continue
            #link_file(from_file,to_file)

    #link directories (after skip_dirs) in source_path
    for entry in compute_symlink_instructions(source_path, skip_dirs):
        from_symlink = Path(entry['source'])
        to_symlink = Path(entry['destination'])
        if os.path.exists(to_symlink):
            if os.path.islink(to_symlink):
                unlink_file(to_symlink, verbose)
            else:
                print_error(f"⚠ {to_symlink} exists but is not a symlink. Skipped.", verbose)
                continue
        link_file(from_symlink, to_symlink, verbose)



def unlink_dotfile(name: str, is_directory: bool = False):
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])

    source_path = dotfiles_dir / name
    # Check if source_path is a directory
    if not source_path.is_dir():
        target = Path.home() / f".{name}"
        if target.is_symlink():
            unlink_file(target)
        elif target.exists():
            print_error(f"⚠ {target} exists but is not a symlink. Skipped.")
        else:
            print_error(f"⚠ {target} does not exist.")
    else:
        if is_directory:
            target = Path.home() / f".{name}"
            if target.is_symlink():
                unlink_file(target)
            elif target.exists():
                print_error(f"⚠ {target} exists but is not a symlink. Skipped.")
            else:
                print_error(f"⚠ {target} does not exist.")
        else:
            print_error(f"⚠ {source_path} is a directory. Use --dir option to unlink.")


def compute_symlink_instructions(source_dir, skip_dirs):
    """
    Génère une liste d'instructions de symlink :
    - Symlink le dossier contenant un fichier s'il est sous un skip_dir.
    - Symlink directement les fichiers qui sont en dehors des skip_dirs.

    :param source_dir: Répertoire racine des dotfiles
    :param skip_dirs: Répertoires à ne pas symlinker eux-mêmes (ex: ['.config', '.local/share'])
    :return: Liste de dicts {'source', 'destination', 'link_name'}
    """
    instructions = []
    skip_dirs_set = set(os.path.normpath(skip) for skip in skip_dirs)
    seen_targets = set()

    for root, dirs, files in os.walk(source_dir, topdown=True):
        rel_root = os.path.relpath(root, source_dir)
        if rel_root == ".":
            rel_root = ""

        norm_rel_root = os.path.normpath(rel_root)

        # Cas : sous un skip_dir → on symlink le dossier parent du fichier
        for skip in skip_dirs_set:
            if norm_rel_root.startswith(skip + os.sep):
                # Ex: .local/share/nvim → on symlink .local/share/nvim une fois
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
            # Fichiers hors skip_dirs → symlink un par un
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

