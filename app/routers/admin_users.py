from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.db.models import User
from app.schemas.admin import BanRequest, UserCreate, UserUpdate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin-users"], dependencies=[Depends(require_admin)])


def _user_out(user: User) -> dict:
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "status": user.status,
        "ban_reason": user.ban_reason,
    }


@router.get("/users")
async def list_users(actor: dict = Depends(require_admin)):
    users = await AdminService.list_users()
    return {"data": [_user_out(u) for u in users]}


@router.post("/users", status_code=201)
async def create_user(body: UserCreate, actor: dict = Depends(require_admin)):
    user = await AdminService.create_user(actor, body)
    return {"data": _user_out(user)}


@router.put("/users/{user_id}")
async def update_user(user_id: str, body: UserUpdate, actor: dict = Depends(require_admin)):
    user = await AdminService.update_user(actor, user_id, body)
    return {"data": _user_out(user)}


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, actor: dict = Depends(require_admin)):
    await AdminService.delete_user(actor, user_id)
    return {"data": {"deleted": True}}


@router.post("/users/{user_id}/ban")
async def ban_user(user_id: str, body: BanRequest, actor: dict = Depends(require_admin)):
    user = await AdminService.ban_user(actor, user_id, body.reason)
    return {"data": _user_out(user)}


@router.post("/users/{user_id}/unban")
async def unban_user(user_id: str, actor: dict = Depends(require_admin)):
    user = await AdminService.unban_user(actor, user_id)
    return {"data": _user_out(user)}
