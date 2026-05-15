from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditLogRead(BaseModel):
    id: int
    table_name: str
    operation: str
    record_id: Optional[str] = None
    changed_data: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
