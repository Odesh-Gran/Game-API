# 🎮 Game API

REST API для RPG-игры «Убежище в замке»: аутентификация, достижения, интеграция с игрой (Pygame) и веб-сайтом.

**Продакшен:** https://api.castle-survival.ru  
**Swagger UI:** https://api.castle-survival.ru/docs  
**Сайт:** https://castle-survival.ru  
**Игра:** [GitHub — RPG_Pygame_Game](https://github.com/Odesh-Gran/RPG_Pygame_Game)
![CI](https://github.com/Odesh-Gran/Game-API/actions/workflows/ci.yml/badge.svg)

REST API для RPG-игры...

---

## 📋 О проекте

Backend для игры и сайта. Игра (Pygame) и веб-сайт обращаются к API за:
- Аутентификацией игроков (JWT).
- Сохранением и загрузкой достижений.
- Синхронизацией прогресса.

API работает **24/7** на VPS с **HTTPS**, **автозапуском** (systemd) и **firewall**.

---

## 🛠 Стек технологий

**Backend:**
- Python 3.12
- FastAPI 0.141
- SQLAlchemy 2.0 (ORM)
- Pydantic 2.13 (валидация)
- pydantic-settings (конфигурация)
- SQLite (БД)
- PostgreSQL 16
- JWT (python-jose)
- passlib (хеширование паролей)

**Инфраструктура:**
- Nginx (reverse proxy)
- Docker
- Docker Compose
- Let's Encrypt (SSL)
- systemd (автозапуск)
- ufw (firewall)
- Ubuntu 24.04

**Клиенты:**
- Pygame (игра)
- HTML/CSS/JS (сайт)

---

## ✨ Возможности

- ✅ Регистрация и логин (JWT)
- ✅ Хеширование паролей (sha256_crypt)
- ✅ Управление достижениями (CRUD)
- ✅ Приватность: игрок видит только свои достижения
- ✅ Автодокументация (Swagger / OpenAPI)
- ✅ CORS для веб-клиентов
- ✅ HTTPS + автопродление сертификата
- ✅ Автозапуск при перезагрузке сервера

---

## 🏗 Архитектура

```
┌─────────────┐     ┌─────────────┐
│   Игра      │     │   Сайт      │
│  (Pygame)   │     │ (HTML/JS)   │
└──────┬──────┘     └──────┬──────┘
       │                   │
       │  HTTPS + JWT      │
       │                   │
       └─────────┬─────────┘
                 │
         ┌───────▼────────┐
         │   Nginx        │
         │ (reverse proxy)│
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │   FastAPI      │
         │   + Uvicorn    │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │   SQLite       │
         └────────────────┘
```

---

## 🚀 Установка (локально)

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Odesh-Gran/Game-API.git
cd Game-API/backend


2. Создать виртуальное окружение
bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows


3. Установить зависимости
bash
pip install -r requirements.txt


4. Создать .env
env
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./game.db
Сгенерировать SECRET_KEY:

bash
python -c "import secrets; print(secrets.token_hex(32))"


5. Запустить сервер
bash
uvicorn app.main:app --reload --port 8000
Открой http://127.0.0.1:8000/docs — Swagger UI.

🔌 API Endpoints
Аутентификация
POST /api/v1/register — регистрация
bash
curl -X POST https://api.castle-survival.ru/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "email": "player@example.com",
    "password": "qwerty123"
  }'
Ответ (201):

json
{"message": "Аккаунт создан!"}
POST /api/v1/login — вход
bash
curl -X POST https://api.castle-survival.ru/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "player1",
    "password": "qwerty123"
  }'
Ответ (200):

json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {"id": 1, "username": "player1", "email": "player@example.com"}
}
Достижения (требуется токен)
GET /api/v1/achievements — список достижений
bash
curl https://api.castle-survival.ru/api/v1/achievements \
  -H "Authorization: Bearer YOUR_TOKEN"
Ответ (200):

json
[
  {
    "id": 1,
    "name": "Первое достижение",
    "description": "Начало пути",
    "earned_at": "2026-09-15T12:00:00"
  }
]
POST /api/v1/achievements — создать достижение
bash
curl -X POST https://api.castle-survival.ru/api/v1/achievements \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Убийца драконов",
    "description": "Победил первого дракона"
  }'
Служебные
GET /api/v1/health — проверка статуса
bash
curl https://api.castle-survival.ru/api/v1/health
Ответ: {"status": "OK", "message": "Бэкенд работает!"}

🎯 Roadmap
□ Переезд на PostgreSQL
□ Alembic (миграции)
□ Docker + docker-compose
□ CI/CD (GitHub Actions)
□ Тесты (pytest, покрытие >70%)
□ Rate limiting (slowapi)
□ Refresh-токены
□ Sentry (мониторинг ошибок)

👤 Автор
Олег — студент 2 курса ИТ (ИБ)
GitHub: @Odesh-Gran