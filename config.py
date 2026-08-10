import json

from app_paths import get_app_dir

CONFIG_PATH = get_app_dir() / "config.json"

DEFAULTS = {
    "shutdown_time": "22:30",
    "enabled": True,
}


def load_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            config = DEFAULTS.copy()
            config.update(data)
            return config
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULTS.copy()


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
