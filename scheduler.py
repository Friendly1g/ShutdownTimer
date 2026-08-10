import subprocess
from datetime import datetime, timedelta

# Flip to True while testing so it never actually shuts your PC down —
# it just prints what it *would* have done.
DRY_RUN = False


def compute_next_occurrence(hh_mm, now=None):
    now = now or datetime.now()
    hour, minute = map(int, hh_mm.split(":"))
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target


def schedule_shutdown(seconds, message="ShutdownTimer: your PC is shutting down. Save your work!"):
    if DRY_RUN:
        print(f"[DRY RUN] Would run: shutdown /s /f /t {seconds}")
        return
    subprocess.run(["shutdown", "/s", "/f", "/t", str(seconds), "/c", message])


def cancel_shutdown():
    if DRY_RUN:
        print("[DRY RUN] Would run: shutdown /a")
        return
    subprocess.run(["shutdown", "/a"])


class Scheduler:
    def __init__(self, config, on_warn_10, on_warn_1):
        self.config = config
        self.on_warn_10 = on_warn_10
        self.on_warn_1 = on_warn_1
        self.next_target = compute_next_occurrence(config["shutdown_time"])
        self.warned_10 = False
        self.warned_1 = False
        self.skip_today = False

    def set_time(self, hh_mm):
        self.config["shutdown_time"] = hh_mm
        self.next_target = compute_next_occurrence(hh_mm)
        self.warned_10 = False
        self.warned_1 = False
        self.skip_today = False

    def cancel_today(self):
        self.skip_today = True
        cancel_shutdown()

    def tick(self, root):
        now = datetime.now()

        if now >= self.next_target:
            # Either the shutdown just happened (this code won't even run
            # again in that case) or it was cancelled — either way, line up
            # tomorrow's occurrence and reset the flags for a fresh cycle.
            self.next_target = compute_next_occurrence(self.config["shutdown_time"], now)
            self.warned_10 = False
            self.warned_1 = False
            self.skip_today = False
        elif self.config.get("enabled", True) and not self.skip_today:
            if not self.warned_10 and now >= self.next_target - timedelta(minutes=10):
                self.warned_10 = True
                self.on_warn_10()
            elif not self.warned_1 and now >= self.next_target - timedelta(minutes=1):
                self.warned_1 = True
                schedule_shutdown(60)
                self.on_warn_1()

        root.after(1000, self.tick, root)
