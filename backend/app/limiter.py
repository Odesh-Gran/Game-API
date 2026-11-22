from fastapi import Request
from slowapi import Limiter

def get_real_ip(request: Request) -> str:
    """Берём реальный IP из заголовка X-Forwarded-For (Nginx)"""
    xff = request.headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return request.client.host

limiter = Limiter(key_func=get_real_ip)