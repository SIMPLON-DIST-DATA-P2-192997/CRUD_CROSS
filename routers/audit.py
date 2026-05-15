from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import AuditLog
from pydantic_schemas.audit_log import AuditLogRead

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/", response_model=List[AuditLogRead])
def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    table_name: Optional[str] = Query(default=None, description="Filter by table name"),
    operation: Optional[str] = Query(default=None, description="Filter by operation: INSERT, UPDATE, DELETE"),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)
    if table_name:
        query = query.filter(AuditLog.table_name == table_name)
    if operation:
        query = query.filter(AuditLog.operation == operation.upper())
    return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{log_id}", response_model=AuditLogRead)
def get_audit_log(log_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException, status
    log = db.query(AuditLog).filter(AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit log not found")
    return log
