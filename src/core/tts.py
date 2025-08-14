# TTS: metni sese çevir (şimdilik pyttsx3 - offline)

import pyttsx3

# TTS motorunu modül seviyesinde 1 kez kurup tekrar kullanacağız
_engine = None

def _get_engine():
    """pyttsx3 motorunu lazy-initialize eder ve döner."""
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Örnek ayarlar:
        # _engine.setProperty('rate', 180)   # konuşma hızı
        # _engine.setProperty('volume', 1.0) # ses yüksekliği 0.0-1.0
    return _engine

def speak(text: str):
    """Verilen metni seslendirir (offline)."""
    eng = _get_engine()
    eng.say(text)
    eng.runAndWait()
