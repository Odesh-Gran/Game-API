# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.limiter import limiter

from app.database import get_db
from app.models import User
from app.auth import (
    hash_password,
    verify_and_migrate,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    revoke_refresh_token,
)

router = APIRouter(prefix="/api/v1", tags=["auth"])


# ===================== СХЕМЫ =====================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


# ===================== РЕГИСТРАЦИЯ =====================

@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")          # 👈 3 регистрации в минуту
def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):  # 👈 request
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Логин уже занят")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Аккаунт создан!"}


# ===================== ЛОГИН =====================

@router.post("/login")
@limiter.limit("5/minute")          # 👈 5 попыток в минуту
def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):  # 👈 request
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # bcrypt + ленивая миграция старых sha256_crypt хешей
    if not verify_and_migrate(user_data.password, user.password_hash, db, user):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


# ===================== REFRESH (ротация) =====================

@router.post("/refresh")
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    token_row = verify_refresh_token(db, body.refresh_token)
    if token_row is None:
        raise HTTPException(status_code=401, detail="Неверный или истёкший refresh-токен")

    # Ротация: отзываем старый, выдаём новую пару
    revoke_refresh_token(db, token_row)

    access_token = create_access_token(data={"sub": str(token_row.user_id)})
    new_refresh = create_refresh_token(db, token_row.user_id)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }


# ===================== LOGOUT =====================

@router.post("/logout")
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    token_row = verify_refresh_token(db, body.refresh_token)
    if token_row is None:
        # уже отозван/истёк — не ошибка, просто выходим
        return {"message": "Выход выполнен"}

    revoke_refresh_token(db, token_row)
    return {"message": "Выход выполнен"}