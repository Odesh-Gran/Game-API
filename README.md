# 🎮 Game API

REST API для RPG-игры «Убежище в замке»: аутентификация, достижения, интеграция с игрой (Pygame) и веб-сайтом.

**Продакшен:** https://api.castle-survival.ru  
**Swagger UI:** https://api.castle-survival.ru/docs  
**Сайт:** https://castle-survival.ru  
**Игра:** [GitHub — RPG_Pygame_Game](https://github.com/Odesh-Gran/RPG_Pygame_Game)

![CI](https://github.com/Odesh-Gran/Game-API/actions/workflows/ci.yml/badge.svg)
![Deploy](https://github.com/Odesh-Gran/Game-API/actions/workflows/deploy.yml/badge.svg)

---

## 📋 О проекте

Backend для игры и сайта. Игра (Pygame) и веб-сайт обращаются к API за:

- Аутентификацией игроков (JWT).
- Сохранением и загрузкой достижений.
- Синхронизацией прогресса.

API работает **24/7** на VPS с **HTTPS**, **автозапуском** (systemd), **firewall** (ufw) и **автодеплоем** через GitHub Actions.

---

## 🛠 Стек технологий

**Backend:**

- Python 3.12
- FastAPI 0.141
- SQLAlchemy 2.0 (ORM)
- Pydantic 2.13 (валидация)
- pydantic-settings (конфигурация)
- Alembic (миграции)
- SQLite (БД; PostgreSQL в roadmap)
- JWT (python-jose)
- bcrypt (хеширование паролей)

**Инфраструктура:**

- Nginx (reverse proxy)
- Let's Encrypt (SSL)
- systemd (автозапуск)
- ufw (firewall)
- Ubuntu 24.04
- GitHub Actions (CI + автодеплой)

**Клиенты:**

- Pygame (игра)
- HTML/CSS/JS (сайт)

---

## ✨ Возможности

- ✅ Регистрация и логин (JWT)
- ✅ Хеширование паролей (**bcrypt**, с ленивой миграцией старых `sha256_crypt` хешей)
- ✅ **Refresh-токены** с ротацией (старый отзывается при `/refresh`)
- ✅ `/logout` с отзывом refresh в БД
- ✅ **Alembic** — миграции схемы БД
- ✅ Управление достижениями (CRUD)
- ✅ Приватность: игрок видит только свои достижения
- ✅ Автодокументация (Swagger / OpenAPI)
- ✅ CORS для веб-клиентов
- ✅ HTTPS + автопродление сертификата
- ✅ Автозапуск при перезагрузке (systemd)
- ✅ **CI/CD** — `git push` → деплой на VPS
- ✅ Rate limiting (slowapi, 5/мин на /login)

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
         │ + Uvicorn      │
         │   (systemd)    │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │ SQLite         │
         │ (Alembic)      │
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
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./game.db
Сгенерировать SECRET_KEY:

bash
python -c "import secrets; print(secrets.token_hex(32))"
5. Применить миграции
bash
alembic upgrade head
6. Запустить сервер
bash
uvicorn app.main:app --reload --port 8000
Открой http://127.0.0.1:8000/docs — Swagger UI.

🔌 API Endpoints
Аутентификация
POST /api/v1/register — регистрация

bash
curl -X POST https://api.castle-survival.ru/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "email": "player@example.com", "password": "qwerty123"}'
Ответ (201): {"message": "Аккаунт создан!"}

POST /api/v1/login — вход

bash
curl -X POST https://api.castle-survival.ru/api/v1/login \
  -H "Content-Type: application/json" \
  -d '{"username": "player1", "password": "qwerty123"}'
Ответ (200):

json
{
  "access_token": "eyJhbGciOi...",
  "refresh_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
POST /api/v1/refresh — обновить пару токенов (ротация)

bash
curl -X POST https://api.castle-survival.ru/api/v1/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
Ответ (200): новая пара access_token + refresh_token. Старый refresh отзывается.

POST /api/v1/logout — отозвать refresh

bash
curl -X POST https://api.castle-survival.ru/api/v1/logout \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
Достижения (требуется токен)
GET /api/v1/achievements — список достижений

bash
curl https://api.castle-survival.ru/api/v1/achievements \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
POST /api/v1/achievements — создать достижение

bash
curl -X POST https://api.castle-survival.ru/api/v1/achievements \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Убийца драконов", "description": "Победил первого дракона"}'
Служебные
GET /api/v1/health — проверка статуса

bash
curl https://api.castle-survival.ru/api/v1/health
Ответ: {"status": "OK", "message": "Бэкенд работает!"}


🔄 CI/CD
При git push в main:

CI (ci.yml) — линт + тесты.

Deploy (deploy.yml) — SSH на VPS → git pull → pip install → alembic upgrade head → systemctl restart gameapi.

Секреты в GitHub: VPS_HOST, VPS_USER, VPS_SSH_KEY.

🎯 Roadmap
⬜ Переезд на PostgreSQL

⬜ Sentry (мониторинг ошибок)

⬜ Покрытие тестами > 85%



👤 Автор
Олег — студент 2 курса ИТ (ИБ)
GitHub: @Odesh-Gran

## Что изменено

- **bcrypt** вместо `sha256_crypt` (с ленивой миграцией).
- **Refresh-токены** с ротацией + `/refresh` + `/logout`.
- **Alembic** — миграции.
- **CI/CD** — бейджи + секция.
- **Docker** убран из стека (на сервере его нет — systemd).
- **Roadmap** сузился: осталось Postgres, Sentry, покрытие.
- **Установка** — добавлен шаг `alembic upgrade head`.
- **`ACCESS_TOKEN_EXPIRE_MINUTES=30`** (было 60).
