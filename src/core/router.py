# LLM dönen JSON'u doğru tool'a yönlendir, bağımlılıkları enjekte et

from loguru import logger
from src.core.tools import TOOLS

def route_and_execute(intent: dict, deps: dict) -> str:
    """
    LLM'den gelen intent JSON'una göre ilgili tool'u çağırır.
    'deps' ile tool'lara ortak bağımlılıkları (dosya yolları, llm_free vs.) enjekte eder.
    """
    name = intent.get("intent")
    args = intent.get("args", {}) or {}

    # Serbest sohbet ise doğrudan LLM'e kısa cevap üretmesini iste
    if name == "chitchat":
        return deps["llm_free"](args.get("text","")).strip()

    # Tool'u bul
    fn = TOOLS.get(name)
    if not fn:
        return f"Bu komutu yapamıyorum: {name}"

    try:
        # Tool bazlı bağımlılık enjeksiyonu
        if name == "take_note":
            return fn(text=args.get("text",""), notes_file=deps["notes_file"])

        if name == "summarize_notes":
            return fn(days=args.get("days"), notes_file=deps["notes_file"], llm_fn=deps["llm_free"])

        if name == "take_screenshot":
            return fn(region=args.get("region"), screenshots_dir=deps["screenshots_dir"])

        if name == "open_app":
            return fn(name=args.get("name",""))

        # Yeni tool ekledikçe yukarıya case ekleyebilir veya
        # tüm tool imzalarını standartlaştırıp tek satırda **args çağırabilirsin.
        return fn(**args)

    except TypeError:
        # Argüman uyuşmazlığında en azından default çağırmayı dene
        return fn()
    except Exception as e:
        logger.exception(e)
        return f"Hata: {e}"

