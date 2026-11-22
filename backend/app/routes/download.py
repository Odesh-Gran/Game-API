from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.limiter import limiter

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/game")
@limiter.limit("5/minute")          # 👈 5 скачиваний в минуту
def download_game(request: Request):  # 👈 request обязателен
    """Скачать последнюю версию игры (архив)."""
    return FileResponse(
        "/var/www/castle-survival.ru/downloads/Castl_Survival_v0.1.zip",
        filename="Castl_Survival_v0.1.zip",
        media_type="application/zip"
    )