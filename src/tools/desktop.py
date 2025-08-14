# Uygulama/program açma tool'u

import os
import platform
import subprocess
from src.core.tools import tool

@tool("open_app")
def open_app(name: str):
    """
    Uygulama/program açar.
    macOS: 'open -a <AppName>'
    Windows: os.startfile("notepad.exe") veya tam yol
    Linux: doğrudan komut adı
    """
    system = platform.system().lower()
    try:
        if "darwin" in system or "mac" in system:
            subprocess.Popen(["open", "-a", name])
        elif "windows" in system:
            os.startfile(name)  # ör: "notepad.exe" veya "C:\\Path\\App.exe"
        else:
            subprocess.Popen([name])  # Linux
        return f"{name} açılıyor."
    except Exception as e:
        return f"Açılamadı: {e}"
