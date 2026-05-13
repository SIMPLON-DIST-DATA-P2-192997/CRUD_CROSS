import json
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

from models import AuditLog


def _get_record_id(instance) -> str | None:
    mapper = inspect(type(instance))
    pk_values = [str(getattr(instance, col.key)) for col in mapper.primary_key]
    return ",".join(pk_values) if pk_values else None


def _serialize(instance) -> str:
    mapper = inspect(type(instance))
    data = {}
    for col in mapper.column_attrs:
        try:
            data[col.key] = str(getattr(instance, col.key))
        except Exception:
            data[col.key] = None
    return json.dumps(data, ensure_ascii=False)


def register_audit_listeners() -> None:
    """
    Buffer INSERT/UPDATE/DELETE during flush using session.info,
    then write audit entries after the flush completes via a raw
    connection insert (avoids SAWarning about session.add during flush).
    """

    @event.listens_for(Session, "after_flush")
    def collect_changes(session: Session, flush_context):
        pending: list[dict] = session.info.setdefault("audit_pending", [])

        for instance in session.new:
            if instance.__tablename__ == "audit_log":
                continue
            pending.append({
                "table_name": instance.__tablename__,
                "operation": "INSERT",
                "record_id": _get_record_id(instance),
                "changed_data": _serialize(instance),
            })

        for instance in session.dirty:
            if instance.__tablename__ == "audit_log":
                continue
            pending.append({
                "table_name": instance.__tablename__,
                "operation": "UPDATE",
                "record_id": _get_record_id(instance),
                "changed_data": _serialize(instance),
            })

        for instance in session.deleted:
            if instance.__tablename__ == "audit_log":
                continue
            pending.append({
                "table_name": instance.__tablename__,
                "operation": "DELETE",
                "record_id": _get_record_id(instance),
                "changed_data": _serialize(instance),
            })

    @event.listens_for(Session, "after_commit")
    def write_audit_entries(session: Session):
        pending: list[dict] = session.info.pop("audit_pending", [])
        if not pending:
            return
        with session.bind.connect() as conn:  # type: ignore[union-attr]
            conn.execute(
                AuditLog.__table__.insert(),  # type: ignore[attr-defined]
                pending,
            )
            conn.commit()

    @event.listens_for(Session, "after_rollback")
    def clear_audit_entries(session: Session):
        session.info.pop("audit_pending", None)

