import customtkinter as ctk
from PIL import Image, ImageDraw

from dark_titlebar import apply_dark_titlebar

AMBER = "#f2a93c"
AMBER_BG = "#4a3410"
RED = "#e2504a"
RED_BG = "#4a1414"


def _center(win):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")


def _make_warning_icon(color):
    size = 96
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    mid = size / 2
    # exclamation mark
    draw.rounded_rectangle((mid - 6, size * 0.22, mid + 6, size * 0.62), radius=6, fill=color)
    draw.ellipse((mid - 6, size * 0.72, mid + 6, size * 0.84), fill=color)
    return img


def _make_warning_popup(root, heading, message, bg_color, icon_color, on_cancel, auto_close_ms=30000):
    win = ctk.CTkToplevel(root)
    win.title("ShutdownTimer")
    win.attributes("-topmost", True)
    win.resizable(False, False)
    apply_dark_titlebar(win)

    frame = ctk.CTkFrame(win, fg_color="transparent")
    frame.pack(padx=28, pady=24)

    icon_holder = ctk.CTkFrame(frame, width=52, height=52, corner_radius=26, fg_color=bg_color)
    icon_holder.pack(pady=(0, 14))
    icon_holder.pack_propagate(False)
    icon_image = ctk.CTkImage(light_image=_make_warning_icon(icon_color), size=(24, 24))
    ctk.CTkLabel(icon_holder, image=icon_image, text="").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text=heading, font=("Segoe UI", 16, "bold"), text_color=icon_color).pack()
    ctk.CTkLabel(frame, text=message, font=("Segoe UI", 12), text_color=("gray40", "gray70")).pack(pady=(4, 18))

    def cancel_and_close():
        on_cancel()
        win.destroy()

    btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
    btn_frame.pack(fill="x")
    btn_frame.grid_columnconfigure((0, 1), weight=1)
    ctk.CTkButton(
        btn_frame,
        text="Cancel shutdown",
        fg_color=icon_color,
        hover_color=icon_color,
        text_color="#1a0d02",
        command=cancel_and_close,
    ).grid(row=0, column=0, padx=(0, 5), sticky="we")
    ctk.CTkButton(
        btn_frame, text="OK", fg_color="transparent", border_width=1, command=win.destroy
    ).grid(row=0, column=1, padx=(5, 0), sticky="we")

    win.after(auto_close_ms, lambda: win.winfo_exists() and win.destroy())

    _center(win)
    win.lift()
    win.focus_force()
    return win


def show_10min_warning(root, on_cancel):
    _make_warning_popup(
        root,
        "Shutdown in 10 minutes",
        "Save your work now.",
        AMBER_BG,
        AMBER,
        on_cancel,
    )


def show_1min_warning(root, on_cancel):
    _make_warning_popup(
        root,
        "Shutdown in 1 minute!",
        "Shutting down now unless cancelled.",
        RED_BG,
        RED,
        on_cancel,
    )
