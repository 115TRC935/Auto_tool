import os
import sys

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

ICON_PATH = get_resource_path("config/brand-amigo.ico")
COLORS_PATH = get_resource_path("config/colors.json")

