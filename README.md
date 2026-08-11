# ShutdownTimer

Shuts your PC down at a set time every day, with warnings 10 and 1 minute before.

Open source under the [MIT license](LICENSE).

## Get it

Download `ShutdownTimer.exe` from [Releases](../../releases) and run it.
(First launch may trigger a SmartScreen warning — click **More info** →
**Run anyway**.)

Set your time, turn on **Activate timer**, hit **Save**. Closing the window
just minimizes it to the tray — right-click the tray icon to reopen it,
cancel tonight's shutdown, or exit.

## Build from source

```bash
git clone https://github.com/Friendly1g/ShutdownTimer.git
cd ShutdownTimer
pip install -r requirements.txt
python main.pyw
```

Package your own `.exe`:

```bash
pyinstaller --onefile --windowed --name ShutdownTimer --icon=shutdowntimer.ico main.pyw
```
