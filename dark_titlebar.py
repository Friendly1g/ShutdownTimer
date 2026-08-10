import ctypes

_DWMWA_USE_IMMERSIVE_DARK_MODE_VALUES = (20, 19)


def apply_dark_titlebar(window):
    """Best-effort: makes a window's native Windows title bar dark to match
    its dark content. Silently does nothing if unsupported (older Windows).
    """
    try:
        window.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        if not hwnd:
            hwnd = window.winfo_id()
        value = ctypes.c_int(1)
        for attribute in _DWMWA_USE_IMMERSIVE_DARK_MODE_VALUES:
            result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attribute, ctypes.byref(value), ctypes.sizeof(value)
            )
            if result == 0:
                break
    except Exception:
        pass
