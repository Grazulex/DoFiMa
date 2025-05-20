import os
from pathlib import Path
from dofima.config import load_config
import typer
from rich.table import Table
from rich.console import Console

def create_dotfile(name: str, target_path: str = None, force: bool = False):
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    container_path = dotfiles_dir / name
    container_path.mkdir(parents=True, exist_ok=True)

    # 🧠 Cherche tous les répertoires de type .config/xxx ou .local/yyy
    mount_points = []
    for p in (container_path).rglob("*"):
        if p.is_dir():
            try:
                rel = p.relative_to(container_path)
                if (
                    len(rel.parts) >= 2 and
                    rel.parts[0].startswith(".")  # ex: .config
                ):
                    mount_points.append(rel)
            except ValueError:
                continue

    if mount_points:
        typer.secho(f"📦 App container detected: {name}", fg=typer.colors.CYAN)
        for rel_path in sorted(set(mount_points)):
            source = container_path / rel_path
            target = Path.home() / rel_path

            if target.exists():
                if target.is_symlink():
                    target.unlink()
                    typer.secho(f"🔁 Replaced symlink: {target}", fg=typer.colors.YELLOW)
                elif force:
                    target.unlink(missing_ok=True)
                    typer.secho(f"⚠ Force removed existing: {target}", fg=typer.colors.YELLOW)
                else:
                    typer.secho(f"❌ {target} exists. Use --force to overwrite.", fg=typer.colors.RED)
                    continue

            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source.resolve(), target_is_directory=True)
            typer.secho(f"✅ Linked {target} → {source}", fg=typer.colors.GREEN)
        return

    # 🧱 Fichier simple
    source_path = container_path
    if not source_path.exists():
        if "." in Path(name).name:
            source_path.touch()
            typer.secho(f"📄 Created file: {source_path}", fg=typer.colors.GREEN)
        else:
            source_path.mkdir(parents=True)
            typer.secho(f"📁 Created directory: {source_path}", fg=typer.colors.GREEN)
    else:
        typer.secho(f"📄 Source already exists: {source_path}", fg=typer.colors.YELLOW)

    target = Path(target_path).expanduser() if target_path else Path.home() / f".{name}"
    if target.exists():
        if target.is_symlink():
            target.unlink()
            typer.secho(f"🔁 Replaced symlink: {target}", fg=typer.colors.YELLOW)
        elif force:
            target.unlink()
            typer.secho(f"⚠ Force removed existing file: {target}", fg=typer.colors.YELLOW)
        else:
            typer.secho(f"❌ {target} exists. Use --force to overwrite.", fg=typer.colors.RED)
            raise typer.Exit(1)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source_path.resolve(), target_is_directory=source_path.is_dir())
    typer.secho(f"✅ Linked {target} → {source_path}", fg=typer.colors.GREEN)

def check_status():
    config = load_config()
    dotfiles_dir = Path(config["dotfiles_dir"])
    home = Path.home()

    table = Table(title="DoFiMa Status")
    table.add_column("Source", style="cyan")
    table.add_column("Target", style="magenta")
    table.add_column("Status", style="bold")

    # 1. Scan all items in dotfiles_dir (flat + containers)
    for item in dotfiles_dir.rglob("*"):
        if not item.is_file() and not item.is_dir():
            continue  # Skip weird entries
        rel_path = item.relative_to(dotfiles_dir)

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

        table.add_row(str(rel_path), str(target_path), status)

    Console().print(table)


def unlink_dotfile(name: str):
    target = Path.home() / f".{name}"
    if target.is_symlink():
        target.unlink()
        typer.secho(f"🧹 Unlinked: {target}", fg=typer.colors.GREEN)
    elif target.exists():
        typer.secho(f"⚠ {target} exists but is not a symlink. Skipped.", fg=typer.colors.YELLOW)
    else:
        typer.secho(f"⚠ {target} does not exist.", fg=typer.colors.YELLOW)

