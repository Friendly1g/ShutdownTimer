import pystray
from PIL import Image, ImageDraw


def _make_icon_image():
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse((4, 4, size - 4, size - 4), fill=(30, 144, 255, 255))
    # simple clock hands
    draw.line((32, 32, 32, 14), fill="white", width=4)
    draw.line((32, 32, 46, 32), fill="white", width=4)
    return img


def build_tray_icon(root, scheduler, open_settings, on_quit):
    def on_open_settings(icon_obj, item):
        root.after(0, open_settings)

    def on_cancel_today(icon_obj, item):
        root.after(0, scheduler.cancel_today)

    def on_exit(icon_obj, item):
        root.after(0, on_quit)

    menu = pystray.Menu(
        pystray.MenuItem("Open settings", on_open_settings),
        pystray.MenuItem("Cancel tonight's shutdown", on_cancel_today),
        pystray.MenuItem("Exit", on_exit),
    )

    return pystray.Icon("ShutdownTimer", _make_icon_image(), "Shutdown Timer", menu)
