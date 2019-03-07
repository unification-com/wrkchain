import os

from pathlib import Path


def repo_root() -> Path:
    current_script = Path(os.path.abspath(__file__))
    return current_script.parent.parent.parent
