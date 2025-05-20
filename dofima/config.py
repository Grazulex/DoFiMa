import json
from pathlib import Path
from dofima.tools.output import print_success, print_error

CONFIG_PATH = Path.home() / ".config/dofima/config.json"

def init_config(dotfiles_path: Path):
    dotfiles_path = dotfiles_path.expanduser().resolve()
    dotfiles_path.mkdir(parents=True, exist_ok=True)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = {"dotfiles_dir": str(dotfiles_path)}

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print_success(f"✔ DoFiMa is now tracking: {dotfiles_path}")

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print_error("❌ DoFiMa not initialized. Run `dofima init` first.")
        return
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)