# app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AchievementCreate(BaseModel):
    name: str
    description: str | None = None


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str | None
    earned_at: datetime

    model_config = ConfigDict(from_attributes=True)