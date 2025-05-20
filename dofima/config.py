import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".config/dofima/config.json"

def init_config(dotfiles_path: Path):
    dotfiles_path = dotfiles_path.expanduser().resolve()
    dotfiles_path.mkdir(parents=True, exist_ok=True)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = {"dotfiles_dir": str(dotfiles_path)}

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("❌ DoFiMa not initialized. Run `dofima init` first.")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)