import json
from pathlib import Path
from dofima.tools.output import print_success, print_error

CONFIG_PATH = Path.home() / ".config/dofima/config.json"

def init_config(dotfiles_path: Path, git_repo: str = None):
    dotfiles_path = dotfiles_path.expanduser().resolve()
    dotfiles_path.mkdir(parents=True, exist_ok=True)

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = {"dotfiles_dir": str(dotfiles_path), "sub_dirs": [".config", ".local/share", ".local/state"], "git_repo": git_repo}

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    print_success(f"✔ DoFiMa is now tracking: {dotfiles_path}")

    if git_repo:
        if not git_repo.startswith("https://") and not git_repo.startswith("git@"):
            print_error("❌ Invalid git repository URL. Must start with https:// or git@.")
            return
        try:
            import subprocess
            subprocess.run(["git", "init", str(dotfiles_path)], check=True)
            subprocess.run(["git", "remote", "add", "origin", git_repo], check=True)
            print_success(f"✔ Git repository initialized at: {dotfiles_path}")
        except Exception as e:
            print_error(f"❌ Failed to initialize git repository: {e}")
            return
        print_success(f"✔ Git repository set to: {git_repo}")

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print_error("❌ DoFiMa not initialized. Run `dofima init` first.")
        return
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)