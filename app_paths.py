import sys
from pathlib import Path


def get_app_dir():
    if getattr(sys, "frozen", False):
        # Packaged .exe: anchor to the exe's own folder, not the
        # temp extraction folder PyInstaller unpacks into.
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent
