from fastapi import APIRouter, Depends, Query

from app.core.security import require_admin
from app.db.models import AuditLog
from app.services.audit_service import AuditService

router = APIRouter(prefix="/admin", tags=["admin-audit"], dependencies=[Depends(require_admin)])


def _audit_out(a: AuditLog) -> dict:
    return {
        "id": str(a.id),
        "actor": a.actor,
        "action": a.action,
        "target_type": a.target_type,
        "target": a.target,
        "metadata": a.metadata,
    }


@router.get("/audit-log")
async def query_audit(
    actor_filter: str = Query(default="", alias="actor"),
    action: str = Query(default=""),
    actor: dict = Depends(require_admin),
):
    entries = await AuditService.query(actor_filter or None, action or None)
    return {"data": [_audit_out(a) for a in entries]}
