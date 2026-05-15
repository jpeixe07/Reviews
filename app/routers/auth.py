from fastapi import APIRouter, status

from app.schemas.user import (
    MessageResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def serialize_user(user):
    return UserResponse(
        name=user.name,
        username=user.username,
        email=user.email,
        bio=user.bio,
        avatar_url=user.avatar_url,
        is_active=user.is_active,
        is_verified=user.is_verified,
        is_private=user.is_private,
        created_at=user.created_at,
    )


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def register(data: UserCreate):
    user = await AuthService.register_user(data)
    return serialize_user(user)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    token = await AuthService.login_user(data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/register/check", response_model=MessageResponse)
async def register_check():
    return {"message": "Auth router funcionando"}