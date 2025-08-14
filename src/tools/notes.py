# Not alma ve notları özetleme tool'ları

import os
from datetime import datetime
from loguru import logger
from src.core.tools import tool

def _expand(p):
    """~ gibi kısayolları ve göreli yolları mutlak path'e çevirir."""
    return os.path.abspath(os.path.expanduser(p))

@tool("take_note")
def take_note(text: str, notes_file: str):
    """
    Notu markdown dosyasına ekler.
    Not: 'notes_file' bağımlılığını router enjekte eder.
    """
    path = _expand(notes_file)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n- {datetime.now():%Y-%m-%d %H:%M} — {text}")
    return "Not alındı."

@tool("summarize_notes")
def summarize_notes(days: int, notes_file: str, llm_fn):
    """
    Not dosyasını okuyup LLM'e özetlettirir.
    'days' şu an kullanılmıyor; ileride tarih filtresi ekleyebilirsin.
    """
    path = _expand(notes_file)
    if not os.path.exists(path):
        return "Henüz bir not yok."
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        return "Not dosyası boş."

    prompt = f"Şu notları kısa ve maddeler halinde özetle (Türkçe, max 10 madde):\n{content}\n\nÖzet:"
    return llm_fn(prompt).strip()

