import typer

def print_success(message: str):
    """
    Print a success message in green.
    """
    typer.secho(message, fg=typer.colors.GREEN)

def print_warning(message: str):
    """
    Print a warning message in yellow.
    """
    typer.secho(message, fg=typer.colors.YELLOW)

def print_error(message: str):
    """
    Print an error message in red.
    """
    typer.secho(message, fg=typer.colors.RED)