# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ============================================
# НОВАЯ ТАБЛИЦА ДЛЯ ДОСТИЖЕНИЙ
# ============================================
class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)          # Название достижения
    description = Column(String, nullable=True)    # Описание (опционально)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)    