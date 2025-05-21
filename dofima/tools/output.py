import typer

def print_success(message: str, verbose: bool = False):
    """
    Print a success message in green.
    """
    if verbose:
        typer.secho(message, fg=typer.colors.GREEN)

def print_warning(message: str, verbose: bool = False):
    """
    Print a warning message in yellow.
    """
    if verbose:
        typer.secho(message, fg=typer.colors.YELLOW)

def print_error(message: str, verbose: bool = False):
    """
    Print an error message in red.
    """
    if verbose:
        typer.secho(message, fg=typer.colors.RED)

def print_info(message: str, verbose: bool = False):
    """
    Print an info message in blue.
    """
    if verbose:
        typer.secho(message, fg=typer.colors.BLUE)