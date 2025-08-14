# Uygulamanın giriş noktası: döngü -> ASR -> LLM -> TOOL -> TTS

import os
import yaml
from loguru import logger

# Çekirdek modüller
from src.core.asr import listen_once          # Mikrofondan komut alır
from src.core.tts import speak                # Metni seslendirir
from src.core.llm import infer_intent         # LLM'den intent JSON'u üretir
from src.core.router import route_and_execute # Intent'i ilgili tool'a yönlendirir

def load_config():
    """config.yaml dosyasını yükler ve dict döner."""
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def make_llm_free(llm_url, model):
    """
    Serbest metin -> kısa yanıt için LLM fonksiyonu üretir.
    (chitchat ya da özetleme gibi durumlarda kullanıyoruz.)
    """
    import requests
    def _call(prompt: str) -> str:
        resp = requests.post(llm_url, json={"model": model, "prompt": prompt, "stream": False}, timeout=60)
        resp.raise_for_status()
        return resp.json().get("response","")
    return _call

def main():
    # Ayarları yükle
    cfg = load_config()
    llm_url = cfg["llm"]["url"]
    llm_model = cfg["llm"]["model"]
    lang = cfg["app"]["language"]
    wake_words = [w.lower() for w in cfg["app"]["wake_words"]]

    # Dosya yollarını hazırla
    notes_file = os.path.expanduser(cfg["paths"]["notes_file"])
    screenshots_dir = cfg["paths"]["screenshots_dir"]

    # Serbest LLM çağrısı için yardımcı fonksiyon
    llm_free = make_llm_free(llm_url, llm_model)

    speak("Nova hazır.")  # Açılış anonsu

    # Sonsuz döngü: dinle -> niyet -> tool -> sesli yanıt
    while True:
        heard = listen_once(lang=lang).lower()  # Mikrofondan bir cümle al
        if not heard:
            speak("Tekrarlar mısın?")
            continue

        print(f"[Kullanıcı] {heard}")

        # Wake word kontrolü: "nova", "selam", "asistan" gibi tetikleyiciler
        if not any(w in heard for w in wake_words):
            # Wake kelimesi olmadan da komut almak istersen bu kontrolü kaldırabilirsin
            # speak("Beni adımla çağır: Nova.")
            # continue
            pass

        # İstersen wake kelimelerini metinden temizle
        for w in wake_words:
            heard = heard.replace(w, "").strip()

        # LLM'den niyet JSON'unu al
        intent = infer_intent(llm_url, llm_model, heard)
        print(f"[Intent] {intent}")

        # Tool'lara iletilecek ortak bağımlılıklar
        deps = {
            "notes_file": notes_file,
            "screenshots_dir": screenshots_dir,
            "llm_free": llm_free,
        }

        # Niyet -> Tool -> Sonuç
        reply = route_and_execute(intent, deps)
        print(f"[Nova] {reply}")
        speak(reply)  # Sonucu seslendir

if __name__ == "__main__":
    # Basit log dosyası
    logger.add("nova.log", rotation="1 MB")
    main()

