from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class FakeUser:
    name: str
    username: str
    email: str
    hashed_password: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    is_private: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)