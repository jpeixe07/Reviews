from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    name: str
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    is_private: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"