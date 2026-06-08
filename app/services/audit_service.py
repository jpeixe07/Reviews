"""Audit service — the single writer and reader of the audit log.

Centralising audit here keeps the non-bypass invariant (RNF03) in one place: every
admin mutation calls `AuditService.record` *after* persisting, while rejected
requests raise before reaching it, so they never produce an entry. Reads go through
`AuditService.query`.
"""

from typing import Optional

from app.db.models import AuditLog


class AuditService:
    @staticmethod
    async def record(
        actor: str,
        action: str,
        target_type: str,
        target: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        await AuditLog(
            actor=actor,
            action=action,
            target_type=target_type,
            target=target,
            metadata=metadata or {},
        ).insert()

    @staticmethod
    async def query(actor: Optional[str] = None, action: Optional[str] = None) -> list[AuditLog]:
        criteria: dict = {}
        if actor:
            criteria["actor"] = actor
        if action:
            criteria["action"] = action
        return await AuditLog.find(criteria).to_list()
