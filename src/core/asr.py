# ASR: mikrofondan dinle, metne çevir (şimdilik SpeechRecognition)

import speech_recognition as sr

# SpeechRecognition tanıyıcıyı modül seviyesinde saklıyoruz
r = sr.Recognizer()

def listen_once(lang="tr-TR") -> str:
    """
    Mikrofondan tek cümle dinler ve metne çevirir.
    Şimdilik Google SR kullanıyor (internet gerekli).
    Sonraki aşamada faster-whisper ile tamamen offline yapacağız.
    """
    with sr.Microphone() as source:
        print("Nova dinliyor…")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language=lang)
            return text.strip()
        except sr.UnknownValueError:
            return ""

