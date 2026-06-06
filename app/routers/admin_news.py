from fastapi import APIRouter, Depends

from app.core.security import require_admin
from app.db.models import News
from app.schemas.admin import NewsCreate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin-news"], dependencies=[Depends(require_admin)])


def _news_out(n: News) -> dict:
    return {"id": str(n.id), "title": n.title, "body": n.body, "tags": n.tags}


@router.post("/news", status_code=201)
async def create_news(body: NewsCreate, actor: dict = Depends(require_admin)):
    news = await AdminService.create_news(actor, body)
    return {"data": _news_out(news)}
