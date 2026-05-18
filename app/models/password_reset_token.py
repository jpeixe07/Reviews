from datetime import datetime
from beanie import Document, Indexed
from pydantic import EmailStr, Field


class PasswordResetToken(Document):
    user_id: str
    email: EmailStr
    token: Indexed(str, unique=True)
    expires_at: datetime
    used: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "password_reset_tokens"