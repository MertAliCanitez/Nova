# Ekran görüntüsü alma tool'u

import os
import time
import mss
from src.core.tools import tool

def _ensure_dir(d):
    """Klasör yoksa oluşturur."""
    os.makedirs(d, exist_ok=True)
    return d

@tool("take_screenshot")
def take_screenshot(region, screenshots_dir: str):
    """
    Tüm ekranın (veya belirtilen bölgenin) görüntüsünü alır.
    region dict'i: {"left":int,"top":int,"width":int,"height":int}
    """
    _ensure_dir(screenshots_dir)
    path = os.path.abspath(os.path.join(screenshots_dir, f"screenshot_{int(time.time())}.png"))

    with mss.mss() as sct:
        if region and all(k in region for k in ("left","top","width","height")):
            mon = {"left":region["left"],"top":region["top"],"width":region["width"],"height":region["height"]}
            img = sct.grab(mon)
        else:
            img = sct.grab(sct.monitors[0])  # tüm ekran
        mss.tools.to_png(img.rgb, img.size, output=path)

    return f"Ekran görüntüsü kaydedildi: {path}"

