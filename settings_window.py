import customtkinter as ctk

import autostart

HOURS = [f"{h:02d}" for h in range(24)]
MINUTES = [f"{m:02d}" for m in range(60)]

GREEN = "#8fd99f"
GREEN_BG = ("#dcf3e2", "#1f3324")
GRAY_TEXT = ("gray30", "gray70")
GRAY_BG = ("gray90", "gray17")


def _switch_row(parent, row, label_text, variable, pady):
    row_frame = ctk.CTkFrame(parent, fg_color="transparent")
    row_frame.grid(row=row, column=0, columnspan=3, sticky="we", pady=pady)
    row_frame.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(row_frame, text=label_text, font=("Segoe UI", 13, "bold"), anchor="w").grid(
        row=0, column=0, sticky="w"
    )
    ctk.CTkSwitch(row_frame, text="", variable=variable).grid(row=0, column=1, sticky="e")


def _center(win):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")


def build_settings_window(root, config, scheduler, save_config, on_quit):
    root.title("ShutdownTimer")
    root.resizable(False, False)

    current_hour, current_minute = config["shutdown_time"].split(":")

    frame = ctk.CTkFrame(root, fg_color="transparent")
    frame.pack(padx=24, pady=20)

    ctk.CTkLabel(frame, text="Shut down at", font=("Segoe UI", 12), text_color=("gray30", "gray70")).grid(
        row=0, column=0, columnspan=3, sticky="w", pady=(0, 8)
    )

    hour_var = ctk.StringVar(value=current_hour)
    minute_var = ctk.StringVar(value=current_minute)
    ctk.CTkOptionMenu(frame, variable=hour_var, values=HOURS, width=80).grid(row=1, column=0)
    ctk.CTkLabel(frame, text=":", font=("Segoe UI", 14)).grid(row=1, column=1, padx=6)
    ctk.CTkOptionMenu(frame, variable=minute_var, values=MINUTES, width=80).grid(row=1, column=2)

    activate_var = ctk.BooleanVar(value=config.get("enabled", True))
    _switch_row(frame, 2, "Activate timer", activate_var, pady=(20, 6))

    autostart_var = ctk.BooleanVar(value=autostart.is_autostart_enabled())
    _switch_row(frame, 3, "Start with Windows", autostart_var, pady=(0, 16))

    status_var = ctk.StringVar()
    status_label = ctk.CTkLabel(
        frame,
        textvariable=status_var,
        corner_radius=8,
        wraplength=260,
        justify="left",
        anchor="w",
    )
    status_label.grid(row=4, column=0, columnspan=3, sticky="we", pady=(0, 18), ipady=8, ipadx=10)

    def refresh_status():
        if config.get("enabled", True):
            status_var.set(f"Timer is on — next shutdown around {scheduler.next_target.strftime('%H:%M')}")
            status_label.configure(fg_color=GREEN_BG, text_color=GREEN)
        else:
            status_var.set("Timer is off")
            status_label.configure(fg_color=GRAY_BG, text_color=GRAY_TEXT)

    def on_save():
        scheduler.set_time(f"{hour_var.get()}:{minute_var.get()}")
        config["enabled"] = activate_var.get()
        save_config(config)

        if autostart_var.get():
            autostart.enable_autostart()
        else:
            autostart.disable_autostart()

        refresh_status()

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.grid(row=5, column=0, columnspan=3, sticky="we", pady=(0, 10))
    btn_frame.grid_columnconfigure((0, 1), weight=1)
    ctk.CTkButton(btn_frame, text="Save", command=on_save).grid(row=0, column=0, padx=(0, 5), sticky="we")
    ctk.CTkButton(
        btn_frame, text="Quit", fg_color="transparent", border_width=1, command=on_quit
    ).grid(row=0, column=1, padx=(5, 0), sticky="we")

    ctk.CTkLabel(
        frame,
        text="Closing this window (X) keeps ShutdownTimer running in the tray.\nClick Quit to fully exit.",
        font=("Segoe UI", 10),
        text_color=("gray45", "gray60"),
        justify="left",
    ).grid(row=6, column=0, columnspan=3, sticky="w")

    root.protocol("WM_DELETE_WINDOW", root.withdraw)

    refresh_status()
    _center(root)
    return refresh_status
