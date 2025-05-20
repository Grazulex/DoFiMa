import os
from pathlib import Path
from dofima.config import load_config
from rich.table import Table
from rich.console import Console
from dofima.tools.output import print_success, print_warning, print_error
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

def link_dotfile(name: str, is_directory: bool = False):
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])

    source_path = dotfiles_dir / name
    if not source_path.is_dir():
        target = Path.home() / f".{name}"
        if is_directory:
            print_error(f"📄 Dotfile {source_path} is a file: and you use the -dir flag.")
        else:
            if target.exists():
                if target.is_symlink():
                    unlink_file(target)
                else:
                    print_error(f"⚠ {target} exists but is not a symlink. Skipped.")
                    return
            link_file(source_path, target)
    else:
        if is_directory:
            #if source_path is a directory like /dotfiles/nvim/ and in this one we have :
            # config.test
            # .config/config2.test
            # .local/config3.test
            # we want to create a symlink in the home directory like :
            # ~/config.test
            # nvim/config.test in the ~/.config/ directory
            # nvim/config.test in the ~/.local/ directory

            # list all files in the directory
            # and create a symlink for each one
            # if the file is a directory, create a symlink in the home directory
            # if the file is a file, create a symlink in the home directory

            files = os.listdir(source_path)
            for file in files:
                file_path = source_path / file
                if file_path.is_dir():
                    target = Path.home() / f".{file}"
                    if target.exists():
                        if target.is_symlink():
                            #target.unlink()
                            print_warning(f"🗑️  Removed existing symlink: {target}")
                        else:
                            print_error(f"⚠ {target} exists but is not a symlink. Skipped.")
                            return
                    #target.symlink_to(file_path, target_is_directory=True)
                    print_success(f"🔗 Created symlink: {target} -> {file_path}")

                else:
                    # create a symlink in the home directory
                    target = Path.home() / f".{file}"
                    if target.exists():
                        if target.is_symlink():
                            unlink_file(target)
                        else:
                            print_error(f"⚠ {target} exists but is not a symlink. Skipped.")
                            return
                    link_file(file_path, target)
        else:
            print_error(f"⚠ {source_path} is a directory. Use --dir option to link.")


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

