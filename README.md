# ShutdownTimer

A small Windows app that lives in your system tray and shuts your PC down at
the same time every day, with warnings 10 minutes and 1 minute before.

Open source under the [MIT license](LICENSE) — use it, copy it, change it,
whatever you want.

## Download and run it (no coding needed)

1. Go to the **[Releases page](../../releases)** of this repo (link in the
   right-hand sidebar too, or click "Releases" near the top).
2. Under the latest release, download **`ShutdownTimer.exe`**.
3. Double-click it to run.

**First launch**: Windows will likely show a blue "Windows protected your PC"
SmartScreen warning, since this is a small homemade app without a paid
certificate — that's normal, not a sign anything's wrong. Click **More info**
→ **Run anyway**. It only asks once per copy of the file.

Once it's open, a small dark settings window appears:

- **Shut down at** — pick the hour and minute you want your PC to shut down every day
- **Activate timer** — turn the whole thing on/off; nothing happens while this is off
- **Start with Windows** — turns on Windows auto-launch for the app; it manages its own Startup shortcut, no manual setup needed
- **Save** — remembers everything above so it's still set after a restart
- **Quit** — fully closes the app

Closing the window with the **X** does *not* quit the app — it just hides it
in the system tray so it keeps working in the background. Look for its small
blue clock icon near your clock (click the **^** arrow if it's hidden) and
right-click it for **Open settings**, **Cancel tonight's shutdown**, or **Exit**.

You'll get a popup warning 10 minutes before shutdown, and another 1 minute
before — each has a **Cancel shutdown** button if you change your mind.

## Building it yourself instead

If you'd rather run it from the source code (e.g. to make changes):

```bash
git clone https://github.com/Friendly1g/ShutdownTimer.git
cd ShutdownTimer
pip install -r requirements.txt
python main.pyw
```

Running with `python` (not `pythonw`) keeps a console window open so you can
see errors. To test the 10-min/1-min warnings without waiting all day, open
the settings window and set the time a couple minutes out. To test without
risking a real shutdown, open `scheduler.py` and change `DRY_RUN = False` to
`DRY_RUN = True` — it'll print what it *would* have done instead. Set it
back to `False` afterward.

To package your own `.exe` after making changes:

```bash
pyinstaller --onefile --windowed --name ShutdownTimer --icon=shutdowntimer.ico main.pyw
```

This produces `dist\ShutdownTimer.exe`. If you don't have
`shutdowntimer.ico` yet (or want to regenerate it), run `python
make_icon.py` first — it's a one-off script, not part of the app itself.

## Troubleshooting

If the app doesn't seem to have started (no tray icon, no window), check for
an `error_log.txt` next to wherever you ran it from — any startup crash gets
written there, since the app has no console to show errors in otherwise.

## What's in this folder

- `main.pyw` — entry point: single-instance check, wires everything together
- `app_paths.py` — finds "the folder this app lives in," correctly for both script and packaged-.exe modes
- `single_instance.py` — the "only one copy running at a time" check
- `config.py` — loads/saves `config.json` (your shutdown time + activated state)
- `scheduler.py` — figures out the next shutdown time and fires the warnings/shutdown/cancel
- `settings_window.py` — the main window (time, Activate, auto-start, status, Save/Quit)
- `tray.py` — the system tray icon and right-click menu
- `popups.py` — the 10-min/1-min warning popups
- `dark_titlebar.py` — makes a window's native Windows title bar dark, to match the dark content below it
- `autostart.py` — creates/removes the Windows Startup shortcut for the auto-start checkbox
- `make_icon.py` — one-off script to generate `shutdowntimer.ico` (not run by the app)
- `requirements.txt` — Python packages needed (only relevant if running as a script or building the .exe)
