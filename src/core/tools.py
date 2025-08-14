# Tool kayıt sistemi (dekoratör + sözlük)

from functools import wraps

# Kayıtlı tool'ları tutacağımız sözlük
TOOLS = {}

def tool(name=None):
    """
    @tool("ad") dekoratörüyle fonksiyonları tool olarak kaydeder.
    Router, LLM'den gelen intent adına göre bu sözlükten çağıracak.
    """
    def dec(func):
        TOOLS[name or func.__name__] = func
        @wraps(func)
        def w(*a, **k):
            return func(*a, **k)
        return w
    return dec

