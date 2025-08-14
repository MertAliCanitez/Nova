# LLM köprüsü: Ollama'ya istek at, niyet JSON'u üret

import json
import requests
from loguru import logger

# LLM'e verdiğimiz "sistem promptu".
# Kullanıcının cümlesini *mutlaka* şu JSON şemasına çevirmesini istiyoruz.
INTENT_SYSTEM_PROMPT = """
Sen Nova'nın komut yönlendiricisisin. Kullanıcı cümlesini şu şemada KESİN geçerli JSON’a çevir:
{"intent":"<tool_name>","args":{...}}

Geçerli tool'lar:
- "take_note": {"text": str}
- "summarize_notes": {"days": null | int}
- "take_screenshot": {"region": null | {"left":int,"top":int,"width":int,"height":int}}
- "open_app": {"name": str}
- "chitchat": {"text": str}

Kurallar:
- Eğer açık bir komut yoksa, intent "chitchat" olsun ve args.text'e doğal bir yanıt önerisi koy.
- Sadece JSON ver. Açıklama yazma.
"""

def infer_intent(llm_url: str, model: str, user_text: str) -> dict:
    """
    Ollama'ya prompt gönderir, dönen metni JSON'a parse eder.
    Parse olmazsa chitchat fallback döner.
    """
    prompt = INTENT_SYSTEM_PROMPT + f"\nKullanıcı: {user_text}\nJSON:"
    resp = requests.post(llm_url, json={"model": model, "prompt": prompt, "stream": False}, timeout=60)
    resp.raise_for_status()
    raw = resp.json().get("response", "").strip().strip("`")  # bazen code-fence olabiliyor
    try:
        return json.loads(raw)
    except Exception as e:
        logger.warning(f"Intent parse edilemedi: {e}; raw={raw[:200]}")
        return {"intent": "chitchat", "args": {"text": "Nasıl yardımcı olabilirim?"}}

