from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/download", tags=["download"])


@router.get("/game")
def download_game():
    """Скачать последнюю версию игры (архив)."""
    return FileResponse(
        "/var/www/castle-survival.ru/downloads/Castl_Survival_v0.1.zip",
        filename="Castl_Survival_v0.1.zip",
        media_type="application/zip"
    )