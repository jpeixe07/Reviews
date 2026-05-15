from datetime import datetime

from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.fake_user import FakeUser
from app.schemas.user import UserCreate, UserLogin, UserUpdate

fake_users_db: list[FakeUser] = []


class AuthService:
    @staticmethod
    async def register_user(data: UserCreate) -> User:
        existing_email = next(
            (user for user in fake_users_db if user.email == data.email),
            None,
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já está em uso",
            )

        existing_username = next(
            (user for user in fake_users_db if user.username == data.username),
            None,
        )
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username já está em uso",
            )

        user = FakeUser(
            name=data.name,
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            bio=None,
            avatar_url=None,
            is_active=True,
            is_verified=False,
            is_private=False,
            created_at=datetime.utcnow(),
        )

        fake_users_db.append(user)
        return user

    @staticmethod
    async def login_user(data: UserLogin) -> str:
        user = next(
            (user for user in fake_users_db if user.email == data.email),
            None,
        )

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="A conta está inativa",
            )

        token = create_access_token(
            {
                "sub": user.email,
                "username": user.username,
            }
        )
        return token

    @staticmethod
    async def get_user_by_email(email: str) -> User:
        user = next((user for user in fake_users_db if user.email == email), None)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return user

    @staticmethod
    async def update_user(current_user: User, data: UserUpdate) -> User:
        update_data = data.model_dump(exclude_unset=True)

        new_username = update_data.get("username")
        if new_username and new_username != current_user.username:
            existing_username = next(
                (
                    user
                    for user in fake_users_db
                    if user.username == new_username and user.email != current_user.email
                ),
                None,
            )
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username já está em uso",
                )

        for field, value in update_data.items():
            setattr(current_user, field, value)

        return current_user

    @staticmethod
    async def deactivate_user(current_user: User) -> User:
        current_user.is_active = False
        return current_user