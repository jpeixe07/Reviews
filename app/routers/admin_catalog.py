from fastapi import APIRouter, Depends, Query

from app.core.security import require_admin
from app.db.models import CatalogContributor
from app.schemas.admin import ContributorCreate
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin-catalog"], dependencies=[Depends(require_admin)])


def _contributor_out(c: CatalogContributor) -> dict:
    return {"id": str(c.id), "name": c.name, "role": c.role}


@router.post("/artists", status_code=201)
async def create_contributor(body: ContributorCreate, actor: dict = Depends(require_admin)):
    contributor = await AdminService.create_contributor(actor, body)
    return {"data": _contributor_out(contributor)}


@router.get("/artists")
async def search_contributors(q: str = Query(default=""), actor: dict = Depends(require_admin)):
    results = await AdminService.search_contributors(q)
    return {"data": [_contributor_out(c) for c in results]}
