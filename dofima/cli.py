import typer
from dofima.config import init_config
from dofima.tools.directories import init_directory
from dofima.dotfile import create_dotfile
from dofima.dotfile import check_status
from dofima.dotfile import unlink_dotfile
from dofima.dotfile import link_dotfile

from pathlib import Path

app = typer.Typer(help="DoFiMa: Dotfiles Manager")

@app.command()
def init(
    directory: str = typer.Option(None, "--dir", "-d", help="Dotfiles root directory"),
    git_repo: str = typer.Option(None, "--git", "-g", help="Git repository URL"),
):
    """Initialize DoFiMa with a dotfiles directory & optionally a git repository"""
    dotfiles_path = Path(directory).expanduser().resolve() if directory else Path.cwd()
    init_config(dotfiles_path, git_repo)

@app.command()
def new(
    name: str = typer.Argument(..., help="Name of the DotFile directory for the application"),
    app_name: str = typer.Option(None, "--app", "-a", help="Name of the application. If not provided, the name will be used"),
):
    """Create a new dotfile directory for a given application"""
    init_directory(name, app_name)

@app.command()
def link(
    name: str = typer.Argument(..., help="Name of the DotFile directory for the application"),
):
    """Link a dotfile directory to the home directory via symlink"""
    link_dotfile(name)