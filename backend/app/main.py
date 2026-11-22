# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app.routes import auth, achievements, download
from app.core.config import settings
from app.limiter import limiter   # 👈 импорт лимитера


# Создаём таблицы (для dev; для прода — Alembic)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
)

# ===== RATE LIMITING =====
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Локальная разработка
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        # GitHub Pages
        "https://odesh-gran.github.io",
        "http://odesh-gran.github.io",
        # Прод-домены
        "https://castle-survival.ru",
        "https://www.castle-survival.ru",
        "https://api.castle-survival.ru",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(achievements.router)
app.include_router(download.router)


@app.get("/")
def root():
    return {"message": "Game API is running!"}


@app.get("/api/v1/health")
def health():
    return {"status": "OK", "message": "Бэкенд работает!"}