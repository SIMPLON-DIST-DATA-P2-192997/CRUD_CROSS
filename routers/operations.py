from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from database import get_db
from models import Operation
from pydantic_schemas.operation import OperationReadFull, OperationCreate, OperationRead, OperationUpdate

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/", response_model=List[OperationRead])
def get_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Operation).offset(skip).limit(limit).all()


@router.get("/{operation_id}", response_model=OperationRead)
def get_operation(operation_id: int, db: Session = Depends(get_db)):
    op = db.query(Operation).filter(Operation.operation_id == operation_id).first()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    return op

@router.get("/full/{operation_id}", response_model=OperationReadFull, status_code=status.HTTP_200_OK)
def get_operation_full(operation_id: int, db: Session = Depends(get_db)):
    op = (
        db.query(Operation).options(
            selectinload(Operation.operations_stats),
            selectinload(Operation.human_results),
            selectinload(Operation.flotteurs),
        )
    ).filter(Operation.operation_id == operation_id).first()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No operation found with this id.")
    return op

@router.post("/", response_model=OperationRead, status_code=status.HTTP_201_CREATED)
def create_operation(payload: OperationCreate, db: Session = Depends(get_db)):
    op = Operation(**payload.model_dump())
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@router.put("/{operation_id}", response_model=OperationRead)
def update_operation(operation_id: int, payload: OperationUpdate, db: Session = Depends(get_db)):
    op = db.query(Operation).filter(Operation.operation_id == operation_id).first()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(op, field, value)
    db.commit()
    db.refresh(op)
    return op


@router.delete("/{operation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operation(operation_id: int, db: Session = Depends(get_db)):
    op = db.query(Operation).filter(Operation.operation_id == operation_id).first()
    if not op:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    db.delete(op)
    db.commit()
