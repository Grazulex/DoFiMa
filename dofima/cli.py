import typer
import globals
from dofima.config import init_config
from dofima.tools.directories import init_directory
from dofima.tools.output import print_success
from dofima.dotfile import link_dotfile

from pathlib import Path

app = typer.Typer(help="DoFiMa: Dotfiles Manager")

@app.command()
def init(
    directory: str = typer.Option(None, "--dir", "-d", help="Dotfiles root directory"),
    git_repo: str = typer.Option(None, "--git", "-g", help="Git repository URL"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """Initialize DoFiMa with a dotfiles directory & optionally a git repository"""
    globals.state["verbose"] = verbose
    dotfiles_path = Path(directory).expanduser().resolve() if directory else Path.cwd()
    init_config(dotfiles_path, git_repo)
    print_success(f"✔ DoFiMa initialized at: {dotfiles_path}")

@app.command()
def new(
    name: str = typer.Argument(..., help="Name of the DotFile directory for the application"),
    app_name: str = typer.Option(None, "--app", "-a", help="Name of the application. If not provided, the name will be used"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    globals.state["verbose"] = verbose
    """Create a new dotfile directory for a given application"""
    init_directory(name, app_name)
    print_success(f"📦 Created dotfiles directory: {name}")

@app.command()
def link(
    name: str = typer.Argument(..., help="Name of the DotFile directory for the application"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    globals.state["verbose"] = verbose
    """Link a dotfile directory to the home directory via symlink"""
    link_dotfile(name)
    print_success(f"🔗 Linked dotfiles directory: {name}")
