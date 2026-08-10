import os
import sys
from pathlib import Path

from app_paths import get_app_dir

STARTUP_DIR = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
SHORTCUT_PATH = STARTUP_DIR / "ShutdownTimer.lnk"


def _target_and_args():
    # --minimized: main.pyw checks for this and starts in the tray instead
    # of showing the settings window, since a login auto-launch shouldn't
    # pop a window in your face every time you sign in.
    if getattr(sys, "frozen", False):
        return sys.executable, "--minimized"
    # Running as a script: launch through pythonw.exe (no console window)
    # rather than whatever interpreter happened to start this process.
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw.exists():
        pythonw = Path(sys.executable)
    script = get_app_dir() / "main.pyw"
    return str(pythonw), f'"{script}" --minimized'


def is_autostart_enabled():
    return SHORTCUT_PATH.exists()


def enable_autostart():
    import win32com.client

    target, args = _target_and_args()
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(str(SHORTCUT_PATH))
    shortcut.TargetPath = target
    shortcut.Arguments = args
    shortcut.WorkingDirectory = str(get_app_dir())
    shortcut.Description = "ShutdownTimer - daily PC shutdown with warnings"
    shortcut.Save()


def disable_autostart():
    if SHORTCUT_PATH.exists():
        SHORTCUT_PATH.unlink()
