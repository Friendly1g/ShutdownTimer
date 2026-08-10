import sys
import threading
import traceback

from app_paths import get_app_dir

APP_DIR = get_app_dir()
ERROR_LOG = APP_DIR / "error_log.txt"


def main():
    from single_instance import acquire_single_instance_lock

    if not acquire_single_instance_lock():
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "ShutdownTimer",
            "ShutdownTimer is already running — look for its icon near the "
            "clock in the system tray (click the ^ arrow to see hidden icons).",
        )
        root.destroy()
        sys.exit(0)

    import customtkinter as ctk

    from config import load_config, save_config
    from dark_titlebar import apply_dark_titlebar
    from popups import show_10min_warning, show_1min_warning
    from scheduler import Scheduler
    from settings_window import build_settings_window
    from tray import build_tray_icon

    config = load_config()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    apply_dark_titlebar(root)

    def on_warn_10():
        show_10min_warning(root, scheduler.cancel_today)

    def on_warn_1():
        show_1min_warning(root, scheduler.cancel_today)

    scheduler = Scheduler(config, on_warn_10, on_warn_1)

    def do_quit():
        icon.stop()
        root.destroy()

    def open_settings():
        root.deiconify()
        root.lift()
        root.focus_force()

    refresh_status = build_settings_window(root, config, scheduler, save_config, do_quit)

    if "--minimized" in sys.argv:
        root.withdraw()

    icon = build_tray_icon(root, scheduler, open_settings, do_quit)

    try:
        icon.run_detached()
    except AttributeError:
        # Older pystray versions don't have run_detached(); run it in a
        # background thread instead so tkinter keeps the main thread.
        threading.Thread(target=icon.run, daemon=True).start()

    def status_loop():
        refresh_status()
        root.after(1000, status_loop)

    root.after(1000, scheduler.tick, root)
    status_loop()
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # pythonw.exe has no console, so an unhandled error here would
        # otherwise vanish silently. Write it to a file instead.
        ERROR_LOG.write_text(traceback.format_exc(), encoding="utf-8")
        sys.exit(1)
