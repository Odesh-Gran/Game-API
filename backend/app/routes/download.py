from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/game")
def download_game():
    """Скачать последнюю версию игры."""
    return FileResponse(
        "/var/www/castle-survival.ru/downloads/Castl_Survival.exe",
        filename="CastleSurvival.exe",
        media_type="application/octet-stream"
    )