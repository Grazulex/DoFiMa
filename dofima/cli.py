import typer
from dofima.config import init_config
from dofima.dotfile import create_dotfile
from dofima.dotfile import check_status
from dofima.dotfile import unlink_dotfile

from pathlib import Path

app = typer.Typer(help="DoFiMa: Dotfiles Manager")

@app.command()
def init(directory: str = typer.Option(None, "--dir", "-d", help="Dotfiles root directory")):
    """Initialize DoFiMa with a dotfiles directory"""
    dotfiles_path = Path(directory).expanduser().resolve() if directory else Path.cwd()
    init_config(dotfiles_path)
    typer.secho(f"✔ DoFiMa is now tracking: {dotfiles_path}", fg=typer.colors.GREEN)

@app.command()
def new(
    name: str,
    target: str = typer.Option(None, "--target", "-t", help="Target path to symlink to"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite of target file")
):
    """Create a new dotfile and symlink it to the given target"""
    create_dotfile(name, target, force)


@app.command()
def unlink(name: str):
    """Remove the symlink and untrack the dotfile"""
    unlink_dotfile(name)


@app.command()
def status():
    """Show status of all tracked dotfiles"""
    check_status()

