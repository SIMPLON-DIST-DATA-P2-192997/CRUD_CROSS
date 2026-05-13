from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import OperationStats
from pydantic_schemas.operation_stats import OperationStatsRead

router = APIRouter(prefix="/operation-stats", tags=["Operation Stats"])


@router.get("/", response_model=List[OperationStatsRead])
def get_operation_stats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(OperationStats).offset(skip).limit(limit).all()


@router.get("/{stat_id}", response_model=OperationStatsRead)
def get_operation_stat(stat_id: int, db: Session = Depends(get_db)):
    stat = db.query(OperationStats).filter(OperationStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation stat not found")
    return stat


@router.get("/by-operation/{operation_id}", response_model=List[OperationStatsRead])
def get_stats_by_operation(operation_id: int, db: Session = Depends(get_db)):
    return db.query(OperationStats).filter(OperationStats.operation_id == operation_id).all()
