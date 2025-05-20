import typer
from dofima.config import init_config
from dofima.dotfile import create_dotfile
from dofima.dotfile import check_status
from dofima.dotfile import unlink_dotfile
from dofima.dotfile import link_dotfile

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
    is_directory : bool = typer.Option(None, "--dir", "-d", help="Dotfiles is a directory"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite of existing dotfile/directory"),
):
    """Create a new dotfile and symlink it"""
    create_dotfile(name, is_directory, force)


@app.command()
def unlink(
    name: str,
    is_directory : bool = typer.Option(None, "--dir", "-d", help="Dotfiles is a directory"),
):
    """Remove the symlink and untrack the dotfile"""
    unlink_dotfile(name, is_directory)

@app.command()
def link(
    name: str,
    is_directory : bool = typer.Option(None, "--dir", "-d", help="Dotfiles is a directory"),
):
    """Create the symlink and track the dotfile"""
    link_dotfile(name, is_directory)


@app.command()
def status():
    """Show status of all tracked dotfiles"""
    check_status()

