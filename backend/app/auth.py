import bcrypt
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.models import RefreshToken, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

REFRESH_TOKEN_EXPIRE_DAYS = 30


# ===================== ПАРОЛИ =====================

def hash_password(password: str) -> str:
    """Хеширует пароль через bcrypt (обрезает до 72 байт)."""
    pw = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль через bcrypt."""
    pw = plain_password.encode("utf-8")[:72]
    try:
        return bcrypt.checkpw(pw, hashed_password.encode("utf-8"))
    except ValueError:
        return False


def verify_and_migrate(plain_password: str, hashed_password: str, db, user) -> bool:
    """
    Проверяет пароль. Если хеш старый (sha256_crypt, начинается с $5$),
    то после успешной проверки перехеширует его в bcrypt и сохраняет.
    """
    if hashed_password.startswith("$5$"):
        from passlib.hash import sha256_crypt
        if sha256_crypt.verify(plain_password, hashed_password):
            user.hashed_password = hash_password(plain_password)
            db.commit()
            return True
        return False
    return verify_password(plain_password, hashed_password)


# ===================== ACCESS ТОКЕН =====================

def create_access_token(data: dict) -> str:
    """Создаёт короткоживущий access-токен."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Достаёт пользователя из access-токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "access":
            raise credentials_exception
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


# ===================== REFRESH ТОКЕН =====================

def create_refresh_token(db, user_id: int) -> str:
    """
    Создаёт refresh-токен, сохраняет его хеш в БД
    и возвращает сырой токен (его отдаём клиенту).
    """
    raw = secrets.token_urlsafe(64)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    db.add(
        RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires,
            revoked=False,
        )
    )
    db.commit()
    return raw


def verify_refresh_token(db, raw_token: str) -> RefreshToken | None:
    """
    Проверяет refresh-токен: есть ли в БД, не отозван, не истёк.
    Возвращает запись или None.
    """
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked == False,
        )
        .first()
    )
    if token is None:
        return None
    if token.expires_at < datetime.now(timezone.utc):
        return None
    return token


def revoke_refresh_token(db, token: RefreshToken) -> None:
    """Отзывает refresh-токен (ставит revoked=True)."""
    token.revoked = True
    db.commit()