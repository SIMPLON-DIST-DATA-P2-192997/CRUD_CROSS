from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import HumainResult
from pydantic_schemas.humain_result import HumainResultCreate, HumainResultRead, HumainResultUpdate

router = APIRouter(prefix="/human-results", tags=["Human Results"])


@router.get("/", response_model=List[HumainResultRead])
def get_human_results(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(HumainResult).offset(skip).limit(limit).all()


@router.get("/{result_id}", response_model=HumainResultRead)
def get_human_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(HumainResult).filter(HumainResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Human result not found")
    return result


@router.get("/by-operation/{operation_id}", response_model=List[HumainResultRead])
def get_human_results_by_operation(operation_id: int, db: Session = Depends(get_db)):
    return db.query(HumainResult).filter(HumainResult.operation_id == operation_id).all()


@router.post("/", response_model=HumainResultRead, status_code=status.HTTP_201_CREATED)
def create_human_result(payload: HumainResultCreate, db: Session = Depends(get_db)):
    result = HumainResult(**payload.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.put("/{result_id}", response_model=HumainResultRead)
def update_human_result(result_id: int, payload: HumainResultUpdate, db: Session = Depends(get_db)):
    result = db.query(HumainResult).filter(HumainResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Human result not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(result, field, value)
    db.commit()
    db.refresh(result)
    return result


@router.delete("/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_human_result(result_id: int, db: Session = Depends(get_db)):
    result = db.query(HumainResult).filter(HumainResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Human result not found")
    db.delete(result)
    db.commit()
