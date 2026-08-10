# ShutdownTimer

A small app that lives in your system tray and shuts your PC down at the
same time every day, with warnings 10 minutes and 1 minute before.

## The easy way: just use the .exe

A ready-to-run copy is at [`dist\ShutdownTimer.exe`](dist/ShutdownTimer.exe).
There's also a shortcut on your Desktop and one in your Startup folder that
both point to it already — you don't need to do anything else to use it.

Double-click the Desktop shortcut (or the exe itself) to open it. A dark,
modern settings window appears (built with a library called CustomTkinter):

- **Shut down at** — Hour and Minute dropdowns for the daily shutdown time
- **Activate timer** — toggle switch; the timer only actually does anything while this is on
- **Start automatically when my PC turns on** — toggle switch; checks whether ShutdownTimer
  is set to auto-launch at login, and lets you turn that on/off. When this
  changes, the app updates its own Startup shortcut for you.
- A status line telling you whether it's on and roughly when it'll fire next
- **Save** — applies and remembers everything above
- **Quit** — fully closes the app

Closing the window with the X does **not** quit the app — it just tucks it
back into the tray so it keeps running in the background. Look for its small
blue clock icon near your clock (click the **^** arrow if you don't see it)
and right-click it for:

- **Open settings** — brings the window back
- **Cancel tonight's shutdown** — skips today only, resumes tomorrow
- **Exit** — fully closes the app

If you try to open ShutdownTimer while it's already running, it'll just show
a short message pointing you to the tray icon instead of opening a second
copy.

The 10-min and 1-min warning popups match the same dark style now too — a
colored icon (amber for the 10-min warning, red for the 1-min one, so it
feels more urgent as the deadline gets closer), a bold heading, and a
"Cancel shutdown" button. The window's title bar is dark-themed as well, so
the whole thing reads as one continuous surface instead of a dark box under
a plain white Windows title bar.

**First time you run the .exe**, Windows may show a blue "Windows protected
your PC" SmartScreen warning if the file was downloaded or copied from
somewhere else (this can happen even between your own folders, since Windows
tracks where a file came from). This is normal for any homemade `.exe`
without a paid certificate — it's not a sign something's wrong. Click
**More info** → **Run anyway**. It only asks once per file. Some antivirus
tools (including Windows Defender) occasionally flag freshly-built
PyInstaller executables as a false positive too — if that happens, check
Windows Security → Protection history and allow/restore the file.

## The developer way: running it as a Python script

Useful if you want to change the code and test your changes without
rebuilding the .exe every time.

```bash
pip install -r requirements.txt
python main.pyw
```

Running with `python` (not `pythonw`) keeps a console window open so you can
see errors. To test the 10-min/1-min warnings without waiting all day, open
the settings window and set the time a couple minutes out. To test without
risking a real shutdown, open `scheduler.py` and change `DRY_RUN = False` to
`DRY_RUN = True` — it'll print what it *would* have done instead. Set it
back to `False` afterward.

## Building the .exe yourself

After making code changes, rebuild with:

```bash
pyinstaller --onefile --windowed --name ShutdownTimer --icon=shutdowntimer.ico main.pyw
```

This produces `dist\ShutdownTimer.exe`. If you don't have
`shutdowntimer.ico` yet (or want to regenerate it), run `python
make_icon.py` first — it's a one-off script, not part of the app itself.

## Troubleshooting

If the app doesn't seem to have started (no tray icon, no window), check
`error_log.txt` next to wherever you ran it from — any startup crash gets
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
